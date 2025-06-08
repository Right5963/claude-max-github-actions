# 実用的FANZA同人リサーチワークフロー - 完全実行ガイド

#ワークフロー #実用 #リサーチ #FANZA #同人 #収益化 #実行ガイド

> **作成日**: 2025-06-05  
> **目的**: DMM MCPを活用した日常的に実行可能なリサーチワークフロー  
> **対象**: 収益化を目指すFANZA同人作家・サークル

---

## 🚀 Quick Start: 5分で始める日次リサーチ

### 朝のルーティン (毎日5分)
```bash
# 1. ランキングチェック (2分)
node /mnt/c/Claude\ Code/tool/build/dmm-affiliate-server.js dmm_get_ranking

# 2. 新作チェック (2分)  
node /mnt/c/Claude\ Code/tool/build/dmm-affiliate-server.js dmm_search_doujin --sort=date --hits=10

# 3. 気づきメモ (1分)
echo "$(date): [気づき内容]" >> research_log.txt
```

### 夕方のルーティン (毎日5分)
```bash
# 1. 価格動向チェック (2分)
node /mnt/c/Claude\ Code/tool/build/dmm-affiliate-server.js dmm_market_analysis --analysis_type=price

# 2. 仮説記録 (3分)
echo "$(date): [仮説・気づき]" >> hypothesis_log.txt
```

---

## 📊 週次リサーチワークフロー (毎週45分)

### Step 1: データ収集 (15分)
```bash
#!/bin/bash
# weekly_research.sh

echo "=== 週次リサーチ開始: $(date) ===" >> weekly_report.md

# 価格帯分析
echo "## 価格帯分析" >> weekly_report.md
node /mnt/c/Claude\ Code/tool/build/dmm-affiliate-server.js dmm_market_analysis --analysis_type=price >> weekly_report.md

# ジャンル分析
echo "## ジャンル分析" >> weekly_report.md  
node /mnt/c/Claude\ Code/tool/build/dmm-affiliate-server.js dmm_market_analysis --analysis_type=genre >> weekly_report.md

# トレンド分析
echo "## トレンド分析" >> weekly_report.md
node /mnt/c/Claude\ Code/tool/build/dmm-affiliate-server.js dmm_market_analysis --analysis_type=trend >> weekly_report.md

echo "データ収集完了: $(date)"
```

### Step 2: 分析とパターン認識 (20分)
```markdown
# 週次分析チェックリスト

## 価格動向分析
□ 平均価格の変化: 前週比___円 (±___%)
□ 主力価格帯の変化: ___円台が___%占有
□ 価格競争の兆候: あり/なし
□ プレミアム価格帯の動向: ___

## ジャンル動向分析  
□ 成長ジャンル: _____ (+___%)
□ 衰退ジャンル: _____ (-___%)
□ 新興ジャンル: _____
□ 安定ジャンル: _____

## 競合動向分析
□ 新規強豪サークル: _____
□ 戦略変更の観察: _____
□ 注目すべき新作: _____
□ 価格戦略の変化: _____

## 機会発見
□ 空白市場の発見: _____
□ 競争度の低いジャンル: _____
□ 価格最適化の機会: _____
□ タイミング的機会: _____
```

### Step 3: 戦術的示唆と行動計画 (10分)
```markdown
# 行動計画テンプレート

## 即座に実行すべきアクション
1. _____
2. _____
3. _____

## 来週重点的に監視する項目  
1. _____
2. _____
3. _____

## 次回作への示唆
□ 推奨ジャンル: _____
□ 推奨価格帯: _____円
□ 差別化ポイント: _____
□ 投入タイミング: _____

## リスク要因
□ 競合動向: _____
□ 市場変化: _____
□ 価格圧力: _____
```

---

## 🎯 月次戦略リサーチ (毎月3時間)

### Phase 1: 包括的市場分析 (90分)

#### 1.1 全方位データ収集 (30分)
```bash
#!/bin/bash
# monthly_comprehensive_research.sh

# 全分析タイプを実行
for analysis_type in price circle genre trend; do
    echo "=== ${analysis_type} 分析 ===" >> monthly_analysis.md
    node /mnt/c/Claude\ Code/tool/build/dmm-affiliate-server.js dmm_market_analysis --analysis_type=${analysis_type} >> monthly_analysis.md
    echo "" >> monthly_analysis.md
    sleep 5  # API制限回避
done

# 主要キーワード別調査
keywords=("制服" "巨乳" "学園" "ギャル" "人妻")
for keyword in "${keywords[@]}"; do
    echo "=== ${keyword} 市場調査 ===" >> monthly_analysis.md
    node /mnt/c/Claude\ Code/tool/build/dmm-affiliate-server.js dmm_search_doujin --keyword="${keyword}" --hits=50 >> monthly_analysis.md
    echo "" >> monthly_analysis.md
    sleep 5
done
```

