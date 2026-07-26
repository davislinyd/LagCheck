# LagCheck

Browser-based real-time network stability diagnostic tool. Measures **connection latency**, **jitter**, **fail/timeout rate**, **network egress (IP/Node/Loc)**, and **download speed simulation under load (bufferbloat)**. Ideal for office IT, warehouse Logistics PDA scanning, online video calls, and remote desktop troubleshooting.

目前版本 / Version: **v1.0.13**

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
| `index.html` | 正式版主程式（v1.0.13，包含網域感知對照排障、Segmented Tab 整合、URL 自動化與 10MB 預設） |
| `test.html` | 測試版主程式（v1.0.13，包含網域感知對照排障、Segmented Tab 整合、URL 自動化與 10MB 預設） |
| `lagcheck_auto.py` | Python Playwright 無頭自動化測試與 JSON / PNG 下載工具 |

依賴：Chart.js 4.4.7（CDN，含 SRI）。CDN 暫時不可用時仍可正常連線量測與匯出，僅圖表不顯示。

---

### 核心功能 (v1.0.13)

- **即時連線探測**：預設間隔 500ms（主要端點 AWS `checkip.amazonaws.com`，備用端點 Cloudflare `one.one.one.one/cdn-cgi/trace`）。
- **📱 跨裝置全平臺相容**：專為電腦 PC、iOS / Android 手機及倉庫 PDA 掃描槍設計。高頻探測採用原生 CORS 相容與無重導向 (Zero-Redirect) 請求，徹底消除 iOS WebKit 沙箱與 302 轉址攔截造成的探測誤判。
- **自動備援探測 (Failover)**：連續失敗達門檻自動切換探測端點，並自動上記日誌。
- **還原預設設定 (Reset Defaults)**：測試設定標題旁附有「還原預設」按鈕，可一鍵恢復原廠預設值與 Failover 狀態。
- **⚡ URL 參數自動化引擎 (URL Automation)**：
  - **人性化網址解析**：輸入 `host=www.google.com` 或 `target=google.com` 時自動補全 `https://`，免輸入 `%3A%2F%2F`。
  - **零點擊自動測試**：支援 `autostart=1`、`samples=30`、`interval=200`、`stress=1`。
  - **多格式自動導出**：支援 `export=json,png` 或 `export=all`，測試完成自動下載 JSON 數據檔與高畫質 PNG 截圖。
  - **Webhook 自動回傳**：支援 `webhook=https://...` 測試完成時自動以 HTTP POST 將 JSON 報告傳回後端。
- **抖動與尖峰記錄**：滾動計算 Jitter 與 MAD，自動擷取異常延遲尖峰。
- **失敗／逾時可靠度**：結合 Wilson 信心區間，精準反映真實丟包與 Timeout。
- **🌐 網路出口資訊多源備援 (Multi-Source Trace Provider)**：自動從多源 (`one.one.one.one/cdn-cgi/trace` 與 `www.cloudflare.com`) 解析公網 IP、Cloudflare 資料中心代碼 (`TPE` 台北) 與地理位置 (`TW`)，若格式受到阻擋，自動備援向 AWS 補全 IP，確保頂部資訊晶片 100% 穩定展示。
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

### 企業評級演算法與數學計算公式 (Rating Algorithm & Mathematical Formulas)

LagCheck 採用**短板封頂對數模型 (Bottleneck-Capped Scale)**，計算邏輯包含「暖機門檻判斷」、「四項指標加權」、「Wilson 統計信心修正」與「短板瓶頸封頂防護」。

#### 1. 核心數學函數 (Core Mathematical Functions)

##### A. 區間線性映射函數 $S(v, g, b)$
將實際測量值 $v$ 映射至 $0 \sim 100$ 分。其中 $g$ (Good) 為完美門檻，$b$ (Bad) 為最差門檻：
$$S(v, g, b) = \begin{cases} 100, & v \le g \\ 0, & v \ge b \\ 100 \times \frac{b - v}{b - g}, & g < v < b \end{cases}$$

