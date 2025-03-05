from typing import List
from datetime import datetime, time
from pydantic import BaseModel, Field


class Item(BaseModel):
    shortDescription: str
    price: float 


class Receipt(BaseModel):
    retailer: str = Field(min_length=1, max_length=100)
    purchaseDate: datetime
    purchaseTime: time
    items: List[Item]
    total: float
