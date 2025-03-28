from sqlalchemy import (BigInteger, CheckConstraint, Column, ForeignKey, Index,
                        Sequence, String)
from sqlalchemy.orm import relationship

from .base import Base


class EducationLevel(Base):
    __tablename__ = "education_level"
    id = Column(BigInteger, Sequence("education_level_id_seq"),
                primary_key=True)
    title = Column(String(255), nullable=False)
    directions = relationship("EducationDirection",
                              back_populates="education_level")

    __table_args__ = (Index("education_level_id_idx", id, unique=True),)


class EducationDirection(Base):
    __tablename__ = "education_direction"
    id = Column(BigInteger, Sequence("education_direction_id_seq"),
                primary_key=True)
    code = Column(String(10),
                  CheckConstraint("code ~ '^\\d\\.\\d{2}\\.\\d{2}\\.\\d{2}$'"),
                  nullable=False)
    title = Column(String(255), nullable=False)
    education_level_id = Column(BigInteger, ForeignKey("education_level.id"),
                                nullable=False)
    education_level = relationship("EducationLevel",
                                   back_populates="directions")
    users = relationship("User", back_populates="education_direction_rel")

    __table_args__ = (Index("education_direction_id_idx", id, unique=True),)


class EducationalInstitution(Base):
    __tablename__ = "educational_institution"
    id = Column(BigInteger, Sequence("educational_institution_id_seq"),
                primary_key=True)
    full_name = Column(String(255), nullable=False)
    short_name = Column(String(255), nullable=False)
    type = Column(BigInteger, nullable=False)  # ENUM
    region_id = Column(BigInteger, ForeignKey("region.id"), nullable=False)
    region = relationship("Region")
    users = relationship("User", back_populates="educational_institution")

    __table_args__ = (Index("educational_institution_id_idx",
                            id, unique=True),)
