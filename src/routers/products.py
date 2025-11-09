from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from src.db import get_db
from src.services.product_service import ProductService, BusinessRuleViolation

router = APIRouter(prefix="/api/v1/products", tags=["products"])

@router.get("/", status_code=status.HTTP_200_OK)
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    svc = ProductService(db)
    products = svc.list(skip, limit)
    # Convert SQLAlchemy objects to dicts for JSON serialization
    return [svc.repo.serialize(p) for p in products]

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(payload: dict, db: Session = Depends(get_db)):
    svc = ProductService(db)
    try:
        new_product = svc.create_product(payload)
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=400, detail=e.errors)
    return svc.repo.serialize(new_product)

@router.get("/{product_id}", status_code=status.HTTP_200_OK)
def get_product(product_id: int, db: Session = Depends(get_db)):
    svc = ProductService(db)
    product = svc.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return svc.repo.serialize(product)

@router.put("/{product_id}", status_code=status.HTTP_200_OK)
def update_product(product_id: int, payload: dict, db: Session = Depends(get_db)):
    svc = ProductService(db)
    try:
        updated = svc.update_product(product_id, payload)
        if not updated:
            raise HTTPException(status_code=404, detail="Product not found")
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=400, detail=e.errors)
    return svc.repo.serialize(updated)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    svc = ProductService(db)
    ok = svc.delete_product(product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
    return
