from pydantic import BaseModel, Field
from typing import Dict, Any

class RequestBody(BaseModel):
    key: str
    value: str


class Key(BaseModel):
    key: str


class JsonData(BaseModel):
    list_name: str
    payload: Dict[str, Any]


class ListNameRequest(BaseModel):
    listname: str


class TLEData(BaseModel):
    satellite_name: str = Field(..., example="Hubble Space Telescope")
    tle1: str = Field(..., example="1 20580U 90037B   20153.28845139  .00000111  00000-0  00000+0 0  9993")
    tle2: str = Field(..., example="2 20580  28.4694 327.5692 0002748 336.7313  23.2995 15.09280881431826")
