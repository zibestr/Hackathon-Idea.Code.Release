from sqlalchemy import (JSON, BigInteger, Boolean, CheckConstraint, Column,
                        DateTime, Float, ForeignKey, Index, Sequence, String)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, Sequence('user_id_seq'), primary_key=True)
    ei_id = Column(BigInteger, ForeignKey('educational_institution.id'))
    deleted = Column(Boolean, nullable=False, server_default='true')
    name = Column(String(255), nullable=False)
    age = Column(BigInteger, CheckConstraint('age >= 18'), nullable=False)
    email = Column(
        String(255),
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'"
        ),
        unique=True, nullable=False
    )
    phone = Column(String(20),
                   CheckConstraint("phone ~ '^\\+7\\d{10}$'"),
                   unique=True, nullable=False)
    vk_id = Column(String(100), unique=True, nullable=False)
    about = Column(String(255))
    locality_id = Column(BigInteger, ForeignKey('locality.id'), nullable=False)
    password_hash = Column(String(255), nullable=False)
    education_direction = Column(BigInteger,
                                 ForeignKey('education_direction.id'))
    is_search = Column(Boolean, nullable=False, server_default='true')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    last_log_moment = Column(DateTime, server_default=func.now())
    rating = Column(Float, nullable=True)

    # Relationships
    educational_institution = relationship("EducationalInstitution",
                                           back_populates="users")
    locality = relationship("Locality", back_populates="users")
    education_direction_rel = relationship("EducationDirection",
                                           back_populates="users")
    habitations = relationship("Habitation", back_populates="user")
    photos = relationship("UserPhoto", back_populates="user")

    __table_args__ = (
        Index('user_email_idx', email, unique=True),
        Index('user_phone_idx', phone, unique=True),
        Index('user_vk_id_idx', vk_id, unique=True),
    )


class Habitation(Base):
    __tablename__ = 'habitation'
    id = Column(BigInteger, Sequence('habitation_id_seq'), primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    address = Column(String(255), nullable=False)
    geo_coords = Column(JSON, nullable=False)
    link = Column(
        String(255),
        CheckConstraint(
            "link ~* '^(https?://)?((avito\\.ru|domclick\\.ru|"
            "cian\\.ru)|arenda\\.yandex\\.ru)'"
        )
    )
    created_at = Column(DateTime, server_default=func.now())
    user = relationship("User", back_populates="habitations")
    photos = relationship("HabitationPhoto", back_populates="habitation")

    __table_args__ = (Index('habitation_id_idx', id, unique=True),)


class UserPhoto(Base):
    __tablename__ = 'user_photo'
    id = Column(BigInteger, Sequence('user_photo_id_seq'), primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    file_name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    user = relationship("User", back_populates="photos")

    __table_args__ = (Index('user_photo_id_idx', id, unique=True),)


class HabitationPhoto(Base):
    __tablename__ = 'habitation_photo'
    id = Column(BigInteger, Sequence('habitation_photo_id_seq'),
                primary_key=True)
    habitation_id = Column(BigInteger, ForeignKey('habitation.id'),
                           nullable=False)
    file_name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    habitation = relationship("Habitation", back_populates="photos")

    __table_args__ = (Index('habitation_photo_id_idx', id, unique=True),)
