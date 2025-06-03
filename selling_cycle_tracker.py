#!/usr/bin/env python3
"""
売上改善サイクル追跡（完全自動化版）
=================================
"default_value"  # input()なし、完全自動で動作する実用システム
"""

import json
import sys
from datetime import datetime, timedelta

class SellingTracker:
    def __init__(self):
        self.data_file = 'selling_data.json'
        self.load_data()
    
    def load_data(self):
        """データ読み込み"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except:
            self.data = {'daily_logs': [], 'insights': []}
    
    def save_data(self):
        """データ保存"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def log_sales(self, sales_amount, item_sold="", notes=""):
        """売上記録（完全自動）"""
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 今日の記録があるかチェック
        today_log = None
        for log in self.data['daily_logs']:
            if log['date'] == today:
                today_log = log
                break
        
        if today_log:
            # 既存記録に追加
            today_log['sales'] += float(sales_amount)
            today_log['items'].append(item_sold)
            today_log['notes'].append(notes)
            today_log['updated'] = datetime.now().isoformat()
        else:
            # 新規記録作成
            new_log = {
                'date': today,
                'sales': float(sales_amount),
                'items': [item_sold] if item_sold else [],
                'notes': [notes] if notes else [],
                'created': datetime.now().isoformat()
            }
            self.data['daily_logs'].append(new_log)
        
        self.save_data()
        
        # 即座分析
        self.auto_analyze()
        
        print(f"✅ 売上記録: {sales_amount}円 ({today})")
        return True
    
    def auto_analyze(self):
        """自動分析実行"""
        
        if len(self.data['daily_logs']) < 3:
            return
        
        # 直近7日分析
        recent_logs = self.data['daily_logs'][-7:]
        total_sales = sum(log['sales'] for log in recent_logs)
        avg_sales = total_sales / len(recent_logs)
        
        # トレンド分析
        if len(recent_logs) >= 3:
            recent_3 = sum(log['sales'] for log in recent_logs[-3:]) / 3
            previous_3 = sum(log['sales'] for log in recent_logs[-6:-3]) / 3 if len(recent_logs) >= 6 else recent_3
            
            if recent_3 > previous_3 * 1.1:
                trend = "上昇"
            elif recent_3 < previous_3 * 0.9:
                trend = "下降"
            else:
                trend = "横ばい"
        else:
            trend = "データ不足"
        
        # 洞察生成
        insight = {
            'date': datetime.now().isoformat(),
            'period': f"直近{len(recent_logs)}日",
            'total_sales': total_sales,
            'avg_sales': avg_sales,
            'trend': trend,
            'recommendation': self.generate_recommendation(trend, avg_sales)
        }
        
        self.data['insights'].append(insight)
        
        # 古い洞察削除（最新10件のみ保持）
        if len(self.data['insights']) > 10:
            self.data['insights'] = self.data['insights'][-10:]
    
    def generate_recommendation(self, trend, avg_sales):
        """改善提案生成"""
        
        if trend == "上昇":
            return f"📈 好調！現在の戦略を継続し、成功要因を他商品にも適用"
        elif trend == "下降": 
            return f"📉 要注意。価格見直し、商品画像改善、競合分析を実施"
        elif avg_sales < 1000:
            return f"💡 売上が低め。タイトル改善、価格調整、出品時間見直しを推奨"
        else:
            return f"✅ 安定。さらなる成長のため新商品カテゴリーの検討を"
    
    def weekly_report(self):
        """週次レポート生成"""
        
        if len(self.data['daily_logs']) < 7:
            print("❌ 週次レポートには7日以上のデータが必要")
            return
        
        # 直近7日
        week_logs = self.data['daily_logs'][-7:]
        total = sum(log['sales'] for log in week_logs)
        avg = total / 7
        best_day = max(week_logs, key=lambda x: x['sales'])
        worst_day = min(week_logs, key=lambda x: x['sales'])
        
        print("📊 週次レポート")
        print("=" * 30)
        print(f"📅 期間: {week_logs[0]['date']} 〜 {week_logs[-1]['date']}")
        print(f"💰 総売上: {total:,.0f}円")
        print(f"💰 日平均: {avg:,.0f}円")
        print(f"🏆 最高日: {best_day['date']} ({best_day['sales']:,.0f}円)")
        print(f"📉 最低日: {worst_day['date']} ({worst_day['sales']:,.0f}円)")
        
        # 最新の洞察表示
        if self.data['insights']:
            latest = self.data['insights'][-1]
            print(f"🎯 提案: {latest['recommendation']}")
    
    def quick_status(self):
        """クイックステータス"""
        
        if not self.data['daily_logs']:
            print("📊 データなし - 売上記録を開始してください")
            return
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 今日の売上
        today_sales = 0
        for log in self.data['daily_logs']:
            if log['date'] == today:
                today_sales = log['sales']
                break
        
        # 直近7日平均
        recent = self.data['daily_logs'][-7:] if len(self.data['daily_logs']) >= 7 else self.data['daily_logs']
        avg_recent = sum(log['sales'] for log in recent) / len(recent)
        
        # 総計
        total_days = len(self.data['daily_logs'])
        total_sales = sum(log['sales'] for log in self.data['daily_logs'])
        
        print("⚡ クイックステータス")
        print("=" * 25)
        print(f"📅 今日: {today_sales:,.0f}円")
        print(f"📈 直近平均: {avg_recent:,.0f}円")
        print(f"📊 総売上: {total_sales:,.0f}円 ({total_days}日)")
        
        # 最新提案
        if self.data['insights']:
            latest = self.data['insights'][-1]
            print(f"💡 提案: {latest['recommendation']}")

def main():
    """メイン実行"""
    
    tracker = SellingTracker()
    
    if len(sys.argv) < 2:
        tracker.quick_status()
        print("\n使用方法:")
        print("python3 selling_cycle_tracker_fixed.py log 1500 'ポスター名' '備考'")
        print("python3 selling_cycle_tracker_fixed.py report")
        print("python3 selling_cycle_tracker_fixed.py status")
        return
    
    command = sys.argv[1]
    
    if command == "log":
        if len(sys.argv) < 3:
            print("❌ 売上額が必要です")
            return
        
        sales = sys.argv[2]
        item = sys.argv[3] if len(sys.argv) > 3 else ""
        notes = sys.argv[4] if len(sys.argv) > 4 else ""
        
        tracker.log_sales(sales, item, notes)
        
    elif command == "report":
        tracker.weekly_report()
        
    elif command == "status":
        tracker.quick_status()
        
    else:
        print("❌ 無効なコマンド")

if __name__ == "__main__":
    main()