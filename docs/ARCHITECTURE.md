# 系統架構圖

本文件描述了智能交易訂單管理系統的整體架構與各服務間的交互關係。

## 服務概覽

- **Django Order App**: 提供核心訂單 CRUD API，處理訂單生命週期管理。
- **FastAPI Pricing Service**: 負責實時計價和風險控制邏輯，包含止損和限額檢查。
- **React Web Frontend**: 網頁管理介面，用於訂單建立、查詢和實時通知顯示。
- **Flutter Mobile App**: 行動端應用，專注於訂單簽核流程和通知中心。
- **PostgreSQL**: 主資料庫，用於持久化訂單數據。
- **AI Engineering Layer**: 負責自動生成代碼骨架、驗證邏輯和測試案例。
- **CI/CD Pipeline (GitHub Actions)**: 自動化測試、構建和部署流程。
- **Audit Log Service**: 獨立的日誌服務，將所有操作記錄上傳到不可篡改的儲存。

## 服務交互圖

```mermaid
graph TD
    subgraph Clients
        A[React Web Frontend] -->|HTTP/API Gateway| B(API Gateway)
        C[Flutter Mobile App] -->|HTTP/API Gateway| B
    end

    subgraph API Gateway (Backend)
        B -->|Order CRUD| D(Django Order App)
        B -->|Pricing/Risk Check| E(FastAPI Pricing Service)
    end

    subgraph Data Stores
        D -->|Reads/Writes| F[PostgreSQL Orders DB]
        E -->|Reads/Writes| F
        D -->|Logs Actions| G(Audit Log Service)
        E -->|Logs Actions| G
        G -->|Stores Immutable Logs| H[Amazon QLDB / ELK Stack]
    end

    subgraph AI/DevOps
        I[AI Engineering Layer] -->|Generates Code/Tests| J(Source Code Repository)
        J -->|Triggers| K(CI/CD Pipeline - GitHub Actions)
    end

    D -- "Real-time Notifications" --> A
    D -- "Real-time Notifications" --> C

    K -->|Deploys| L[Staging/Production Environments]
    L -- "Monitoring/Alerts" --> M[Prometheus/Grafana/Slack]
```

### 說明:

-   **客戶端 (Clients)**：React Web 和 Flutter App 是使用者互動的介面，它們通過 API Gateway 與後端服務通信。
-   **API Gateway (Backend)**：由 Django Order App 和 FastAPI Pricing Service 組成。Django 處理基本的訂單管理，FastAPI 處理實時計價和風險檢查。
-   **資料儲存 (Data Stores)**：PostgreSQL 作為主要的訂單數據庫。獨立的審計日誌服務將操作記錄推送到不可篡改的儲存系統。
-   **AI/DevOps**：AI 工程層輔助開發，生成程式碼和測試，這些變更會觸發 CI/CD 管道，最終部署到環境中。
-   **實時通知**: Django Order App 可以將實時更新或簽核請求推送到前端和行動應用。
