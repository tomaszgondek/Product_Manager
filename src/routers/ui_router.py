from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.db import get_db
from src.services.product_service import ProductService, BusinessRuleViolation
from src.repositories.product_repository import BannedPhraseRepository

router = APIRouter(prefix="/ui", tags=["ui"])
templates = Jinja2Templates(directory="src/templates")

@router.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    svc = ProductService(db)
    products = svc.list()
    banned_repo = BannedPhraseRepository(db)
    banned_phrases = banned_repo.list()
    return templates.TemplateResponse("index.html", {"request": request, "products": products, "banned_phrases": banned_phrases, "errors": {}})

@router.post("/add")
def add_product(request: Request, name: str = Form(...), description: str = Form(''), price: float = Form(...), quantity: int = Form(...), category: str = Form(...), db: Session = Depends(get_db)):
    svc = ProductService(db)
    try:
        svc.create_product({"name": name, "description": description, "price": price, "quantity": quantity, "category": category})
    except BusinessRuleViolation as e:
        banned_repo = BannedPhraseRepository(db)
        banned_phrases = banned_repo.list()
        return templates.TemplateResponse("index.html", {"request": request, "products": svc.list(), "banned_phrases": banned_phrases, "errors": e.errors, "form": {"name": name, "description": description, "price": price, "quantity": quantity, "category": category}})
    return RedirectResponse("/ui", status_code=303)

@router.get("/edit/{product_id}")
def edit_page(product_id: int, request: Request, db: Session = Depends(get_db)):
    svc = ProductService(db)
    prod = svc.get(product_id)
    if not prod:
        return RedirectResponse("/ui", status_code=303)
    banned_repo = BannedPhraseRepository(db)
    banned_phrases = banned_repo.list()
    return templates.TemplateResponse("edit.html", {"request": request, "product": prod, "banned_phrases": banned_phrases, "errors": {}})

@router.post("/edit/{product_id}")
def edit_product(product_id: int, request: Request, name: str = Form(...), description: str = Form(''), price: float = Form(...), quantity: int = Form(...), category: str = Form(...), db: Session = Depends(get_db)):
    svc = ProductService(db)
    try:
        svc.update_product(product_id, {"name": name, "description": description, "price": price, "quantity": quantity, "category": category})
    except BusinessRuleViolation as e:
        prod = svc.get(product_id)
        banned_repo = BannedPhraseRepository(db)
        banned_phrases = banned_repo.list()
        return templates.TemplateResponse("edit.html", {"request": request, "product": prod, "banned_phrases": banned_phrases, "errors": e.errors})
    return RedirectResponse("/ui", status_code=303)

@router.post("/delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    svc = ProductService(db)
    svc.delete_product(product_id)
    return RedirectResponse("/ui", status_code=303)

@router.post("/add_banned")
def add_banned_phrase(phrase: str = Form(...), db: Session = Depends(get_db)):
    repo = BannedPhraseRepository(db)
    if not repo.get_by_phrase(phrase):
        repo.create(phrase)
    return RedirectResponse("/ui", status_code=303)

@router.post("/delete_banned/{phrase_id}")
def delete_banned_phrase(phrase_id: int, db: Session = Depends(get_db)):
    repo = BannedPhraseRepository(db)
    repo.delete(phrase_id)
    return RedirectResponse("/ui", status_code=303)
