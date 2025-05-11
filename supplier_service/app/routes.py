from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Supplier
from app.database import suppliers_db, save_suppliers_to_json
from app.rabbitmq import publish_event

router = APIRouter()



@router.get("/suppliers", response_model=List[Supplier])
def get_suppliers():
    return suppliers_db

@router.get("/suppliers/{id}", response_model=Supplier)
def get_supplier(id: int):
    supplier = next((p for p in suppliers_db if p.id == id), None)
    if supplier:
        publish_event("supplier_found", supplier.dict())
        return supplier
    publish_event("supplier_not_found", {})
    raise HTTPException(status_code=404, detail="Supplier not found")

@router.post("/suppliers", response_model=Supplier, status_code=201)
def create_product(supplier: Supplier):
    if any(p.id == supplier.id for p in suppliers_db):
        raise HTTPException(status_code=400, detail="Supplier with this ID already exists")
    suppliers_db.append(supplier)
    save_suppliers_to_json(suppliers_db)
    publish_event("supplier_created", supplier.dict())
    return supplier

@router.put("/suppliers/{id}", response_model=Supplier)
def update_supplier(id: int, updated_product: Supplier):
    for index, supplier in enumerate(suppliers_db):
        if supplier.id == id:
            suppliers_db[index] = updated_product
            save_suppliers_to_json(suppliers_db)
            publish_event("supplier_updated", updated_product.dict())
            return updated_product
    raise HTTPException(status_code=404, detail="Supplier not found")

@router.delete("/suppliers/{id}", status_code=204)
def delete_supplier(id: int):
    for index, supplier in enumerate(suppliers_db):
        if supplier.id == id:
            deleted_supplier = suppliers_db.pop(index)
            save_suppliers_to_json(suppliers_db)
            publish_event("supplier_deleted", deleted_supplier.dict())
            return
    raise HTTPException(status_code=404, detail="Supplier not found")
