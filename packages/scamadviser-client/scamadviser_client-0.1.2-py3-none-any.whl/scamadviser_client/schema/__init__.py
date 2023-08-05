from pydantic import BaseModel


class BaseParams(BaseModel):
    apikey: str
