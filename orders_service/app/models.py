from pydantic import BaseModel
from typing import List, Optional


class Order(BaseModel):
    id: int
    customer_id: int
    order_date: str
    product_id: int
    quantity: int
    order_status: str