# 🧹 システム大掃除2.0 実行プラン

## 🚨 緊急事態: システム再爆発

### 原因分析
- **2025-06-03**: 87→48システムに大掃除完了
- **2025-06-04**: 93システムに再増殖（45個増加）
- **主犯**: 自動生成・一時ファイル・重複レポート

## 🎯 削除対象（推定60-70個）

### 即座削除（安全確認済み）
```bash
# 1. 重複日付ファイル群（50+個）
rm *20250602_* *20250603_*
rm popularity_research_report_*.md
rm value_cycle_reproduction_guide_*.md
rm download_*.bat download_*.ps1

# 2. テスト・一時ファイル（15+個）
rm test_*.md *_test.* 
rm wildcard_*.txt
rm yahoo_obsidian_result_*.txt

# 3. 重複システム（10+個）
rm yahoo_auto_*.txt
rm obsidian_wildcard__*.txt
```

### 保持すべき価値システム（30個以下）

#### 絶対保持（10個）
1. `mcp_bridge_extended.sh` - MCP統合
2. `git_quick_insight.py` - 開発分析
3. `smart_git_auto_commit.py` - 自動知識化
4. `auto_research_system.py` - 自動リサーチ
5. `instant_research_ai.py` - 瞬間リサーチ
6. `development_review_system.py` - レビュー
7. `session_manager_simple.py` - セッション管理
8. `start.py` - 新セッション開始
9. `git_god_tool.py` - TAL思考Git
10. `mcp_auto_manager.py` - MCP管理

#### 検証保持（15個）
- `civitai_analyzer.py` - 市場分析
- `sales_improvement_core.py` - 売上改善
- `poster_prompt_generator.py` - プロンプト生成
- `wildcard_generator_unified.py` - ワイルドカード
- `content_creation_pipeline.sh` - 創作パイプライン
- その他価値検証済みシステム

#### 条件保持（5個）
- 設定・管理用スクリプト
- 必要最小限のユーティリティ

## ⚡ 実行手順

### Phase 1: 緊急削除（5分）
```bash
# 一時・重複ファイル完全削除
find . -name "*20250602*" -delete
find . -name "*20250603*" -delete  
find . -name "test_*" -delete
find . -name "*_test.*" -delete
```

### Phase 2: システム精査（10分）
```bash
# 価値システムのみ残存確認
ls *.py | wc -l  # 目標: 25個以下
ls *.sh | wc -l  # 目標: 15個以下
```

### Phase 3: 自動生成停止（5分）
```bash
# 自動保存プロセス確認・停止
ps aux | grep auto
# 重複生成システムの無効化
```

## 🎯 目標結果

**Before**: 93システム（混沌・重複・一時ファイル）
**After**: 30システム以下（価値・実用・継続性）

**削除率**: 67%以上（90→30）

## 🔒 再発防止策

### 1. 自動生成制御
- 一時ファイルは `/tmp/` 配下に生成
- 日付付きファイルは最新1個のみ保持
- 自動削除機能を全システムに追加

### 2. システム品質管理
- 新システム作成時の価値評価必須
- 1週間使用されないシステムは自動削除候補
- Simple First原則の強制適用

### 3. 定期メンテナンス  
- 週次システム数チェック
- 月次価値評価・削除
- Obsidian統合による知識継続性確保

**結論**: 今すぐ大掃除2.0を実行し、30システム以下の健全な環境を復元する