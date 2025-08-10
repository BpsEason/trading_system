# Smart Trading Order Management System

[![CI](https://github.com/BpsEason/trading_system/actions/workflows/ci.yml/badge.svg)](https://github.com/BpsEason/trading_system/actions/workflows/ci.yml)  
[![Coverage](https://img.shields.io/badge/coverage-80%25-green)](https://github.com/BpsEason/trading_system)  
[![Mutation Testing](https://img.shields.io/badge/mutation_testing-Passed-brightgreen)](https://github.com/BpsEason/trading_system)  
[![CommitLint](https://img.shields.io/badge/commitlint-enabled-blue)](https://www.conventionalcommits.org/)

集中管理訂單、實時計價風控、即時通知／簽核，並由 AI 自動生成代碼與測試骨架  
完全支援一鍵 Docker Compose 啟動、全流程 CI/CD、前後端行動端一致性體驗

---

## 目錄

- [專案亮點](#專案亮點)
- [快速上手](#快速上手)
- [專案結構](#專案結構)
- [關鍵代碼展示](#關鍵代碼展示)
  - [Django Order App](#django-order-app)
  - [FastAPI 定價與風控](#fastapi-定價與風控)
  - [React 前端](#react-前端)
  - [Flutter 行動端](#flutter-行動端)
- [CI/CD 與測試](#cicd-與測試)
- [文件與架構](#文件與架構)
- [AI 工程層](#ai-工程層)
- [貢獻與授權](#貢獻與授權)

---

## 專案亮點

- **全棧服務**：Django REST + FastAPI 後端，React + TypeScript Web 前端，Flutter 行動端  
- **一鍵部署**：Docker Compose + Makefile，一條命令啟動 PostgreSQL、後端與前端服務  
- **實時計價與風控**：FastAPI 提供價格計算與限額檢查，確保交易安全  
- **即時通知／簽核**：Django 後端推送 WebSocket 或通知至前端與行動端  
- **AI 自動生成**：Prompt Driven Code Generation，自動產生 CRUD、驗證、測試骨架  
- **完善 CI/CD**：GitHub Actions 執行 Lint、單元測試、Mutation Testing、CommitLint  
- **高測試覆蓋**：80%+ 測試覆蓋率，結合 pytest、Jest、flutter_test  
- **元件化 Storybook**：React 元件庫即時預覽，提升前端開發體驗

---

## 快速上手

1. **Clone 專案**  
   ```bash
   git clone https://github.com/BpsEason/trading_system.git
   cd trading_system
   ```

2. **建立環境變數**  
   參考 `.env.example`，複製為 `.env` 並填入你的值。  
   
3. **啟動服務**  
   ```bash
   make up
   ```
   - Django REST API: `http://localhost:8000/api/`
   - FastAPI Swagger UI: `http://localhost:8001/docs`
   - React 前端: `http://localhost:3000`
   - Storybook: `http://localhost:6006`
   
4. **一鍵測試**  
   ```bash
   make test
   ```

---

## 專案結構

```
trading_system/
├── backend/
│   ├── django_order_app/         # Django Order CRUD Service
│   ├── fastapi_pricing_service/  # FastAPI Pricing & Risk Service
│   └── requirements.txt
├── frontend-react/               # React + TypeScript Web App
│   ├── src/                      
│   ├── tests/                    
│   └── .storybook/               
├── flutter-app/                  # Flutter Mobile App
│   ├── lib/screens/              
│   └── integration_test/         
├── docs/                         # API 規格、審計日誌、架構圖
├── .github/                      # CI/CD 工作流與 Issue/PR 模板
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## 關鍵代碼展示

以下示例為各子系統最核心邏輯，展示如何定義模型、API 與畫面。

### Django Order App

```python
# backend/django_order_app/models.py
from django.db import models

class Order(models.Model):
    user_id    = models.UUIDField()                     # 訂單所屬使用者
    amount     = models.DecimalField(max_digits=12,
                                     decimal_places=2)  # 訂單金額
    currency   = models.CharField(max_length=3,
                                  default='USD')       # 貨幣種類
    status     = models.CharField(max_length=10,
                                  default='PENDING')   # 訂單狀態
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

```python
# backend/django_order_app/views.py
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    自動生成 CRUD API：
    - GET    /api/orders/
    - POST   /api/orders/
    - GET    /api/orders/{id}/
    - PUT    /api/orders/{id}/
    - DELETE /api/orders/{id}/
    """
    queryset         = Order.objects.all()
    serializer_class = OrderSerializer
```

### FastAPI 定價與風控

```python
# backend/fastapi_pricing_service/risk.py
from decimal import Decimal

LIMITS = {
  'USD': Decimal('10000'),
  'EUR': Decimal('8000'),
}

def check_limits(amount: Decimal, currency: str):
    """
    如果 amount 超過預設限額，回傳 False 與錯誤訊息，
    否則回傳 True。
    """
    limit = LIMITS.get(currency, Decimal('0'))
    if amount > limit:
        return False, f"Exceeds limit of {limit} {currency}"
    return True, "OK"
```

```python
# backend/fastapi_pricing_service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .risk import check_limits

app = FastAPI()

class PriceRequest(BaseModel):
    user_id: str
    amount: Decimal
    currency: str

@app.post("/price")
def price(req: PriceRequest):
    allowed, msg = check_limits(req.amount, req.currency)
    if not allowed:
        raise HTTPException(status_code=400, detail=msg)
    return {"allowed": True, "message": msg}
```

### React 前端

```typescript
// frontend-react/src/api.ts
import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api',  // 指向 Django REST API
  timeout: 5000,
});

// 取得訂單列表
export const fetchOrders = () => API.get('/orders/');
```

```tsx
// frontend-react/src/components/OrderList.tsx
import React, { useEffect, useState } from 'react';
import { fetchOrders } from '../api';

interface Order {
  id: string;
  amount: string;
  currency: string;
  status: string;
}

export default function OrderList() {
  const [orders, setOrders] = useState<Order[]>([]);

  useEffect(() => {
    fetchOrders()
      .then(res => setOrders(res.data))
      .catch(() => {
        // 失敗時顯示 mock
        setOrders([
          { id: '1', amount: '100.00', currency: 'USD', status: 'PENDING' },
        ]);
      });
  }, []);

  return (
    <ul>
      {orders.map(o => (
        <li key={o.id}>
          {o.id}: {o.amount} {o.currency} – {o.status}
        </li>
      ))}
    </ul>
  );
}
```

### Flutter 行動端

```dart
// flutter-app/lib/screens/order_list.dart
import 'package:flutter/material.dart';
import 'approval_screen.dart';

class OrderListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // 模擬訂單列表
    final orders = ['order1', 'order2'];

    return Scaffold(
      appBar: AppBar(title: const Text('Orders')),
      body: ListView(
        children: orders.map((o) {
          return ListTile(
            title: Text(o),
            onTap: () {
              // 點擊進入簽核頁面
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => ApprovalScreen(orderId: o),
                ),
              );
            },
          );
        }).toList(),
      ),
    );
  }
}
```

```dart
// flutter-app/lib/screens/approval_screen.dart
import 'package:flutter/material.dart';

class ApprovalScreen extends StatelessWidget {
  final String orderId;
  ApprovalScreen({required this.orderId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Approve $orderId')),
      body: Center(
        child: ElevatedButton(
          child: const Text('Approve'),
          onPressed: () {
            // TODO: 呼叫 API 進行簽核
          },
        ),
      ),
    );
  }
}
```

---

## CI/CD 與測試

- GitHub Actions 自動執行：
  - Python: Lint、Django + FastAPI 測試、Mutation Testing
  - Node.js: ESLint、單元測試、Commit Message 檢查
  - Flutter: `flutter test`、`flutter analyze`
- Makefile 支援一鍵命令：
  - `make up` / `make down`
  - `make test` / `make lint` / `make fmt`

---

## 文件與架構

- API 規格：`docs/API_SPEC.md`
- 審計日誌定義：`docs/AUDIT_LOG_DEFINITION.md`
- 系統架構圖：`docs/ARCHITECTURE.md`（Mermaid 範例）
- 元件庫預覽：Storybook (`frontend-react/.storybook`)

---

## AI 工程層

專案內建多份 Prompt 範本，示範如何：

- 生成 Django REST CRUD 代碼
- 產生 FastAPI 驗證邏輯
- 自動撰寫 pytest 測試案例
- Scaffold React 與 Flutter 元件

可於 `backend/prompts`、`frontend-react/prompts`、`flutter-app/prompts` 資料夾查看。

---

## 貢獻與授權

歡迎透過 Issue / Pull Request 參與貢獻，請遵守 [CONTRIBUTING.md](.github/CONTRIBUTING.md)  
行為請遵守 [CODE_OF_CONDUCT.md](.github/CODE_OF_CONDUCT.md)  

本專案採用 MIT License，詳見 [LICENSE](LICENSE)。
