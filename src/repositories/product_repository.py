from sqlalchemy.orm import Session
from src.models import Product, ProductHistory, BannedPhrase
from typing import List, Optional, Dict, Any
from datetime import datetime

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
        self._add_history(product.id, "CREATED", None, _serialize_product(product))
        return product

    def update(self, product: Product, changes: Dict[str, Any]) -> Product:
        previous = _serialize_product(product)
        for k, v in changes.items():
            setattr(product, k, v)
        from datetime import datetime
        product.updated_at = datetime.utcnow()
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        self._add_history(product.id, "UPDATED", previous, _serialize_product(product))
        return product

    def delete(self, product: Product) -> None:
        prev = _serialize_product(product)
        self.db.delete(product)
        self.db.commit()
        self._add_history(None, "DELETED", prev, None)

    def _add_history(self, product_id: Optional[int], change_type: str, previous: Optional[Dict], current: Optional[Dict]) -> None:
        hist = ProductHistory(product_id=product_id, change_type=change_type, previous=previous, current=current)
        self.db.add(hist)
        self.db.commit()

class BannedPhraseRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[BannedPhrase]:
        return self.db.query(BannedPhrase).all()

    def get_by_phrase(self, phrase: str) -> Optional[BannedPhrase]:
        return self.db.query(BannedPhrase).filter(BannedPhrase.phrase == phrase).first()

    def create(self, phrase: str) -> BannedPhrase:
        obj = BannedPhrase(phrase=phrase)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, phrase_id: int) -> None:
        obj = self.db.query(BannedPhrase).filter(BannedPhrase.id == phrase_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

def _serialize_product(product: Product) -> dict:
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
