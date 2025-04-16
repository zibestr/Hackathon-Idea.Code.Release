from sqlalchemy import Column, BigInteger, String
from .base import Base


class BadHabit(Base):
    __tablename__ = 'bad_habits'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BigInteger, primary_key=True, server_default="nextval('bad_habits_id_seq')")
    title = Column(String(100), nullable=False)


class Interest(Base):
    __tablename__ = 'interest'
    __table_args__ = {'schema': 'public'}
    
    id = Column(BigInteger, primary_key=True, server_default="nextval('interest_id_seq')")
    title = Column(String(100), nullable=False)
