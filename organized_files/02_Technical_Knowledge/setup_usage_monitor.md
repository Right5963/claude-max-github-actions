# Claude Usage Stats Setup Guide
Cursor Usage Stats風のClaude使用量リアルタイム表示システム

## 🚀 実装完了機能

### 1. 使用量追跡システム
- **SQLiteデータベース**による使用履歴記録
- **5時間セッション**管理（Claude Max制限に対応）
- **モデル別使用量**追跡（Opus/Sonnet）
- **リアルタイム使用率**計算

### 2. コマンドラインインターフェース
```bash
# 現在の使用統計表示
./claude_wrapper.sh stats

# スマート使用量管理（自動モデル選択）
./claude_wrapper.sh smart "Write a Python function"

# 使用量追跡付きClaude実行
./claude_wrapper.sh track --model sonnet "Hello world"

# セッションリセット（新5時間開始）
./claude_wrapper.sh reset

# バックグラウンド監視開始/停止
./claude_wrapper.sh monitor-start
./claude_wrapper.sh monitor-stop
```

### 3. 表示例
```
============================================================
🎯 CLAUDE CODE USAGE STATS
============================================================
📅 Session: 20250601_10 (Started: 10:17)
⏰ Time Remaining: 4:59:59
------------------------------------------------------------
OPUS     |   0/200 (  0.0%) | 🟢 SAFE | 🔤 0 tokens
SONNET   |   0/300 (  0.0%) | 🟢 SAFE | 🔤 0 tokens
============================================================
```

### 4. 自動制限管理
- **70%到達**: 警告表示
- **80%到達**: モデル切り替え推奨  
- **90%到達**: 無料システム自動切り替え
- **95%到達**: Claude使用停止

## 📊 VSCode拡張（開発中）

### ステータスバー表示
- **リアルタイム使用量**: `$(check) Claude: O15/200 S8/300 ⏱️4:30:15`
- **色分け**: 緑(安全) → 黄(注意) → 橙(警告) → 赤(危険)
- **詳細表示**: クリックで詳細ウィンドウ

### VSCode拡張インストール方法
```bash
# 将来実装予定
code --install-extension claude-usage-stats.vsix
```

## 🎯 使用例

### 基本的な使用フロー
```bash
# 1. 使用量確認
./claude_wrapper.sh stats

# 2. スマート実行（使用量に応じて最適モデル選択）
./claude_wrapper.sh smart "Add error handling to this function"

# 3. 使用量再確認
./claude_wrapper.sh stats
```

### 制限管理フロー
```bash
# Opus使用量が高い場合の自動切り替え
./claude_wrapper.sh smart "Simple task"
# → 自動的にSonnetまたは無料システムを選択
```

## ⚙️ 設定・カスタマイズ

### 制限値調整
`claude_usage_tracker.py`内で調整可能：
```python
# 各モデルの推定制限値
max_requests = 200 if model == 'opus' else 300
```

### 警告レベル調整
`claude_wrapper.sh`内で調整可能：
```bash
# 警告レベル（80%, 90%）
if (( $(echo "$opus_usage < 70" | bc -l) )); then
```

## 🎯 期待効果

### コスト管理
- **制限超過防止**: 自動監視で$100超過リスクゼロ
- **使用量最適化**: モデル別制限を最大活用
- **可視化**: 使用パターンの把握・改善

### 生産性向上
- **自動選択**: 最適モデルの自動判定
- **継続性**: 制限到達時の自動フォールバック
- **効率化**: 使用量を意識した作業計画

### 監視・分析
- **履歴追跡**: 使用パターンの長期分析
- **セッション管理**: 5時間サイクルの最適活用
- **アラート**: 制限近接時の自動警告

この**Claude Usage Stats**システムにより、Cursor Usage Stats同様の常時可視化と、制限管理の自動化を実現しました！