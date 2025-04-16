from sqlalchemy import (Column, BigInteger, Boolean, String, ForeignKey, 
                        CheckConstraint, TIMESTAMP, Double, text)
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, server_default="nextval('user_id_seq')")
    ei_id = Column(BigInteger, ForeignKey('educational_institution.id'))
    is_active = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)
    name = Column(String(255), nullable=False)
    age = Column(BigInteger, CheckConstraint('age >= 18'), nullable=False)
    email = Column(String(255), 
                  CheckConstraint("email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'"), 
                  unique=True, nullable=False)
    phone = Column(String(20), 
                  CheckConstraint("phone ~ '^\\+7\\d{10}$'"), 
                  unique=True, nullable=False)
    vk_id = Column(String(100), unique=True, nullable=False)
    about = Column(String(255))
    locality_id = Column(BigInteger, ForeignKey('locality.id'), nullable=False)
    password_hash = Column(String(255), nullable=False)
    education_direction = Column(BigInteger, ForeignKey('education_direction.id'))
    is_search = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    last_log_moment = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    rating = Column(Double, default=5.0)
    budget = Column(BigInteger)
    
    locality = relationship("Locality")
    bad_habits = relationship("BadHabit", secondary="user_bad_habits")
    interests = relationship("Interest", secondary="user_interest")


class UserBadHabits(Base):
    __tablename__ = 'user_bad_habits'
    user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    bad_habits_id = Column(BigInteger, ForeignKey('bad_habits.id'), primary_key=True)


class UserInterest(Base):
    __tablename__ = 'user_interest'
    user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    interest_id = Column(BigInteger, ForeignKey('interest.id'), primary_key=True)
