from src.repositories.product_repository import ProductRepository, BannedPhraseRepository
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

PRICE_LIMITS = {
    "Electronics": (50, 50000),
    "Books": (5, 500),
    "Clothing": (10, 5000),
}

class BusinessRuleViolation(Exception):
    def __init__(self, errors):
        super().__init__(errors)
        self.errors = errors

class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProductRepository(db)
        self.banned_repo = BannedPhraseRepository(db)

    def _is_name_allowed(self, name: str) -> bool:
        phrases = [p.phrase.lower() for p in self.banned_repo.list()]
        for ph in phrases:
            if ph in name.lower():
                return False
        return True

    def _validate_domain_rules(self, data: Dict[str, Any], is_update: bool = False, product_id: Optional[int] = None):
        errors = {}
        name = data.get("name")
        if name is not None:
            if not (3 <= len(name) <= 20):
                errors["name"] = "Name must be between 3 and 20 characters."
            if not name.isalnum():
                errors["name"] = "Name must contain only letters and numbers."
            existing = self.repo.get_by_name(name)
            if existing and (not is_update or existing.id != product_id):
                errors["name"] = "Product with this name already exists."

        category = data.get("category")
        price = data.get("price")
        if category and price is not None:
            if category in PRICE_LIMITS:
                min_p, max_p = PRICE_LIMITS[category]
                if not (min_p <= price <= max_p):
                    errors["price"] = f"Price for category {category} must be between {min_p} and {max_p} PLN."

        quantity = data.get("quantity")
        if quantity is not None:
            try:
                if int(quantity) < 0:
                    errors["quantity"] = "Quantity cannot be negative."
            except Exception:
                errors["quantity"] = "Quantity must be an integer."

        if errors:
            raise BusinessRuleViolation(errors)

    def create_product(self, data: Dict[str, Any]):
        self._validate_domain_rules(data, is_update=False)
        if not self._is_name_allowed(data["name"]):
            raise BusinessRuleViolation({"name": "Name contains a banned phrase."})
        return self.repo.create(data)

    def update_product(self, product_id: int, changes: Dict[str, Any]):
        prod = self.repo.get(product_id)
        if not prod:
            return None
        combined = self.repo.serialize(prod)
        combined.update(changes)
        self._validate_domain_rules(combined, is_update=True, product_id=prod.id)
        if "name" in changes and not self._is_name_allowed(changes["name"]):
            raise BusinessRuleViolation({"name": "Name contains a banned phrase."})
        return self.repo.update(prod, changes)

    def delete_product(self, product_id: int):
        prod = self.repo.get(product_id)
        if not prod:
            return False
        self.repo.delete(prod)
        return True

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip, limit)

    def get(self, pid: int):
        return self.repo.get(pid)
