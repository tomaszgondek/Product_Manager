from fastapi.testclient import TestClient
from src.main import app
from src.db import Base, engine
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    from src.main import seed_products
    seed_products()
    yield

def test_ui_index():
    r = client.get("/ui/")
    assert r.status_code == 200
    assert "Panel produktów" in r.text

def test_add_product_via_ui():
    data = {
        "name": "UITestProd1",
        "description": "x",
        "price": "100",
        "quantity": "2",
        "category": "Elektronika"
    }
    r = client.post("/ui/add", data=data, allow_redirects=False)
    assert r.status_code in (302,303)
