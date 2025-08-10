from fastapi.testclient import TestClient
from fastapi_pricing_service.main import app

client = TestClient(app)

def test_within():
    res = client.post("/price", json={"user_id":"u","amount":100,"currency":"USD"})
    assert res.status_code == 200
    assert res.json()["allowed"]

def test_exceed():
    res = client.post("/price", json={"user_id":"u","amount":20000,"currency":"USD"})
    assert res.status_code == 400