##### B. Wilson 95% 信心區間上界 $W(k, n, z)$
針對小樣本數探測，計算失敗率的 95% 統計上界，防範抽樣誤差：
$$W(k, n, z) = \frac{\hat{p} + \frac{z^2}{2n} + z \sqrt{\frac{\hat{p}(1 - \hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$
*其中 $\hat{p} = \frac{k}{n}$ ($k$ 為失敗次數，$n$ 為總採樣數)，$z = 1.96$。*

---

#### 2. 各指標分項得分算式 (Sub-score Calculations)

* **連線延遲得分 ($S_{\text{latency}}$)**：
  $$S_{\text{latency}} = 0.5 \times S(P_{50}, 220, 600) + 0.5 \times S(P_{95}, 400, 900)$$

* **網路抖動得分 ($S_{\text{jitter}}$)**：
  $$S_{\text{jitter}} = 0.6 \times S(\text{Jitter}, 60, 180) + 0.4 \times S(\text{MAD}, 45, 140)$$

* **失敗 / 逾時率得分 ($S_{\text{loss}}$)**：
  $$S_{\text{loss}} = S\Big(100 \times W(k, n, 1.96), \; 4.0, \; 16.0\Big)$$

* **異常尖峰率得分 ($S_{\text{spike}}$)**：
  $$S_{\text{spike}} = S(\text{Rate}_{\text{spike}}, 12.0, 40.0)$$

---

#### 3. 總分與短板瓶頸封頂算式 (Final Score & Bottleneck Cap)

* **原始加權總分 ($S_{\text{raw}}$)**：
  $$S_{\text{raw}} = 0.35 S_{\text{latency}} + 0.25 S_{\text{jitter}} + 0.30 S_{\text{loss}} + 0.10 S_{\text{spike}}$$

* **短板瓶頸封頂門檻 ($C_{\text{bottleneck}}$)**：
  $$C_{\text{bottleneck}} = \min\big(S_{\text{loss}} + 25, \; S_{\text{latency}} + 25\big)$$

* **最終評級總分 ($S_{\text{final}}$)**：
  $$S_{\text{final}} = \min\big(S_{\text{raw}}, \; C_{\text{bottleneck}}\big)$$

---

#### 4. 具體計算示範與過程 (Detailed Calculation Example)

**假設採樣 $n = 50$ 筆**，量測數據如下：
* $P_{50} = 150\text{ ms}, \; P_{95} = 280\text{ ms}$
* 失敗次數 $k = 2$ 次 (原始失敗率 $4\%$)
* $\text{Jitter} = 12\text{ ms}, \; \text{MAD} = 8\text{ ms}$
* 發生 1 次尖峰 ($\text{Rate}_{\text{spike}} = 2\%$)

**計算過程展開**：
1. **延遲分數**：$S(150, 220, 600) = 100$, $S(280, 400, 900) = 100 \implies S_{\text{latency}} = 100$
2. **遺失率分數**：代入 $W(2, 50, 1.96) \approx 0.0664 \ (6.64\%)$
   $$S_{\text{loss}} = S(6.64, 4.0, 16.0) = 100 \times \frac{16.0 - 6.64}{16.0 - 4.0} = 78.0$$
3. **抖動分數**：$S(12, 60, 180) = 100$, $S(8, 45, 140) = 100 \implies S_{\text{jitter}} = 100$
4. **尖峰分數**：$S(2.0, 12.0, 40.0) = 100 \implies S_{\text{spike}} = 100$
5. **總分導出**：
   $$S_{\text{raw}} = (100 \times 0.35) + (100 \times 0.25) + (78.0 \times 0.30) + (100 \times 0.10) = 93.4$$
   $$C_{\text{bottleneck}} = \min(78.0 + 25, \; 100 + 25) = 103.0$$
   $$S_{\text{final}} = \min(93.4, 103.0) = \mathbf{93.4 \text{ 分 (S 級)}}$$

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
| `index.html` | Single-file application for Production (v1.0.13 with domain-aware troubleshooting, Segmented Tab consolidation & 10MB default download) |
| `test.html` | Staging single-file application (v1.0.13 with domain-aware troubleshooting, Segmented Tab consolidation & 10MB default download) |
| `lagcheck_auto.py` | Python Playwright headless automation script for automated probing & JSON/PNG report downloads |

*Dependencies*: Chart.js 4.4.7 via CDN (with SRI). Even if the CDN is temporarily unreachable, latency probing and data exports remain fully functional (only line charts are hidden).

---

### Key Features (v1.0.13)

- **Real-Time Latency Probing**: Default 500ms interval (Primary endpoint AWS `checkip.amazonaws.com`, Fallback endpoint Cloudflare `one.one.one.one/cdn-cgi/trace`).
- **📱 Cross-Device & Platform Compatibility**: Tailored for Desktop PCs, iOS/Android Mobiles, and Warehouse Logistics PDAs. High-frequency probing uses native CORS-compliant, zero-redirect requests to eliminate false positives caused by iOS WebKit sandbox restrictions or 302 redirects.
- **Automated Failover Probing**: Automatically switches active probe endpoint upon consecutive failure threshold with instant event logging.
- **Reset to Defaults**: Dedicated "Reset Defaults" button in settings panel to restore default configurations and Failover status with a single click.
- **⚡ URL Automation Engine**:
  - **Smart Protocol Auto-Prefixing**: Automatically prefixes `https://` when passing `host=www.google.com` or `target=google.com` (no `%3A%2F%2F` encoding required).
  - **Zero-Touch Automated Testing**: Supports `autostart=1`, `samples=30`, `interval=200`, and `stress=1`.
  - **Multi-Format Auto Export**: Supports `export=json,png` or `export=all` to automatically download JSON data files and high-res PNG screenshots upon completion.
  - **Webhook Integration**: Supports `webhook=https://...` to automatically HTTP POST JSON diagnostic reports to backend servers.
- **Jitter & Spike Tracking**: Rolling calculation of Jitter and MAD (Median Absolute Deviation), with automatic spike logging.
- **Reliability & Timeout Rate**: Applies Wilson score confidence interval for accurate loss estimation under small sample sizes.
- **🌐 Multi-Source Trace Provider (IP / Node / Loc)**: Multi-source fallback (`one.one.one.one/cdn-cgi/trace` and `www.cloudflare.com`) for public IP, Cloudflare edge data center node (`TPE` = Taipei), and country location (`TW`), with automated AWS fallback for 100% chip display stability.
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

### Rating Algorithm & Mathematical Formulas

LagCheck utilizes a **Bottleneck-Capped Scale** model, incorporating warm-up validation, 4-metric weighted scoring, Wilson confidence bounds, and bottleneck capping protection.

#### 1. Core Mathematical Functions

##### A. Range Linear Mapping Function $S(v, g, b)$
Maps raw measurement $v$ into a $0 \sim 100$ score, given good threshold $g$ and bad threshold $b$:
$$S(v, g, b) = \begin{cases} 100, & v \le g \\ 0, & v \ge b \\ 100 \times \frac{b - v}{b - g}, & g < v < b \end{cases}$$

##### B. Wilson 95% Confidence Interval Upper Bound $W(k, n, z)$
Calculates the 95% upper confidence bound for failure rate under small sample sizes:
$$W(k, n, z) = \frac{\hat{p} + \frac{z^2}{2n} + z \sqrt{\frac{\hat{p}(1 - \hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$
*Where $\hat{p} = \frac{k}{n}$ ($k$: failures, $n$: total samples), $z = 1.96$.*

---

#### 2. Sub-score Calculations

* **Latency Score ($S_{\text{latency}}$)**:
  $$S_{\text{latency}} = 0.5 \times S(P_{50}, 220, 600) + 0.5 \times S(P_{95}, 400, 900)$$

* **Jitter Score ($S_{\text{jitter}}$)**:
  $$S_{\text{jitter}} = 0.6 \times S(\text{Jitter}, 60, 180) + 0.4 \times S(\text{MAD}, 45, 140)$$

* **Loss Rate Score ($S_{\text{loss}}$)**:
  $$S_{\text{loss}} = S\Big(100 \times W(k, n, 1.96), \; 4.0, \; 16.0\Big)$$

* **Spike Rate Score ($S_{\text{spike}}$)**:
  $$S_{\text{spike}} = S(\text{Rate}_{\text{spike}}, 12.0, 40.0)$$

---

#### 3. Final Score & Bottleneck Cap Guard

* **Raw Weighted Score ($S_{\text{raw}}$)**:
  $$S_{\text{raw}} = 0.35 S_{\text{latency}} + 0.25 S_{\text{jitter}} + 0.30 S_{\text{loss}} + 0.10 S_{\text{spike}}$$

* **Bottleneck Cap Limit ($C_{\text{bottleneck}}$)**:
  $$C_{\text{bottleneck}} = \min\big(S_{\text{loss}} + 25, \; S_{\text{latency}} + 25\big)$$

* **Final Rating Score ($S_{\text{final}}$)**:
  $$S_{\text{final}} = \min\big(S_{\text{raw}}, \; C_{\text{bottleneck}}\big)$$

---

#### 4. Detailed Calculation Example

Given $n = 50$ total samples:
* $P_{50} = 150\text{ ms}, \; P_{95} = 280\text{ ms}$
* Failure count $k = 2$ (Raw loss rate $4\%$)
* $\text{Jitter} = 12\text{ ms}, \; \text{MAD} = 8\text{ ms}$
* 1 spike event ($\text{Rate}_{\text{spike}} = 2\%$)

**Step-by-step Execution**:
1. **Latency**: $S(150, 220, 600) = 100$, $S(280, 400, 900) = 100 \implies S_{\text{latency}} = 100$
2. **Loss**: Evaluate $W(2, 50, 1.96) \approx 0.0664 \ (6.64\%)$
   $$S_{\text{loss}} = S(6.64, 4.0, 16.0) = 100 \times \frac{16.0 - 6.64}{16.0 - 4.0} = 78.0$$
3. **Jitter**: $S(12, 60, 180) = 100$, $S(8, 45, 140) = 100 \implies S_{\text{jitter}} = 100$
4. **Spike**: $S(2.0, 12.0, 40.0) = 100 \implies S_{\text{spike}} = 100$
5. **Final Evaluation**:
   $$S_{\text{raw}} = (100 \times 0.35) + (100 \times 0.25) + (78.0 \times 0.30) + (100 \times 0.10) = 93.4$$
   $$C_{\text{bottleneck}} = \min(78.0 + 25, \; 100 + 25) = 103.0$$
   $$S_{\text{final}} = \min(93.4, 103.0) = \mathbf{93.4 \ (\text{Grade S})}$$

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
