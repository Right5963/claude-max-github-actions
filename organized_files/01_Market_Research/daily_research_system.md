# ブーム周期追跡システム - 日次リサーチ自動化

## 🎯 ブーム周期理論の実装

### ジャンル周期マップ（2025年6月基準）
```
GENRE_CYCLE_MAP:
ギャル系: 
  前回ピーク: 2024年10月
  現在: 衰退期（飽和）
  次回ピーク予測: 2025年12月

清楚系:
  前回ピーク: 2024年8月  
  現在: 成長期
  次回ピーク予測: 2025年9月

NTR系:
  前回ピーク: 2025年3月
  現在: 成熟期→飽和期
  次回ピーク予測: 2026年1月

制服系:
  安定ジャンル（通年需要）
  小波動: 3ヶ月周期

人妻系:
  前回ピーク: 2024年12月
  現在: 成長期
  次回ピーク予測: 2025年8月
```

### 日次監視指標
```
DAILY_MONITORING_KPIs:
□ 新着TOP20のジャンル分布変化
□ 人気ランキング上位の顔ぶれ変化  
□ 新規参入サークルの戦略
□ 価格トレンドの変動
□ レビューキーワードの変化
□ SNS話題度の推移
□ 競合の投稿頻度・戦略変更
```

## 🛠️ 自動リサーチスクリプト

### 1. 日次データ収集
```python
#!/usr/bin/env python3
# daily_fanza_research.py

import requests
import json
import datetime
from collections import defaultdict

class DailyFanzaResearch:
    def __init__(self):
        self.api_id = "uGday1gfBB2SXRLwH454"
        self.affiliate_id = "right999-990"
        self.base_url = "https://api.dmm.com/affiliate/v3"
        
    def get_daily_rankings(self):
        """日次ランキング取得"""
        rankings = {}
        
        # 新着ランキング
        rankings['new'] = self.fetch_ranking('date', 50)
        # 人気ランキング  
        rankings['popular'] = self.fetch_ranking('rank', 50)
        
        return rankings
    
    def analyze_genre_trends(self, rankings):
        """ジャンルトレンド分析"""
        genre_count = defaultdict(int)
        
        for rank_type, items in rankings.items():
            for item in items:
                genres = item.get('iteminfo', {}).get('genre', [])
                for genre in genres:
                    genre_count[genre['name']] += 1
                    
        return dict(genre_count)
    
    def detect_boom_signals(self, current_data, historical_data):
        """ブーム兆候検出"""
        signals = []
        
        for genre, current_count in current_data.items():
            historical_avg = historical_data.get(genre, 0)
            if current_count > historical_avg * 1.5:
                signals.append({
                    'genre': genre,
                    'growth_rate': current_count / max(historical_avg, 1),
                    'signal_strength': 'HIGH' if current_count > historical_avg * 2 else 'MEDIUM'
                })
                
        return signals
    
    def save_daily_report(self, data):
        """日次レポート保存"""
        today = datetime.date.today().strftime("%Y%m%d")
        filename = f"daily_research_{today}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# 実行例
researcher = DailyFanzaResearch()
daily_data = researcher.get_daily_rankings()
genre_trends = researcher.analyze_genre_trends(daily_data)
print("今日のジャンルトレンド:", genre_trends)
```

### 2. ブーム周期トラッキング
```python
# boom_cycle_tracker.py

class BoomCycleTracker:
    def __init__(self):
        self.cycle_data = {}
        self.load_historical_data()
    
    def update_cycle_position(self, genre, current_popularity):
        """ジャンルの周期位置更新"""
        if genre not in self.cycle_data:
            self.cycle_data[genre] = {
                'history': [],
                'current_phase': 'unknown',
                'last_peak': None,
                'predicted_next_peak': None
            }
        
        self.cycle_data[genre]['history'].append({
            'date': datetime.date.today(),
            'popularity': current_popularity
        })
        
        # 周期分析
        self.analyze_cycle_phase(genre)
    
    def analyze_cycle_phase(self, genre):
        """周期段階分析"""
        history = self.cycle_data[genre]['history']
        if len(history) < 30:  # 30日未満は分析不可
            return
        
        recent_trend = self.calculate_trend(history[-14:])  # 2週間トレンド
        monthly_trend = self.calculate_trend(history[-30:])  # 1ヶ月トレンド
        
        # 段階判定
        if recent_trend > 20 and monthly_trend > 15:
            phase = "growth"  # 成長期
        elif recent_trend > 10:
            phase = "mature"  # 成熟期
        elif recent_trend < -10:
            phase = "decline"  # 衰退期
        else:
            phase = "stable"  # 安定期
            
        self.cycle_data[genre]['current_phase'] = phase
    
    def predict_next_boom(self, genre):
        """次回ブーム予測"""
        if genre not in self.cycle_data:
            return None
            
        history = self.cycle_data[genre]['history']
        peaks = self.find_peaks(history)
        
        if len(peaks) >= 2:
            # 周期計算
            intervals = [peaks[i+1]['date'] - peaks[i]['date'] 
                        for i in range(len(peaks)-1)]
            avg_interval = sum(intervals, datetime.timedelta()) / len(intervals)
            
            last_peak = peaks[-1]['date']
            predicted_next = last_peak + avg_interval
            
            return predicted_next
        
        return None
```

