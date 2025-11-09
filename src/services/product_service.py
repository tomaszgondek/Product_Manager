from src.repositories.product_repository import ProductRepository, BannedPhraseRepository
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from src.repositories.product_repository import _serialize_product

PRICE_LIMITS = {
    "Elektronika": (50, 50000),
    "Książki": (5, 500),
    "Odzież": (10, 5000),
}

class BusinessRuleViolation(Exception):
    pass

class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProductRepository(db)
        self.banned_repo = BannedPhraseRepository(db)

    def _is_name_allowed(self, name: str) -> bool:
        phrases = [p.phrase.lower() for p in self.banned_repo.list()]
        name_l = name.lower()
        for ph in phrases:
            if ph in name_l:
                return False
        return True

    def _validate_domain_rules(self, data: Dict[str, Any], is_update=False, product_id=None):
        errors = {}

        # Unikalna nazwa
        if "name" in data and data.get("name") is not None:
            existing = self.repo.get_by_name(data["name"])
            if existing and (not is_update or existing.id != product_id):
                errors["name"] = "Produkt o tej nazwie już istnieje."

        # Cena zależna od kategorii
        cat = data.get("category")
        price = data.get("price")
        if cat and price is not None:
            if cat in PRICE_LIMITS:
                min_p, max_p = PRICE_LIMITS[cat]
                if not (min_p <= price <= max_p):
                    errors["price"] = f"Cena dla kategorii {cat} musi być między {min_p} a {max_p} PLN."

        # Ilość nieujemna
        if "quantity" in data and data.get("quantity") is not None:
            if data["quantity"] < 0:
                errors["quantity"] = "Ilość nie może być ujemna."

        if errors:
            raise BusinessRuleViolation(errors)

    def create_product(self, data: Dict[str, Any]):
        self._validate_domain_rules(data, is_update=False)
        if not self._is_name_allowed(data["name"]):
            raise BusinessRuleViolation({"name": "Nazwa zawiera zabronioną frazę"})
        return self.repo.create(data)

    def update_product(self, product_id: int, changes: Dict[str, Any]):
        prod = self.repo.get(product_id)
        if not prod:
            return None
        combined = _serialize_product(prod)
        combined.update(changes)
        self._validate_domain_rules(combined, is_update=True, product_id=prod.id)
        if "name" in changes and not self._is_name_allowed(changes["name"]):
            raise BusinessRuleViolation({"name": "Nazwa zawiera zabronioną frazę"})
        return self.repo.update(prod, changes)

    def delete_product(self, product_id: int):
        prod = self.repo.get(product_id)
        if not prod:
            return False
        self.repo.delete(prod)
        return True

    def get(self, pid: int):
        return self.repo.get(pid)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip, limit)

    def get_history(self, product_id: int = None):
        q = self.db.query(__import__('app.models', fromlist=['ProductHistory']).ProductHistory)
        if product_id:
            q = q.filter(__import__('app.models', fromlist=['ProductHistory']).ProductHistory.product_id == product_id)
        return q.order_by(__import__('app.models', fromlist=['ProductHistory']).ProductHistory.timestamp.desc()).all()
