from typing import List, Optional

from pydantic import BaseModel


class Item(BaseModel):
    shortDescription: str
    price: float


class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    items: List[Item]
    total: float
