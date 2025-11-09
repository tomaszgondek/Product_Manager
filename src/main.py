from fastapi import FastAPI
from src.db import engine, Base
from src.routers import products, banned_phrases, ui
from sqlalchemy.orm import Session
from src.models import Product, BannedPhrase
from datetime import datetime

app = FastAPI(title="Products API")

app.include_router(products.router)
app.include_router(banned_phrases.router)
app.include_router(ui.router)

Base.metadata.create_all(bind=engine)


def seed_products_and_phrases():
    db = Session(bind=engine)

    # --- Seed Products ---
    if db.query(Product).count() == 0:
        sample_products = [
            {"name": "LaptopPro15", "description": "Laptop 15 inch", "price": 4999.99, "quantity": 5, "category": "Electronics"},
            {"name": "PythonBook", "description": "Comprehensive Python programming guide", "price": 89.99, "quantity": 40, "category": "Books"},
            {"name": "SportHoodie", "description": "Lightweight sport hoodie", "price": 149.0, "quantity": 25, "category": "Clothing"},
            {"name": "SmartWatchX", "description": "Fitness smart watch", "price": 899.0, "quantity": 15, "category": "Electronics"},
            {"name": "DataScienceBook", "description": "Data Science for Beginners", "price": 120.0, "quantity": 60, "category": "Books"},
            {"name": "WinterJacket", "description": "Warm insulated jacket", "price": 399.0, "quantity": 10, "category": "Clothing"},
            {"name": "GamingMouse", "description": "RGB optical gaming mouse", "price": 199.0, "quantity": 50, "category": "Electronics"},
            {"name": "SciFiNovel", "description": "Classic sci-fi novel", "price": 59.0, "quantity": 80, "category": "Books"},
            {"name": "RunningShoes", "description": "Comfortable running shoes", "price": 299.0, "quantity": 30, "category": "Clothing"},
            {"name": "BluetoothSpeaker", "description": "Portable Bluetooth speaker", "price": 249.0, "quantity": 20, "category": "Electronics"},
        ]
        for p in sample_products:
            db.add(Product(**p, created_at=datetime.utcnow(), updated_at=datetime.utcnow()))
        db.commit()

    # --- Seed Banned Phrases ---
    if db.query(BannedPhrase).count() == 0:
        sample_phrases = ["fake", "banned", "illegal", "test", "scam"]
        for phrase in sample_phrases:
            db.add(BannedPhrase(phrase=phrase, created_at=datetime.utcnow()))
        db.commit()

    db.close()



seed_products_and_phrases()


@app.get("/")
def root():
    return {"message": "Products API running successfully with seeded data"}
