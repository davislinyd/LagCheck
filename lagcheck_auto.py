#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LagCheck 自動化測試腳本 (Playwright 版 - 支援 JSON 數據 + 高畫質 PNG 畫面截圖)
說明：自動啟動 Headless 瀏覽器呼叫 LagCheck 線上測試版 (test.html)，採樣完成後自動捕獲 JSON 報告與完整畫面截圖。

使用前需安裝依依：
    pip install playwright
    playwright install chromium

執行範例：
    python3 lagcheck_auto.py
    python3 lagcheck_auto.py --endpoint https://www.google.com --samples 50
    python3 lagcheck_auto.py --no-headless (開啟瀏覽器畫面觀察)
"""

import os
import sys
import json
import time
import argparse
from playwright.sync_api import sync_playwright

def run_lagcheck_test(
    endpoint: str = "https://www.google.com",
    samples: int = 30,
    interval_ms: int = 500,
    headless: bool = True,
    save_screenshot: bool = True,
    output_dir: str = None
):
    """
    呼叫 LagCheck 進行連線品質探測，下載 JSON 報告並可選擇自動擷取高畫質網頁截圖 (PNG)
    
    :param endpoint: 要探測的目標網址 (例: https://www.google.com)
    :param samples: 目標採樣樣本數 (預設: 30 筆)
    :param interval_ms: 探測間隔毫秒數 (預設: 500 ms)
    :param headless: 是否使用無頭模式
    :param save_screenshot: 是否自動儲存畫面截圖 (PNG)
    :param output_dir: 指定檔案儲存目錄 (預設為當前目錄)
    """
    base_url = "https://davislinyd.github.io/LagCheck/test.html"
    target_url = (
        f"{base_url}?"
        f"endpoint={endpoint}&"
        f"interval={interval_ms}&"
        f"samples={samples}&"
        f"autostart=1&"
        f"export=json"
    )
    
    print("=" * 60)
    print("🚀 【LagCheck 自動化測試 (JSON + PNG 截圖)】")
    print(f" • 目標端點 : {endpoint}")
    print(f" • 採樣數量 : {samples} 筆")
    print(f" • 探測間隔 : {interval_ms} ms")
    print(f" • 自動截圖 : {'開啟 (PNG)' if save_screenshot else '關閉'}")
    print(f" • 測試網址 : {target_url}")
    print("=" * 60)

    start_time = time.time()
    save_dir = output_dir or os.getcwd()

    with sync_playwright() as p:
        # 設定 2x 視網膜高解析度視窗 (1280x900) 以取得清晰圖表與文字
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            accept_downloads=True,
            viewport={"width": 1280, "height": 900},
            device_scale_factor=2
        )
        page = context.new_page()

        try:
            print("⏳ 正在開啟瀏覽器進行探測，請稍候...")
            
            # 設定連線逾時時間 (依據樣本數動態計算，最少 40 秒)
            max_wait_ms = max(40000, int((samples * (interval_ms / 1000.0) + 15) * 1000))
            
            # 監聽瀏覽器觸發的 JSON 報告下載事件
            with page.expect_download(timeout=max_wait_ms) as download_info:
                page.goto(target_url)

            # 成功捕獲 JSON 下載檔案
            download = download_info.value
            suggested_filename = download.suggested_filename
            json_save_path = os.path.join(save_dir, suggested_filename)
            download.save_as(json_save_path)
            
            # 截取全網頁高畫質 PNG 截圖
            png_save_path = None
            if save_screenshot:
                timestamp_str = time.strftime("%Y%m%d_%H%M%S")
                png_filename = f"lagcheck_screenshot_{timestamp_str}.png"
                png_save_path = os.path.join(save_dir, png_filename)
                # 等待動畫完全穩定後截圖
                page.wait_for_timeout(300)
                page.screenshot(path=png_save_path, full_page=True)

            browser.close()
            
            elapsed = round(time.time() - start_time, 2)
            print(f"✅ 測試完成！總耗時: {elapsed} 秒")
            print(f"📁 JSON 數據報告 : {json_save_path}")
            if png_save_path:
                print(f"🖼️  PNG 畫面截圖 : {png_save_path}")
            print()

            # 解析並印出詳細統計報告
            parse_and_print_report(json_save_path)
            return json_save_path, png_save_path

        except Exception as e:
            browser.close()
            print(f"❌ 測試過程中發生錯誤或下載逾時: {e}", file=sys.stderr)
            return None, None

def parse_and_print_report(json_file_path: str):
    """讀取 JSON 檔案並印出格式化統計結果"""
    if not os.path.exists(json_file_path):
        return

    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    stats = data.get("stats", {})
    client_info = data.get("clientInfo", {})
    settings = data.get("settings", {})

    print("📊 【品質評級與統計摘要 (Report Summary)】")
    print("-" * 45)
    print(f"  • 企業綜合評級 (Grade) : {stats.get('grade', 'N/A')}")
    print(f"  • 中位數延遲 (P50)     : {stats.get('current', stats.get('p50', '—'))} ms")
    print(f"  • 百分位延遲 (P95)     : {stats.get('p95', '—')} ms")
    print(f"  • 網路抖動 (Jitter)    : {stats.get('jitter', '—')} ms")
    print(f"  • 遺失/逾時率 (Loss)   : {stats.get('loss', 0)} %")
    print(f"  • 最大異常尖峰 (Spike) : {stats.get('spike', '—')} ms")
    print("-" * 45)
    print("🌐 【出口網路與節點資訊】")
    print(f"  • 存取 IP 地址 (IP)    : {client_info.get('ip', '—')}")
    print(f"  • CDN 節點 (Colo)      : {client_info.get('colo', '—')}")
    print(f"  • 所在地區 (Loc)       : {client_info.get('loc', '—')}")
    print("-" * 45)
    print(f"  • 探測 Version        : {data.get('version', 'N/A')}")
    print(f"  • 實際探測端點        : {settings.get('endpoint', 'N/A')}")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="LagCheck 自動化測試與下載工具 (JSON + PNG 截圖)")
    parser.add_argument("--endpoint", "-e", default="https://www.google.com", help="要探測的目標 URL (預設: https://www.google.com)")
    parser.add_argument("--samples", "-s", type=int, default=30, help="採樣樣本數 N (預設: 30)")
    parser.add_argument("--interval", "-i", type=int, default=500, help="採樣間隔毫秒數 (預設: 500 ms)")
    parser.add_argument("--no-headless", action="store_true", help="關閉無頭模式，顯示瀏覽器操作畫面")
    parser.add_argument("--no-screenshot", action="store_true", help="關閉 PNG 畫面截圖儲存")
    parser.add_argument("--output-dir", "-o", default=None, help="檔案儲存目錄")
    
    args = parser.parse_args()
    
    run_lagcheck_test(
        endpoint=args.endpoint,
        samples=args.samples,
        interval_ms=args.interval,
        headless=not args.no_headless,
        save_screenshot=not args.no_screenshot,
        output_dir=args.output_dir
    )

if __name__ == "__main__":
    main()
