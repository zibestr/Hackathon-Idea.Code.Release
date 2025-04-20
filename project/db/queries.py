import redis.asyncio as redis
import json
import requests
from sqlmodel import select, and_, or_, alias, func
from typing import Optional, List, Dict, Any
import random
from config import settings

from db import (
    create_models,
    init_db,
    get_session,
    BadHabit,
    District,
    EducationLevel,
    Interest,
    EducationDirection,
    Region,
    EducationalInstitution,
    Locality,
    User,
    Habitation,
    t_user_bad_habits,
    t_user_interest,
    UserPhoto,
    UserResponse,
    UserScore,
    HabitationPhoto,
    Match,
    Message
)

from utils import (
    logs,
    save_image,
    ModelReadiness,
    TextRequest,
    ToxicityResponse,
    RankingPairRequest,
    RankingResponse,
    NSFWRequest,
    NSFWResponse,
    Token,
    TokenData,
    UserData,
    UserIdentify,
    UserAuth
)

#TODO только один населенный пункт, анкета активна, ранжируется твоей морделью, если модель гг, то просто случайный порядок списка 
#TODO приходит id (user листает ленту) -> если в user_response при request_user_id == user_id исключаем response_user_id из поиска, остальных пользователей
#TODO для каждой пары json(user, searching_for user)
# я кидаю дане запрос на получение кластера для нового пользователя и получаю кластер, записываю
host, port = settings.redis.split(':')
r = redis.Redis(host=host, port=port, db=0, decode_responses=True)


async def get_user_by_email(email: str) -> Optional[User]:
    async with get_session() as session:
        result = await session.exec(
            select(User)
            .where(User.email == email)
        )
        return result.first()


async def create_user(user: UserAuth) -> Optional[User]:
    data = user.about
    ml_api_toxicity_state: ModelReadiness = requests.get(f'{settings.ml_api}/check_model_toxicity')
    if data != '' and ml_api_toxicity_state.ready:
        payload = dict(text=data)
        response = requests.post(f'{settings.ml_api}/predict_toxicity', data=payload)
        if response.status_code == 200:
            if response.json()['non_toxicity'] < 0.6:
                return

    async with get_session() as session:
        locality_id = await session.exec(
            select(Locality.id)
            .join(Region)
            .where(
                and_(
                    Locality.name == user.locality_name,
                    Region.title == user.region_name
                )
            )
        )

        ei_id = await session.exec(
            select(EducationalInstitution.id)
            .where(EducationalInstitution.short_name == user.educational_institution)
        )
        
        ed_dir_id = await session.exec(
            select(EducationDirection.id)
            .where(EducationDirection.title == user.education_direction)
        )
        
        user = User(
            name=user.name,
            age=user.age,
            email=user.email,
            phone=user.phone,
            vk_id=user.vk_id,
            about=user.about,
            locality_id=locality_id.first(),
            password_hash=user.hashed_password,
            education_direction=ed_dir_id.first() if ed_dir_id.first() else None,
            ei_id=ei_id.first() if ei_id.first() else None,
            budget=user.budget,
            gender=user.gender
        )

        session.add(user)
        await session.flush()
        
        for photo in enumerate(user.photos):
            photo_filename = await save_image(
                user.id,
                photo,
                category='profile'
            )
            
            photo = UserPhoto(
                user_id=user.id,
                file_name=photo_filename,
            )
            session.add(photo)
        
        if user.habits:
            habits = await session.exec(select(BadHabit.id)
                                        .where(
                                            BadHabit.title.in_(user.habits)
                                        )
            )

            habit_ids = habits.all()
            for habit_id in habit_ids:
                user_habit = t_user_bad_habits(
                    user_id=user.id,
                    bad_habits_id=habit_id
                )
                session.add(user_habit)
        
        if user.interests:
            interests = await session.exec(select(Interest.id)
                                           .where(
                                               Interest.title.in_(user.interests)
                                           )
            )

            interest_ids = interests.all()
            for interest_id in interest_ids:
                user_interest = t_user_interest(
                    user_id=user.id,
                    interest_id=interest_id
                )
                session.add(user_interest)
        
        await session.commit()
        return user.id



async def getregions():
    async with get_session() as session:
        result = await session.exec(select(Region.title))
        return result.all()


async def get_cities_by_region_name(region_title: str):
    async with get_session() as session:
        region_result = await session.exec(select(Region).where(Region.title == region_title))
        region = region_result.first()

        if not region:
            raise HTTPException(status_code=404, detail="Регион не найден")

        cities_result = await session.exec(
            select(Locality.name).where(Locality.region_id == region.id)
        )
        return cities_result.all()

async def get_bad_habits():
    async with get_session() as session:
        result = await session.exec(select(BadHabit.title))
        return result.all()

async def get_interests():
    async with get_session() as session:
        result = await session.exec(select(Interest.title))
        return result.all()


