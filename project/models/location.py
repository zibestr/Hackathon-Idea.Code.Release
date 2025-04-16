from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class District(Base):
    __tablename__ = 'district'
    id = Column(BigInteger, primary_key=True, server_default="nextval('district_id_seq')")
    name = Column(String(255), nullable=False)
    regions = relationship("Region", back_populates="district")


class Region(Base):
    __tablename__ = 'region'
    id = Column(BigInteger, primary_key=True, server_default="nextval('region_id_seq')")
    name = Column(String(255), nullable=False)
    district_id = Column(BigInteger, ForeignKey('district.id'), nullable=False)
    district = relationship("District", back_populates="regions")
   
    localities = relationship("Locality", back_populates="region")


class LocalityType(Base):
    __tablename__ = 'locality_type'
    id = Column(BigInteger, primary_key=True, server_default="nextval('locality_type_id_seq')")
    name = Column(String(255), nullable=False)


class Locality(Base):
    __tablename__ = 'locality'
    id = Column(BigInteger, primary_key=True, server_default="nextval('locality_id_seq')")
    type_id = Column(BigInteger, ForeignKey('locality_type.id'), nullable=False)
    region_id = Column(BigInteger, ForeignKey('region.id'), nullable=False)
    name = Column(String(255), nullable=False)
    type = relationship("LocalityType")
    region = relationship("Region", back_populates="localities")
