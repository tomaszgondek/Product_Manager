from repositories.product_repository import ProductRepository, BannedPhraseRepository
from sqlalchemy.orm import Session
from typing import Dict, Any, List

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

    def create_product(self, data: Dict[str, Any]):
        if not self._is_name_allowed(data["name"]):
            raise BusinessRuleViolation("Product name contains banned phrase")
        return self.repo.create(data)

    def update_product(self, product_id: int, changes: Dict[str, Any]):
        prod = self.repo.get(product_id)
        if not prod:
            return None
        if "name" in changes and not self._is_name_allowed(changes["name"]):
            raise BusinessRuleViolation("Product name contains banned phrase")
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
        q = self.db.query(ProductHistory)
        if product_id:
            q = q.filter(ProductHistory.product_id == product_id)
        return q.order_by(ProductHistory.timestamp.desc()).all()