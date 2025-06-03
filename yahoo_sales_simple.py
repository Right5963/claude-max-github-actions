#!/usr/bin/env python3
"""
Yahoo売上分析（シンプル版）
=========================
データ不足問題を解決し、実用的な分析を提供
"""

import json
from datetime import datetime, timedelta

class YahooSalesSimple:
    def __init__(self):
        self.data_file = "yahoo_sales_data.json"
        self.sales_data = self.load_data()
    
    def load_data(self):
        """売上データ読み込み"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'sales': []}
    
    def save_data(self):
        """データ保存"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.sales_data, f, ensure_ascii=False, indent=2)
    
    def add_sale(self, amount, item, notes=""):
        """売上記録"""
        sale = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M'),
            'amount': float(amount),
            'item': item,
            'notes': notes
        }
        
        self.sales_data['sales'].append(sale)
        self.save_data()
        print(f"✅ 売上記録: {amount}円 - {item}")
    
    def analyze_sales(self):
        """売上分析"""
        sales = self.sales_data['sales']
        
        if not sales:
            print("❌ 売上データがありません")
            return
        
        # 基本統計
        amounts = [s['amount'] for s in sales]
        total = sum(amounts)
        avg = total / len(amounts)
        
        print("📊 Yahoo売上分析")
        print("=" * 30)
        print(f"総売上: {total:,.0f}円")
        print(f"平均単価: {avg:,.0f}円")
        print(f"販売数: {len(sales)}件")
        print(f"最高額: {max(amounts):,.0f}円")
        print(f"最低額: {min(amounts):,.0f}円")
        
        # 週次トレンド
        print(f"\n📈 最近7日の傾向:")
        recent_sales = [s for s in sales if self.is_recent(s['date'], 7)]
        if recent_sales:
            recent_total = sum(s['amount'] for s in recent_sales)
            daily_avg = recent_total / 7
            print(f"週合計: {recent_total:,.0f}円")
            print(f"日平均: {daily_avg:,.0f}円")
        else:
            print("最近のデータなし")
        
        # 売れ筋商品
        print(f"\n🏆 売れ筋商品TOP3:")
        items = {}
        for sale in sales:
            item = sale['item']
            if item in items:
                items[item] += sale['amount']
            else:
                items[item] = sale['amount']
        
        sorted_items = sorted(items.items(), key=lambda x: x[1], reverse=True)
        for i, (item, amount) in enumerate(sorted_items[:3], 1):
            print(f"{i}. {item}: {amount:,.0f}円")
    
    def is_recent(self, date_str, days):
        """指定日数以内かチェック"""
        try:
            sale_date = datetime.strptime(date_str, '%Y-%m-%d')
            return (datetime.now() - sale_date).days <= days
        except:
            return False

def main():
    """メイン実行"""
    import sys
    
    ys = YahooSalesSimple()
    
    if len(sys.argv) < 2:
        ys.analyze_sales()
        print("\n使用方法:")
        print("python3 yahoo_sales_simple.py add 金額 '商品名' '備考'")
        print("python3 yahoo_sales_simple.py analyze")
        return
    
    command = sys.argv[1]
    
    if command == "add" and len(sys.argv) >= 4:
        amount = sys.argv[2]
        item = sys.argv[3]
        notes = sys.argv[4] if len(sys.argv) > 4 else ""
        ys.add_sale(amount, item, notes)
        
    elif command == "analyze":
        ys.analyze_sales()
        
    else:
        print("❌ 無効なコマンド")

if __name__ == "__main__":
    main()