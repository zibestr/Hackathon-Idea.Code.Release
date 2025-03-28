from sqlalchemy import (BigInteger, Column, DateTime, ForeignKey, Index,
                        Sequence, String)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class Match(Base):
    __tablename__ = 'match'
    id = Column(BigInteger, Sequence('match_id_seq'), primary_key=True)
    user_id1 = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    user_id2 = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    habitation_id = Column(BigInteger, ForeignKey('habitation.id'))
    created_at = Column(DateTime, server_default=func.now())
    user1 = relationship("User", foreign_keys=[user_id1])
    user2 = relationship("User", foreign_keys=[user_id2])
    habitation = relationship("Habitation")
    chat = relationship("Chat", uselist=False, back_populates="match")

    __table_args__ = (Index('match_id_idx', id, unique=True),)


class Chat(Base):
    __tablename__ = 'chat'
    id = Column(BigInteger, Sequence('chat_id_seq'), primary_key=True)
    match_id = Column(BigInteger, ForeignKey('match.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    match = relationship("Match", back_populates="chat")
    messages = relationship("Message", back_populates="chat")

    __table_args__ = (Index('chat_id_idx', id, unique=True),)


class Message(Base):
    __tablename__ = 'message'
    id = Column(BigInteger, Sequence('message_id_seq'), primary_key=True)
    message = Column(String(255), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    chat_id = Column(BigInteger, ForeignKey('chat.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    user = relationship("User")
    chat = relationship("Chat", back_populates="messages")

    __table_args__ = (Index('message_id_idx', id, unique=True),)


class UserScore(Base):
    __tablename__ = 'user_score'
    user_from_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    user_to_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    score = Column(BigInteger, nullable=False)

    __table_args__ = (Index('user_score_idx', user_from_id,
                            user_to_id, unique=True),)


class HabitationResponse(Base):
    __tablename__ = 'habitation_response'
    habitation_id = Column(BigInteger, ForeignKey('habitation.id'),
                           primary_key=True)
    request_user_id = Column(BigInteger, ForeignKey('users.id'),
                             primary_key=True)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (Index('habitation_response_idx', habitation_id,
                            request_user_id, unique=True),)


class UserResponse(Base):
    __tablename__ = 'user_response'
    response_user_id = Column(BigInteger, ForeignKey('users.id'),
                              primary_key=True)
    request_user_id = Column(BigInteger, ForeignKey('users.id'),
                             primary_key=True)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (Index('user_reponse_idx', response_user_id,
                            request_user_id, unique=True),)
