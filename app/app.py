from fastapi import FastAPI, HTTPException
from src.db import DataBase
from datetime import datetime
from starlette.responses import JSONResponse

from src.utils import (
    FlushRequest,
    AddChannelRequest,
    AddNewsRequest,
    SelectNewsRequest,
)

CONFIG_PATH = "configs/config.yaml"

db = DataBase(config_path=CONFIG_PATH)

app = FastAPI()

@app.get("/version")
async def get_config():
    return JSONResponse(db.config)

@app.get("/health")
async def health_checks():
    return JSONResponse(status_code=200, content={"response": "OK! I am fine!"})

@app.post("/flush")
def flush(request: FlushRequest):
    """
    Request payload: {'remain_n_days': 1}
    """
    db.flush_old_news(last_n_days=request.remain_n_days)
    return JSONResponse(status_code=200, content={"response": "Flushed!"})


@app.post("/add_channel")
def add_channel(request: AddChannelRequest):
    """
    Request payload: {'channel_name': 'example_name'}
    """
    db.add_channel(name=request.channel_name)
    return JSONResponse(
        status_code=200,
        content={"response": f"Channel {request.channel_name} added!"},
    )


@app.post("/add_news")
def add_news(request: AddNewsRequest):
    """
    Request payload:
    {
        'message': 'message',
        'date': 'datetime',
        'channel': 'channel_name',
        'topic': 'topic_title'
    }
    """
    print(request.message)
    db.add_news(
        message=request.message,
        date=request.date,
        channel=request.channel,
        topic=request.topic,
    )
    return JSONResponse(
        status_code=200,
        content={"response": f"News '{request.message}' added to channel {request.channel}!"},
    )


@app.get("/select_news")
def select_news_by_time_period(request: SelectNewsRequest):
    """
    Request payload: {'start_date': 'datetime', 'end_date': 'datetime'}
    """
    news = db.select_news_by_time_period(
        start_time=request.start_date, end_time=request.end_date
    )
    
    serialized_news = [news_item.to_dict() for news_item in news]

    return JSONResponse(
        status_code=200,
        content={"response": serialized_news},
    )