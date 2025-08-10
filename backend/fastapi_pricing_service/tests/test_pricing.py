from fastapi.testclient import TestClient
from fastapi_pricing_service.main import app

client = TestClient(app)

def test_price_within_limit():
    res = client.post("/price", json={"user_id":"testuser", "amount":100.00, "currency":"USD"})
    assert res.status_code == 200
    assert res.json()["allowed"] == True
    assert "price" in res.json()
    assert res.json()["message"] == "交易獲准"

def test_price_exceed_limit():
    res = client.post("/price", json={"user_id":"testuser", "amount":20000.00, "currency":"USD"})
    assert res.status_code == 400
    assert res.json()["detail"]["message"] == "交易被拒絕: USD 金額 20000.00 超出限額 10000"

def test_price_invalid_currency():
    res = client.post("/price", json={"user_id":"testuser", "amount":100.00, "currency":"XYZ"})
    assert res.status_code == 422 # Pydantic validation error for regex
    # 這裡的 detail 會是 FastAPI 自動生成的 Pydantic 驗證錯誤訊息，會包含 "value is not a valid enumeration member" 或 "string does not match regex"
    # 因此，我們只需要檢查錯誤的存在，而非精確的訊息匹配
    assert "detail" in res.json()
    assert len(res.json()["detail"]) > 0

def test_price_zero_amount():
    res = client.post("/price", json={"user_id":"testuser", "amount":0.00, "currency":"USD"})
    assert res.status_code == 422 # Pydantic validation error for gt=0
    assert "detail" in res.json()
    assert len(res.json()["detail"]) > 0
