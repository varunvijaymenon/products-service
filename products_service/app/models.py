from pydantic import BaseModel
from typing import List, Optional


class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool