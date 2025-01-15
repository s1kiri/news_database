from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import yaml
from datetime import datetime, timedelta

from .models import Channel, News, Base

DATABASE_URL = "sqlite:///./test.db"  

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DataBase:
    def __init__(self, config_path: str):
        self.db = SessionLocal()
        Base.metadata.create_all(bind=engine)
        self.config = self.load_config(path=config_path)

    @staticmethod
    def load_config(path: str):
        with open(path, 'r') as file:
            return yaml.safe_load(file)
    
    def flush_old_news(self, last_n_days: int):
        cutoff_time = datetime.now() - timedelta(days=last_n_days)
        self.db.query(News).filter(News.date < cutoff_time).delete()
        self.db.commit()
    
    def add_channel(self, name: str):
        new_channel = Channel(name=name)
        self.db.add(new_channel)
        self.db.commit()
        self.db.refresh(new_channel)
        return new_channel

    def add_news(self, message: str, date: datetime, channel: int, topic: str):
        channel_id = self.db.query(Channel).filter(Channel.name == channel).id
        news_item = News(message=message, date=date, channel_id=channel_id, topic=topic)
        self.db.add(news_item)
        self.db.commit()
        self.db.refresh(news_item)
        return news_item

    def select_news_by_time_period(self, start_time: datetime, end_time: datetime):
        return self.db.query(News).filter(News.date.between(start_time, end_time)).all()


