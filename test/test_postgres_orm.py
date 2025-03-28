from sqlalchemy.orm import Session

from project.postgres_database import get_db, init_db
from project.postgres.education import (EducationalInstitution,
                                        EducationDirection, EducationLevel)
from project.postgres.geography import District, Locality, LocalityType, Region
from project.postgres.matching import Chat, Match, Message
from project.postgres.user import Habitation, HabitationPhoto, User, UserPhoto

# Инициализация БД
init_db()


# Создаем тестовые данные
def create_test_data(db: Session):
    # Geography
    district = District(name="Центральный округ")
    db.add(district)

    region = Region(name="г. Москва", district=district)
    db.add(region)

    locality_type = LocalityType(name="Город")
    db.add(locality_type)

    locality = Locality(
        name="Москва", 
        type=locality_type,
        region=region
    )
    db.add(locality)

    # Education
    edu_level = EducationLevel(title="Бакалавриат")
    db.add(edu_level)

    edu_direction = EducationDirection(
        code="1.23.45.67",
        title="Компьютерные науки",
        education_level=edu_level
    )
    db.add(edu_direction)

    edu_institution = EducationalInstitution(
        full_name="Национальный исследовательский университет технологий",
        short_name="НИУТ",
        type=1,
        region=region
    )
    db.add(edu_institution)

    db.commit()

    # Users
    user1 = User(
        name="Иван Петров",
        age=25,
        email="ivan@example.com",
        phone="+79161234567",
        vk_id="id123456",
        locality=locality,
        password_hash="hashed_password",
        education_direction_rel=edu_direction,
        educational_institution=edu_institution
    )
    db.add(user1)

    habitation = Habitation(
        user=user1,
        address="ул. Тверская, 1",
        geo_coords='{"lat": 55.7558, "lng": 37.6173}',
        link="https://cian.ru/flat/123"
    )
    db.add(habitation)

    user_photo = UserPhoto(user=user1, file_name="ivan_photo.jpg")
    db.add(user_photo)

    hab_photo = HabitationPhoto(habitation=habitation,
                                file_name="flat_photo.jpg")
    db.add(hab_photo)

    # Matching
    user2 = User(
        name="Мария Сидорова",
        age=28,
        email="maria@example.com",
        phone="+79167654321",
        vk_id="id654321",
        locality=locality,
        password_hash="hashed_password_2"
    )
    db.add(user2)
    db.commit()

    match = Match(user_id1=user1.id, user_id2=user2.id, habitation=habitation)
    db.add(match)

    chat = Chat(match=match)
    db.add(chat)

    message = Message(
        message="Привет! Интересует ваше жилье",
        user=user2,
        chat=chat
    )
    db.add(message)

    db.commit()


# Проверка данных
def check_data(db: Session):
    # Проверка пользователей
    users = db.query(User).all()
    print("\nПользователи:")
    for user in users:
        print(f"{user.id}: {user.name} ({user.email})")

    # Проверка жилья
    habs = db.query(Habitation).all()
    print("\nЖилье:")
    for hab in habs:
        print(f"{hab.id}: {hab.address} | Владелец: {hab.user.name}")

    # Проверка сообщений
    messages = db.query(Message).join(Chat).all()
    print("\nСообщения:")
    for msg in messages:
        print(f"Чат {msg.chat.id}: [{msg.user.name}] {msg.message}")


if __name__ == "__main__":
    db = next(get_db())

    try:
        create_test_data(db)
        check_data(db)

    finally:
        db.close()
