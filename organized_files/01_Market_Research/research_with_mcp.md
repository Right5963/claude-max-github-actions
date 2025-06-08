# MCPを活用したリサーチ手法

## 1. Playwright活用例

### 技術調査
```bash
# 最新のAI技術トレンドを調査
./mcp_bridge_extended.sh browser_open "https://arxiv.org/list/cs.AI/recent"
./mcp_bridge_extended.sh browser_screenshot "https://papers.nips.cc/"

# GitHubのトレンドプロジェクト調査
./mcp_bridge_extended.sh browser_open "https://github.com/trending/python?since=weekly"
```

### 競合分析
```bash
# 競合サービスの機能調査
./mcp_bridge_extended.sh browser_screenshot "https://cursor.sh/features"
./mcp_bridge_extended.sh browser_screenshot "https://www.tabnine.com/"
```

## 2. note-api活用例

### 技術記事検索
```bash
# TAL関連の記事を検索
mcp_note-api__search-notes "TAL プロンプトエンジニアリング"
mcp_note-api__search-notes "Claude API 活用"

# 人気の技術記事を分析
mcp_note-api__analyze-notes "AI 開発" --sort popular --size 20
```

### トレンド分析
```bash
# 急上昇中の技術トピック
mcp_note-api__search-notes "LLM" --sort hot
mcp_note-api__search-notes "RAG" --sort hot
```

## 3. 組み合わせリサーチ

### 包括的な技術調査フロー
1. **note-apiで記事検索** → 日本語の実践的な知見
2. **Playwrightでarxiv/GitHub調査** → 最新の研究・実装
3. **Obsidianに知見を集約** → 知識の体系化
4. **メモリ管理で重要情報を保存** → セッション間での継続

## 実装例：AI技術トレンド調査

```python
# 1. noteで日本語記事を収集
note_results = mcp_note-api__search-notes("生成AI 2025")

# 2. 海外の最新動向を調査
playwright_navigate("https://huggingface.co/papers")
playwright_screenshot("trending_papers.png")

# 3. 調査結果をObsidianに記録
obsidian_content = f"""# AI技術トレンド調査 {datetime.now()}

## 日本の動向（note.com）
{format_note_results(note_results)}

## 世界の動向（HuggingFace/arXiv）
![トレンド論文](trending_papers.png)

## 重要な発見
- ...
"""
mcp_obsidian__create_note("Research/AI_Trends_2025.md", obsidian_content)

# 4. 重要情報をメモリに保存
mcp_memory__store("ai_trends_2025", key_findings)
```

## なぜ使われていなかったか

1. **MCPブリッジの実装不足**
   - note-api用のブリッジコマンドが未実装
   - Playwright用の高度な操作が未実装

2. **リサーチワークフローの未確立**
   - MCPツールを組み合わせた調査手法が未定義
   - 自動化スクリプトの不在

## 今後の改善案

1. **MCPブリッジ拡張**
```bash
# note-api用コマンド追加
note_search [query]        # note記事検索
note_analyze [query]       # 記事分析
note_trending             # トレンド取得

# Playwright高度な操作
browser_login [site]      # ログイン自動化
browser_extract [selector] # データ抽出
browser_monitor [url]     # 定期監視
```

2. **リサーチ自動化スクリプト**
```bash
./research_assistant.sh "AI技術トレンド"
# → note検索 + Web調査 + Obsidian記録を自動実行
```

これらのツールを活用すれば、リサーチ効率が大幅に向上します！