#!/usr/bin/env python3
"""
売上改善コアシステム
==================
売上追跡、PDCA、競合分析、AI洞察を統合した完全版
"""

import json
import sys
import requests
from datetime import datetime, timedelta

class SalesImprovementCore:
    def __init__(self):
        self.data_file = 'sales_core_data.json'
        self.load_data()
    
    def load_data(self):
        """データ読み込み"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except:
            self.data = {
                'daily_sales': [],
                'pdca_cycles': [],
                'competitor_insights': [],
                'ai_recommendations': [],
                'improvement_history': []
            }
    
    def save_data(self):
        """データ保存"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    # === 売上記録機能 ===
    def record_sale(self, amount, item="", notes="", price=0, platform="Yahoo"):
        """売上記録"""
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        sale_record = {
            'date': today,
            'amount': float(amount),
            'item': item,
            'notes': notes,
            'price': float(price),
            'platform': platform,
            'timestamp': datetime.now().isoformat()
        }
        
        # 今日の記録に追加
        today_sales = [s for s in self.data['daily_sales'] if s['date'] == today]
        if today_sales:
            self.data['daily_sales'].append(sale_record)
        else:
            self.data['daily_sales'].append(sale_record)
        
        self.save_data()
        
        # 自動分析トリガー
        self.auto_analyze_sales()
        
        print(f"✅ 売上記録: {amount}円 - {item}")
        return True
    
    def get_sales_summary(self, days=7):
        """売上サマリー"""
        
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        recent_sales = [s for s in self.data['daily_sales'] if s['date'] >= cutoff_date]
        
        if not recent_sales:
            return {"total": 0, "count": 0, "average": 0, "trend": "データなし"}
        
        total = sum(s['amount'] for s in recent_sales)
        count = len(recent_sales)
        average = total / count
        
        # トレンド計算
        mid_point = len(recent_sales) // 2
        if len(recent_sales) >= 4:
            first_half = sum(s['amount'] for s in recent_sales[:mid_point]) / mid_point
            second_half = sum(s['amount'] for s in recent_sales[mid_point:]) / (len(recent_sales) - mid_point)
            
            if second_half > first_half * 1.1:
                trend = "上昇"
            elif second_half < first_half * 0.9:
                trend = "下降"
            else:
                trend = "横ばい"
        else:
            trend = "判定不可"
        
        return {
            "total": total,
            "count": count,
            "average": average,
            "trend": trend,
            "days": days
        }
    
    # === PDCA機能 ===
    def start_pdca(self, hypothesis, target, actions, duration=7):
        """PDCAサイクル開始"""
        
        cycle = {
            'id': len(self.data['pdca_cycles']) + 1,
            'start_date': datetime.now().isoformat(),
            'hypothesis': hypothesis,
            'target': target,
            'planned_actions': actions,
            'duration_days': duration,
            'daily_logs': [],
            'status': 'active',
            'results': None
        }
        
        self.data['pdca_cycles'].append(cycle)
        self.save_data()
        
        print(f"🚀 PDCAサイクル{cycle['id']}開始")
        print(f"仮説: {hypothesis}")
        print(f"目標: {target}")
        
        return cycle['id']
    
    def log_pdca_progress(self, observations, actions_taken):
        """PDCA進捗記録"""
        
        active_cycles = [c for c in self.data['pdca_cycles'] if c['status'] == 'active']
        
        if not active_cycles:
            print("❌ アクティブなPDCAサイクルがありません")
            return False
        
        cycle = active_cycles[-1]  # 最新のアクティブサイクル
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        log_entry = {
            'date': today,
            'observations': observations,
            'actions_taken': actions_taken,
            'timestamp': datetime.now().isoformat()
        }
        
        cycle['daily_logs'].append(log_entry)
        
        # 期間チェック
        start_date = datetime.fromisoformat(cycle['start_date']).date()
        days_elapsed = (datetime.now().date() - start_date).days
        
        if days_elapsed >= cycle['duration_days']:
            self.complete_pdca_cycle(cycle)
        
        self.save_data()
        
        print(f"✅ PDCA進捗記録 ({days_elapsed+1}/{cycle['duration_days']}日)")
        return True
    
    def complete_pdca_cycle(self, cycle):
        """PDCAサイクル完了"""
        
        # 結果分析
        sales_during_cycle = self.get_sales_summary(cycle['duration_days'])
        
        # 目標達成判定
        target_amount = self.extract_number_from_text(cycle['target'])
        achievement_rate = 0
        
        if target_amount > 0:
            achievement_rate = (sales_during_cycle['total'] / target_amount) * 100
        
        # 成功レベル判定
        if achievement_rate >= 100:
            success_level = "目標達成"
        elif achievement_rate >= 80:
            success_level = "ほぼ達成"
        elif achievement_rate >= 50:
            success_level = "部分達成"
        else:
            success_level = "要改善"
        
        cycle['results'] = {
            'completion_date': datetime.now().isoformat(),
            'sales_total': sales_during_cycle['total'],
            'target_amount': target_amount,
            'achievement_rate': achievement_rate,
            'success_level': success_level,
            'key_learnings': self.extract_key_learnings(cycle['daily_logs'])
        }
        
        cycle['status'] = 'completed'
        
        # 改善履歴に追加
        improvement = {
            'date': datetime.now().isoformat(),
            'cycle_id': cycle['id'],
            'hypothesis': cycle['hypothesis'],
            'result': success_level,
            'learning': cycle['results']['key_learnings'],
            'next_action': self.suggest_next_action(cycle['results'])
        }
        
        self.data['improvement_history'].append(improvement)
        
        print(f"📊 PDCAサイクル{cycle['id']}完了: {success_level}")
        print(f"達成率: {achievement_rate:.1f}%")
        
        return cycle['results']
    
    # === 競合分析機能 ===
    def analyze_competitors(self, keywords="ポスター アニメ"):
        """簡易競合分析"""
        
        analysis_date = datetime.now().isoformat()
        
        # 模擬的な競合分析（実際はスクレイピング等で実装）
        competitor_data = {
            'analysis_date': analysis_date,
            'keywords': keywords,
            'findings': [
                "平均価格帯: 2,500-3,500円",
                "人気キーワード: 限定、美少女、高画質",
                "最適出品時間: 20-22時終了",
                "成功要因: 鮮明な画像、詳細な説明文"
            ],
            'recommendations': [
                "価格を2,800円前後に設定",
                "タイトルに「限定」「高画質」を含める",
                "商品画像の品質向上",
                "終了時間を21時頃に設定"
            ]
        }
        
        self.data['competitor_insights'].append(competitor_data)
        
        # 最新10件のみ保持
        if len(self.data['competitor_insights']) > 10:
            self.data['competitor_insights'] = self.data['competitor_insights'][-10:]
        
        self.save_data()
        
        print("🔍 競合分析完了")
        for finding in competitor_data['findings']:
            print(f"   • {finding}")
        
        return competitor_data
    
    # === AI分析機能 ===
    def auto_analyze_sales(self):
        """売上データの自動AI分析"""
        
        recent_sales = self.get_sales_summary(7)
        
        if recent_sales['count'] < 3:
            return  # データ不足
        
        # 簡易AI分析
        recommendations = []
        
        if recent_sales['average'] < 2000:
            recommendations.append("価格戦略見直し: 2500円以上での価格設定を検討")
        
        if recent_sales['trend'] == "下降":
            recommendations.append("緊急対策: 商品画像・説明文の改善が必要")
        elif recent_sales['trend'] == "上昇":
            recommendations.append("好調維持: 現在の戦略を継続し他商品にも展開")
        
        if len(self.data['daily_sales']) >= 7:
            # 曜日分析
            weekday_sales = {}
            for sale in self.data['daily_sales'][-21:]:  # 3週間分
                date_obj = datetime.fromisoformat(sale['timestamp'])
                weekday = date_obj.strftime('%A')
                weekday_sales[weekday] = weekday_sales.get(weekday, 0) + sale['amount']
            
            if weekday_sales:
                best_day = max(weekday_sales, key=weekday_sales.get)
                recommendations.append(f"最適出品日: {best_day}の出品が効果的")
        
        if recommendations:
            ai_analysis = {
                'analysis_date': datetime.now().isoformat(),
                'data_period': f"直近{recent_sales['days']}日",
                'sales_summary': recent_sales,
                'recommendations': recommendations
            }
            
            self.data['ai_recommendations'].append(ai_analysis)
            
            # 最新10件のみ保持
            if len(self.data['ai_recommendations']) > 10:
                self.data['ai_recommendations'] = self.data['ai_recommendations'][-10:]
            
            self.save_data()
            
            print("🤖 AI分析完了 - 新しい推奨事項が生成されました")
    
    # === ユーティリティ機能 ===
    def extract_number_from_text(self, text):
        """テキストから数値抽出"""
        import re
        numbers = re.findall(r'\\d+', str(text))
        return int(numbers[0]) if numbers else 0
    
    def extract_key_learnings(self, daily_logs):
        """日次ログから重要な学習事項を抽出"""
        if not daily_logs:
            return "学習事項なし"
        
        # 最後のログから学習事項を取得
        last_log = daily_logs[-1]
        return last_log.get('observations', '継続観察中')
    
    def suggest_next_action(self, results):
        """次のアクション提案"""
        if results['achievement_rate'] >= 100:
            return "成功要因を他商品・戦略にも適用"
        elif results['achievement_rate'] >= 50:
            return "部分的成功を完全成功に押し上げる改善"
        else:
            return "根本的な戦略変更を検討"
    
    # === 統合ダッシュボード ===
    def show_dashboard(self):
        """総合ダッシュボード表示"""
        
        print("📊 売上改善ダッシュボード")
        print("=" * 50)
        
        # 売上サマリー
        weekly_sales = self.get_sales_summary(7)
        monthly_sales = self.get_sales_summary(30)
        
        print(f"💰 売上状況:")
        print(f"   週間: {weekly_sales['total']:,.0f}円 ({weekly_sales['count']}件) - {weekly_sales['trend']}")
        print(f"   月間: {monthly_sales['total']:,.0f}円 ({monthly_sales['count']}件)")
        
        # PDCAステータス
        active_pdca = [c for c in self.data['pdca_cycles'] if c['status'] == 'active']
        completed_pdca = [c for c in self.data['pdca_cycles'] if c['status'] == 'completed']
        
        print(f"\\n🔄 PDCA状況:")
        print(f"   アクティブサイクル: {len(active_pdca)}")
        print(f"   完了サイクル: {len(completed_pdca)}")
        
        if active_pdca:
            cycle = active_pdca[-1]
            start_date = datetime.fromisoformat(cycle['start_date']).date()
            days_elapsed = (datetime.now().date() - start_date).days
            print(f"   現在: {cycle['hypothesis']} ({days_elapsed+1}/{cycle['duration_days']}日)")
        
        # 最新AI推奨事項
        if self.data['ai_recommendations']:
            latest_ai = self.data['ai_recommendations'][-1]
            print(f"\\n🤖 最新AI推奨:")
            for rec in latest_ai['recommendations'][:2]:
                print(f"   • {rec}")
        
        # 最新競合分析
        if self.data['competitor_insights']:
            latest_competitor = self.data['competitor_insights'][-1]
            print(f"\\n🔍 最新競合洞察:")
            for rec in latest_competitor['recommendations'][:2]:
                print(f"   • {rec}")

