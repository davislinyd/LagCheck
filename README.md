# LagCheck

Browser-based real-time network stability diagnostic tool. Measures **connection latency**, **jitter**, **fail/timeout rate**, **network egress (IP/Node/Loc)**, and **download speed simulation under load (bufferbloat)**. Ideal for office IT, warehouse Logistics PDA scanning, online video calls, and remote desktop troubleshooting.

目前版本 / Version: **v1.0.10**

[ 繁體中文 ](#-繁體中文) | [ English ](#-english)

---

## 🌐 繁體中文

### 🌐 線上直接使用 (GitHub Pages)

本專案已支援 GitHub Pages 一鍵託管，線上版本：
👉 **[https://davislinyd.github.io/LagCheck/](https://davislinyd.github.io/LagCheck/)**

---

### 快速開始

無需建置。用瀏覽器直接開啟：

```text
index.html
```

或在本機起一個靜態伺服器：

```bash
python3 -m http.server 8080
# 開啟 http://localhost:8080/index.html
```

| 檔案 | 說明 |
|------|------|
| `index.html` | 單檔案主程式（含 v1.0.10 自動備援、短板封頂對數模型與資源優化） |

依賴：Chart.js 4.4.7（CDN，含 SRI）。CDN 失敗時仍可量測與匯出，僅曲線不可用。

### 核心功能

- **即時連線探測**：預設間隔 500ms（主端點 Cloudflare `cdn-cgi/trace`，備用端點 AWS `checkip.amazonaws.com`）。
- **自動備援探測 (Failover)**：連續失敗達門檻自動切換探測端點。
- **抖動與尖峰記錄**：滾動計算 Jitter 與 MAD，自動擷取異常延遲尖峰。
- **失敗／逾時可靠度**：結合 Wilson 信心區間，精準反映真實丟包與 Timeout。
- **網路出口資訊 (IP / Node / Loc)**：自動解析公網 IP、Cloudflare 資料中心代碼 (`TPE` 台北) 與地理位置 (`TW`)。
- **模擬下載速度**：並行大流量背景下載，評估頻寬吃滿時的傳輸速度與 Bufferbloat 延遲衝擊。
- **自動停止定時保護**：可設定自動停止時間（預設 10 分鐘，可選 5、10、30、60 分鐘或無限制）。
- **分頁省電保護**：切換至背景分頁時自動暫停繪製，防止 GPU/CPU 資源浪費。
- **匯出與診斷報告**：即時事件紀錄、Markdown 診斷報告、CSV 數據與 PNG 畫面截圖。
- **雙語切換**：支援 Traditional Chinese 與 English 即時動態切換。

### 使用提示

1. 按 **開始** 開始採樣（預設間隔 500ms）。
2. 前 3 筆為**暖機**，不計入評級與尖峰紀錄。累積達 30/60 筆採樣門檻自動解鎖綜合評級。
3. 需要連線抗壓測試時開啟 **模擬下載速度**（預設 5MB × 2 並行，設有 100MB 流量安全上限與平均速度計算）。
4. **複製報告** / **匯出 CSV** / **匯出截圖** 取得結果。

### 指標語意（重要）

| 畫面名稱 | 實際意義 |
|----------|----------|
| 連線延遲 | 應用層 `fetch` 往返時間（含 DNS／TLS 影響；非 ICMP RTT） |
| 失敗／逾時率 | Probe 逾時或連線失敗比例；**不是** L3 packet loss（`no-cors` 無法讀 HTTP status） |
| 抖動 | 相鄰成功樣本延遲差的滾動統計 |
| 壅塞延遲差 | 負載中平均延遲 − 閒置 baseline |

### 預設參數（v1.0.10）

| 參數 | 預設 | 合法限制範圍 |
|------|------|-------------|
| 主探測端點 (Primary Probe) | `https://www.cloudflare.com/cdn-cgi/trace` | URL |
| 備用探測端點 (Fallback Probe) | `https://checkip.amazonaws.com` | URL |
| 失敗切換門檻 (Failover Limit) | 5 次 | 3 – 10 次 |
| 下載測試檔 URL | `https://speed.cloudflare.com/__down?bytes=5000000` | URL |
| 採樣間隔 (Sample Interval) | 500 ms | 200 – 2000 ms |
| 逾時門檻 (Timeout Limit) | 2000 ms | 1000 – 5000 ms |
| 樣本數 N (Sample Size) | 200 筆 | 30 – 500 筆 |
| 自動停止 (Auto-Stop) | 10 分鐘 | 5, 10, 30, 60 分鐘或無限制 |

### 隱私與安全

- 純前端，無後端；設定僅存於本機 `localStorage`（key：`lagcheck-light-v1`）。
- 下載速度測試會產生實際下行流量，設有 100MB 安全上限保護。

---

## 🌐 English

### 🌐 Live Online Access (GitHub Pages)

Access the live tool directly via GitHub Pages:
👉 **[https://davislinyd.github.io/LagCheck/](https://davislinyd.github.io/LagCheck/)**

---

### Quick Start

No build step required. Open `index.html` directly in your browser:

```text
index.html
```

Or serve locally with any static HTTP server:

```bash
python3 -m http.server 8080
# Open http://localhost:8080/index.html
```

| File | Description |
|------|-------------|
| `index.html` | Single-file application (includes v1.0.10 automated failover, bottleneck-capped scale, and energy-saving features) |

*Dependencies*: Chart.js 4.4.7 via CDN (with SRI). Even if CDN fails, latency probes and data export remain fully functional.

### Key Features

- **Real-Time Latency Probing**: Probes every 500ms (primary endpoint Cloudflare `cdn-cgi/trace`, fallback AWS `checkip.amazonaws.com`).
- **Automated Failover**: Switches active probe endpoint automatically when consecutive failures hit threshold.
- **Jitter & Spike Tracking**: Calculates rolling Jitter/MAD and automatically logs latency spikes.
- **Reliability & Timeout Rate**: Applies Wilson score confidence interval for accurate loss estimation.
- **Network Egress Info (IP / Node / Loc)**: Displays public egress IP, Cloudflare edge node (e.g. `TPE` = Taipei), and country location (`TW`).
- **Simulate Download Speed**: Concurrent background downloads to measure download speed and Bufferbloat under load.
- **Auto-Stop Timer**: Configurable safety auto-stop protection (default 10 min, optional 5, 10, 30, 60 min or unlimited).
- **Background Energy Safeguard**: Automatically pauses canvas rendering in hidden browser tabs (Page Visibility API).
- **Export & Reports**: Instant event log, Markdown diagnostic reports, CSV raw data export, and PNG screenshot.
- **Dynamic I18N**: Real-time switching between Traditional Chinese and English.

### Default Configuration (v1.0.10)

| Setting | Default | Input Range |
|---------|---------|-------------|
| Primary probe endpoint | `https://www.cloudflare.com/cdn-cgi/trace` | URL |
| Fallback probe endpoint | `https://checkip.amazonaws.com` | URL |
| Failover threshold | 5 fails | 3 – 10 fails |
| Download test URL | `https://speed.cloudflare.com/__down?bytes=5000000` | URL |
| Sample interval | 500 ms | 200 – 2000 ms |
| Timeout threshold | 2000 ms | 1000 – 5000 ms |
| Sample size N | 200 pts | 30 – 500 pts |
| Auto-stop protection | 10 min | 5, 10, 30, 60 min or unlimited |

### Privacy & Security

- **100% Client-side**: Zero backend dependency; configurations stored locally in `localStorage` (`lagcheck-light-v1`).
- **Network Awareness**: Download speed simulation consumes real bandwidth (capped at 100MB for protection).

### License & Attribution

Project code is subject to maintainer declarations. Third-party dependency: Chart.js (MIT License via CDN).
