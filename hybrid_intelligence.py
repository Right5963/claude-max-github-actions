#!/usr/bin/env python3
"""
ハイブリッド・インテリジェンス（実用版）
=====================================
人間の記録 + 自動AI分析 = 実際の売上改善
"""

import json
import sys
import subprocess
from datetime import datetime, timedelta

class HybridIntelligence:
    def __init__(self):
        self.data_file = 'hybrid_intelligence.json'
        self.load_data()
    
    def load_data(self):
        """データ読み込み"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except:
            self.data = {
                'daily_records': [],
                'ai_analyses': [],
                'actionable_insights': []
            }
    
    def save_data(self):
        """データ保存"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def record_daily_observation(self, sales, actions, observations, competitors=""):
        """日次観察記録（人間の洞察）"""
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        record = {
            'date': today,
            'sales': float(sales),
            'actions_taken': actions,
            'human_observations': observations,
            'competitor_notes': competitors,
            'recorded_at': datetime.now().isoformat()
        }
        
        # 今日の記録があれば更新、なければ追加
        updated = False
        for i, existing in enumerate(self.data['daily_records']):
            if existing['date'] == today:
                self.data['daily_records'][i] = record
                updated = True
                break
        
        if not updated:
            self.data['daily_records'].append(record)
        
        self.save_data()
        
        # 7日溜まったら自動AI分析
        if len(self.data['daily_records']) >= 7:
            self.auto_ai_analysis()
        
        print(f"✅ 観察記録完了: {sales}円 ({today})")
        return True
    
    def auto_ai_analysis(self):
        """自動AI分析実行"""
        
        recent_week = self.data['daily_records'][-7:]
        
        # 分析データ準備
        analysis_data = {
            'period': f"{recent_week[0]['date']} - {recent_week[-1]['date']}",
            'total_sales': sum(r['sales'] for r in recent_week),
            'daily_sales': [r['sales'] for r in recent_week],
            'actions_summary': [r['actions_taken'] for r in recent_week],
            'observations_summary': [r['human_observations'] for r in recent_week],
            'competitor_intelligence': [r['competitor_notes'] for r in recent_week if r['competitor_notes']]
        }
        
        # AI分析実行
        ai_insights = self.execute_ai_analysis(analysis_data)
        
        # 実行可能な提案生成
        actionable_insights = self.generate_actionable_insights(analysis_data, ai_insights)
        
        # 結果保存
        analysis_result = {
            'analysis_date': datetime.now().isoformat(),
            'data_analyzed': analysis_data,
            'ai_insights': ai_insights,
            'actionable_insights': actionable_insights
        }
        
        self.data['ai_analyses'].append(analysis_result)
        self.data['actionable_insights'].extend(actionable_insights)
        
        # 古いデータ削除
        if len(self.data['ai_analyses']) > 10:
            self.data['ai_analyses'] = self.data['ai_analyses'][-10:]
        
        if len(self.data['actionable_insights']) > 20:
            self.data['actionable_insights'] = self.data['actionable_insights'][-20:]
        
        self.save_data()
        
        print("🤖 AI分析完了 - 新しい洞察が生成されました")
        return analysis_result
    
    def execute_ai_analysis(self, data):
        """AI分析実行（利用可能なLLMを自動選択）"""
        
        # 分析プロンプト構築
        prompt = f"""
ヤフオクポスター販売の週次データを専門家として分析してください。

【分析データ】
期間: {data['period']}
総売上: {data['total_sales']:,.0f}円
日別売上: {data['daily_sales']}
実行したアクション: {data['actions_summary']}
観察された現象: {data['observations_summary']}
競合情報: {data['competitor_intelligence']}

【分析してください】
1. 売上パターンの特徴
2. 成功したアクションの特定
3. 改善が必要な領域
4. 競合との差別化要因
5. 来週の具体的改善提案

実行可能で具体的な分析をお願いします。
"""
        
        # Ollama優先で分析
        ai_response = self.try_ollama_analysis(prompt)
        if ai_response:
            return ai_response
        
        # フォールバック：ルールベース分析
        return self.rule_based_analysis(data)
    
    def try_ollama_analysis(self, prompt):
        """Ollama分析試行"""
        
        try:
            import requests
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'llama3.2:3b',
                    'prompt': prompt,
                    'stream': False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', '')
                if len(ai_response) > 100:
                    return f"🤖 Llama3.2分析:\n{ai_response}"
        except:
            pass
        
        return None
    
    def rule_based_analysis(self, data):
        """ルールベース分析（AI不可時）"""
        
        avg_sales = data['total_sales'] / 7
        max_sales = max(data['daily_sales'])
        min_sales = min(data['daily_sales'])
        
        analysis = f"""🔍 自動分析結果:
        
【売上パターン】
- 週平均: {avg_sales:,.0f}円/日
- 最高日: {max_sales:,.0f}円
- 最低日: {min_sales:,.0f}円
- 安定性: {'高' if (max_sales - min_sales) < avg_sales else '要改善'}

【推奨アクション】
"""
        
        if avg_sales < 2000:
            analysis += "- 価格戦略の見直し（2500-3000円帯をテスト）\n"
            analysis += "- 商品画像の改善（アイキャッチ強化）\n"
        
        if max_sales > avg_sales * 1.5:
            analysis += "- 好調日の成功要因を他の日にも適用\n"
        
        if len(data['competitor_intelligence']) > 0:
            analysis += "- 競合分析を活用した差別化戦略\n"
        
        return analysis
    
    def generate_actionable_insights(self, data, ai_insights):
        """実行可能な洞察生成"""
        
        insights = []
        
        # 売上分析ベースの洞察
        avg_sales = data['total_sales'] / 7
        
        if avg_sales < 2000:
            insights.append({
                'type': '価格最適化',
                'action': '商品価格を2500-3000円に調整',
                'priority': 'high',
                'expected_impact': '売上20-30%向上',
                'implementation': '次回出品時に価格変更',
                'date': datetime.now().isoformat()
            })
        
        # 成功パターン特定
        daily_sales = data['daily_sales']
        if max(daily_sales) > avg_sales * 1.3:
            best_day_idx = daily_sales.index(max(daily_sales))
            best_action = data['actions_summary'][best_day_idx]
            
            insights.append({
                'type': '成功パターン活用',
                'action': f'「{best_action}」を他の日にも適用',
                'priority': 'medium',
                'expected_impact': '一貫した売上向上',
                'implementation': '明日から実行',
                'date': datetime.now().isoformat()
            })
        
        # 競合対策
        if data['competitor_intelligence']:
            insights.append({
                'type': '競合対策',
                'action': '競合分析に基づく差別化要因の強化',
                'priority': 'medium',
                'expected_impact': '市場シェア拡大',
                'implementation': '週次での競合チェック継続',
                'date': datetime.now().isoformat()
            })
        
        return insights
    
    def get_current_insights(self):
        """現在の洞察表示"""
        
        print("💡 現在のアクション可能な洞察")
        print("=" * 40)
        
        if not self.data['actionable_insights']:
            # 蓄積済みデータがあれば基本分析を提供
            if self.data['daily_records']:
                self.generate_basic_insights()
                return
            
            print("📊 まだ洞察データがありません")
            print("日次データを記録して分析を開始してください")
            print("使用例: python3 hybrid_intelligence.py record 2500 '価格調整' '売れ行き良好'")
            return
        
        # 最新5件の洞察表示
        recent_insights = self.data['actionable_insights'][-5:]
        
        for i, insight in enumerate(recent_insights, 1):
            print(f"\n{i}. {insight['type']} ({insight['priority']})")
            print(f"   アクション: {insight['action']}")
            print(f"   期待効果: {insight['expected_impact']}")
            print(f"   実行方法: {insight['implementation']}")
    
    def generate_basic_insights(self):
        """基本洞察生成（少ないデータでも有用な分析）"""
        
        if not self.data['daily_records']:
            return
        
        print(f"📊 現在のデータ: {len(self.data['daily_records'])}日分")
        
        # 最近の売上データから基本分析
        recent_sales = [r['sales'] for r in self.data['daily_records'][-7:]]
        avg_sales = sum(recent_sales) / len(recent_sales)
        
        print(f"💰 平均売上: {avg_sales:,.0f}円")
        
        # 即座に実行可能な提案
        print("\n⚡ 即座実行可能な改善案:")
        
        if avg_sales < 2000:
            print("• 価格を2500-3000円に上げてテスト")
        elif avg_sales > 4000:
            print("• 高価格帯商品の追加投入")
        
        if len(self.data['daily_records']) < 7:
            needed = 7 - len(self.data['daily_records'])
            print(f"• あと{needed}日分のデータで詳細AI分析が開始されます")
        
        # 最新記録の分析
        latest = self.data['daily_records'][-1]
        print(f"\n📈 最新記録 ({latest['date']}):")
        print(f"   売上: {latest['sales']:,.0f}円")
        print(f"   アクション: {latest['actions_taken']}")
        print(f"   観察: {latest['human_observations']}")
    
    def weekly_intelligence_report(self):
        """週次インテリジェンスレポート"""
        
        if len(self.data['daily_records']) < 7:
            print("❌ 週次レポートには7日以上のデータが必要")
            return
        
        recent_week = self.data['daily_records'][-7:]
        total_sales = sum(r['sales'] for r in recent_week)
        
        print("🧠 週次インテリジェンスレポート")
        print("=" * 50)
        print(f"📅 期間: {recent_week[0]['date']} - {recent_week[-1]['date']}")
        print(f"💰 総売上: {total_sales:,.0f}円")
        print(f"📊 日平均: {total_sales/7:,.0f}円")
        
        # 最新AI分析
        if self.data['ai_analyses']:
            latest_analysis = self.data['ai_analyses'][-1]
            print(f"\n🤖 AI分析:")
            print(latest_analysis['ai_insights'])
        
        # 実行推奨アクション
        print(f"\n⚡ 今週の実行推奨:")
        self.get_current_insights()

    def add_sample_data(self):
        """サンプルデータ追加（デモ用）"""
        
        print("📝 サンプルデータを追加中...")
        
        # 過去6日分のサンプルデータ
        sample_data = [
            {"sales": 2800, "actions": "新デザイン投入", "observations": "ゲーム系好調"},
            {"sales": 3200, "actions": "価格調整", "observations": "夜の時間帯売れる"},
            {"sales": 1900, "actions": "タイトル変更", "observations": "アニメ系不調"},
            {"sales": 4100, "actions": "タグ最適化", "observations": "美少女系人気"},
            {"sales": 3600, "actions": "画像改善", "observations": "土日売上向上"},
            {"sales": 2400, "actions": "競合分析", "observations": "価格競争激化"}
        ]
        
        # 今日から過去6日間のデータを追加
        for i, data in enumerate(sample_data):
            date = (datetime.now() - timedelta(days=6-i)).strftime('%Y-%m-%d')
            
            record = {
                'date': date,
                'sales': float(data['sales']),
                'actions_taken': data['actions'],
                'human_observations': data['observations'],
                'competitor_notes': '',
                'recorded_at': datetime.now().isoformat()
            }
            
            # 重複チェック
            exists = any(r['date'] == date for r in self.data['daily_records'])
            if not exists:
                self.data['daily_records'].append(record)
        
        self.save_data()
        
        print(f"✅ {len(sample_data)}日分のサンプルデータを追加")
        print("🤖 7日以上のデータが揃ったので自動AI分析を実行中...")
        
        # 自動AI分析実行
        self.auto_ai_analysis()
        
        print("\n📊 現在の状況:")
        self.get_current_insights()

def main():
    """メイン実行"""
    
    hi = HybridIntelligence()
    
    if len(sys.argv) < 2:
        hi.get_current_insights()
        print("\n使用方法:")
        print("python3 hybrid_intelligence.py record 売上額 'アクション' '観察' '競合情報'")
        print("python3 hybrid_intelligence.py insights")
        print("python3 hybrid_intelligence.py report")
        print("python3 hybrid_intelligence.py demo  # サンプルデータでデモ実行")
        return
    
    command = sys.argv[1]
    
    if command == "record":
        if len(sys.argv) < 5:
            print("❌ 引数不足: 売上額、アクション、観察が必要")
            return
        
        sales = sys.argv[2]
        actions = sys.argv[3]
        observations = sys.argv[4]
        competitors = sys.argv[5] if len(sys.argv) > 5 else ""
        
        hi.record_daily_observation(sales, actions, observations, competitors)
        
    elif command == "insights":
        hi.get_current_insights()
        
    elif command == "report":
        hi.weekly_intelligence_report()
        
    elif command == "demo":
        hi.add_sample_data()
        
    else:
        print("❌ 無効なコマンド")

if __name__ == "__main__":
    main()