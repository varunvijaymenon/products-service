from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Order
from app.database import orders_db, save_orders_to_json
from app.rabbitmq import publish_event

router = APIRouter()



@router.get("/orders", response_model=List[Order])
def get_orders():
    return orders_db

@router.get("/orders/{id}", response_model=Order)
def get_order(id: int):
    order = next((p for p in orders_db if p.id == id), None)
    if order:
        publish_event("order_found", order.dict())
        return order
    publish_event("order_not_found", {})
    raise HTTPException(status_code=404, detail="Order not found")

@router.post("/orders", response_model=Order, status_code=201)
def create_order(order: Order):
    if any(p.id == order.id for p in orders_db):
        raise HTTPException(status_code=400, detail="Order with this ID already exists")
    orders_db.append(order)
    save_orders_to_json(orders_db)
    publish_event("order_created", order.dict())
    return order

@router.put("/orders/{id}", response_model=Order)
def update_order(id: int, updated_order: Order):
    for index, order in enumerate(orders_db):
        if order.id == id:
            orders_db[index] = updated_order
            save_orders_to_json(orders_db)
            publish_event("order_updated", updated_order.dict())
            return updated_order
    raise HTTPException(status_code=404, detail="Order not found")

@router.delete("/orders/{id}", status_code=204)
def delete_order(id: int):
    for index, order in enumerate(orders_db):
        if order.id == id:
            deleted_order = orders_db.pop(index)
            save_orders_to_json(orders_db)
            publish_event("order_deleted", deleted_order.dict())
            return
    raise HTTPException(status_code=404, detail="Order not found")
