from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    name: str


class Offer(BaseModel):
    quantity: float
    price: float
    user: User
    id: str
    server: str
    date: Optional[datetime]

    def __eq__(self, other):
        equal = self.quantity == other.quantity
        equal = equal and self.price == other.price
        equal = equal and self.user == other.user
        equal = equal and self.id == other.id
        equal = equal and self.server == other.server
        return equal
