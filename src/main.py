from fastapi import FastAPI
from db import engine, Base
from routers import products as products_router
from routers import banned_phrases as banned_router
from sqlalchemy.orm import Session
from models import Product
from datetime import datetime

def seed_products():
    db = Session(bind=engine)
    if db.query(Product).count() == 0:  # tylko jeśli baza pusta
        sample_products = [
            {"name": "Laptop Pro 15", "description": "Laptop 15 cali, 16GB RAM", "price": 4999.99, "quantity": 5},
            {"name": "Smartfon Galaxy X", "description": "Smartfon z ekranem OLED", "price": 2999.00, "quantity": 12},
            {"name": "Monitor UltraSharp 27", "description": "Monitor 27 cali 4K", "price": 1799.00, "quantity": 8},
            {"name": "Klawiatura Mechaniczna", "description": "Podświetlana klawiatura RGB", "price": 399.00, "quantity": 20},
            {"name": "Mysz Bezprzewodowa", "description": "Ergonomiczna mysz bezprzewodowa", "price": 149.00, "quantity": 25},
            {"name": "Drukarka Laserowa", "description": "Szybka drukarka monochromatyczna", "price": 699.00, "quantity": 10},
            {"name": "Kamera Internetowa", "description": "Full HD 1080p, mikrofon wbudowany", "price": 249.00, "quantity": 15},
            {"name": "Słuchawki Bluetooth", "description": "Dźwięk Hi-Fi, redukcja szumów", "price": 599.00, "quantity": 18},
            {"name": "Tablet 10.5", "description": "Tablet z rysikiem, 128GB pamięci", "price": 2199.00, "quantity": 9},
            {"name": "Powerbank 20000mAh", "description": "Szybkie ładowanie PD 3.0", "price": 199.00, "quantity": 30},
            {"name": "Router Wi-Fi 6", "description": "Obsługa MU-MIMO, 3 anteny", "price": 499.00, "quantity": 7},
            {"name": "Dysk SSD 1TB", "description": "NVMe, odczyt 3500 MB/s", "price": 549.00, "quantity": 11},
            {"name": "Pendrive 128GB", "description": "USB 3.2, metalowa obudowa", "price": 89.00, "quantity": 50},
            {"name": "Kabel HDMI 2.1", "description": "4K 120Hz, 2 metry", "price": 39.00, "quantity": 60},
            {"name": "Głośnik Bluetooth", "description": "Wodoodporny, 10h pracy", "price": 299.00, "quantity": 14},
        ]
        for p in sample_products:
            db.add(Product(**p, created_at=datetime.utcnow(), updated_at=datetime.utcnow()))
        db.commit()
        print("✅ Dodano przykładowe produkty do bazy danych")
    db.close()

seed_products()

app = FastAPI(title="Products API - N-Layer Example")

# include routers
app.include_router(products_router.router)
app.include_router(banned_router.router)

# create tables
Base.metadata.create_all(bind=engine)

# root
@app.get("/")
def root():
    return {"message": "Products API. See /docs for OpenAPI UI"}
