from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .models import Channel, News

def add_channel(db: Session, name: str):
    new_channel = Channel(name=name)
    db.add(new_channel)
    db.commit()
    db.refresh(new_channel)
    return new_channel

def add_news(db: Session, content: str, timestamp: datetime, channel_id: int):
    news_item = News(content=content, timestamp=timestamp, channel_id=channel_id)
    db.add(news_item)
    db.commit()
    db.refresh(news_item)
    return news_item

def select_news_by_time_period(db: Session, start_time: datetime, end_time: datetime):
    return db.query(News).filter(News.timestamp.between(start_time, end_time)).all()

def flush_old_news(db: Session):
    cutoff_time = datetime.now() - timedelta(days=1)
    db.query(News).filter(News.timestamp < cutoff_time).delete()
    db.commit()