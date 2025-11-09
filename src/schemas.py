from pydantic import BaseModel, Field, validator
from typing import Optional, List, Any
from datetime import datetime

ALLOWED_CATEGORIES = ["Elektronika", "Książki", "Odzież"]

class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)
    description: Optional[str]
    price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
    category: str = Field(...)

    @validator("name")
    def validate_name(cls, v):
        if not v.isalnum():
            raise ValueError("Nazwa może zawierać tylko litery i cyfry")
        return v

    @validator("category")
    def validate_category(cls, v):
        if v not in ALLOWED_CATEGORIES:
            raise ValueError(f"Kategoria musi być jedną z: {', '.join(ALLOWED_CATEGORIES)}")
        return v

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=20)
    description: Optional[str]
    price: Optional[float] = Field(None, ge=0)
    quantity: Optional[int] = Field(None, ge=0)
    category: Optional[str]
    active: Optional[bool]

    @validator("name")
    def validate_name(cls, v):
        if v is None:
            return v
        if not v.isalnum():
            raise ValueError("Nazwa może zawierać tylko litery i cyfry")
        return v

    @validator("category")
    def validate_category(cls, v):
        if v is None:
            return v
        if v not in ALLOWED_CATEGORIES:
            raise ValueError(f"Kategoria musi być jedną z: {', '.join(ALLOWED_CATEGORIES)}")
        return v

class ProductOut(ProductBase):
    id: int
    active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ProductHistoryOut(BaseModel):
    id: int
    product_id: Optional[int]
    timestamp: datetime
    change_type: str
    previous: Optional[Any]
    current: Optional[Any]

    class Config:
        orm_mode = True

class BannedPhraseCreate(BaseModel):
    phrase: str

class BannedPhraseOut(BaseModel):
    id: int
    phrase: str
    created_at: datetime

    class Config:
        orm_mode = True
