import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.models.base import Base
from project.models.user import User
from project.models.location import District, Region


TEST_DB_URL = "postgresql+psycopg2://hackathonshik:g01da_p0wer!@localhost/neighbor_service"


@pytest.fixture(scope="module")
def test_engine():
    engine = create_engine(TEST_DB_URL)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


def test_user_creation(test_engine):
    Session = sessionmaker(bind=test_engine)
    session = Session()
    
    # Тест валидации email
    invalid_user = User(
        email="invalid_email",
        phone="+71234567890",
        vk_id="123",
        name="Test",
        age=20,
        locality_id=1,
        password_hash="hash"
    )
    with pytest.raises(Exception):
        session.add(invalid_user)
        session.commit()

    # Тест возраста
    young_user = User(
        email="test@example.com",
        phone="+71234567891",
        vk_id="124",
        name="Test",
        age=17,
        locality_id=1,
        password_hash="hash"
    )
    with pytest.raises(Exception):
        session.add(young_user)
        session.commit()

    # Тест связи регион-район
    district = District(name="Central District")
    region = Region(name="Moscow Region", district=district)
    session.add_all([district, region])
    session.commit()
    
    assert region.district_id == district.id
