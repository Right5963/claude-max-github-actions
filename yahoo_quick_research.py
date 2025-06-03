#!/usr/bin/env python3
"""
ヤフオク高速リサーチツール
========================
キーワードから売れ筋・価格帯を瞬時に調査
"""

import sys
import urllib.parse
import subprocess

def quick_research(keyword):
    """キーワードから調査用URLを生成して開く"""
    encoded = urllib.parse.quote(keyword)
    
    # 落札相場（350円以上の売れたもの）
    sold_url = f"https://auctions.yahoo.co.jp/closedsearch/closedsearch?p={encoded}&va={encoded}&aucminprice=350&b=1&n=50"
    
    # 現在出品中（競合調査）
    active_url = f"https://auctions.yahoo.co.jp/search/search?p={encoded}&va={encoded}&aucminprice=350"
    
    print(f"🔍 '{keyword}' のリサーチ開始\n")
    print("1️⃣ 落札相場を確認...")
    subprocess.run(['powershell.exe', '-Command', f'Start-Process "{sold_url}"'])
    
    print("2️⃣ 現在の競合を確認...")
    subprocess.run(['powershell.exe', '-Command', f'Start-Process "{active_url}"'])
    
    print("\n✅ チェックポイント:")
    print("  - 平均落札価格")
    print("  - 人気の画像スタイル")
    print("  - 売れているサイズ（A4/B2等）")
    print("  - タイトルのキーワード")

if __name__ == "__main__":
    keyword = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "ポスター"
    quick_research(keyword)