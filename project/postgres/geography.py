from sqlalchemy import (BigInteger, Column, ForeignKey,
                        Index, Sequence, String)
from sqlalchemy.orm import relationship

from .base import Base


class District(Base):
    __tablename__ = "district"
    id = Column(BigInteger, Sequence("district_id_seq"), primary_key=True)
    name = Column(String(255), nullable=False)
    regions = relationship("Region", back_populates="district")

    __table_args__ = (Index("district_id_idx", id, unique=True),)


class Region(Base):
    __tablename__ = "region"
    id = Column(BigInteger, Sequence("region_id_seq"), primary_key=True)
    name = Column(String(255), nullable=False)
    district_id = Column(BigInteger, ForeignKey("district.id"), nullable=False)
    district = relationship("District", back_populates="regions")
    localities = relationship("Locality", back_populates="region")

    __table_args__ = (Index("region_id_idx", id, unique=True),)


class LocalityType(Base):
    __tablename__ = "locality_type"
    id = Column(BigInteger, Sequence("locality_type_id_seq"), primary_key=True)
    name = Column(String(255), nullable=False)
    localities = relationship("Locality", back_populates="type")

    __table_args__ = (Index("locality_type_id_idx", id, unique=True),)


class Locality(Base):
    __tablename__ = "locality"
    id = Column(BigInteger, Sequence("locality_id_seq"), primary_key=True)
    type_id = Column(BigInteger, ForeignKey("locality_type.id"),
                     nullable=False)
    region_id = Column(BigInteger, ForeignKey("region.id"), nullable=False)
    name = Column(String(255), nullable=False)
    type = relationship("LocalityType", back_populates="localities")
    region = relationship("Region", back_populates="localities")
    users = relationship("User", back_populates="locality")

    __table_args__ = (Index("locality_id_idx", id, unique=True),)
