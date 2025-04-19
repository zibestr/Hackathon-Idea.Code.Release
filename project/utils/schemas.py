from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class ModelReadiness(BaseModel):
    """Ответ модели о готовности.
    Fields:
        - ready: bool - Готова модель или нет.
    """
    ready: bool


class TextRequest(BaseModel):
    """Запрос к модели классификации токсичности текста.
    Fields:
        - text: str - Текст для классификации, максимальная длина 1000.
    """
    text: str = Field(example="Пример текста", max_length=1000)


class RankingPairRequest(BaseModel):
    """Запрос к моделе ранжирования пар пользователей.
    Fields:
        - ei_id_main: int - университет пользователя, осуществляющего поиск.
        - age_main: int - возраст пользователя, осуществляющего поиск.
        - education_direction_main: int - образовательное учреждение
        пользователя, осуществляющего поиск.
        - year_created_at_main: int - год создания аккаунта
        пользователя, осуществляющего поиск.
        - budget_main: int - бюджет пользователя, осуществляющего поиск.
        - rating_main: float - рейтинг пользователя, осуществляющего поиск.
        - gender_main: int - пол пользователя, осуществляющего поиск,
        0 - девушка, 1 - мужчина.
        - habit_ids_main: list[int] - список id вредных привычек пользователя,
        осуществляющего поиск.
        - interest_ids_main: list[int] - список id интересов пользователя,
        осуществляющего поиск.

        - ei_id_candidate: int - университет кандидата.
        - age_candidate: int - возраст кандидата.
        - education_direction_candidate: int - образовательное учреждение
        кандидата.
        - year_created_at_candidate: int - год создания аккаунта
        кандидата.
        - budget_candidate: int - бюджет кандидата.
        - rating_candidate: float - рейтинг кандидата.
        - gender_candidate: int - пол кандидата.
        - habit_ids_candidate: list[int] - список id вредных привычек
        кандидата.
        - interest_ids_candidate: list[int] - список id интересов кандидата.
    """
    ei_id_main: int
    age_main: int
    education_direction_main: int
    year_created_at_main: int
    budget_main: int
    rating_main: float
    gender_main: int = Field(ge=0, le=1)
    habit_ids_main: list[int]
    interest_ids_main: list[int]

    ei_id_candidate: int
    age_candidate: int
    education_direction_candidate: int
    year_created_at_candidate: int
    budget_candidate: int
    rating_candidate: float
    gender_candidate: int = Field(ge=0, le=1)
    habit_ids_candidate: list[int]
    interest_ids_candidate: list[int]


class NSFWRequest(BaseModel):
    """Запрос к модели определения NSFW контента на изображение.

    Fields:
        image: str - base64 код изображения
    """
    image: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class User(BaseModel):
    name: str
    gender: int
    age: int
    vk_id: str
    city: str
    region: str
    district: str
    educational_code: str
    intersts: list[str]
    bad_habits: list[str]


class UserInDB(User):
    hashed_password: str
