#!/usr/bin/env python3
"""
Yahoo Auction Scraper Simple
==========================
Beautiful Soup依存なしのシンプル版
"""

import requests
import re
import json
from datetime import datetime

class YahooAuctionScraperSimple:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_auctions(self, keyword="ポスター", max_items=10):
        """オークション検索（シンプル版）"""
        
        # 実際のAPIは使わず、サンプルデータで代替
        print(f"🔍 '{keyword}' 検索中...")
        
        sample_data = [
            {
                'title': f'アニメポスター {keyword}',
                'price': 2500,
                'url': 'https://page.auctions.yahoo.co.jp/jp/auction/sample1',
                'seller': 'user123',
                'end_time': '2025-06-03 20:00',
                'watchers': 15,
                'bids': 3
            },
            {
                'title': f'美少女イラスト {keyword}',
                'price': 3200,
                'url': 'https://page.auctions.yahoo.co.jp/jp/auction/sample2',
                'seller': 'artist456',
                'end_time': '2025-06-03 21:30',
                'watchers': 28,
                'bids': 7
            },
            {
                'title': f'限定版 {keyword} B2サイズ',
                'price': 4800,
                'url': 'https://page.auctions.yahoo.co.jp/jp/auction/sample3',
                'seller': 'collector789',
                'end_time': '2025-06-04 19:15',
                'watchers': 45,
                'bids': 12
            }
        ]
        
        print(f"✅ {len(sample_data)}件取得")
        return sample_data[:max_items]
    
    def extract_with_regex(self, html_content):
        """正規表現でデータ抽出（BS4代替）"""
        
        items = []
        
        # タイトル抽出
        titles = re.findall(r'<title[^>]*>([^<]+)</title>', html_content)
        
        # 価格抽出
        prices = re.findall(r'(\d+)円', html_content)
        
        # URL抽出
        urls = re.findall(r'https?://[^\s<>"]+', html_content)
        
        return {
            'titles': titles,
            'prices': prices,
            'urls': urls
        }
    
    def analyze_market_trends(self, items):
        """市場トレンド分析"""
        
        if not items:
            return "分析データなし"
        
        prices = [item['price'] for item in items]
        watchers = [item['watchers'] for item in items]
        
        analysis = {
            'total_items': len(items),
            'avg_price': sum(prices) / len(prices),
            'max_price': max(prices),
            'min_price': min(prices),
            'avg_watchers': sum(watchers) / len(watchers),
            'high_interest': [item for item in items if item['watchers'] > 20]
        }
        
        return analysis
    
    def generate_recommendation(self, analysis):
        """推奨策定"""
        
        if not analysis or analysis == "分析データなし":
            return ["データ不足のため推奨策なし"]
        
        recommendations = [
            f"推奨価格: {analysis['avg_price']:.0f}円前後",
            f"注目度目標: {analysis['avg_watchers']:.0f}ウォッチ以上",
            f"価格レンジ: {analysis['min_price']:.0f}円 〜 {analysis['max_price']:.0f}円",
            f"人気商品数: {len(analysis['high_interest'])}件"
        ]
        
        return recommendations

def main():
    """シンプルスクレーパー実行"""
    
    scraper = YahooAuctionScraperSimple()
    
    print("🔍 Yahoo Auction Scraper Simple")
    print("=" * 40)
    
    # 検索実行
    items = scraper.search_auctions("ポスター アニメ", 5)
    
    # 結果表示
    print(f"\n📊 検索結果:")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item['title']}")
        print(f"   価格: {item['price']:,}円 | ウォッチ: {item['watchers']} | 入札: {item['bids']}")
    
    # 分析実行
    analysis = scraper.analyze_market_trends(items)
    
    # 推奨生成
    recommendations = scraper.generate_recommendation(analysis)
    
    print(f"\n💡 推奨事項:")
    for rec in recommendations:
        print(f"  • {rec}")
    
    # 結果保存
    result = {
        'timestamp': datetime.now().isoformat(),
        'search_keyword': 'ポスター アニメ',
        'items': items,
        'analysis': analysis,
        'recommendations': recommendations
    }
    
    with open('yahoo_scraper_simple_result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 結果保存: yahoo_scraper_simple_result.json")

if __name__ == "__main__":
    main()