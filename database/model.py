from sqlalchemy import Column, String, Text, Float, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    model_used = Column(Text, nullable=False)
    response_time = Column(Float, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

    feedbacks = relationship("Feedback", back_populates="conversation")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, ForeignKey("conversations.id"))
    feedback = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

    conversation = relationship("Conversation", back_populates="feedbacks")
