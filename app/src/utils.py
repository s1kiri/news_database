from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BaseRequest(BaseModel):
    """
    Base model for all requests, providing a common structure if needed.
    """
    request_id: Optional[str] = Field(
        None, description="Optional unique identifier for the request."
    )


class FlushRequest(BaseRequest):
    """
    Model for the /flush endpoint.
    """
    remain_n_days: int = Field(..., ge=0, description="Number of recent days to keep.")


class AddChannelRequest(BaseRequest):
    """
    Model for the /add_channel endpoint.
    """
    channel_name: str = Field(..., min_length=1, description="Name of the channel to add.")


class AddNewsRequest(BaseRequest):
    """
    Model for the /add_news endpoint.
    """
    message: str = Field(..., description="The message content of the news.")
    date: datetime = Field(..., description="The date and time of the news in ISO format.")
    channel: str = Field(..., min_length=1, description="The name of the channel.")
    topic: str = Field(..., min_length=1, description="The topic of the news.")


class SelectNewsRequest(BaseRequest):
    """
    Model for the /select_news_by_time_period endpoint.
    """
    start_date: datetime = Field(..., description="The start date in ISO format.")
    end_date: datetime = Field(..., description="The end date in ISO format.")