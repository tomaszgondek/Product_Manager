from fastapi import FastAPI
from src.db import engine, Base
from src.routers import products as products_router
from src.routers import banned_phrases as banned_router
from src.ui import router as ui_router
from sqlalchemy.orm import Session
from src.models import Product
from datetime import datetime

app = FastAPI(title="Products API + UI")

# include routers
app.include_router(products_router.router)
app.include_router(banned_router.router)
app.include_router(ui_router)

# create tables
Base.metadata.create_all(bind=engine)

# seed data (only if empty)
def seed_products():
    db = Session(bind=engine)
    if db.query(Product).count() == 0:
        sample_products = [
            {"name": "LaptopPro15", "description": "Laptop 15 cali, 16GB RAM", "price": 4999.99, "quantity": 5, "category": "Elektronika"},
            {"name": "SmartfonGalaxyX", "description": "Smartfon z ekranem OLED", "price": 2999.00, "quantity": 12, "category": "Elektronika"},
            {"name": "MonitorUltraSharp27", "description": "Monitor 27 cali 4K", "price": 1799.00, "quantity": 8, "category": "Elektronika"},
            {"name": "KlawiaturaMechaniczna", "description": "Podświetlana klawiatura RGB", "price": 399.00, "quantity": 20, "category": "Elektronika"},
            {"name": "MyszBezprzewodowa", "description": "Ergonomiczna mysz bezprzewodowa", "price": 149.00, "quantity": 25, "category": "Elektronika"},
            {"name": "DrukarkaLaserowa", "description": "Szybka drukarka monochromatyczna", "price": 699.00, "quantity": 10, "category": "Elektronika"},
            {"name": "KsiazkaPython", "description": "Podręcznik Pythona", "price": 99.99, "quantity": 50, "category": "Książki"},
            {"name": "KsiazkaHistoria", "description": "Historia Polski", "price": 59.00, "quantity": 30, "category": "Książki"},
            {"name": "KsiazkaRomans", "description": "Lekka lektura", "price": 19.99, "quantity": 40, "category": "Książki"},
            {"name": "BluzaSportowa", "description": "Bawełniana bluza", "price": 149.00, "quantity": 20, "category": "Odzież"},
            {"name": "KoszulkaBawelniana", "description": "Koszulka z nadrukiem", "price": 59.00, "quantity": 60, "category": "Odzież"},
            {"name": "SpodnieJeans", "description": "Jeansy klasyczne", "price": 199.00, "quantity": 35, "category": "Odzież"},
            {"name": "Powerbank20000", "description": "Szybkie ładowanie PD 3.0", "price": 199.00, "quantity": 30, "category": "Elektronika"},
            {"name": "DyskSSD1TB", "description": "NVMe, odczyt 3500 MB/s", "price": 549.00, "quantity": 11, "category": "Elektronika"},
            {"name": "Pendrive128GB", "description": "USB 3.2, metalowa obudowa", "price": 89.00, "quantity": 50, "category": "Elektronika"},
        ]
        for p in sample_products:
            db.add(Product(**p, created_at=datetime.utcnow(), updated_at=datetime.utcnow()))
        db.commit()
        print("Exemplary products added to db.")
    db.close()

seed_products()

@app.get("/")
def root():
    return {"message": "Products API + UI. See /docs and /ui"}
