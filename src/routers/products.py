from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from db import get_db
from schemas import ProductCreate, ProductOut, ProductUpdate, ProductHistoryOut
from services.product_service import ProductService, BusinessRuleViolation

router = APIRouter(prefix="/api/v1/products", tags=["products"])

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    svc = ProductService(db)
    try:
        prod = svc.create_product(payload.dict())
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=400, detail=str(e))
    return prod

@router.get("/", response_model=List[ProductOut])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    svc = ProductService(db)
    return svc.list(skip, limit)

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    svc = ProductService(db)
    prod = svc.get(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    svc = ProductService(db)
    try:
        prod = svc.update_product(product_id, payload.dict(exclude_unset=True))
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    svc = ProductService(db)
    ok = svc.delete_product(product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
    return

@router.get("/{product_id}/history", response_model=List[ProductHistoryOut])
def get_history(product_id: int, db: Session = Depends(get_db)):
    svc = ProductService(db)
    return svc.get_history(product_id)