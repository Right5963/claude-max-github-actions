# Perplexity MCP × Claude 瞬間リサーチAI クイックスタート

## 🚀 セットアップ (1分で完了)

```bash
# 1. セットアップ実行
./setup_perplexity_mcp.sh

# 2. API キー設定 (必須)
export PERPLEXITY_API_KEY=your_actual_api_key

# 3. 接続テスト
python3 instant_research_ai.py test
```

## ⚡ 使用例

### 瞬間検索 (数秒で回答)
```bash
# 最新技術動向
python3 instant_research_ai.py instant "Claude MCP 最新機能"

# 市場分析
python3 instant_research_ai.py instant "AI art市場 2024年動向"

# 技術質問
python3 instant_research_ai.py instant "Stable Diffusion XL 最適設定"
```

### 深層リサーチ (構造化レポート)
```bash
# 技術詳細分析
python3 instant_research_ai.py deep "Perplexity API"

# 市場調査
python3 instant_research_ai.py deep "生成AI 商用利用"

# 競合分析
python3 instant_research_ai.py deep "Claude vs ChatGPT"
```

### 包括的リサーチセッション (5つの観点)
```bash
# 新技術の完全調査
python3 instant_research_ai.py session "MCP プロトコル"

# ビジネス分析
python3 instant_research_ai.py session "AI副業"

# トレンド分析
python3 instant_research_ai.py session "2024年 AI画像生成"
```

### 履歴管理
```bash
# 履歴確認
python3 instant_research_ai.py history

# ショートカット使用
./research.sh history
```

## 🔧 ショートカット利用

```bash
# セットアップ後に作成される便利なショートカット
./research.sh instant "検索クエリ"
./research.sh deep "深層テーマ"
./research.sh session "包括テーマ"
./research.sh test
./research.sh history
```

## 📁 自動保存

- **Obsidian**: `G:\マイドライブ\Obsidian Vault\Research\AI_Generated\`
- **履歴DB**: `research_history.db` (SQLite)
- **設定**: `research_config.json`

## 💰 API使用量目安

- **瞬間検索**: ~500トークン
- **深層リサーチ**: ~2000トークン  
- **包括セッション**: ~8000トークン (5つの観点)

## 🎯 実際の活用例

### 1. 技術調査
```bash
# 新技術の基本理解
./research.sh instant "WebAssembly 用途"

# 実装方法の詳細
./research.sh deep "WebAssembly Python 統合"

# 完全な技術評価
./research.sh session "WebAssembly vs JavaScript"
```

### 2. 市場分析
```bash
# 市場規模確認
./research.sh instant "NFT市場 2024"

# 詳細な市場分析
./research.sh deep "NFT マーケットプレイス 比較"

# 包括的事業分析
./research.sh session "NFT 事業機会"
```

### 3. 学習・研究
```bash
# 概念理解
./research.sh instant "量子コンピュータ 基本"

# 技術詳細
./research.sh deep "量子優位性 実例"

# 分野全体の理解
./research.sh session "量子コンピュータ 産業応用"
```

## 🔄 Obsidian 連携効果

- 自動的にMarkdown形式で保存
- タグ付けによる分類
- 関連ファイルリンク
- 検索・参照の容易性
- 知識の蓄積と再利用

## 🚨 注意事項

- API使用量に応じて課金されます
- 個人情報や機密情報の検索は避けてください
- 結果の事実確認は適切に行ってください
- APIキーは安全に管理してください

## 🎉 期待される効果

- **情報収集時間**: 90%短縮
- **調査品質**: AI専門性による向上
- **知識管理**: Obsidianでの体系化
- **作業効率**: ワンコマンドでの包括調査

Simple First原則: 外部は1コマンド、内部は高機能AIリサーチエンジン