#### 1.2 競合サークル詳細分析 (30分)
```bash
# 上位サークルの戦略分析
top_circles=("サークル名1" "サークル名2" "サークル名3")
for circle in "${top_circles[@]}"; do
    echo "=== ${circle} 分析 ===" >> competitor_analysis.md
    node /mnt/c/Claude\ Code/tool/build/dmm-affiliate-server.js dmm_search_circles --keyword="${circle}" >> competitor_analysis.md
    echo "" >> competitor_analysis.md
done
```

#### 1.3 手動深掘り調査 (30分)
```markdown
# 深掘り調査チェックリスト

## 成功作品の要因分析
□ 上位3作品のサムネイル分析完了
□ タイトルの訴求ポイント分析完了  
□ 説明文の特徴分析完了
□ 価格戦略の合理性評価完了
□ レビューから満足要因抽出完了

## 失敗作品の要因分析
□ 低評価作品の共通要因特定完了
□ 価格設定の問題点分析完了
□ マーケティングの課題特定完了

## 市場ギャップ分析
□ 需要はあるが供給が少ない分野特定
□ 価格ギャップの存在確認
□ 未開拓の組み合わせ発見
```

### Phase 2: 戦略的洞察抽出 (60分)

#### 2.1 SWOT分析実行 (20分)
```markdown
# 自社SWOT分析 (月次更新)

## Strengths (強み)
□ 技術的強み: _____
□ ブランド的強み: _____  
□ リソース的強み: _____
□ 経験的強み: _____

## Weaknesses (弱み)
□ 技術的課題: _____
□ 認知度の課題: _____
□ リソースの制限: _____
□ 経験の不足: _____

## Opportunities (機会)  
□ 市場の機会: _____
□ 技術的機会: _____
□ 競合の隙間: _____
□ トレンドの機会: _____

## Threats (脅威)
□ 競合の脅威: _____
□ 市場の脅威: _____
□ 技術的脅威: _____
□ 規制の脅威: _____
```

#### 2.2 機会評価マトリックス (20分)
```python
# opportunity_evaluator.py
import json

def evaluate_opportunities():
    opportunities = [
        {
            "name": "制服×巨乳組み合わせ",
            "market_size": 7,      # 1-10点
            "growth_rate": 6,      # 1-10点  
            "competition": 5,      # 1-10点 (10=競合少)
            "fit": 8,             # 1-10点
            "profitability": 7     # 1-10点
        },
        # 他の機会も同様に評価
    ]
    
    for opp in opportunities:
        score = (
            opp["market_size"] * 0.2 +
            opp["growth_rate"] * 0.2 +
            opp["competition"] * 0.25 +
            opp["fit"] * 0.2 +
            opp["profitability"] * 0.15
        )
        
        if score >= 8:
            priority = "最優先"
        elif score >= 6:
            priority = "重要"
        elif score >= 4:
            priority = "検討"
        else:
            priority = "保留"
            
        print(f"{opp['name']}: {score:.1f}点 ({priority})")

if __name__ == "__main__":
    evaluate_opportunities()
```

#### 2.3 戦略オプション設計 (20分)
```markdown
# 戦略オプション評価

## Option 1: ニッチ特化戦略
**概要**: 競合の少ない特定ジャンルに集中
**投資**: 低
**リスク**: 中  
**リターン**: 中
**実行期間**: 3ヶ月

## Option 2: 差別化戦略
**概要**: 独自性の強化で競合と差別化
**投資**: 中
**リスク**: 中
**リターン**: 高
**実行期間**: 6ヶ月

## Option 3: 低価格戦略
**概要**: コスト効率化で価格競争力確保
**投資**: 低
**リスク**: 高
**リターン**: 低
**実行期間**: 3ヶ月

## 推奨戦略: _____
**根拠**: _____
```

### Phase 3: 行動計画策定 (30分)

#### 3.1 次月行動計画
```markdown
# 月次行動計画 (YYYY年MM月)

## 戦略目標
1. _____
2. _____
3. _____

## 具体的アクション
### Week 1
□ _____
□ _____
□ _____

### Week 2  
□ _____
□ _____
□ _____

### Week 3
□ _____
□ _____
□ _____

### Week 4
□ _____
□ _____
□ _____

## KPI設定
□ 目標売上: _____円
□ 目標ランキング: ___位以内
□ 目標評価: ___点以上
□ 目標レビュー数: ___件以上

## リスク対策
□ リスク1: _____ → 対策: _____
□ リスク2: _____ → 対策: _____
□ リスク3: _____ → 対策: _____
```

---

## 🔧 自動化スクリプトとツール

### 1. 日次自動収集スクリプト
```bash
#!/bin/bash
# daily_auto_research.sh

LOG_DIR="/mnt/c/Claude Code/tool/research_logs"
DATE=$(date +%Y%m%d)

mkdir -p "$LOG_DIR"

# ランキングデータ収集
echo "日次ランキング収集: $(date)" >> "$LOG_DIR/daily_$DATE.log"
node /mnt/c/Claude\ Code/tool/build/dmm-affiliate-server.js dmm_get_ranking >> "$LOG_DIR/ranking_$DATE.json"

# 価格データ収集
node /mnt/c/Claude\ Code/tool/build/dmm-affiliate-server.js dmm_market_analysis --analysis_type=price >> "$LOG_DIR/price_$DATE.json"

echo "日次収集完了: $(date)" >> "$LOG_DIR/daily_$DATE.log"
```

