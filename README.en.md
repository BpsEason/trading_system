# Smart Trading Order Management System

[![Coverage](https://img.shields.io/badge/coverage-80%25-green)](https://github.com/BpsEason/trading_system)  
[![Mutation Testing](https://img.shields.io/badge/mutation_testing-Passed-brightgreen)](https://github.com/BpsEason/trading_system)  

Centralize order management, real-time pricing & risk control, instant notifications/approvals—and AI-driven code and test scaffolding for end-to-end coverage from backend to web to mobile.

## Table of Contents

- [AI-Driven Scaffolding & Testing](#ai-driven-scaffolding-testing)  
- [1. Prompt Templates](#1-prompt-templates)  
- [2. Automation Script](#2-automation-script)  
- [3. Running Scaffolding](#3-running-scaffolding)  
- [4. Generated File Mapping](#4-generated-file-mapping)  
- [Key Code Examples](#key-code-examples)  
- [Quick Start](#quick-start)  
  - [Clone the Repository](#clone-the-repository)  
  - [Environment Setup](#environment-setup)  
  - [Install Dependencies](#install-dependencies)  
  - [Launch Services](#launch-services)  
- [Testing](#testing)  
- [CI/CD](#ci-cd)  
- [Documentation & Visualization](#documentation-visualization)  
- [Contributing](#contributing)  
- [License](#license)  

---

## AI-Driven Scaffolding & Testing

We use OpenAI GPT-4 with custom natural-language prompts and an automation script to generate:

- Backend APIs & tests  
- React components  
- Flutter screens  

All with one command.

---

### 1. Prompt Templates

Place human-readable templates in each `prompts/` folder.

- **Django API** (`backend/prompts/api_scaffold_prompt.txt`)
  ```text
  Generate a Django REST Framework viewset and serializer for a Product model with:
  - name: CharField(max_length=100)
  - description: TextField
  - price: DecimalField(max_digits=10, decimal_places=2)
  - stock: IntegerField
  Provide full CRUD operations.
  ```
- **Django Tests** (`backend/prompts/test_case_prompt.txt`)
  ```text
  Create pytest cases for OrderViewSet.create:
  1. Successful order creation.
  2. Missing user_id validation error.
  ```
- **React Component** (`frontend-react/prompts/component_scaffold_prompt.txt`)
  ```text
  Generate a React TypeScript functional component named UserList.
  Props: users: User[] where User has id, name, email.
  Render each user’s name and email using map, with a unique key.
  ```
- **Flutter Screen** (`flutter-app/prompts/screen_scaffold_prompt.txt`)
  ```text
  Generate a StatelessWidget named DashboardScreen.
  Include an AppBar titled "Dashboard" and a Column with:
  - Text("Welcome to Dashboard!")
  - Text("Summary data will be here.")
  ```

---

### 2. Automation Script

`tools/scaffold.py` reads prompts, calls the OpenAI ChatCompletion API, and writes output files:

```python
import os, openai

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("⚠️ OPENAI_API_KEY not set; skipping AI scaffolding.")
    # Do not exit to avoid CI interruption

def run_prompt(prompt_path, output_path, model="gpt-4-turbo-preview"):
    prompt = open(prompt_path, encoding="utf-8").read()
    print(f"🔧 Generating {output_path}")
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful code generator."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.2
    )
    code = resp.choices[0].message.content
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"✅ Written {output_path}")

if __name__ == "__main__":
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    run_prompt(f"{ROOT}/backend/prompts/api_scaffold_prompt.txt",
               f"{ROOT}/backend/django_order_app/views_product.py")
    run_prompt(f"{ROOT}/backend/prompts/test_case_prompt.txt",
               f"{ROOT}/backend/django_order_app/tests/test_product_api.py")
    run_prompt(f"{ROOT}/frontend-react/prompts/component_scaffold_prompt.txt",
               f"{ROOT}/frontend-react/src/components/UserList.tsx")
    run_prompt(f"{ROOT}/flutter-app/prompts/screen_scaffold_prompt.txt",
               f"{ROOT}/flutter-app/lib/screens/dashboard_screen.dart")
```

---

### 3. Running Scaffolding

Add to `Makefile`:

```makefile
.PHONY: scaffold
scaffold:
    @echo "Starting AI scaffolding..."
    python tools/scaffold.py
```

Run:

```bash
make scaffold
```

- If `OPENAI_API_KEY` is missing, the script prints a warning and skips.
- Generated files appear in their respective folders.

---

### 4. Generated File Mapping

| Prompt Type      | Template Path                                           | Generated File                                          |
|------------------|---------------------------------------------------------|---------------------------------------------------------|
| Django API       | `backend/prompts/api_scaffold_prompt.txt`               | `backend/django_order_app/views_product.py`             |
| Django Test      | `backend/prompts/test_case_prompt.txt`                  | `backend/django_order_app/tests/test_product_api.py`    |
| React Component  | `frontend-react/prompts/component_scaffold_prompt.txt`  | `frontend-react/src/components/UserList.tsx`            |
| Flutter Screen   | `flutter-app/prompts/screen_scaffold_prompt.txt`        | `flutter-app/lib/screens/dashboard_screen.dart`         |

---

## Key Code Examples

### Django `OrderViewSet`

```python
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from .audit import AuditLog

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        AuditLog.log_create(self.request.user, instance)
```

### FastAPI Pricing & Risk Endpoint

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from decimal import Decimal
from .risk import check_limits

app = FastAPI()

class PriceRequest(BaseModel):
    user_id: str    = Field(..., example="user123")
    amount: Decimal = Field(..., gt=0)
    currency: str   = Field(..., regex="^(USD|EUR|JPY)$")

@app.post("/price")
async def price(req: PriceRequest):
    allowed, msg = check_limits(req.amount, req.currency)
    if not allowed:
        raise HTTPException(status_code=400, detail={"message": msg})
    final_price = req.amount * Decimal("1.001")
    return {"allowed": True, "price": final_price, "message": "Trade approved"}
```

### React `OrderList` Component

```tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Order { id: string; amount: string; currency: string; status: string; }

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

### Flutter Order Screens

```dart
// order_list.dart
ListView(
  children: ['order1','order2'].map((o) =>
    ListTile(
      title: Text(o),
      onTap: () => Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => ApprovalScreen(orderId: o))
      ),
    )
  ).toList(),
);
```

---

## Quick Start

### Clone the Repository

```bash
git clone https://github.com/BpsEason/trading_system.git
cd trading_system
```

### Environment Setup

Copy and fill in `.env` from `.env.example`.  
Ensure `OPENAI_API_KEY` is set to enable AI scaffolding.

### Install Dependencies

```bash
make install_backend_deps
make install_frontend_deps
make install_flutter_deps
```

### Launch Services

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

### Generate AI-Powered Scaffolding

```bash
make scaffold
```

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

## Documentation & Visualization

- API Specs → `docs/API_SPEC.md`  
- Audit Log Definition → `docs/AUDIT_LOG_DEFINITION.md`  
- Architecture Diagram → `docs/ARCHITECTURE.md` (Mermaid support)  
- Storybook → http://localhost:6006  

---

## Contributing

Please refer to `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
