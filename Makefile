.PHONY: up down build test fmt lint install_frontend_deps install_backend_deps scaffold

up: ## 啟動所有 Docker Compose 服務 (後端服務與資料庫)
	docker-compose up -d --build

down: ## 停止所有 Docker Compose 服務
	docker-compose down

build: ## 重新構建 Docker 映像 (可選，通常 'up' 會包含 --build)
	docker-compose build

install_backend_deps: ## 安裝後端 Python 依賴
	@echo "正在安裝後端 Python 依賴..."
	pip install -r backend/requirements.txt

install_frontend_deps: ## 安裝前端 Node.js 依賴
	@echo "正在安裝前端 Node.js 依賴..."
	cd frontend-react && npm install

install_flutter_deps: ## 安裝 Flutter 依賴
	@echo "正在安裝 Flutter 依賴..."
	cd flutter-app && flutter pub get

test: ## 運行所有測試
	@echo "運行後端 Python 測試..."
	docker-compose run --rm django pytest django_order_app/tests
	docker-compose run --rm fastapi pytest fastapi_pricing_service/tests
	@echo "運行前端 React 單元測試..."
	cd frontend-react && npm test
	@echo "運行前端 React 整合測試 (E2E)..."
	# cd frontend-react && npx cypress run --headless # Placeholder for Cypress
	@echo "運行行動端 Flutter 測試..."
	cd flutter-app && flutter test

fmt: ## 格式化程式碼
	@echo "運行程式碼格式化工具..."
	black backend/
	cd frontend-react && npm run format
	cd flutter-app && dart format lib/

lint: ## 運行程式碼檢查
	@echo "運行程式碼檢查工具..."
	pylint backend/django_order_app backend/fastapi_pricing_service # Basic pylint example
	cd frontend-react && npm run lint
	cd flutter-app && flutter analyze

scaffold: ## 根據 prompts 自動生成程式碼骨架
	@echo "正在根據 prompts 自動生成程式碼骨架..."
	python tools/scaffold.py

help: ## 顯示此幫助訊息
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
