# LagCheck

Browser-based real-time network stability diagnostic tool. Measures **connection latency**, **jitter**, **fail/timeout rate**, **network egress (IP/Node/Loc)**, and **download speed simulation under load (bufferbloat)**. Ideal for office IT, warehouse Logistics PDA scanning, online video calls, and remote desktop troubleshooting.

目前版本 / Version: **v1.0.12**

[ 中文 ](#-中文) | [ English ](#-english)

---

## 🌐 中文

### 🌐 線上直接使用 (GitHub Pages)

本專案支援 GitHub Pages 雙軌託管與發布：
- 👉 **正式版 (Production)**：[https://davislinyd.github.io/LagCheck/](https://davislinyd.github.io/LagCheck/)
- 🧪 **測試版 (Staging / Beta)**：[https://davislinyd.github.io/LagCheck/test.html](https://davislinyd.github.io/LagCheck/test.html)

---

### 快速開始

無需建置步驟，使用瀏覽器直接開啟：

```text
index.html
```

或在本機啟動靜態 HTTP 伺服器：

```bash
python3 -m http.server 8080
# 開啟 http://localhost:8080/index.html
```

| 檔案 | 說明 |
|------|------|
| `index.html` | 正式版主程式（v1.0.12，包含 URL 自動化引擎、還原預設、短板封頂對數模型與資源優化） |
| `test.html` | 測試版獨立發布檔（用於線上 Candidate 功能驗證） |
| `lagcheck_auto.py` | Python Playwright 無頭自動化測試與 JSON / PNG 下載工具 |

依賴：Chart.js 4.4.7（CDN，含 SRI）。CDN 暫時不可用時仍可正常連線量測與匯出，僅圖表不顯示。

---

### 核心功能 (v1.0.12)

- **即時連線探測**：預設間隔 500ms（主要端點 Cloudflare `cdn-cgi/trace`，備用端點 AWS `checkip.amazonaws.com`）。
- **自動備援探測 (Failover)**：連續失敗達門檻自動切換探測端點，並自動上記日誌。
- **還原預設設定 (Reset Defaults)**：測試設定標題旁附有「還原預設」按鈕，可一鍵恢復原廠預設值與 Failover 狀態。
- **⚡ URL 參數自動化引擎 (URL Automation)**：
  - **人性化網址解析**：輸入 `host=www.google.com` 或 `target=google.com` 時自動補全 `https://`，免輸入 `%3A%2F%2F`。
  - **零點擊自動測試**：支援 `autostart=1`、`samples=30`、`interval=200`、`stress=1`。
  - **多格式自動導出**：支援 `export=json,png` 或 `export=all`，測試完成自動下載 JSON 數據檔與高畫質 PNG 截圖。
  - **Webhook 自動回傳**：支援 `webhook=https://...` 測試完成時自動以 HTTP POST 將 JSON 報告傳回後端。
- **抖動與尖峰記錄**：滾動計算 Jitter 與 MAD，自動擷取異常延遲尖峰。
- **失敗／逾時可靠度**：結合 Wilson 信心區間，精準反映真實丟包與 Timeout。
- **網路出口資訊 (IP / Node / Loc)**：自動解析公網 IP、Cloudflare 資料中心代碼 (`TPE` 台北) 與地理位置 (`TW`)。
- **模擬下載速度**：並行大流量背景下載，評估頻寬吃滿時的傳輸速度與 Bufferbloat 延遲衝擊。
- **分頁省電保護**：切換至背景分頁時自動暫停 Canvas 繪製，保護 CPU/GPU 資源。
- **雙語切換**：支援 Traditional Chinese 與 English 即時動態切換。

---

### ⚡ URL 參數自動化使用範例

#### 1. 簡潔網址（一鍵探測 Google 並完成後同時下載 JSON 與 PNG 截圖）：
```text
https://davislinyd.github.io/LagCheck/?host=www.google.com&autostart=1&samples=30&export=json,png
```

#### 2. 高頻連線抗壓測試 + 完成自動 Webhook 回傳伺服器：
```text
https://davislinyd.github.io/LagCheck/?host=www.google.com&interval=200&stress=1&autostart=1&samples=50&webhook=https%3A%2F%2Fapi.mycompany.com%2Freport
```

---

### 指標語意（重要）

| 畫面名稱 | 實際意義 |
|----------|----------|
| 連線延遲 | 應用層 `fetch` 往返時間（含 DNS／TLS 影響；非 ICMP RTT） |
| 失敗／逾時率 | Probe 逾時或連線失敗比例；**不是** L3 packet loss（`no-cors` 無法讀 HTTP status） |
| 抖動 | 相鄰成功樣本延遲差的滾動統計 |
| 壅塞延遲差 | 負載中平均延遲 − 閒置 baseline |

---

### 預設參數（v1.0.12）

| 參數 | 預設 | 合法限制範圍 | URL 簡寫參數別名 |
|------|------|-------------|------------------|
| 主探測端點 (Primary Probe) | `https://www.cloudflare.com/cdn-cgi/trace` | URL | `endpoint`, `host`, `target`, `url`, `domain` |
| 備用探測端點 (Fallback Probe) | `https://checkip.amazonaws.com` | URL | `fallback`, `fallbackEndpoint` |
| 失敗切換門檻 (Failover Limit) | 5 次 | 3 – 10 次 | `failover`, `failoverThreshold` |
| 下載測試檔 URL | `https://speed.cloudflare.com/__down?bytes=5000000` | URL | `download`, `downloadUrl` |
| 採樣間隔 (Sample Interval) | 500 ms | 200 – 2000 ms | `interval` |
| 逾時門檻 (Timeout Limit) | 2000 ms | 1000 – 5000 ms | `timeout` |
| 樣本數 N (Sample Size) | 200 筆 | 30 – 500 筆 | `samples`, `percentileN` |
| 自動啟動 / 自動測試 | 關閉 | 0 或 1 | `autostart` |
| 自動導出格式 | 無 | `json`, `csv`, `png`, `all`, `json,png` | `export` |
| Webhook 回傳 URL | 無 | URL | `webhook` |

---

### 隱私與安全

- **純前端無後端**：零後端依賴，設定僅存於本機 `localStorage`（key：`lagcheck-light-v1`）。
- **敏感字樣衛生保證**：無任何私有服務或內部域名洩漏，預設均使用權威公有端點（Cloudflare / AWS / Google）。

---

### 聯絡與反饋 (Contact & Support)

- **Maintainer**: Davis Lin
- **Email**: [davislinyd@gmail.com](mailto:davislinyd@gmail.com)

---

## 🌐 English

### 🌐 Live Online Access (GitHub Pages)

Dual-track hosting and release supported on GitHub Pages:
- 👉 **Production**: [https://davislinyd.github.io/LagCheck/](https://davislinyd.github.io/LagCheck/)
- 🧪 **Staging / Beta**: [https://davislinyd.github.io/LagCheck/test.html](https://davislinyd.github.io/LagCheck/test.html)

---

### Quick Start

No build step required. Open directly in your browser:

```text
index.html
```

Or serve locally using any static HTTP server:

```bash
python3 -m http.server 8080
# Open http://localhost:8080/index.html
```

| File | Description |
|------|-------------|
| `index.html` | Single-file application for Production (v1.0.12 with URL Automation Engine, Reset Defaults, bottleneck-capped scale, and energy-saving safeguards) |
| `test.html` | Independent Staging application (for online Candidate feature verification) |
| `lagcheck_auto.py` | Python Playwright headless automation script for automated probing & JSON/PNG report downloads |

*Dependencies*: Chart.js 4.4.7 via CDN (with SRI). Even if the CDN is temporarily unreachable, latency probing and data exports remain fully functional (only line charts are hidden).

---

### Key Features (v1.0.12)

- **Real-Time Latency Probing**: Default 500ms interval (Primary endpoint Cloudflare `cdn-cgi/trace`, Fallback endpoint AWS `checkip.amazonaws.com`).
- **Automated Failover Probing**: Automatically switches active probe endpoint upon consecutive failure threshold with instant event logging.
- **Reset to Defaults**: Dedicated "Reset Defaults" button in settings panel to restore default configurations and Failover status with a single click.
- **⚡ URL Automation Engine**:
  - **Smart Protocol Auto-Prefixing**: Automatically prefixes `https://` when passing `host=www.google.com` or `target=google.com` (no `%3A%2F%2F` encoding required).
  - **Zero-Touch Automated Testing**: Supports `autostart=1`, `samples=30`, `interval=200`, and `stress=1`.
  - **Multi-Format Auto Export**: Supports `export=json,png` or `export=all` to automatically download JSON data files and high-res PNG screenshots upon completion.
  - **Webhook Integration**: Supports `webhook=https://...` to automatically HTTP POST JSON diagnostic reports to backend servers.
- **Jitter & Spike Tracking**: Rolling calculation of Jitter and MAD (Median Absolute Deviation), with automatic spike logging.
- **Reliability & Timeout Rate**: Applies Wilson score confidence interval for accurate loss estimation under small sample sizes.
- **Network Egress Info (IP / Node / Loc)**: Parses client public IP, Cloudflare edge data center node (`TPE` = Taipei), and country location (`TW`).
- **Simulate Download Speed**: Concurrent background downloads to evaluate bandwidth throughput and Bufferbloat latency impact under heavy load.
- **Background Energy Safeguard**: Automatically pauses Canvas rendering in hidden browser tabs (Page Visibility API) to save GPU/CPU resources.
- **Dynamic I18N**: Real-time switching between Traditional Chinese and English.

---

### ⚡ URL Automation Usage Examples

#### 1. Concise Link (One-click Google Probe + Auto JSON & PNG Download):
```text
https://davislinyd.github.io/LagCheck/?host=www.google.com&autostart=1&samples=30&export=json,png
```

#### 2. High-Frequency Stress Test + Automated Webhook POST:
```text
https://davislinyd.github.io/LagCheck/?host=www.google.com&interval=200&stress=1&autostart=1&samples=50&webhook=https%3A%2F%2Fapi.mycompany.com%2Freport
```

---

### Metric Semantics & Definitions (Important)

| UI Display | Technical Meaning & Definition |
|------------|--------------------------------|
| Connection Latency | Application-layer `fetch` round-trip time (RTT), including DNS lookup & TLS handshake (Not Layer 3 ICMP ping). |
| Fail / Timeout Rate | Percentage of failed/timed-out probes; **Not** Layer 3 IP packet loss (`no-cors` mode cannot read HTTP status). |
| Network Jitter | Rolling statistics of latency variation between consecutive successful samples. |
| Bufferbloat Delta | Average latency under load − Idle baseline latency. |

---

### Default Configuration (v1.0.12)

| Setting | Default | Input Range | URL Short Parameter Aliases |
|---------|---------|-------------|-----------------------------|
| Primary probe endpoint | `https://www.cloudflare.com/cdn-cgi/trace` | URL | `endpoint`, `host`, `target`, `url`, `domain` |
| Fallback probe endpoint | `https://checkip.amazonaws.com` | URL | `fallback`, `fallbackEndpoint` |
| Failover threshold | 5 fails | 3 – 10 fails | `failover`, `failoverThreshold` |
| Download test URL | `https://speed.cloudflare.com/__down?bytes=5000000` | URL | `download`, `downloadUrl` |
| Sample interval | 500 ms | 200 – 2000 ms | `interval` |
| Timeout threshold | 2000 ms | 1000 – 5000 ms | `timeout` |
| Sample size N | 200 pts | 30 – 500 pts | `samples`, `percentileN` |
| Auto-Start / Auto-Test | Disabled | `0` or `1` | `autostart` |
| Auto-Export formats | None | `json`, `csv`, `png`, `all`, `json,png` | `export` |
| Webhook Target URL | None | URL | `webhook` |

---

### Privacy & Security

- **100% Client-Side Only**: Zero backend dependency; configurations stored locally in `localStorage` (`lagcheck-light-v1`).
- **Privacy Assurance**: No private service names or internal domain leaks; default endpoints use public authoritative infrastructure (Cloudflare / AWS / Google).

---

### License & Attribution

Project code is subject to maintainer declarations. Third-party dependency: Chart.js (MIT License via CDN).

---

### Contact & Support

- **Maintainer**: Davis Lin
- **Email**: [davislinyd@gmail.com](mailto:davislinyd@gmail.com)
