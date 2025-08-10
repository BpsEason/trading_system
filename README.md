# 智能交易訂單管理系統

[![CI](https://github.com/your-username/trading_system/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/trading_system/actions/workflows/ci.yml)  
[![Coverage](https://img.shields.io/badge/coverage-80%25-green)](https://github.com/your-username/trading_system)  
[![Mutation Testing](https://img.shields.io/badge/mutation_testing-Passed-brightgreen)](https://github.com/your-username/trading_system)  
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

一體化平台，集訂單 CRUD、實時計價風控、即時通知簽核與 AI 自動生成骨架，從 Web 到行動端無縫覆蓋。

---

## 關鍵代碼示例

### 1. Django OrderViewSet

```python
# views.py
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    # 指定查詢集，讀取所有訂單
    queryset = Order.objects.all()
    # 指定序列化器，處理輸入驗證與輸出格式
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        # 自訂建立時機：建立後自動寫入審計日誌
        instance = serializer.save()
        AuditLog.log_create(self.request.user, instance)
```

> 上述程式碼展示如何在 `perform_create` 中插入審計邏輯，確保所有訂單操作都有不可篡改的日誌。

---

### 2. FastAPI 定價與風控接口

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .risk import check_limits

app = FastAPI()

class PriceRequest(BaseModel):
    user_id: str
    amount: float
    currency: str

@app.post("/price")
async def price(req: PriceRequest):
    # 驗證限額
    ok, msg = check_limits(req.amount, req.currency)
    if not ok:
        # 超限時拋出 400 錯誤
        raise HTTPException(status_code=400, detail=msg)
    # 計算最終價格（示意）
    return {"allowed": True, "price": req.amount * 1.01}
```

> 使用 Pydantic 模型確保請求格式正確，透過自訂例外實現簡潔的風控反饋。

---

### 3. React 訂單列表元件

```tsx
// src/components/OrderList.tsx
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
    // 向後端請求訂單列表
    axios.get<Order[]>('http://localhost:8000/api/orders/')
      .then(res => setOrders(res.data))
      .catch(console.error);
  }, []);

  return (
    <ul>
      {orders.map(o => (
        <li key={o.id}>
          {/* 顯示訂單摘要 */}
          {o.id}: {o.amount} {o.currency} — {o.status}
        </li>
      ))}
    </ul>
  );
}
```

> 實際開發中，可搭配 Storybook 撰寫相應的元件示例與測試。

---

### 4. Flutter 行動端簽核畫面

```dart
// lib/screens/order_list.dart
import 'package:flutter/material.dart';
import 'approval_screen.dart';

class OrderListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final orders = ['order1', 'order2']; // 模擬資料

    return Scaffold(
      appBar: AppBar(title: Text('訂單列表')),
      body: ListView(
        children: orders.map((o) => ListTile(
          title: Text(o),
          onTap: () {
            // 點擊後導向簽核畫面
            Navigator.push(context,
              MaterialPageRoute(builder: (_) => ApprovalScreen(orderId: o)));
          },
        )).toList(),
      ),
    );
  }
}
```

> 以上結合 `Navigator` 實現畫面切換，API 呼叫可在 `ApprovalScreen` 中補充完成。

---

## 問與答 (Q&A)

| 問題                                             | 回答                                                                                                                                       |
|--------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| 為何同時採用 Django 與 FastAPI？                 | Django 適合快速構建 CRUD 與自動管理後台，FastAPI 提供非同步與高併發定價／風控邏輯。二者互補，提升開發效率與執行效能。                           |
| 如何實現實時通知？                               | 後端透過 Django Channels + Redis Pub/Sub 將訂單異動推送 WebSocket，前端訂閱後即時更新；手機端使用 Push Notification。                       |
| AI scaffold 如何融入開發流程？                   | `tools/scaffold.py` 讀取 `prompts/` 目錄下的範本，呼叫 OpenAI 完成骨架程式與測試生成，`make scaffold` 一鍵執行，減少樣板代碼耗時。              |
| 測試強度如何保證？                               | 結合 pytest、Jest、Flutter Test 並加入 Mutation Testing，最低覆蓋率 ≥ 80%，確保業務邏輯分支與邊界都被測試到。                                |
| CI/CD 如何無縫串接？                             | GitHub Actions 在每次 push 或 PR 自動運行 lint、單元測試、Mutation Test 及 commitlint，確保主分支始終保持可部署狀態；並可延伸至 Kubernetes。 |

---

## 技術棧

| 範疇         | 技術                                                         |
|------------|------------------------------------------------------------|
| 後端         | Python 3.10 · Django 3.2 · Django REST Framework · FastAPI · Uvicorn |
| 資料庫       | PostgreSQL · Amazon QLDB (審計日誌)                            |
| 前端 (Web)   | React 18 · TypeScript · Storybook · Axios                    |
| 行動端       | Flutter 3.x · Dart · http                                     |
| AI 工具      | OpenAI GPT-4 · 自動 scaffold 腳本                             |
| CI/CD      | GitHub Actions · Docker Compose                              |
| 測試框架      | pytest · pytest-django · pytest-mutation · Jest · @testing-library · Flutter Test |
| 監控告警      | Prometheus · Grafana · Slack Webhook                          |

---

## 快速啟動

1. git clone + `.env`  
2. `docker-compose up -d --build`  
3. 訪問  
   - Web UI：`http://localhost:3000`  
   - Django API：`http://localhost:8000/api/`  
   - FastAPI Docs：`http://localhost:8001/docs`  
   - Storybook：`http://localhost:6006`

---

## 未來規劃

- 即時分析圖表：整合 ECharts/Highcharts  
- Kubernetes ✕ 多雲部署：Terraform + Helm  
- AI 強化：異常偵測、自動回滾策略生成  

---

## 授權

採用 MIT License，詳見 `LICENSE`。
