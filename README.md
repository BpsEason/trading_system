# 智能交易訂單管理系統

[![Coverage](https://img.shields.io/badge/coverage-80%25-green)](https://github.com/your-username/trading_system) <!-- Placeholder, integrate with coverage reports later -->
[![Mutation Testing](https://img.shields.io/badge/mutation_testing-Passed-brightgreen)](https://github.com/your-username/trading_system) <!-- Placeholder, integrate with mutation testing reports later -->

集中管理訂單、實時計價風控、即時通知／簽核，並由 AI 自動生成代碼骨架與測試。

## 目錄
- `backend/` Django REST + FastAPI 後端服務
- `frontend-react/` React + TypeScript 前端應用
- `flutter-app/` Flutter 行動端應用
- `docs/` API 規格、審計日誌、系統架構圖
- `.github/` GitHub Actions CI/CD 工作流與專案模板
- `tools/` 專案開發輔助腳本，包含 AI 代碼生成工具

## 關鍵程式碼範例

---

### 1. Django `OrderViewSet`（後端訂單 CRUD + 審計日誌）

```python
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from .audit import AuditLog  # 假設已有審計日誌服務模組

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()            # 取出所有訂單
    serializer_class = OrderSerializer        # 指定使用的序列化器

    def perform_create(self, serializer):
        # 在建立訂單時，先儲存資料
        instance = serializer.save()         
        # 建立一筆 CREATE 操作的審計日誌
        AuditLog.log_create(self.request.user, instance)  
```

- `serializer.save()`：新增一筆訂單到資料庫  
- `AuditLog.log_create(...)`：記錄「誰」「何時」「新增了哪筆訂單」

---

### 2. FastAPI 「計價與風控」接口

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from decimal import Decimal
from .risk import check_limits

app = FastAPI(title="Pricing Service")

class PriceRequest(BaseModel):
    user_id: str  = Field(..., example="user123", description="使用者 ID")
    amount: Decimal = Field(..., gt=0, description="交易金額，必須大於 0")
    currency: str   = Field(..., regex="^(USD|EUR|JPY)$", description="貨幣：USD/EUR/JPY")

@app.post("/price")
async def price(req: PriceRequest):
    # 風控檢查：檢驗金額、貨幣是否合規
    ok, msg = check_limits(req.amount, req.currency)
    if not ok:
        # 超限或格式錯誤，回 400 並帶出錯誤訊息
        raise HTTPException(status_code=400, detail={"message": msg})

    # 計算最終價格（範例：加 0.1%）
    final_price = req.amount * Decimal("1.001")
    return {
        "allowed": True,                   # 交易是否可執行
        "price": final_price,              # 最終成交價格
        "message": "交易獲准"              # 成功訊息
    }
```

- `Field(..., gt=0)`：Pydantic 自動驗證 `amount > 0`  
- `regex="^(USD|EUR|JPY)$"`：僅允許三種貨幣  
- `check_limits(…)`：自訂的風控邏輯函式

---

### 3. React 訂單列表元件（前端展示與 API 呼叫）

```tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Order {
  id: string;
  amount: string;
  currency: string;
  status: string;
}

export default function OrderList() {
  const [orders, setOrders] = useState<Order[]>([]);

  useEffect(() => {
    // 向 Django 後端請求訂單列表
    axios.get<Order[]>('http://localhost:8000/api/orders/')
      .then(res => setOrders(res.data))    // 成功後更新狀態
      .catch(err => console.error(err));   // 錯誤處理
  }, []);

  return (
    <ul>
      {orders.map(o => (
        <li key={o.id}>
          {/* 顯示訂單編號、金額、貨幣與狀態 */}
          {o.id}: {o.amount} {o.currency} — {o.status}
        </li>
      ))}
    </ul>
  );
}
```

- `useEffect`：元件掛載後觸發一次  
- `axios.get`：呼叫 `/api/orders/` 取得資料  
- `orders.map`：動態渲染每筆訂單

---

### 4. Flutter 簽核流程畫面（行動端導航）

```dart
import 'package:flutter/material.dart';
import 'approval_screen.dart';

class OrderListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final orders = ['order1', 'order2']; // 模擬訂單清單

    return Scaffold(
      appBar: AppBar(title: Text('Orders')), // 頂部標題列
      body: ListView(
        children: orders.map((o) => ListTile(
          title: Text(o),                     // 顯示訂單 ID
          onTap: () {
            // 點擊後導向簽核畫面，帶入 orderId
            Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => ApprovalScreen(orderId: o))
            );
          },
        )).toList(),
      ),
    );
  }
}

