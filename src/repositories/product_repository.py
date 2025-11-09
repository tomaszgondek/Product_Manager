from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from src.models import Product, BannedPhrase

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def list(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.db.query(Product).offset(skip).limit(limit).all()

    def get_by_name(self, name: str) -> Optional[Product]:
        return self.db.query(Product).filter(Product.name == name).first()

    def create(self, product_data: Dict[str, Any]) -> Product:
        product = Product(**product_data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product, changes: Dict[str, Any]) -> Product:
        for k, v in changes.items():
            setattr(product, k, v)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()

    def serialize(self, product: Product) -> dict:
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity,
            "category": product.category,
            "active": product.active,
            "created_at": product.created_at.isoformat() if product.created_at else None,
            "updated_at": product.updated_at.isoformat() if product.updated_at else None,
        }


class BannedPhraseRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[BannedPhrase]:
        return self.db.query(BannedPhrase).all()

    def get_by_phrase(self, phrase: str) -> Optional[BannedPhrase]:
        return self.db.query(BannedPhrase).filter(BannedPhrase.phrase == phrase).first()

    def create(self, phrase: str) -> BannedPhrase:
        bp = BannedPhrase(phrase=phrase)
        self.db.add(bp)
        self.db.commit()
        self.db.refresh(bp)
        return bp

    def delete(self, phrase_id: int) -> None:
        obj = self.db.query(BannedPhrase).filter(BannedPhrase.id == phrase_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()