async def get_educ_dir():
    async with get_session() as session:
        result = await session.exec(select(EducationDirection.code))
        return result.all()

async def update_user(user_id: int, update_data: Dict[str, Any]) -> Optional[User]:
    # danya model
    async with get_session() as session:
        user = await session.get(User, user_id)
        if not user:
            return None

        for key, value in update_data.items():
            setattr(user, key, value)

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def check_password(user_email: str, user_password: str) -> bool:
    user = await get_user_by_email(user_email)
    if not user:
        return False
    return user.verify_password(user_password)


# как получить id текущего пользователя который отправил запрос
async def get_recommendations(user_id: int) -> List[Dict[str, Any]]:
    async with get_session() as session:
        # Получаем текущего пользователя
        current_user = await session.get(User, user_id)
        if not current_user or not current_user.questionnaire_active:
            return []
        
        # Получаем ID уже просмотренных пользователей
        viewed_result = await session.exec(
            select(UserResponse.response_user_id)
            .where(UserResponse.request_user_id == user_id)
        )
        viewed_ids = [user_id] + [v[0] for v in viewed_result.all()]
        
        # Запрос на подходящих пользователей
        query = select(User).where(
            and_(
                User.habitation_id == current_user.habitation_id,
                User.questionnaire_active == True,
                User.id.not_in(viewed_ids)
            )
        )
        result = await session.exec(query)
        users = result.all()
        
        # Перемешиваем, если модель не GG
        if not current_user.is_gg_model:
            random.shuffle(users)
        
        # Формируем ответ
        return [
            {
                "user": user.dict(),
                "searching_for": user.searching_for
            }
            for user in users
        ]



async def cache_recomendations(user_id: int):
    # Здесь может быть логика кеширования в Redis или другом хранилище
    recommendations = await get_recomendations(user_id)
    # Реализация кеширования зависит от вашей инфраструктуры
    return recommendations


async def write_opinion(user_id_req: int, user_id_rep: int, opinion: bool) -> Tuple[bool, Optional[Match]]:
    async with get_session() as session:
        # Проверка на взаимный лайк
        mutual_like_query = select(UserResponse).where(
            and_(
                UserResponse.request_user_id == user_id_rep,
                UserResponse.response_user_id == user_id_req,
                UserResponse.opinion == True
            )
        )
        mutual_like_result = await session.exec(mutual_like_query)
        is_mutual = mutual_like_result.first()

        # Сохраняем реакцию пользователя
        response = UserResponse(
            request_user_id=user_id_req,
            response_user_id=user_id_rep,
            opinion=opinion
        )
        session.add(response)
        await session.commit()

        # Если лайк взаимный — создаём Match
        if opinion and is_mutual:
            match = Match(
                user1_id=min(user_id_req, user_id_rep),
                user2_id=max(user_id_req, user_id_rep)
            )
            session.add(match)
            await session.commit()
            return True, match

        return False, None

async def get_matches(user_id: int) -> List[Dict[str, Any]]:
    async with get_session() as session:
        query = select(Match).where(
            or_(
                Match.user1_id == user_id,
                Match.user2_id == user_id
            )
        )
        result = await session.exec(query)
        matches = result.all()
        
        # Получаем информацию о пользователях для каждого мэтча
        match_data = []
        for match in matches:
            other_user_id = match.user2_id if match.user1_id == user_id else match.user1_id
            other_user = await session.get(User, other_user_id)
            match_data.append({
                "match_id": match.id,
                "user": other_user.dict(),
                "created_at": match.created_at
            })
        
        return match_data

async def get_habitation() -> List[Habitation]:
    async with get_session() as session:
        result = await session.exec(select(Habitation))
        return result.all()

async def create_habitation(name: str) -> Habitation:
    async with get_session() as session:
        habitation = Habitation(name=name)
        session.add(habitation)
        await session.commit()
        await session.refresh(habitation)
        return habitation

async def update_habitation(habitation_id: int, new_name: str) -> Optional[Habitation]:
    async with get_session() as session:
        habitation = await session.get(Habitation, habitation_id)
        if not habitation:
            return None
        
        habitation.name = new_name
        session.add(habitation)
        await session.commit()
        await session.refresh(habitation)
        return habitation
    

async def get_matches(user_id: int):
    async with get_session() as session:
        user_matches = await session.exec(
            select(UserResponse.response_user_id).where(
                UserResponse.request_user_id == user_id).join(
                    Match, Match.response_id == UserResponse.id
            )
        )
        return user_matches.all()


async def get_all_matches():
    async with get_session() as session:
        all_user_matches = await session.exec(

        )
        return all_user_matches.all()
      

async def store_user_relation(hash_name: str, user_id: int, related_ids: list[int]) -> None:
    value = json.dumps(related_ids)
    await r.hset(hash_name, user_id, value)


async def get_user_relation(hash_name: str, user_id: int) -> list[int]:
    value = await r.hget(hash_name, user_id)
    return json.loads(value) if value else []
