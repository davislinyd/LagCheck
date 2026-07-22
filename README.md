# LagCheck

瀏覽器端網路穩定度監測工具：量測**連線延遲**、**抖動**、**失敗／逾時率**與**壅塞延遲（bufferbloat）**，適合遊戲、會議、遠端桌面與直播排障。

目前版本：**v1.0.5-rc2**（Light 版）

## 🌐 線上直接使用 (GitHub Pages)

本專案已支援 GitHub Pages 一鍵託管，線上版本：
👉 **[https://davislinyd.github.io/LagCheck/](https://davislinyd.github.io/LagCheck/)**

---

## 快速開始

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
| `index.html` | 單檔案主程式（含 v1.0.5-rc2 自動備援、短板封頂對數模型與資源優化） |

依賴：Chart.js 4.4.7（CDN，含 SRI）。CDN 失敗時仍可量測與匯出，僅曲線不可用。

## 功能

- 週期性 latency probe（預設主端點 Cloudflare `cdn-cgi/trace`，備用端點 AWS `checkip.amazonaws.com`）
- 自動備援探測（Failover Probing，連續失敗達門檻自動切換探測點）
- 抖動（相鄰延遲差滾動平均 + EWMA 顯示）
- 失敗／逾時率（含 Wilson upper bound，用於評級）
- 綜合評級（p50/p95、jitter/MAD、spike rate、壅塞延遲差；含 hysteresis）
- 壅塞模擬：並行下載，觀察 under-load 延遲差
- 即時曲線與背景分頁資源保護（Page Visibility 智慧節能）
- 事件紀錄、Markdown 報告、CSV 匯出
- 中／英介面；設定與語言寫入 `localStorage`

## 使用提示

1. 按 **開始** 開始採樣（預設間隔 1000ms）。
2. 前 3 筆為**暖機**，不計入評級與尖峰紀錄。
3. 需要 bufferbloat 測試時開啟 **壅塞延遲模擬**（預設 5MB × 2 並行）。
4. **複製報告** / **匯出 CSV** 取得結果。

### 指標語意（重要）

| 畫面名稱 | 實際意義 |
|----------|----------|
| 連線延遲 | 應用層 `fetch` 往返時間（含 DNS／TLS 影響；非 ICMP RTT） |
| 失敗／逾時率 | Probe 逾時或連線失敗比例；**不是** L3 packet loss（`no-cors` 無法讀 HTTP status） |
| 抖動 | 相鄰成功樣本延遲差的滾動統計 |
| 壅塞延遲差 | 負載中平均延遲 − 閒置 baseline |

## 預設參數（Light v1.0.5-rc2）

| 參數 | 預設 |
|------|------|
| Primary probe endpoint | `https://www.cloudflare.com/cdn-cgi/trace` |
| Fallback probe endpoint | `https://checkip.amazonaws.com` |
| Failover threshold | 5 次失敗 |
| Stress download | `https://speed.cloudflare.com/__down?bytes=5000000` |
| 採樣間隔 | 1000 ms（200–2000） |
| 逾時 | 2000 ms |
| 暖機樣本 | 3 |
| 圖表／統計時間窗 | 60 s |
| Stress 並行 | 2 |

## 隱私與安全

- 純前端，無後端；設定僅存於本機 `localStorage`（key：`lagcheck-light-v1`）。
- 探測 URL 由使用者可改；請勿指向未授權的內部資源。
- 壅塞測試會產生實際下行流量，注意流量與費用。

## 授權

專案用途以倉庫維護者聲明為準。第三方：Chart.js（CDN）。
