# Smart Trading Order Management System

[![CI](https://github.com/your-username/trading_system/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/trading_system/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-80%25-green)](https://github.com/your-username/trading_system) <!-- Placeholder, integrate with coverage reports later -->
[![Mutation Testing](https://img.shields.io/badge/mutation_testing-Passed-brightgreen)](https://github.com/your-username/trading_system) <!-- Placeholder, integrate with mutation testing reports later -->

A comprehensive system for centralized order management, real-time pricing and risk control, instant notifications/approvals, and AI-driven code and test generation.

## Table of Contents
- `backend/` Django REST + FastAPI Backend Services
- `frontend-react/` React + TypeScript Frontend Application
- `flutter-app/` Flutter Mobile Application
- `docs/` API Specifications, Audit Log Definitions, System Architecture Diagram
- `.github/` GitHub Actions CI/CD Workflows and Project Templates

## Quick Start

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/trading_system.git](https://github.com/your-username/trading_system.git)
cd trading_system
```

### 2. Environment Setup
Create a `.env` file based on `.env.example`.

### 3. Using Docker Compose (Recommended)
Start backend services and PostgreSQL database with one command:
```bash
docker-compose up -d --build
```
Once services are up, you can access:
- **Django REST API**: `http://localhost:8000/api/`
- **FastAPI (Pricing/Risk)**: `http://localhost:8001/docs` (Built-in Swagger UI)

### 4. Frontend (React)
```bash
cd frontend-react
npm install
npm run lint    # Run ESLint checks
npm run format  # Run Prettier formatting
npm run test    # Run unit tests
npm run storybook # Start Storybook component library
npm run start   # In http://localhost:3000 Start the development server
```

### 5. Mobile (Flutter)
```bash
cd flutter-app
flutter pub get
flutter run # Start Flutter application
```

### 6. Running Tests
You can use the `Makefile` to run all tests with one command:
```bash
make test
```
Or run them separately:
- **Backend (Django & FastAPI)**:
  ```bash
  cd backend
  pip install -r requirements.txt
  cd django_order_app
  python manage.py migrate # Required for first run
  pytest tests
  cd ../fastapi_pricing_service
  pytest tests
  ```
- **Frontend (React)**:
  ```bash
  cd frontend-react
  npm install
  npm test
  ```
- **Mobile (Flutter)**:
  ```bash
  cd flutter-app
  flutter pub get
  flutter test
  ```

### 7. CI/CD
`.github/workflows/ci.yml` automatically runs Lint, Unit Tests, Mutation Tests, and Commit Message Checks on every `push` or `pull_request`.

## Documentation & Visualization

- **API Specifications**: See `docs/API_SPEC.md`
- **Audit Log Definition**: See `docs/AUDIT_LOG_DEFINITION.md`
- **System Architecture Diagram**: See `docs/ARCHITECTURE.md` (Preview with [Mermaid](https://mermaid.live/))
- **FastAPI Interactive API Docs**: Visit `http://localhost:8001/docs`
- **Project Screenshots/Demos**: See `docs/assets/` (Currently empty, place app screenshots here)
- **React Component Library**: Visit Storybook (access `http://localhost:6006` after running `npm run storybook` locally)

## Contributing Guidelines

Please see `CONTRIBUTING.md` for information on how to contribute.
Please follow the Code of Conduct outlined in `CODE_OF_CONDUCT.md`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
