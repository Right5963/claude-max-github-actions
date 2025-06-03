# 🚀 ヤフオクポスター販売 クイックスタートガイド

## 📋 初期設定（初回のみ）

### 1. 作業ディレクトリに移動
```bash
cd "/mnt/c/Claude Code/tool"
```

### 2. 実行権限の付与
```bash
chmod +x daily_workflow_test.sh
chmod +x *.py
```

### 3. 初期データの確認
```bash
python3 system_health_check.py
```

## 🌅 毎朝のルーティン（5分）

### オプション1: 全自動実行
```bash
./daily_workflow_test.sh
```

### オプション2: 手動実行
```bash
# 1. 市場調査
python3 yahoo_auction_simple.py

# 2. 今日のテーマ決定
python3 yahoo_poster_workflow.py "美少女 ファンタジー"

# 3. AI推奨確認
python3 civitai_model_fetcher.py "fantasy anime"
```

## 🎨 画像生成時の設定

### SD最適設定を取得
```bash
python3 sd_intelligent_advisor.py "美少女 ファンタジー"
```

出力される設定をStable Diffusion WebUIにコピペ：
- Model: 推奨されたCheckpoint
- LoRA: 推奨されたLoRA（weight含む）
- Prompt: 生成されたプロンプト
- Settings: width, height, steps, cfg_scale

## 💰 売上記録（出品後）

### 簡易記録
```bash
python3 yahoo_sales_analyzer.py quick "ファンタジー美少女A4" 2800
```

### 詳細記録
```bash
python3 yahoo_sales_analyzer.py record "商品名" 2800 "1girl,fantasy,cute" "Anything V5" "ポスター"
```

## 📊 分析とレポート

### 日次確認
```bash
python3 sales_improvement_core.py dashboard
```

### 週次分析
```bash
# 売上分析レポート
python3 yahoo_sales_analyzer.py analyze

# PDCA評価
python3 llm_pdca_automation.py aicheck

# システム状態
python3 system_health_check.py
```

## 🎯 PDCA実行

### 新しいPDCAサイクル開始
```bash
python3 llm_pdca_automation.py aiplan "価格を2500円に調整" "週売上3万円"
```

### 日次記録
```bash
python3 llm_pdca_automation.py do 2800 "新商品3点出品" "反応良好" "競合少ない"
```

## 💡 便利なコマンド集

### 最新の市場価格を確認
```bash
python3 yahoo_auction_simple.py | grep "平均価格"
```

### 今週の売上合計を確認
```bash
python3 sales_improvement_core.py dashboard | grep "週間"
```

### 競合の必須キーワードを確認
```bash
python3 competitor_analyzer_unified.py | grep "必須キーワード"
```

## ⚠️ トラブルシューティング

### システムが動かない場合
```bash
python3 system_health_check.py
```

### 売上データをリセットしたい場合
```bash
rm yahoo_sales_data.json
rm selling_data.json
```

### ログを確認したい場合
```bash
cat yahoo_research_log.txt | tail -20
```

## 📈 成功のコツ

1. **毎日実行する** - データ蓄積が重要
2. **価格は市場に合わせる** - 自動提案を参考に
3. **人気キーワードを使う** - 分析結果を活用
4. **PDCAを回す** - 週次で必ず評価

---
最終更新: 2025-06-02
バージョン: 1.0