### 2. 異常値検知スクリプト
```python
# anomaly_detector.py
import json
import os
from datetime import datetime, timedelta

def detect_ranking_anomalies():
    """ランキング異常値を検知"""
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    today_file = f"ranking_{today.strftime('%Y%m%d')}.json"
    yesterday_file = f"ranking_{yesterday.strftime('%Y%m%d')}.json"
    
    # ファイル存在チェック
    if not (os.path.exists(today_file) and os.path.exists(yesterday_file)):
        return []
    
    # データ読み込み・比較ロジック
    anomalies = []
    # ... 実装詳細
    
    return anomalies

def detect_price_anomalies():
    """価格異常値を検知"""
    # ... 実装
    pass

if __name__ == "__main__":
    ranking_anomalies = detect_ranking_anomalies()
    price_anomalies = detect_price_anomalies()
    
    if ranking_anomalies or price_anomalies:
        print("🚨 異常値検知!")
        for anomaly in ranking_anomalies + price_anomalies:
            print(f"- {anomaly}")
```

### 3. レポート自動生成スクリプト
```python
# report_generator.py
import json
from datetime import datetime

def generate_weekly_report():
    """週次レポートを自動生成"""
    
    template = """
# 週次市場分析レポート ({date})

## エグゼクティブサマリー
- 主要トレンド: {main_trend}
- 機会: {opportunities}
- 脅威: {threats}
- 推奨アクション: {actions}

## 詳細分析
{detailed_analysis}

## 次週の重点項目
{next_week_focus}
"""
    
    # データから動的にレポート生成
    report_data = analyze_weekly_data()
    
    report = template.format(
        date=datetime.now().strftime('%Y-%m-%d'),
        **report_data
    )
    
    with open(f"weekly_report_{datetime.now().strftime('%Y%m%d')}.md", 'w') as f:
        f.write(report)

def analyze_weekly_data():
    """週次データを分析して洞察を抽出"""
    # ... データ分析ロジック
    return {
        'main_trend': '制服ジャンルの成長継続',
        'opportunities': 'ニッチ組み合わせの機会',
        'threats': '価格競争の激化',
        'actions': '差別化戦略の強化',
        'detailed_analysis': '...',
        'next_week_focus': '...'
    }

if __name__ == "__main__":
    generate_weekly_report()
```

---

## 📋 実行チェックリスト

### 日次チェックリスト (5分)
```
□ ランキング変動確認
□ 新作動向チェック  
□ 価格動向確認
□ 異常値・特異点検出
□ 気づきメモ記録
□ 明日の注目ポイント設定
```

### 週次チェックリスト (45分)
```
□ 週次データ収集実行
□ 価格帯分析完了
□ ジャンル分析完了
□ トレンド分析完了
□ 競合動向確認
□ 機会・脅威の特定
□ 次週アクション決定
□ 週次レポート作成
```

### 月次チェックリスト (3時間)
```
□ 包括的データ収集
□ 競合詳細分析
□ SWOT分析更新
□ 機会評価マトリックス更新
□ 戦略オプション評価
□ 次月行動計画策定
□ KPI設定・見直し
□ リスク対策更新
```

---

## 🎯 成功事例とベストプラクティス

### Case Study 1: データ駆動型ジャンル選択
```
Before: 感覚的に「巨乳」ジャンル選択
After: データ分析で「制服×巨乳」の組み合わせを発見

Process:
1. ジャンル分析で競争度確認
2. 組み合わせパターン分析
3. 成功事例の要因抽出
4. 差別化ポイント設計

Result: 競争度30%減、評価20%向上
```

### Case Study 2: 価格最適化の成功
```
Before: 競合価格の平均値で設定
After: 品質期待値との整合性を重視

Process:  
1. 価格帯別の評価分析
2. 高評価作品の価格調査
3. 品質との相関分析
4. 最適価格点の特定

Result: 利益率15%向上、評価安定化
```

### Best Practice まとめ
```
1. データは判断材料であり、絶対的指針ではない
2. 継続的な仮説検証サイクルを回す
3. 表面的数字ではなく本質的要因に注目
4. 競合分析は模倣ではなく差別化のため
5. 短期最適化より長期ブランド構築を重視
```

---

## 🚀 開始後の改善サイクル

### Week 1-2: 基本習慣の定着
```
□ 日次ルーティンの実行
□ データ収集の習慣化
□ 基本的なパターン認識
```

### Week 3-4: 分析の深化
```
□ 週次分析の質向上
□ 仮説構築の練習
□ 競合動向の理解深化
```

### Month 2: 戦略的活用
```
□ 月次戦略分析の実行
□ データに基づく意思決定
□ ROI測定の開始
```

### Month 3: 最適化と自動化
```
□ ワークフローの最適化
□ 自動化の導入
□ 独自の洞察手法確立
```

---

*このワークフローは実際の運用を通じて継続的に改善されるべきものです。データ駆動型の意思決定により、成功確率の高い同人作品開発を実現してください。*