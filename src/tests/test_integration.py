from fastapi.testclient import TestClient
import os
import tempfile
import json
from main import app
from db import Base, engine

client = TestClient(app)


def setup_module(module):
    # make fresh DB
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception:
        pass
    Base.metadata.create_all(bind=engine)


def test_create_and_get_product():
    payload = {"name": "Test product", "description": "A test", "price": 9.99, "quantity": 5}
    r = client.post("/api/v1/products/", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["name"] == "Test product"

    r2 = client.get(f"/api/v1/products/{body['id']}")
    assert r2.status_code == 200


def test_banned_phrase_blocks_creation_and_update():
    # add banned phrase
    r = client.post("/api/v1/banned-phrases/", json={"phrase": "banned"})
    assert r.status_code == 201

    # try create product with banned in name
    payload = {"name": "Not allowed Banned Item", "description": "X", "price": 1, "quantity": 1}
    r = client.post("/api/v1/products/", json=payload)
    assert r.status_code == 400

    # create allowed product
    payload2 = {"name": "Allowed item", "description": "ok", "price": 2, "quantity": 2}
    r = client.post("/api/v1/products/", json=payload2)
    assert r.status_code == 201
    pid = r.json()["id"]

    # try update name to banned
    r = client.put(f"/api/v1/products/{pid}", json={"name": "contains banned phrase"})
    assert r.status_code == 400


def test_history_tracking():
    # create
    payload = {"name": "HistProd", "description": "orig", "price": 3.0, "quantity": 10}
    r = client.post("/api/v1/products/", json=payload)
    assert r.status_code == 201
    pid = r.json()["id"]

    # update price and quantity
    r = client.put(f"/api/v1/products/{pid}", json={"price": 5.0, "quantity": 8})
    assert r.status_code == 200

    # get history
    r = client.get(f"/api/v1/products/{pid}/history")
    assert r.status_code == 200
    hist = r.json()
    # at least two entries: CREATED and UPDATED
    types = [h["change_type"] for h in hist]
    assert "CREATED" in types
    assert "UPDATED" in types


def test_delete_and_history_on_delete():
    payload = {"name": "ToDelete", "description": "x", "price": 1.0, "quantity": 1}
    r = client.post("/api/v1/products/", json=payload)
    pid = r.json()["id"]

    r = client.delete(f"/api/v1/products/{pid}")
    assert r.status_code == 204

    # history should include DELETED
    r = client.get(f"/api/v1/products/{pid}/history")
    assert r.status_code == 200
    hist = r.json()
    types = [h["change_type"] for h in hist]
    assert "DELETED" in types