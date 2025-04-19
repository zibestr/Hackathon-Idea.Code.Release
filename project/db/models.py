from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, DateTime, Double, ForeignKeyConstraint, Index, PrimaryKeyConstraint, Sequence, SmallInteger, String, Table, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime


class Base(DeclarativeBase):
    pass


class BadHabit(Base):
    __tablename__ = 'bad_habits'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='bad_habits_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    users: Mapped[List['User']] = relationship('User', secondary='user_bad_habits', back_populates='bad_habitss')


class District(Base):
    __tablename__ = 'district'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='district_pkey'),
        Index('district_id_idx', 'id', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))

    regions: Mapped[List['Region']] = relationship('Region', back_populates='district')


class EducationLevel(Base):
    __tablename__ = 'education_level'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='education_level_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))

    education_directions: Mapped[List['EducationDirection']] = relationship('EducationDirection', back_populates='education_level')


class Interest(Base):
    __tablename__ = 'interest'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='interest_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    users: Mapped[List['User']] = relationship('User', secondary='user_interest', back_populates='interests')


class EducationDirection(Base):
    __tablename__ = 'education_direction'
    __table_args__ = (
        CheckConstraint("code::text ~ '^\\d\\.\\d\\d\\.\\d\\d\\.\\d\\d$'::text", name='education_direction_code_check'),
        ForeignKeyConstraint(['education_level_id'], ['education_level.id'], name='education_direction_education_level_id_fkey'),
        PrimaryKeyConstraint('id', name='education_direction_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code: Mapped[str] = mapped_column(String(10))
    title: Mapped[str] = mapped_column(String(255))
    education_level_id: Mapped[int] = mapped_column(BigInteger)

    education_level: Mapped['EducationLevel'] = relationship('EducationLevel', back_populates='education_directions')
    userss: Mapped[List['User']] = relationship('User', back_populates='education_direction_')


class Region(Base):
    __tablename__ = 'region'
    __table_args__ = (
        ForeignKeyConstraint(['district_id'], ['district.id'], name='region_district_id_fkey'),
        PrimaryKeyConstraint('id', name='region_pkey'),
        Index('region_id_idx', 'id', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    district_id: Mapped[int] = mapped_column(BigInteger)

    district: Mapped['District'] = relationship('District', back_populates='regions')
    educational_institutions: Mapped[List['EducationalInstitution']] = relationship('EducationalInstitution', back_populates='region')
    localities: Mapped[List['Locality']] = relationship('Locality', back_populates='region')


class EducationalInstitution(Base):
    __tablename__ = 'educational_institution'
    __table_args__ = (
        ForeignKeyConstraint(['region_id'], ['region.id'], name='educational_institution_region_id_fkey'),
        PrimaryKeyConstraint('id', name='educational_institution_pkey'),
        Index('educational_institution_id_idx', 'id', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    short_name: Mapped[str] = mapped_column(String(255))
    type: Mapped[int] = mapped_column(BigInteger)
    region_id: Mapped[int] = mapped_column(BigInteger)

    region: Mapped['Region'] = relationship('Region', back_populates='educational_institutions')
    userss: Mapped[List['User']] = relationship('User', back_populates='ei')


class Locality(Base):
    __tablename__ = 'locality'
    __table_args__ = (
        ForeignKeyConstraint(['region_id'], ['region.id'], name='locality_region_id_fkey'),
        PrimaryKeyConstraint('id', name='locality_pkey'),
        Index('locality_id_idx', 'id', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    region_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(255))

    region: Mapped['Region'] = relationship('Region', back_populates='localities')
    userss: Mapped[List['User']] = relationship('User', back_populates='locality')


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint('age >= 18', name='users_age_check'),
        CheckConstraint("email::text ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'::text", name='users_email_check'),
        CheckConstraint("phone::text ~ '^\\+7\\d{10}$'::text", name='users_phone_check'),
        ForeignKeyConstraint(['education_direction'], ['education_direction.id'], name='users_education_direction_fkey'),
        ForeignKeyConstraint(['ei_id'], ['educational_institution.id'], name='users_ei_id_fkey'),
        ForeignKeyConstraint(['locality_id'], ['locality.id'], name='users_locality_id_fkey'),
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key'),
        UniqueConstraint('phone', name='users_phone_key'),
        UniqueConstraint('vk_id', name='users_vk_id_key'),
        Index('user_email_idx', 'email', unique=True),
        Index('user_id_idx', 'id', unique=True),
        Index('user_phone_idx', 'phone', unique=True),
        Index('user_vk_id_idx', 'vk_id', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, Sequence('user_id_seq'), primary_key=True)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text('true'))
    deleted: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
    name: Mapped[str] = mapped_column(String(255))
    age: Mapped[int] = mapped_column(BigInteger)
    email: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(20))
    vk_id: Mapped[str] = mapped_column(String(100))
    locality_id: Mapped[int] = mapped_column(BigInteger)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_search: Mapped[bool] = mapped_column(Boolean, server_default=text('true'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    last_log_moment: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    rating: Mapped[float] = mapped_column(Double(53), server_default=text('5'))
    ei_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    about: Mapped[Optional[str]] = mapped_column(String(255))
    education_direction: Mapped[Optional[int]] = mapped_column(BigInteger)
    budget: Mapped[Optional[int]] = mapped_column(BigInteger)
    gender: Mapped[Optional[int]] = mapped_column(SmallInteger)

    bad_habitss: Mapped[List['BadHabit']] = relationship('BadHabit', secondary='user_bad_habits', back_populates='users')
    interests: Mapped[List['Interest']] = relationship('Interest', secondary='user_interest', back_populates='users')
    education_direction_: Mapped[Optional['EducationDirection']] = relationship('EducationDirection', back_populates='userss')
    ei: Mapped[Optional['EducationalInstitution']] = relationship('EducationalInstitution', back_populates='userss')
    locality: Mapped['Locality'] = relationship('Locality', back_populates='userss')
    habitations: Mapped[List['Habitation']] = relationship('Habitation', back_populates='user')
    user_photos: Mapped[List['UserPhoto']] = relationship('UserPhoto', back_populates='user')
    user_responses: Mapped[List['UserResponse']] = relationship('UserResponse', foreign_keys='[UserResponse.request_user_id]', back_populates='request_user')
    user_responses_: Mapped[List['UserResponse']] = relationship('UserResponse', foreign_keys='[UserResponse.response_user_id]', back_populates='response_user')
    user_scores: Mapped[List['UserScore']] = relationship('UserScore', foreign_keys='[UserScore.user_from_id]', back_populates='user_from')
    user_scores_: Mapped[List['UserScore']] = relationship('UserScore', foreign_keys='[UserScore.user_to_id]', back_populates='user_to')
    messages: Mapped[List['Message']] = relationship('Message', back_populates='user')


class Habitation(Base):
    __tablename__ = 'habitation'
    __table_args__ = (
        CheckConstraint("link::text ~ '^(https?:\\/\\/)?(([a-zA-Z0-9-]+\\.)?(avito\\.ru|domclick\\.ru|cian\\.ru)|arenda\\.yandex\\.ru)(\\/.*)?$'::text", name='habitation_link_check'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='habitation_user_id_fkey'),
        PrimaryKeyConstraint('id', name='habitation_pkey'),
        Index('habitation_id_idx', 'id', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    address: Mapped[str] = mapped_column(String(255))
    geo_coords: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    monthly_price: Mapped[int] = mapped_column(BigInteger)
    link: Mapped[Optional[str]] = mapped_column(String(255))

    user: Mapped['User'] = relationship('User', back_populates='habitations')
    habitation_photos: Mapped[List['HabitationPhoto']] = relationship('HabitationPhoto', back_populates='habitation')


t_user_bad_habits = Table(
    'user_bad_habits', Base.metadata,
    Column('user_id', BigInteger, nullable=False),
    Column('bad_habits_id', BigInteger, nullable=False),
    ForeignKeyConstraint(['bad_habits_id'], ['bad_habits.id'], name='user_bad_habits_bad_habits_id_fkey'),
    ForeignKeyConstraint(['user_id'], ['users.id'], name='user_bad_habits_user_id_fkey')
)


t_user_interest = Table(
    'user_interest', Base.metadata,
    Column('user_id', BigInteger, nullable=False),
    Column('interest_id', BigInteger, nullable=False),
    ForeignKeyConstraint(['interest_id'], ['interest.id'], name='user_interest_interest_id_fkey'),
    ForeignKeyConstraint(['user_id'], ['users.id'], name='user_interest_user_id_fkey')
)


class UserPhoto(Base):
    __tablename__ = 'user_photo'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], name='user_photo_user_id_fkey'),
        PrimaryKeyConstraint('id', name='user_photo_pkey'),
        UniqueConstraint('file_name', name='user_photo_file_name_key'),
        Index('user_photo_id_idx', 'id', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    file_name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped['User'] = relationship('User', back_populates='user_photos')


class UserResponse(Base):
    __tablename__ = 'user_response'
    __table_args__ = (
        ForeignKeyConstraint(['request_user_id'], ['users.id'], name='user_response_request_user_id_fkey'),
        ForeignKeyConstraint(['response_user_id'], ['users.id'], name='user_response_response_user_id_fkey'),
        PrimaryKeyConstraint('id', name='user_response_pkey'),
        Index('user_reponse_pair_idx', 'response_user_id', 'request_user_id', unique=True),
        Index('user_response_idx', 'id', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    response_user_id: Mapped[int] = mapped_column(BigInteger)
    request_user_id: Mapped[int] = mapped_column(BigInteger)

    request_user: Mapped['User'] = relationship('User', foreign_keys=[request_user_id], back_populates='user_responses')
    response_user: Mapped['User'] = relationship('User', foreign_keys=[response_user_id], back_populates='user_responses_')
    matches: Mapped[List['Match']] = relationship('Match', back_populates='response')


class UserScore(Base):
    __tablename__ = 'user_score'
    __table_args__ = (
        ForeignKeyConstraint(['user_from_id'], ['users.id'], name='user_score_user_from_id_fkey'),
        ForeignKeyConstraint(['user_to_id'], ['users.id'], name='user_score_user_to_id_fkey'),
        PrimaryKeyConstraint('user_from_id', 'user_to_id', name='user_score_pkey'),
        Index('user_score_idx', 'user_from_id', 'user_to_id', unique=True)
    )

    user_from_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_to_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    score: Mapped[int] = mapped_column(BigInteger)

    user_from: Mapped['User'] = relationship('User', foreign_keys=[user_from_id], back_populates='user_scores')
    user_to: Mapped['User'] = relationship('User', foreign_keys=[user_to_id], back_populates='user_scores_')


class HabitationPhoto(Base):
    __tablename__ = 'habitation_photo'
    __table_args__ = (
        ForeignKeyConstraint(['habitation_id'], ['habitation.id'], name='habitation_photo_habitation_id_fkey'),
        PrimaryKeyConstraint('id', name='habitation_photo_pkey'),
        UniqueConstraint('file_name', name='habitation_photo_file_name_key'),
        Index('habitation_photo_id_idx', 'id', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    habitation_id: Mapped[int] = mapped_column(BigInteger)
    file_name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    habitation: Mapped['Habitation'] = relationship('Habitation', back_populates='habitation_photos')


class Match(Base):
    __tablename__ = 'match'
    __table_args__ = (
        ForeignKeyConstraint(['response_id'], ['user_response.id'], name='match_response_id_fkey'),
        PrimaryKeyConstraint('id', name='match_pkey'),
        Index('match_id_idx', 'id', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    response_id: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    response: Mapped['UserResponse'] = relationship('UserResponse', back_populates='matches')
    messages: Mapped[List['Message']] = relationship('Message', back_populates='match')


class Message(Base):
    __tablename__ = 'message'
    __table_args__ = (
        ForeignKeyConstraint(['match_id'], ['match.id'], name='message_match_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='message_user_id_fkey'),
        PrimaryKeyConstraint('id', name='message_pkey'),
        Index('message_id_idx', 'id', unique=True)
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    message: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(BigInteger)
    match_id: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    match: Mapped['Match'] = relationship('Match', back_populates='messages')
    user: Mapped['User'] = relationship('User', back_populates='messages')
