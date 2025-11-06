from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    quantity = Column(Integer, nullable=False, default=0)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


history = relationship("ProductHistory", back_populates="product", cascade="all, delete-orphan")


class ProductHistory(Base):
    __tablename__ = "product_history"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    change_type = Column(String, nullable=False) # CREATED, UPDATED, DELETED
    previous = Column(JSON, nullable=True)
    current = Column(JSON, nullable=True)


product = relationship("Product", back_populates="history")


class BannedPhrase(Base):
    __tablename__ = "banned_phrases"
    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)