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
    

async def get_user(id: int) -> Optional[User]:
    async with get_session() as session:
        result = await session.exec(
            select(User)
            .where(User.id == id)
        )
        return result.first()


async def create_user(user: UserAuth) -> Optional[User]:
    data = user.about
    ml_api_toxicity_state = requests.get(f'{settings.ml_api}/check_model_toxicity')
    if data != '' and json.loads(ml_api_toxicity_state.text)['ready']:
        payload = dict(text=data)
        response = requests.post(f'{settings.ml_api}/predict_toxicity', data=payload)
        if response.status_code == 200:
            if response.json()['non_toxicity'] < 0.6:
                return

    async with get_session() as session:
        locality_id = (await session.exec(
            select(Locality.id)
            .join(Region)
            .where(
                and_(
                    Locality.name == user.locality_name,
                    Region.title == user.region_name
                )
            )
        )).first()

        ei_id = (await session.exec(
            select(EducationalInstitution.id)
            .where(EducationalInstitution.short_name == user.educational_institution)
        )).first()
        
        ed_dir_id = (await session.exec(
            select(EducationDirection.id)
            .where(EducationDirection.title == user.education_direction)
        )).first()
        
        user_entity = User(
            name=user.name,
            age=user.age,
            email=user.email,
            phone=user.phone,
            vk_id=user.vk_id,
            about=user.about,
            locality_id=locality_id,
            password_hash=user.hashed_password,
            education_direction=ed_dir_id,
            ei_id=ei_id,
            budget=user.budget,
            gender=user.gender
        )

        session.add(user_entity)
        await session.flush()
        
        for photo in enumerate(user.photos):
            photo_filename = await save_image(
                user_entity.id,
                photo,
                category='profile'
            )
            
            photo = UserPhoto(
                user_id=user_entity.id,
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
                    user_id=user_entity.id,
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
                    user_id=user_entity.id,
                    interest_id=interest_id
                )
                session.add(user_interest)
        
        await session.commit()
        return user_entity


async def get_regions():
    async with get_session() as session:
        result = await session.exec(select(Region.title))
        return list(result.all())


async def get_cities_by_region_name(region_title: str) -> List[str]:
    async with get_session() as session:
        cities_result = await session.exec(
            select(Locality.name)
            .where(Region.title == region_title)
            .join(Region, Region.id == Locality.region_id)
        )
        return list(cities_result.all())

async def get_bad_habits() -> List[str]:
    async with get_session() as session:
        result = await session.exec(select(BadHabit.title))
        return list(result.all())

async def get_interests() -> List[str]:
    async with get_session() as session:
        result = await session.exec(select(Interest.title))
        return list(result.all())


async def get_educ_dir() -> List[tuple[str, str]]:
    async with get_session() as session:
        result = await session.exec(select(EducationDirection.code, EducationDirection.title))
        return list(result.all())


async def get_recs_for_user(email: str) -> List[User]:
    async with get_session() as session:
        current_user = await get_user_by_email(email)

        viewed = await session.exec(
            select(User)
            .join(UserResponse, UserResponse.request_user_id == User.id)
        )
        return list(recs.all())


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
    

async def get_matches(user_id: int) -> Optional[list[int]]:
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
            #TODO DANYA WRITE IT PLEASE((((
        )
        return all_user_matches.all()
      

async def store_user_relation(email: str, related_ids: list[int]) -> None:
    value = json.dumps(related_ids)
    await r.hset(hash_name, user_id, value)


async def get_user_relation(email: str, user_id: int) -> list[int]:
    value = await r.hget(hash_name, user_id)
    return json.loads(value) if value else []
