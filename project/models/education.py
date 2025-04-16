from sqlalchemy import Column, BigInteger, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base


class EducationLevel(Base):
    __tablename__ = 'education_level'
    id = Column(BigInteger, primary_key=True, server_default="nextval('education_level_id_seq')")
    title = Column(String(255), nullable=False)
    directions = relationship("EducationDirection", back_populates="level")


class EducationDirection(Base):
    __tablename__ = 'education_direction'
    id = Column(BigInteger, primary_key=True, server_default="nextval('education_direction_id_seq')")
    code = Column(String(10), CheckConstraint("code ~ '^\\d\\.\\d\\d\\.\\d\\d\\.\\d\\d$'"), nullable=False)
    title = Column(String(255), nullable=False)
    education_level_id = Column(BigInteger, ForeignKey('education_level.id'), nullable=False)
    level = relationship("EducationLevel", back_populates="directions")


class EducationalInstitution(Base):
    __tablename__ = 'educational_institution'
    id = Column(BigInteger, primary_key=True, server_default="nextval('educational_institution_id_seq')")
    full_name = Column(String(255), nullable=False)
    short_name = Column(String(255), nullable=False)
    type = Column(BigInteger, nullable=False)
    region_id = Column(BigInteger, ForeignKey('region.id'), nullable=False)
