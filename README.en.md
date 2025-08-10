# Smart Trading Order Management System

[![Coverage](https://img.shields.io/badge/coverage-80%25-green)](https://github.com/BpsEason/trading_system)  
[![Mutation Testing](https://img.shields.io/badge/mutation_testing-Passed-brightgreen)](https://github.com/BpsEason/trading_system)  
[![MIT License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)  

GitHub Repository: https://github.com/BpsEason/trading_system.git  

A unified platform for order CRUD, real-time pricing & risk control, instant notifications/approvals, and AI-driven code & test scaffolding—from web to mobile, end-to-end coverage.

---

## Directory Structure

```
trading_system/
├── backend/
│   ├── django_order_app/         # Django REST API + tests + migrations
│   ├── fastapi_pricing_service/  # FastAPI pricing & risk + tests
│   └── prompts/                  # AI scaffolding templates
├── frontend-react/
│   ├── src/                      # React + TypeScript source
│   ├── tests/                    # React unit tests
│   ├── prompts/                  # AI scaffolding templates
│   └── .storybook/               # Storybook configuration
├── flutter-app/
│   ├── lib/                      # Flutter source (screens, main)
│   ├── integration_test/         # Flutter integration tests
│   └── prompts/                  # AI scaffolding templates
├── docs/                         # API specs, audit log definition, architecture diagram
├── .github/                      # CI/CD workflows & issue/PR templates
├── tools/                        # scaffold.py (AI code generator)
├── docker-compose.yml
├── .env.example
├── Makefile
├── pytest.ini                    # Mutation testing config
└── LICENSE
```

---

## Key Code Examples

### 1. Django `OrderViewSet` (Order CRUD + Audit Log)

```python
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from .audit import AuditLog  # assumed audit service module

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()           # select all orders
    serializer_class = OrderSerializer       # apply serializer

    def perform_create(self, serializer):
        instance = serializer.save()         # save new order
        AuditLog.log_create(self.request.user, instance)
        # record who/when created which order
```

### 2. FastAPI Pricing & Risk Endpoint

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from decimal import Decimal
from .risk import check_limits

app = FastAPI(title="Pricing Service")

class PriceRequest(BaseModel):
    user_id: str       = Field(..., example="user123", description="User ID")
    amount: Decimal    = Field(..., gt=0, description="Trade amount (>0)")
    currency: str      = Field(..., regex="^(USD|EUR|JPY)$", description="Currency code")

@app.post("/price")
async def price(req: PriceRequest):
    allowed, msg = check_limits(req.amount, req.currency)
    if not allowed:
        raise HTTPException(status_code=400, detail={"message": msg})

    final_price = req.amount * Decimal("1.001")  # simple 0.1% markup
    return {
        "allowed": True,
        "price": final_price,
        "message": "Trade approved"
    }
```

### 3. React `OrderList` Component

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
    axios.get<Order[]>('http://localhost:8000/api/orders/')
      .then(res => setOrders(res.data))
      .catch(console.error);
  }, []);

  return (
    <ul>
      {orders.map(o => (
        <li key={o.id}>
          {o.id}: {o.amount} {o.currency} — {o.status}
        </li>
      ))}
    </ul>
  );
}
```

### 4. Flutter `OrderListScreen` & `ApprovalScreen`

```dart
// lib/screens/order_list.dart
import 'package:flutter/material.dart';
import 'approval_screen.dart';

class OrderListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final orders = ['order1', 'order2'];

    return Scaffold(
      appBar: AppBar(title: Text('Orders')),
      body: ListView(
        children: orders.map((o) => ListTile(
          title: Text(o),
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => ApprovalScreen(orderId: o))
          ),
        )).toList(),
      ),
    );
  }
}

// lib/screens/approval_screen.dart
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
          child: Text('Approve'),
          onPressed: () {
            // TODO: call backend approval API
          },
        ),
      ),
    );
  }
}
```

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/BpsEason/trading_system.git
cd trading_system
```

### 2. Environment

Copy and fill in `.env` from `.env.example`.  
Set `OPENAI_API_KEY` to enable AI scaffolding.

### 3. Install Dependencies

```bash
# Backend
make install_backend_deps

# Frontend
make install_frontend_deps

# Flutter
make install_flutter_deps
```

### 4. Launch Services

#### Docker Compose (Recommended)

```bash
docker-compose up -d --build
```

- Django API → http://localhost:8000/api/  
- FastAPI Docs → http://localhost:8001/docs  

#### Local Development

- **Django**  
  ```bash
  cd backend/django_order_app
  python manage.py migrate
  python manage.py runserver
  ```
- **FastAPI**  
  ```bash
  cd backend/fastapi_pricing_service
  uvicorn main:app --reload
  ```
- **React**  
  ```bash
  cd frontend-react
  npm start
  ```
- **Flutter**  
  ```bash
  cd flutter-app
  flutter run
  ```

### 5. Generate AI Code Scaffolding

```bash
make scaffold
```

This calls `tools/scaffold.py` to read prompts and output:

| Prompt Type     | Template Path                                           | Generated File                                           |
|-----------------|---------------------------------------------------------|----------------------------------------------------------|
| Django API      | backend/prompts/api_scaffold_prompt.txt                 | backend/django_order_app/views_product.py                |
| Django Test     | backend/prompts/test_case_prompt.txt                    | backend/django_order_app/tests/test_product_api.py       |
| React Component | frontend-react/prompts/component_scaffold_prompt.txt    | frontend-react/src/components/UserList.tsx               |
| Flutter Screen  | flutter-app/prompts/screen_scaffold_prompt.txt          | flutter-app/lib/screens/dashboard_screen.dart            |

---

## Testing

```bash
make test
```

Or individually:

- **Backend**: `pytest backend/django_order_app/tests backend/fastapi_pricing_service/tests`  
- **React**:  
  ```bash
  cd frontend-react
  npm test
  ```
- **Flutter**:  
  ```bash
  cd flutter-app
  flutter test
  ```

---

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) runs on each push/PR:

- Lint checks  
- Unit tests  
- Mutation testing  
- Commit message validation  

---

## Documentation

- API Specs → `docs/API_SPEC.md`  
- Audit Log Definition → `docs/AUDIT_LOG_DEFINITION.md`  
- Architecture Diagram → `docs/ARCHITECTURE.md` (Mermaid support)  
- Storybook → http://localhost:6006  

---

## Contributing

See `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` for guidelines.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
