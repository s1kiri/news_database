from sqlalchemy.orm import Session
from database.connection import Base, engine, SessionLocal
from database.models import Channel, News
from database.crud import add_channel, add_news, select_news_by_time_period, flush_old_news
from parser.parser import parse_channel
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)

def main():
    db = SessionLocal()
    try:
        channel_name = "@anapa005"
        parsed_news = parse_channel(channel_name)

        for news_item in parsed_news:
            channel = db.query(Channel).filter_by(name=news_item["channel_name"]).first()
            if not channel:
                channel = add_channel(db, name=news_item["channel_name"])

            add_news(
                db,
                content=news_item["content"],
                timestamp=datetime.fromisoformat(news_item["datetime"]),
                channel_id=channel.id,
            )

        start_time = datetime.now() - timedelta(days=1)
        end_time = datetime.now()
        recent_news = select_news_by_time_period(db, start_time, end_time)
        print(f"Последние новости: {[news.content for news in recent_news]}")

        flush_old_news(db)
        print("База очищена.")

    finally:
        db.close()


if __name__ == "__main__":
    main()