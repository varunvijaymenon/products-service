from pydantic import BaseModel
from typing import List, Optional


class Supplier(BaseModel):
    id: int
    name: str
    address: str
    phone_number: str
    email: str