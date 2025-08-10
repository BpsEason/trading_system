# API 規格

## Django Order API

### GET /api/orders/
列出所有訂單。

### POST /api/orders/
建立新訂單。

### GET /api/orders/{id}/
取得單筆訂單。

### PUT /api/orders/{id}/
更新訂單狀態。

### DELETE /api/orders/{id}/
刪除訂單。

## FastAPI 定價與風控

### POST /price
檢查限額並計算價格。
