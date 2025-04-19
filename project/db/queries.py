import redis.asyncio as redis
import json
from sqlmodel import select, and_, or_
from typing import Optional, List, Dict, Any
import random
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

#TODO только один населенный пункт, анкета активна, ранжируется твоей морделью, если модель гг, то просто случайный порядок списка 
#TODO приходит id (user листает ленту) -> если в user_response при request_user_id == user_id исключаем response_user_id из поиска, остальных пользователей
#TODO для каждой пары json(user, searching_for user)
# я кидаю дане запрос на получение кластера для нового пользователя и получаю кластер, записываю
r = redis.Redis(host='localhost', port=6777, db=0, decode_responses=True)


async def get_user_by_email(email: str) -> Optional[User]:
    async with get_session() as session:
        result = await session.exec(
            select(User).where(User.email == email)
        )
        return result.first()


async def create_user(fields: Dict[str, Any]) -> User:
    # danya model
    async with get_session() as session:
        user = User(**fields)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


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
      
async def store_user_relation(hash_name: str, user_id: int, related_ids: list[int]) -> None:
    value = json.dumps(related_ids)
    await r.hset(hash_name, user_id, value)

async def get_user_relation(hash_name: str, user_id: int) -> list[int]:
    value = await r.hget(hash_name, user_id)
    return json.loads(value) if value else []
