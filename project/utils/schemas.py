from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class ModelReadiness(BaseModel):
    """Ответ модели о готовности.
    
    Attributes:
        ready (bool): Готова модель или нет.
    """
    ready: bool


class TextRequest(BaseModel):
    """Запрос к модели классификации токсичности текста.
    
    Attributes:
        text (str): Текст для классификации. Максимальная длина - 1000 символов.
                    Пример: "Пример текста для анализа".
    """
    text: str = Field(example="Пример текста", max_length=1000)


class ToxicityResponse(BaseModel):
    """Ответ от модели классификации токсичности текста.
    
    Attributes:
        non_toxicity (float): Вероятность нетоксичности текста. Диапазон: 0-1.
        insult (float): Вероятность содержания оскорблений. Диапазон: 0-1.
        obscenity (float): Вероятность содержания непристойностей. Диапазон: 0-1.
        threat (float): Вероятность содержания угроз. Диапазон: 0-1.
        dangerous (float): Вероятность нанесения вреда репутации. Диапазон: 0-1.
    """
    non_toxicity: float = Field(ge=0, le=1)
    insult: float = Field(ge=0, le=1)
    obscenity: float = Field(ge=0, le=1)
    threat: float = Field(ge=0, le=1)
    dangerous: float = Field(ge=0, le=1)


class RankingPairRequest(BaseModel):
    """Запрос к модели ранжирования пар пользователей.
    
    Attributes:
        ei_id_main (int): ID университета основного пользователя.
        age_main (int): Возраст основного пользователя.
        education_direction_main (int): Направление образования основного пользователя.
        year_created_at_main (int): Год создания аккаунта основного пользователя.
        budget_main (int): Бюджет основного пользователя.
        rating_main (float): Рейтинг основного пользователя.
        gender_main (int): Пол основного пользователя (0 - женский, 1 - мужской).
        habit_ids_main (list[int]): Список ID вредных привычек основного пользователя.
        interest_ids_main (list[int]): Список ID интересов основного пользователя.
        
        ei_id_candidate (int): ID университета кандидата.
        age_candidate (int): Возраст кандидата.
        education_direction_candidate (int): Направление образования кандидата.
        year_created_at_candidate (int): Год создания аккаунта кандидата.
        budget_candidate (int): Бюджет кандидата.
        rating_candidate (float): Рейтинг кандидата.
        gender_candidate (int): Пол кандидата (0 - женский, 1 - мужской).
        habit_ids_candidate (list[int]): Список ID вредных привычек кандидата.
        interest_ids_candidate (list[int]): Список ID интересов кандидата.
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


class RankingResponse(BaseModel):
    """Ответ модели ранжирования пар пользователей.
    
    Attributes:
        coincidence (float): Вероятность совпадения пользователей. Диапазон: 0-1.
                            По умолчанию: 0.0.
    """
    coincidence: float = Field(default=0.0, ge=0, le=1)


class NSFWRequest(BaseModel):
    """Запрос к модели определения NSFW контента на изображении.
    
    Attributes:
        image (str): Изображение в формате base64.
    """
    image: str


class NSFWResponse(BaseModel):
    """Ответ модели определения NSFW контента на изображении.
    
    Attributes:
        normal (float): Вероятность что изображение безопасно. Диапазон: 0-1.
        nsfw (float): Вероятность что изображение содержит NSFW контент. Диапазон: 0-1.
    """
    normal: float = Field(ge=0, le=1)
    nsfw: float = Field(ge=0, le=1)


class Token(BaseModel):
    """Модель JWT токена для аутентификации.
    
    Attributes:
        access_token (str): JWT токен для доступа.
        token_type (str): Тип токена (обычно "bearer").
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Данные, хранящиеся в JWT токене.
    
    Attributes:
        email (Optional[str]): Email пользователя. По умолчанию: None.
    """
    email: Optional[str] = None


class UserData(BaseModel):
    """Модель данных пользователя для регистрации и обновления профиля.
    
    Attributes:
        name (str): Имя пользователя.
        photos (list[str]): Список фотографий пользователя в формате base64.
        gender (int): Пол пользователя (0 - женский, 1 - мужской).
        age (int): Возраст пользователя.
        email (EmailStr): Email пользователя.
        phone (str): Номер телефона пользователя.
        vk_id (str): ID пользователя в VK.
        region_name (str): Название региона проживания.
        locality_name (str): Название населенного пункта.
        education_direction (str): Направление образования.
        educational_institution (str): Учебное заведение.
        habit_ids (list[int]): Список ID вредных привычек.
        interest_ids (list[int]): Список ID интересов.
        budget (int): Бюджет пользователя.
        about (str): Информация о пользователе.
    """
    name: str
    photos: list[str] = list()
    gender: int
    age: int
    email: EmailStr
    phone: str
    vk_id: str
    region_name: str
    locality_name: str
    education_direction: str
    educational_institution: str
    habits: list[str]
    interests: list[str]
    budget: Optional[int]
    about: str


class UserIdentify(BaseModel):
    """Модель пользователя для входа (идентификации).
    
    Attributes:
        login (str): E-mail пользователя.
        password (str): Пароль для входа.
    """
    login: EmailStr
    password: str


class UserAuth(UserData):
    """Модель пользователя для аутентификации, расширяет UserData.
    
    Attributes:
        hashed_password (str): Хэшированный пароль пользователя.
    """
    hashed_password: str


class MessageResponse(BaseModel):
    """Модель сообщения пользователя.

    Attributes:
        user_id: int
        message_text: str
        created_at: datetime
    """
    user_id: int
    message_text: str
    created_at: datetime
