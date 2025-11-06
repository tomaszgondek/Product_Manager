from pydantic import BaseModel, Field, validator
from typing import Optional, List, Any
from datetime import datetime


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str]
    price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    quantity: Optional[int]
    active: Optional[bool]


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