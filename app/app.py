from fastapi import FastAPI
from src.db import DataBase
from src.models import Channel
import datetime
from starlette.responses import JSONResponse

from src.utils import BaseRequest

CONFIG_PATH = 'configs/config.yaml'

db = DataBase(config_path=CONFIG_PATH)

app = FastAPI()

@app.get("/version")
async def get_config() :
    return JSONResponse(db.config)

@app.get("/health")
async def health_checks() :
    return JSONResponse(status_code=200, content={'response':'OK! I am fine!'})

@app.post("/flush")
def flush(request: BaseRequest):
    '''
    {'remain_n_days': 1}
    '''
    db.flush_old_news(last_n_days=request['remain_n_days'])
    return JSONResponse(status_code=200, content={'response':'Flushed!'})

@app.post("/add_channel")
def add_channel(request: BaseRequest):
    '''
    {'channel_name': 'example_name'}
    '''
    db.add_channel(name=request['name'])
    return JSONResponse(status_code=200, content={'response':f'Channel {request['name']}!'})

@app.post("/add_news")
def add_news(request: BaseRequest):
    '''
    {
        'message': 'message',
        'date': '12:00:00 12.12.24',
        'channel': 'channel_name',
        'topic': 'topic_title'
    }
    '''
    db.add_news(
                db,
                message=request["message"],
                date=datetime.fromisoformat(request["date"]),
                channel=request['channel'],
                topic=request["topic"],
            )
    return JSONResponse(status_code=200, content={'response':f'Channel {request['name']} has been added!'})

@app.get("/add_news")
def select_news_by_time_period(request: BaseRequest):
    '''
    {'start_date': '01.01.2024', 'end_date': '02.01.24'}
    '''
    news = db.select_news_by_time_period(start_time=request['start_date'], end_time=request['end_date'])
    return JSONResponse(status_code=200, content={'response':[newss for newss in news]})
    
    