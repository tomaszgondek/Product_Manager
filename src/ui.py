from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.db import get_db
from src.services.product_service import ProductService, BusinessRuleViolation

router = APIRouter(prefix="/ui", tags=["ui"])
templates = Jinja2Templates(directory="src/templates")

@router.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    svc = ProductService(db)
    products = svc.list()
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

@router.post("/add")
def add_product(
    name: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    category: str = Form(...),
    db: Session = Depends(get_db)
):
    svc = ProductService(db)
    try:
        svc.create_product({
            "name": name,
            "price": price,
            "quantity": quantity,
            "category": category,
            "description": "",
        })
    except BusinessRuleViolation as e:
        return {"error": e.args[0]}
    return RedirectResponse("/ui", status_code=303)


# 🗑️ NEW: Delete product endpoint
@router.post("/delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    svc = ProductService(db)
    product = svc.get_product(product_id)
    if not product:
        return RedirectResponse("/ui", status_code=303)
    svc.delete_product(product_id)
    return RedirectResponse("/ui", status_code=303)