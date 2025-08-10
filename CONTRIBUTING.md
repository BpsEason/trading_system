# 貢獻指南

感謝您對本專案的興趣！我們非常歡迎各種形式的貢獻，無論是錯誤報告、功能建議、文件改進，還是程式碼提交。

請在貢獻之前閱讀以下指南，以確保流暢的協作過程。

## 如何報告錯誤

如果您發現錯誤，請透過 GitHub Issue 追蹤器提交：

1.  **檢查現有 Issue**：在提交新的 Issue 之前，請先檢查是否有其他人已經報告了相同的錯誤。
2.  **使用 Issue 模板**: 請使用我們提供的 Issue 模板 (`.github/ISSUE_TEMPLATE/`) 來報告錯誤或提出功能請求，以確保所有必要資訊都被包含在內。
3.  **提供詳細資訊**：
    * 明確描述錯誤行為。
    * 提供重現錯誤的步驟。
    * 附上錯誤訊息和堆疊追蹤 (如果有的話)。
    * 提供您使用的環境資訊 (作業系統、Python 版本、套件版本等)。

## 如何建議功能

如果您有新的功能想法，也請透過 GitHub Issue 追蹤器提交：

1.  **檢查現有 Issue**：先檢查是否有類似的功能建議。
2.  **使用 Issue 模板**: 請使用我們提供的 Issue 模板 (`.github/ISSUE_TEMPLATE/`) 來報告錯誤或提出功能請求。
3.  **描述您的想法**：
    * 清楚說明您想要什麼功能，以及它將解決什麼問題。
    * 提供一些使用情境的範例。
    * 如果可以，說明您認為這個功能對專案的價值。

## 程式碼貢獻

我們鼓勵程式碼貢獻！請遵循以下步驟：

1.  **Fork 專案**：將本專案 fork 到您自己的 GitHub 帳戶。
2.  **Clone 您的 Fork**：將您的 fork 克隆到本地：
    ```bash
    git clone [https://github.com/您的用戶名/trading_system.git](https://github.com/您的用戶名/trading_system.git)
    cd trading_system
    ```
3.  **建立新分支**：為您的功能或錯誤修正建立一個新的分支：
    ```bash
    git checkout -b feature/您的功能名 或 bugfix/您的錯誤名
    ```
4.  **設定開發環境**：
    * **Docker Compose**: 推薦使用 `docker-compose up -d --build` 啟動後端服務和資料庫。
    * **本地安裝**: 參考 `README.md` 中的「快速上手」部分，分別安裝後端、前端和 Flutter 的依賴。
5.  **編寫程式碼**：確保您的程式碼遵循專案的風格指南。
6.  **編寫測試**：為您的變更編寫相應的測試，並確保所有測試通過。
    * 可以使用 `make test` 運行所有測試。
7.  **Linting 和格式化**：在提交前運行程式碼格式化工具和 linting 檢查。
    * 前端：`cd frontend-react && npm run lint && npm run format`
    * 後端：`make fmt` (待實作 Python 格式化工具)
8.  **提交變更**：
    ```bash
    git add .
    git commit -m "feat: 新增您的功能" 或 "fix: 修正某個錯誤"
    ```
    * 請遵循 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) 規範來編寫提交訊息。提交時會自動進行 commitlint 檢查。
9.  **推送到您的 Fork**：
    ```bash
    git push origin feature/您的功能名
    ```
10. **建立 Pull Request (PR)**：
    * 前往您的 GitHub 上的 Fork 頁面，點擊「New pull request」。
    * 請使用我們提供的 Pull Request 模板 (`.github/PULL_REQUEST_TEMPLATE.md`) 來填寫您的 PR 說明，以確保所有必要資訊都被包含在內。
    * 選擇正確的基礎分支 (通常是 `main`) 和您的功能分支。
    * 清楚描述您的變更內容、解決的問題以及如何測試。

## 行為準則

請務必閱讀並遵循我們的 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

再次感謝您的貢獻！