class ApprovalScreen extends StatelessWidget {
  final String orderId;
  ApprovalScreen({required this.orderId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Approve $orderId')),  // 顯示訂單 ID
      body: Center(
        child: ElevatedButton(
          child: Text('Approve'),               // 按鈕文字
          onPressed: () {
            // TODO: 呼叫後端簽核 API
          },
        ),
      ),
    );
  }
}
```

- `ListView` + `ListTile`：呈現可點擊清單  
- `Navigator.push`：使用路由實現畫面跳轉  
- `ApprovalScreen`：接收 `orderId` 顯示與按鈕執行動作

---

## 快速上手

### 1. 複製專案
```bash
git clone [https://github.com/你的帳號/trading_system.git](https://github.com/你的帳號/trading_system.git)
cd trading_system
```

### 2. 環境設定
建立 `.env` 檔案，可參考 `.env.example`。

### 3. 使用 Docker Compose (推薦)
一鍵啟動後端服務與 PostgreSQL 資料庫：
```bash
docker-compose up -d --build
```
等待服務啟動後，你可以透過以下方式存取：
- **Django REST API**: `http://localhost:8000/api/`
- **FastAPI (Pricing/Risk)**: `http://localhost:8001/docs` (內建 Swagger UI)

### 4. 前端 (React)
```bash
cd frontend-react
npm install
npm run lint    # 運行 ESLint 檢查
npm run format  # 運行 Prettier 格式化
npm run test    # 運行單元測試
npm run storybook # 啟動 Storybook 元件庫
npm run start   # 在 http://localhost:3000 啟動開發伺服器
```

### 5. 行動端 (Flutter)
```bash
cd flutter-app
flutter pub get
flutter run # 啟動 Flutter 應用
```

### 6. 運行測試
你可以使用 `Makefile` 一鍵運行所有測試：
```bash
make test
```
或者分開運行：
- **後端 (Django & FastAPI)**:
  ```bash
  cd backend
  pip install -r requirements.txt
  cd django_order_app
  python manage.py migrate # 首次運行需要
  pytest tests
  cd ../fastapi_pricing_service
  pytest tests
  ```
- **前端 (React)**:
  ```bash
  cd frontend-react
  npm install
  npm test
  ```
- **行動端 (Flutter)**:
  ```bash
  cd flutter-app
  flutter pub get
  flutter test
  ```

### 7. CI/CD
`.github/workflows/ci.yml` 會在每次 `push` 或 `pull_request` 時自動執行 Lint、單元測試與 Mutation Test，並進行 Commit Message 檢查。

### 8. AI 自動生成代碼
運行以下命令，根據 `prompts` 資料夾中的範本自動生成程式碼骨架：
```bash
make scaffold
```

## 文件與可視化

- **API 規格**: 查看 `docs/API_SPEC.md`
- **審計日誌定義**: 查看 `docs/AUDIT_LOG_DEFINITION.md`
- **系統架構圖**: 查看 `docs/ARCHITECTURE.md` (使用 [Mermaid](https://mermaid.live/) 預覽)
- **FastAPI 互動式 API 文件**: 訪問 `http://localhost:8001/docs`
- **專案截圖/演示**: 請查看 `docs/assets/` (目前為空，可放入應用截圖)
- **React 元件庫**: 訪問 Storybook (本地運行 `npm run storybook` 後訪問 `http://localhost:6006`)

## 貢獻指南

請參閱 `CONTRIBUTING.md` 了解如何貢獻。
請遵循 `CODE_OF_CONDUCT.md` 中的行為準則。

## 許可證

本專案採用 MIT 許可證。請參閱 `LICENSE` 文件了解更多詳情。