def main():
    """メイン実行"""
    
    core = SalesImprovementCore()
    
    if len(sys.argv) < 2:
        core.show_dashboard()
        print("\\n使用方法:")
        print("python3 sales_improvement_core.py sale 金額 [商品名] [備考] [価格] [プラットフォーム]")
        print("python3 sales_improvement_core.py pdca-start '仮説' '目標' '行動計画' [期間]")
        print("python3 sales_improvement_core.py pdca-log '観察' '実行内容'")
        print("python3 sales_improvement_core.py competitor [キーワード]")
        print("python3 sales_improvement_core.py dashboard")
        return
    
    command = sys.argv[1]
    
    if command == "sale":
        if len(sys.argv) < 3:
            print("❌ 売上金額が必要です")
            return
        
        amount = sys.argv[2]
        item = sys.argv[3] if len(sys.argv) > 3 else ""
        notes = sys.argv[4] if len(sys.argv) > 4 else ""
        price = sys.argv[5] if len(sys.argv) > 5 else "0"
        platform = sys.argv[6] if len(sys.argv) > 6 else "Yahoo"
        
        core.record_sale(amount, item, notes, price, platform)
        
    elif command == "pdca-start":
        if len(sys.argv) < 5:
            print("❌ 仮説、目標、行動計画が必要です")
            return
        
        hypothesis = sys.argv[2]
        target = sys.argv[3]
        actions = sys.argv[4]
        duration = int(sys.argv[5]) if len(sys.argv) > 5 else 7
        
        core.start_pdca(hypothesis, target, actions, duration)
        
    elif command == "pdca-log":
        if len(sys.argv) < 4:
            print("❌ 観察と実行内容が必要です")
            return
        
        observations = sys.argv[2]
        actions = sys.argv[3]
        
        core.log_pdca_progress(observations, actions)
        
    elif command == "competitor":
        keywords = sys.argv[2] if len(sys.argv) > 2 else "ポスター アニメ"
        core.analyze_competitors(keywords)
        
    elif command == "dashboard":
        core.show_dashboard()
        
    else:
        print("❌ 無効なコマンド")

if __name__ == "__main__":
    main()