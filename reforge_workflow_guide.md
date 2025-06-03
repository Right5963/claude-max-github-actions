# Stability Matrix + Reforge 統合ワークフロー完全ガイド

## 🔥 環境情報
- **ツール**: Stability Matrix + Reforge
- **URL**: http://127.0.0.1:8500
- **API**: http://127.0.0.1:8500/sdapi/v1
- **統合**: 完全自動化パイプライン実装済み

## 🚀 クイックスタート

### 基本生成
```bash
# 環境確認
./reforge_integration_complete.sh check_reforge

# クイック生成
./reforge_integration_complete.sh quick_gen "anime girl, masterpiece"

# ポスター向け生成
./reforge_integration_complete.sh poster_gen "beautiful landscape"
```

### 高品質生成
```bash
# 高品質アニメ
./reforge_integration_complete.sh hq_anime "magical girl"

# 市場向けバッチ
./reforge_integration_complete.sh market_batch "cyberpunk girl"
```

## 🎯 完全自動化ワークフロー

### ワークフロー1: 市場分析→生成
```bash
# 完全自動化
./reforge_integration_complete.sh full_workflow "reference_image.jpg"

# 市場特化
./reforge_integration_complete.sh market_workflow "cyberpunk"
```

**実行内容:**
1. 環境確認 (Reforge稼働チェック)
2. 市場分析 (Civitai/ヤフオクトレンド)
3. プロンプト最適化 (AIパイプライン)
4. Reforge生成 (最適設定)
5. 品質確認 (複数パターン比較)

### ワークフロー2: コンテンツ分析→再現
```bash
# 成功作品分析
./content_creation_pipeline.sh analyze_image "bestseller.jpg"

# プロンプト逆算
./content_creation_pipeline.sh image_to_prompt "bestseller.jpg"

# スタイル再現
./reforge_integration_complete.sh hq_anime "extracted_style, new_character"
```

## 📊 Reforge最適設定

### 用途別設定

#### 1. ヤフオク向けポスター
```json
{
    "width": 1024,
    "height": 768,
    "steps": 28,
    "cfg_scale": 8,
    "sampler_name": "DPM++ 2M SDE Karras"
}
```

#### 2. 同人CG集
```json
{
    "width": 768,
    "height": 1024,
    "steps": 35,
    "cfg_scale": 7.5,
    "sampler_name": "DPM++ 2M Karras"
}
```

#### 3. クイック生成
```json
{
    "width": 768,
    "height": 1024,
    "steps": 20,
    "cfg_scale": 7,
    "sampler_name": "DPM++ 2M Karras"
}
```

## 💰 収益化最適化

### 1. 大量生成戦略
```bash
# バッチ生成で複数パターン
./reforge_integration_complete.sh market_batch "popular_theme"

# サイズバリエーション
for size in "768x1024" "1024x768" "1024x1024"; do
    echo "生成: $size"
done
```

### 2. 品質管理
```bash
# 高品質設定で生成
./reforge_integration_complete.sh hq_anime "premium_prompt"

# 複数モデル比較
./reforge_integration_complete.sh get_models
```

### 3. 市場適応
```bash
# トレンド分析→生成
./specialized_research_bridge.sh civitai_models checkpoint
./reforge_integration_complete.sh market_workflow "trending_style"
```

## 🔧 実用コマンド集

### 日常ルーティン
```bash
#!/bin/bash
# daily_generation.sh

# 1. 環境確認
./reforge_integration_complete.sh check_reforge

# 2. トレンド調査
./specialized_research_bridge.sh civitai_models checkpoint

# 3. 市場分析
./specialized_research_bridge.sh yahoo_auction_ai "人気キーワード"

# 4. 生成実行
./reforge_integration_complete.sh market_batch "今日のトレンド"
```

### 品質重視ワークフロー
```bash
# 1. 参考画像分析
./content_creation_pipeline.sh full_pipeline "reference.jpg"

# 2. 高品質生成
./reforge_integration_complete.sh hq_anime "analyzed_prompt"

# 3. バリエーション展開
./reforge_integration_complete.sh style_batch "base_prompt"
```

## 🎨 生成のコツ

### プロンプトの工夫
1. **基本構造**: `[subject], [style], [quality tags]`
2. **品質タグ**: `masterpiece, best quality, ultra detailed`
3. **スタイル指定**: `anime style`, `realistic`, `oil painting`
4. **ネガティブ**: `lowres, bad anatomy, blurry, worst quality`

### Reforge特有の最適化
1. **CFG Scale**: 7-8が最適
2. **Sampler**: DPM++ 2M Karras推奨
3. **Steps**: 20(速度重視) / 28-35(品質重視)
4. **解像度**: 768x1024 (標準) / 1024x768 (横長)

## 🚀 次のレベルへ

### LoRA活用
- Civitaiから人気LoRAをダウンロード
- 独自スタイルの確立
- 市場ニーズに合わせたカスタマイズ

### 自動化拡張
- 生成結果の自動評価
- 品質スコアによる自動選別
- 販売サイト向け自動リサイズ

### 収益最大化
- A/Bテストによる最適プロンプト発見
- 季節・イベントに合わせた企画
- 独自ブランドの確立

## 結論

Stability Matrix + Reforge + 分析パイプラインで、**最強のAIコンテンツ創作環境**が完成！

- **分析**: 市場・競合・技術トレンド
- **生成**: 高品質・大量・効率的
- **最適化**: 継続的改良・品質向上
- **収益化**: 市場ニーズに最適化

これで「見る→理解する→再現する→超える→稼ぐ」の完全サイクルが実現します！