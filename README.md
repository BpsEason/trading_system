# 智能交易訂單管理系統

[![CI](https://github.com/your-username/trading_system/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/trading_system/actions/workflows/ci.yml)
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