### 3. 競合分析自動化
```python
# competitor_analyzer.py

class CompetitorAnalyzer:
    def __init__(self):
        self.tracked_circles = []
        self.performance_data = {}
    
    def add_competitor(self, circle_name):
        """競合サークル追加"""
        self.tracked_circles.append(circle_name)
    
    def daily_competitor_check(self):
        """日次競合チェック"""
        results = {}
        
        for circle in self.tracked_circles:
            circle_data = self.get_circle_performance(circle)
            results[circle] = circle_data
            
        return results
    
    def detect_strategy_changes(self, circle_name):
        """戦略変更検出"""
        current = self.get_recent_works(circle_name, days=7)
        previous = self.get_recent_works(circle_name, days=14, offset=7)
        
        changes = {}
        
        # 価格戦略変化
        current_avg_price = sum(w['price'] for w in current) / len(current)
        previous_avg_price = sum(w['price'] for w in previous) / len(previous)
        
        if abs(current_avg_price - previous_avg_price) > 200:
            changes['pricing'] = {
                'change': 'increase' if current_avg_price > previous_avg_price else 'decrease',
                'amount': abs(current_avg_price - previous_avg_price)
            }
        
        # ジャンル変化
        current_genres = set(self.extract_genres(current))
        previous_genres = set(self.extract_genres(previous))
        
        new_genres = current_genres - previous_genres
        if new_genres:
            changes['new_genres'] = list(new_genres)
            
        return changes
```

## 📊 リアルタイム監視ダッシュボード

### ブーム周期可視化
```python
# dashboard.py

import matplotlib.pyplot as plt
import seaborn as sns

class BoomDashboard:
    def __init__(self, tracker):
        self.tracker = tracker
    
    def create_cycle_chart(self):
        """周期チャート作成"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 主要ジャンルの周期表示
        major_genres = ['ギャル', '清楚', 'NTR', '制服']
        
        for i, genre in enumerate(major_genres):
            ax = axes[i//2, i%2]
            
            if genre in self.tracker.cycle_data:
                history = self.tracker.cycle_data[genre]['history']
                dates = [h['date'] for h in history]
                popularity = [h['popularity'] for h in history]
                
                ax.plot(dates, popularity, label=genre)
                ax.set_title(f'{genre}ジャンル周期')
                ax.set_ylabel('人気度')
                
                # 現在段階を色で表示
                phase = self.tracker.cycle_data[genre]['current_phase']
                color_map = {
                    'growth': 'green',
                    'mature': 'orange', 
                    'decline': 'red',
                    'stable': 'blue'
                }
                ax.axhline(y=popularity[-1] if popularity else 0, 
                          color=color_map.get(phase, 'gray'), 
                          linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig('boom_cycle_dashboard.png', dpi=150, bbox_inches='tight')
        return fig
```

## 🎯 AIRサークル専用改善プラン

### 緊急実行タスク（今日から3日間）
```
DAY 1: 現状完全把握
□ 既存全作品の詳細分析
□ 競合TOP10の戦略調査
□ 現在のブーム周期位置確認
□ サークル名検索順位調査

DAY 2: 戦略的方針決定  
□ 集中特化ジャンル決定
□ サークル名改名案検討
□ シリーズ化企画立案
□ 価格戦略見直し

DAY 3: 実行準備完了
□ 新作品企画完成
□ 投稿スケジュール策定
□ ブランドアイデンティティ確定
□ 日次監視システム構築
```

### 週次改善サイクル
```
WEEKLY_IMPROVEMENT_CYCLE:
月曜: 週間データ分析・戦略調整
火曜: 新作品制作開始
水曜: 競合動向チェック・差別化強化
木曜: 作品完成・品質確認
金曜: 投稿・初動反応監視
土曜: 結果分析・改善点抽出
日曜: 次週計画策定
```

### 月次戦略見直し
```
MONTHLY_STRATEGY_REVIEW:
□ ブーム周期予測の精度検証
□ シリーズ化効果測定
□ ブランド認知度調査
□ 競合ポジション分析
□ 価格最適化テスト
□ 次月重点施策決定
```

このシステムにより、ブーム周期を先読みし、最適なタイミングでの作品投入が可能になります。AIRサークルの根本的な問題である「存在認知」から「継続的売上」への転換を実現できます。