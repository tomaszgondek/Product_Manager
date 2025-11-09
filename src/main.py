from fastapi import FastAPI
from src.db import engine, Base
from src.routers import products, banned_phrases, ui
from sqlalchemy.orm import Session
from src.models import Product
from datetime import datetime

app = FastAPI(title="Products Clean API")

# Register routers
app.include_router(products.router)
app.include_router(banned_phrases.router)
app.include_router(ui.router)

# Create DB tables
Base.metadata.create_all(bind=engine)

def seed_products():
    db = Session(bind=engine)
    if db.query(Product).count() == 0:
        sample = [
            {"name": "LaptopPro15", "description": "Laptop 15 inch", "price": 4999.99, "quantity": 5, "category": "Electronics"},
            {"name": "PythonBook", "description": "Python programming guide", "price": 99.99, "quantity": 50, "category": "Books"},
            {"name": "SportHoodie", "description": "Lightweight hoodie", "price": 149.00, "quantity": 20, "category": "Clothing"},
        ]
        for p in sample:
            db.add(Product(**p, created_at=datetime.utcnow(), updated_at=datetime.utcnow()))
        db.commit()
    db.close()

seed_products()

@app.get("/")
def root():
    return {"message": "Products API running successfully"}
