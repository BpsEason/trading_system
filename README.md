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

## AI 自動生成骨架與測試：從後端到前端再到行動端

利用 OpenAI GPT-4 結合自訂 Prompt 與自動化腳本，讓專案「後端 API」、「前端元件」及「Flutter 畫面」的樣板程式與測試案例一鍵生成。以下說明完整流程與關鍵程式。

---

### 1. Prompt 範本撰寫

將需求以自然語言寫入各子專案的 `prompts/` 資料夾，以模板驅動生成。  
- **Django 後端 API**  
  `backend/prompts/api_scaffold_prompt.txt`  
  ```text
  請根據以下描述為 Django REST Framework 生成一個新的 API 視圖與序列化器：
  模型名稱：Product
  欄位：
  - name (CharField, max_length=100)
  - description (TextField)
  - price (DecimalField, max_digits=10, decimal_places=2)
  - stock (IntegerField)
  需求：提供所有 CRUD 操作的 API。
  ```
- **Django 後端測試**  
  `backend/prompts/test_case_prompt.txt`  
  ```text
  請為 Django REST Framework 中的 OrderViewSet 的 create 操作
  生成一個 pytest 測試案例，涵蓋成功建立與缺少 user_id 的場景。
  ```
- **React 前端元件**  
  `frontend-react/prompts/component_scaffold_prompt.txt`  
  ```text
  請生成一個 React TypeScript 功能型元件 UserList，
  接收 props `users: User[]`（含 id、name、email），
  並 map 渲染姓名與郵件。
  ```
- **Flutter 畫面**  
  `flutter-app/prompts/screen_scaffold_prompt.txt`  
  ```text
  請生成一個 StatelessWidget DashboardScreen，
  包含 AppBar 標題“Dashboard”，以及 Column 內兩行 Text，
  顯示 “Welcome to Dashboard!” 與 “Summary data will be here.”。
  ```

---

### 2. 自動化腳本 `tools/scaffold.py`

核心邏輯：讀取各 Prompt，呼叫 OpenAI ChatCompletion API，將回應寫入指定檔案。  

```python
import os, openai

# 從環境變數讀取 API Key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("⚠️ 警告：未設定 OPENAI_API_KEY，跳過 AI 生成功能。")
    # 不中斷腳本，以避免阻塞 CI

def run_prompt(prompt_path: str, output_path: str, model: str="gpt-4-turbo-preview"):
    # 讀取 Prompt
    prompt = open(prompt_path, encoding="utf-8").read()
    print(f"🔧 正在生成：{output_path}")
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful code generator."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.2  # 低溫度提升輸出一致性
    )
    code = resp.choices[0].message.content
    # 寫入檔案
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"✅ 已寫入：{output_path}")

if __name__ == "__main__":
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Django API 與測試
    run_prompt(
        os.path.join(PROJECT_ROOT, "backend/prompts/api_scaffold_prompt.txt"),
        os.path.join(PROJECT_ROOT, "backend/django_order_app/views_product.py")
    )
    run_prompt(
        os.path.join(PROJECT_ROOT, "backend/prompts/test_case_prompt.txt"),
        os.path.join(PROJECT_ROOT, "backend/django_order_app/tests/test_product_api.py")
    )

    # React 元件
    run_prompt(
        os.path.join(PROJECT_ROOT, "frontend-react/prompts/component_scaffold_prompt.txt"),
        os.path.join(PROJECT_ROOT, "frontend-react/src/components/UserList.tsx")
    )

    # Flutter 螢幕
    run_prompt(
        os.path.join(PROJECT_ROOT, "flutter-app/prompts/screen_scaffold_prompt.txt"),
        os.path.join(PROJECT_ROOT, "flutter-app/lib/screens/dashboard_screen.dart")
    )
```

---

### 3. 執行方式

在專案根目錄的 `Makefile` 中定義：

```makefile
.PHONY: scaffold
scaffold:  ## 根據 prompts 自動生成程式碼骨架
    @echo "開始 AI 自動 scaffold..."
    python tools/scaffold.py
```

執行：

```bash
make scaffold
```

- 若未設定 `OPENAI_API_KEY`，腳本會跳過生成並顯示警告。
- 完成後，自動在相應位置新增樣板程式與測試。

---

### 4. 生成檔案對照

| Prompt 類型       | Prompt 檔案路徑                                           | 生成結果檔案                                        |
|----------------|-------------------------------------------------------|-------------------------------------------------|
| Django API     | `backend/prompts/api_scaffold_prompt.txt`             | `backend/django_order_app/views_product.py`     |
| Django Test    | `backend/prompts/test_case_prompt.txt`                | `backend/django_order_app/tests/test_product_api.py` |
| React Component| `frontend-react/prompts/component_scaffold_prompt.txt`| `frontend-react/src/components/UserList.tsx`    |
| Flutter Screen | `flutter-app/prompts/screen_scaffold_prompt.txt`      | `flutter-app/lib/screens/dashboard_screen.dart` |

---

### 5. 與 CI/CD 整合

建議在 Pull Request 流程中，於測試前或檢查階段運行 `make scaffold`，並將生成結果納入版本控制，比對有無差異，確保 Prompt 與程式碼始終同步。

---

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
