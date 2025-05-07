from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Product
from app.database import products_db, save_products_to_json
from app.rabbitmq import publish_event

router = APIRouter()



@router.get("/products", response_model=List[Product])
def get_products():
    return products_db

@router.get("/products/{id}", response_model=Product)
def get_product(id: int):
    product = next((p for p in products_db if p.id == id), None)
    if product:
        publish_event("product_found", product.dict())
        return product
    publish_event("product_not_found", {})
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("/products", response_model=Product, status_code=201)
def create_product(product: Product):
    if any(p.id == product.id for p in products_db):
        raise HTTPException(status_code=400, detail="Product with this ID already exists")
    products_db.append(product)
    save_products_to_json(products_db)
    publish_event("product_created", product.dict())
    return product

@router.put("/products/{id}", response_model=Product)
def update_product(id: int, updated_product: Product):
    for index, product in enumerate(products_db):
        if product.id == id:
            products_db[index] = updated_product
            save_products_to_json(products_db)
            publish_event("product_updated", updated_product.dict())
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/products/{id}", status_code=204)
def delete_product(id: int):
    for index, product in enumerate(products_db):
        if product.id == id:
            deleted_product = products_db.pop(index)
            save_products_to_json(products_db)
            publish_event("product_deleted", deleted_product.dict())
            return
    raise HTTPException(status_code=404, detail="Product not found")
