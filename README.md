# 智能交易訂單管理系統

[![CI](https://github.com/your-username/trading_system/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/trading_system/actions/workflows/ci.yml)  
[![Coverage](https://img.shields.io/badge/coverage-80%25-green)](https://github.com/your-username/trading_system)  
[![Mutation Testing](https://img.shields.io/badge/mutation_testing-Passed-brightgreen)](https://github.com/your-username/trading_system)  
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

一站式平台，集訂單管理、實時計價風控、即時通知簽核與 AI 代碼骨架生成於一體，從 Web 到行動端全棧覆蓋，快速部署，擴展無憂。

---

## Demo 預覽

![Web 端截圖](docs/assets/web_screenshot_placeholder.png)  
React 管理介面：訂單列表、實時通知與簽核狀態展示。

![Mobile 端截圖](docs/assets/mobile_screenshot_placeholder.png)  
Flutter 行動端：簽核流程與推送通知。

---

## 核心功能

- 全棧微服務架構  
  - Django REST 負責訂單 CRUD  
  - FastAPI 處理定價、限額檢查與風控策略  

- 即時通知與簽核  
  WebSocket/Push 推送，訂單狀態秒級同步至所有前端與行動端  

- AI 驅動開發輔助  
  自動從 prompts 生成 Python、TypeScript、Dart 代碼與測試案例  

- 測試與品質保障  
  pytest + Jest + Flutter Test 覆蓋，Mutation Testing 強度 ≥ 80%，ESLint/Prettier/Black 自動格式化  

- 無縫 CI/CD 流水線  
  GitHub Actions 自動 lint、測試、mutation testing、commitlint 串接，一鍵部署  

---

## 系統架構

```mermaid
graph TD
  subgraph Clients
    Web[React Web UI] --> Gateway
    Mobile[Flutter App] --> Gateway
  end

  subgraph Backend
    Gateway(API Gateway) --> Django[Django Order App]
    Gateway --> FastAPI[FastAPI Pricing Service]
  end

  subgraph DataStores
    Django --> Postgres[(PostgreSQL)]
    FastAPI --> Postgres
    Django --> Audit[Audit Log Service]
    FastAPI --> Audit
    Audit --> QLDB[(Amazon QLDB / ELK)]
  end

  subgraph DevOps
    AI[AI Scaffold Layer] --> Repo[Source Code Repo]
    Repo --> CI[GitHub Actions]
    CI --> Envs[Staging/Production]
    Envs --> Monitor[Prometheus/Grafana]
  end

  Django -.-> Web
  Django -.-> Mobile

---

## 技術棧

| 範疇         | 技術                                                         |
|------------|------------------------------------------------------------|
| 後端         | Python 3.10・Django 3.2・DRF・FastAPI・Uvicorn                   |
| 資料庫       | PostgreSQL・Amazon QLDB (稽核日誌)                            |
| 前端 (Web)   | React 18・TypeScript・Storybook・Axios                         |
| 行動端       | Flutter 3.x・Dart・http                                       |
| AI 工具      | OpenAI GPT-4・自動 scaffold 腳本                                |
| CI/CD      | GitHub Actions・Docker Compose                              |
| 測試框架      | pytest・pytest-django・pytest-mutation・Jest・@testing-library・Flutter Test |
| 監控告警      | Prometheus・Grafana・Slack Webhook                            |

---

## 快速上手

### 一鍵啟動（推薦）

```bash
git clone https://github.com/your-username/trading_system.git
cd trading_system
docker-compose up -d --build
```

- Django REST API：`http://localhost:8000/api/`  
- FastAPI Swagger UI：`http://localhost:8001/docs`  
- React 開發伺服器：`http://localhost:3000`  
- Storybook：`http://localhost:6006`

### 本地開發

#### 後端

```bash
cd backend
pip install -r requirements.txt

# Django
cd django_order_app
python manage.py migrate
python manage.py runserver

# FastAPI
cd ../fastapi_pricing_service
uvicorn main:app --reload
```

#### 前端

```bash
cd frontend-react
npm install
npm run lint
npm run format
npm run start
```

#### 行動端

```bash
cd flutter-app
flutter pub get
flutter run
```

---

## 文件資源

- API 規格：`docs/API_SPEC.md`  
- 審計日誌定義：`docs/AUDIT_LOG_DEFINITION.md`  
- 系統架構圖：`docs/ARCHITECTURE.md`  
- FastAPI 互動式文件：`http://localhost:8001/docs`  
- 截圖與示例：`docs/assets/`

---

## 未來規劃

- 即時圖表與趨勢預測：整合 ECharts/Highcharts  
- 多雲與 Kubernetes 支援：Terraform + Helm + CI Pipeline  
- AI 模塊擴充：異常檢測、回滾策略自動化  

---

## 貢獻指南

請參閱 `CONTRIBUTING.md` 了解提報 Issue、提交 PR 流程。  
詳讀 `CODE_OF_CONDUCT.md` 以維護友善共識。

---

## 授權

本專案採用 MIT License，詳見 `LICENSE` 文件。  
```
