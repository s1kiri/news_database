from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    news = relationship("News", back_populates="channel")

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    topic = Column(String, nullable=False)
    channel = relationship("Channel", back_populates="news")