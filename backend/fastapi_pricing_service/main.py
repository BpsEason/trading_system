from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from decimal import Decimal
from .risk import check_limits

app = FastAPI(
    title="FastAPI Pricing Service",
    description="實時計價與風險控制服務",
    version="0.0.1",
)

class PriceRequest(BaseModel):
    user_id: str = Field(..., example="user123", description="用戶ID")
    amount: Decimal = Field(..., gt=0, decimal_places=2, example=100.00, description="交易金額")
    currency: str = Field(..., pattern="^(USD|EUR|JPY)$", example="USD", description="交易貨幣 (USD, EUR, JPY)")

@app.post("/price", summary="執行計價與風險檢查", response_description="成功計價或風險不通過訊息")
def price(req: PriceRequest):
    """
    接收交易請求，檢查是否超出風險限額，並返回計價結果。
    - **user_id**: 進行交易的用戶ID。
    - **amount**: 交易金額，必須大於0。
    - **currency**: 交易貨幣，目前支援 USD, EUR, JPY。
    """
    allowed, msg = check_limits(req.amount, req.currency)
    if not allowed:
        raise HTTPException(status_code=400, detail={"message": f"交易被拒絕: {msg}"})
    
    # 假設這裡會根據複雜的邏輯計算最終價格
    final_price = req.amount * Decimal('1.001') # 簡單的加價模擬

    return {"allowed": True, "price": final_price, "message": "交易獲准"}
