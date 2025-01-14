from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.connection import Base

class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    news = relationship("News", back_populates="channel")

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    channel = relationship("Channel", back_populates="news")