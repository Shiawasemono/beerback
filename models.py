import uuid
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class iSpindel(BaseModel):
    ID: int = Field(...)
    RSSI: int = Field(...)
    angle: float = Field(...)
    battery: float = Field(...)
    gravity: float = Field(...)
    interval: int = Field(...)
    name: str = Field(...)
    temp_units: str = Field(...)
    temperature: float = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "ID": 2353478,
                "RSSI": -63,
                "angle": 89.54399109,
                "battery": 4.108446121,
                "gravity": 25.59607697,
                "interval": 30,
                "name": "iSpindel001",
                "temp_units": "C",
                "temperature": 20.5625
            }
        }

class iSpindelDB(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    ID: int = Field(...)
    RSSI: int = Field(...)
    angle: float = Field(...)
    battery: float = Field(...)
    gravity: float = Field(...)
    interval: int = Field(...)
    name: str = Field(...)
    temp_units: str = Field(...)
    temperature: float = Field(...)
    datetime: Optional[datetime]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "ID": 2353478,
                "RSSI": -63,
                "angle": 89.54399109,
                "battery": 4.108446121,
                "gravity": 25.59607697,
                "interval": 30,
                "name": "iSpindel001",
                "temp_units": "C",
                "temperature": 20.5625,
                "datetime": "2023-01-21T23:16:11.942Z"
            }
        }

class activateiSpindel(BaseModel):
    name: str = Field(...)
    time: datetime = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "iSpindel001",
                "time": "2023-01-21T23:16:11.942Z",
            }
        }

class activateiSpindelDB(BaseModel):
    name: str = Field(...)
    time: datetime = Field(...)
    in_use: bool = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "iSpindel001",
                "time": "2023-01-21T23:16:11.942Z",
                "in_use": True,
            }
        }