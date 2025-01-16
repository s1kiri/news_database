from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    news = relationship("News", back_populates="channel")

class News(Base):
    __tablename__ = 'news'
    
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)
    date = Column(DateTime)
    channel_id = Column(Integer, ForeignKey('channels.id'))
    topic = Column(String)
    
    channel = relationship("Channel", back_populates="news")

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "date": self.date.isoformat(), 
            "channel_id": self.channel_id,
            "channel_name": self.channel.name,  # Include channel name if needed
            "topic": self.topic
        }