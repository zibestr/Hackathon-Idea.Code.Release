from sqlalchemy import Column, BigInteger, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import text
from .base import Base


class UserResponse(Base):
    __tablename__ = 'user_response'
    __table_args__ = (
        {'schema': 'public'},
    )
    
    id = Column(BigInteger, primary_key=True, server_default="nextval('user_response_id_seq')")
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    response_user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    request_user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)


class Match(Base):
    __tablename__ = 'match'
    
    id = Column(BigInteger, primary_key=True, server_default="nextval('match_id_seq')")
    response_id = Column(BigInteger, ForeignKey('user_response.id'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))


class Message(Base):
    __tablename__ = 'message'
    
    id = Column(BigInteger, primary_key=True, server_default="nextval('message_id_seq')")
    message = Column(String(255), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    match_id = Column(BigInteger, ForeignKey('match.id'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))


class UserScore(Base):
    __tablename__ = 'user_score'
    __table_args__ = (
        {'schema': 'public'},
    )
    
    user_from_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    user_to_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    score = Column(BigInteger, nullable=False)
