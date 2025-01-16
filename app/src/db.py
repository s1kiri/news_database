from datetime import datetime, timedelta

import yaml
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from .models import Channel, News, Base


class DataBase:
    def __init__(self, config_path: str):
        self.config = self.load_config(path=config_path)
        DATABASE_URL = f"sqlite:///./{self.config['db']['name']}"  
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.db: Session = SessionLocal()
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def load_config(path: str):
        try:
            with open(path, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="Config file not found.")
        except yaml.YAMLError:
            raise HTTPException(status_code=500, detail="Error parsing config file.")

    def flush_old_news(self, last_n_days: int):
        try:
            cutoff_time = datetime.now() - timedelta(days=last_n_days)
            rows_deleted = self.db.query(News).filter(News.date < cutoff_time).delete()
            self.db.commit()
            return {"message": f"Flushed {rows_deleted} old news items."}
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Error flushing old news: {str(e)}"
            )

    def add_channel(self, name: str):
        try:
            new_channel = Channel(name=name)
            self.db.add(new_channel)
            self.db.commit()
            self.db.refresh(new_channel)
            return new_channel
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Error adding channel '{name}': {str(e)}"
            )

    def add_news(self, message: str, date: datetime, channel: str, topic: str):
        try:
            channel_obj = self.db.query(Channel).filter(Channel.name == channel).first()
            if not channel_obj:
                raise HTTPException(
                    status_code=404, detail=f"Channel '{channel}' not found."
                )
            news_item = News(
                message=message,
                date=date,
                channel_id=channel_obj.id,
                topic=topic,
            )
            self.db.add(news_item)
            self.db.commit()
            self.db.refresh(news_item)
            return news_item
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Error adding news: {str(e)}"
            )

    def select_news_by_time_period(self, start_time: datetime, end_time: datetime):
        try:
            news = (
                self.db.query(News)
                .filter(News.date.between(start_time, end_time))
                .all()
            )
            return news
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching news for the time period: {str(e)}",
            )


