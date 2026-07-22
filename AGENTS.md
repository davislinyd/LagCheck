# AGENTS.md - LagCheck 專案開發與 Agent 指南

本文件為 AI Coding Agent（如 Antigravity / Cursor-Agent / Claude-Code）在此 repository (`LagCheck`) 工作時的權威參考指南。

---

## 1. 專案概覽與目標受眾 (Project Overview)

* **專案簡介**：LagCheck 是一個零後端依賴、單一檔案架構的即時網路穩定度與品質監測工具 (`index.html`)。
* **目標應用情境與對象**：
  * **辦公室同仁**：線上會議、ERP/CRM 系統、Google Workspace 穩定度診斷。
  * **電商倉庫與出貨人員**：PDA 條碼掃描槍、POS 系統、WMS 出貨 API 連線品質排障。
* **核心哲學**：對延遲適度放寬（倉庫與辦公 API 具備 Retry 重傳機制），但對嚴重斷線與短板故障保持極高敏感度與科學評估。

---

## 2. 技術架構與原則 (Architecture & Guidelines)

1. **單檔案 HTML 原則 (Single-file Component)**：
   * 主體程式碼統一維持在根目錄 [index.html](file:///Users/lindav/git/LagCheck/index.html)，此為專案唯一的權威主程式。
   * HTML 結構、CSS 樣式與原生 JavaScript (ES Modules) 皆在該檔內完成，禁止無謂地拆分額外本機 JS/CSS 檔案。
2. **多國語言支援 (Dynamic I18N)**：
   * 所有文本必須登錄在 `I18N` 字典中 (`zh` / `en`)。
   * 網路事件紀錄 (Event Log) 必須儲存 `log_*` 字典 Key 與參數，確保使用者點擊語言切換時，過往累積的所有歷史 Log 能**即時動態翻譯**。
3. **瀏覽器效能保護機制 (Resource Safeguard)**：
   * 採用 Page Visibility API (`document.hidden`)，分頁切換至背景時必須暫停 Chart.js Canvas 重繪，保護使用者瀏覽器 CPU/GPU 資源。
   * `state.eventLog` 硬性上限 100 筆，超過自動溢出清除 DOM。

---

## 3. 核心評級與探測演算法 (Key Algorithms)

### 3.1 雙端點自動備援探測 (Failover Probing)
* **主要探測點**：`https://www.cloudflare.com/cdn-cgi/trace`
* **備用探測點**：`https://checkip.amazonaws.com`
* **運作機制**：探測連續失敗達門檻（預設 5 次，可設定 1~20 次）自動切換 Active Probe，並觸發全自動日誌上記。
* **Active Endpoint Badge**：UI 上需即時顯示當前探測 Hostname。

### 3.2 短板封頂對數評級模型 (Bottleneck-Capped Scale)
* **指標權重**：延遲 p50/p95 (35%)、抖動 Jitter/MAD (25%)、失敗/逾時率 Loss (30%)、尖峰率 Spike (10%)。
* **平滑寬容區 (Tolerance Zone)**：延遲在 180ms ~ 480ms 內、丟包率在 2.5% 內皆維持在 90-100 高分區間。
* **短板瓶頸封頂防護 (Bottleneck Cap Guard)**：
  $$\text{FinalScore} = \min\Big(\text{WeightedScore}, \; \text{LossScore} + 18, \; \text{LatencyScore} + 18\Big)$$
  防範嚴重斷線/丟包 (Loss 0分) 被低延遲指標 (100分) 虛高拉低總評級。

### 3.3 動態採樣解鎖門檻 (Warm-up Threshold)
* 當設定樣本數 $N > 100$ 時，必須累積採樣測試達 **60 次** 才解鎖並顯示評級。
* 當設定樣本數 $N \le 100$ 時，必須累積採樣測試達 **30 次** 才解鎖顯示評級。
* 未達門檻前，評級徽章顯示灰色 `—` 並標註進度（如 `尚無資料 (18/60)`）。

---

## 4. 開發與驗證協定 (Development & Verification Protocol)

1. **語法與編譯自動檢查**：
   每次編輯完根目錄 `index.html` 後，必須執行以下 Node.js 指令進行腳本與語法解析驗證：
   ```bash
   node -e "const fs = require('fs'); const html = fs.readFileSync('index.html', 'utf8'); const js = html.match(/<script type=\"module\">([\s\S]*?)<\/script>/)[1]; new Function(js);"
   ```
2. **Git Commit 規範**：
   * 訊息前綴需符合標示：`feat:`, `fix:`, `refactor:`, `docs:`。
   * 推送前必須驗證 remote 分支與追蹤目標 (`origin/master`)。
3. **Git Push 嚴格授權機制 (Strict Git Push Protocol)**：
   * ⚠️ **未經使用者明確口頭或文字授權（如「請 push」、「同意推送」），AI Agent 絕對禁止主動執行 `git push` 指令！**
   * 本機可依規範完成 `git commit` 並回報變更細節與語法驗證結果，必須等待使用者明確指示授權後方可推送到遠端倉庫。
