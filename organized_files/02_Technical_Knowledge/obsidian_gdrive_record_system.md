# 🏦 Gドライブ Obsidian 記録システム

## 🎯 真の知識基盤への統合

### Obsidian Vault 場所
- **Gドライブ**: `G:\マイドライブ\Obsidian Vault`
- **アクセス方法**: PowerShell経由、MCPブリッジ経由

## 📝 常時記録：Obsidianへの統合

### 1. セッション記録の自動保存
```bash
# PowerShell経由でObsidianに記録
powershell.exe -Command "Add-Content -Path 'G:\\マイドライブ\\Obsidian Vault\\Daily Notes\\$(Get-Date -Format 'yyyy-MM-dd').md' -Value '## Claude Code セッション記録' -Encoding UTF8"

# 学習内容をObsidianに追加
powershell.exe -Command "Add-Content -Path 'G:\\マイドライブ\\Obsidian Vault\\Learning\\Claude_Sessions\\$(Get-Date -Format 'yyyy-MM-dd')_learnings.md' -Value '[学習内容]' -Encoding UTF8"
```

### 2. MCPブリッジ経由の記録
```bash
# Obsidianに直接記録
./mcp_bridge_extended.sh obsidian_write "Learning/Claude_Sessions/$(date +%Y%m%d)_session.md" "## 今日の学習..."
./mcp_bridge_extended.sh obsidian_write "Failures/$(date +%Y%m%d)_failures.md" "## 今日の失敗..."
./mcp_bridge_extended.sh obsidian_write "Successes/$(date +%Y%m%d)_successes.md" "## 今日の成功..."
```

## 🔍 常時活用：Obsidianからの知識取得

### 1. セッション開始時の必須確認
```bash
# Obsidianから過去の失敗・成功パターンを確認
./mcp_bridge_extended.sh obsidian_search "Simple First"
./mcp_bridge_extended.sh obsidian_search "記録は宝"
./mcp_bridge_extended.sh obsidian_search "失敗パターン"
```

### 2. 類似問題の検索
```bash
# 問題発生時にObsidianで過去事例検索
./mcp_bridge_extended.sh obsidian_search "[今回の問題キーワード]"
powershell.exe -Command "Select-String -Path 'G:\\マイドライブ\\Obsidian Vault\\**\\*.md' -Pattern '[問題キーワード]' | Select-Object -First 5"
```

### 3. 知識の体系的活用
```bash
# Obsidianの構造化知識を活用
./mcp_bridge_extended.sh obsidian_read "Core_Knowledge/開発原則.md"
./mcp_bridge_extended.sh obsidian_read "Templates/問題解決テンプレート.md"
```

## 🔄 統合ワークフロー

### セッション開始
1. Obsidianから過去記録確認
2. 類似問題・解決策検索
3. 今日の記録ファイル準備

### セッション中
1. リアルタイムでObsidianに記録
2. 問題発生時は即座にObsidian検索
3. 解決策もObsidianに蓄積

### セッション終了
1. 今日の学習をObsidianに整理
2. 既存知識との関連付け
3. 次回アクセス用のタグ・リンク設定

## 🎯 即座実行テスト

### 今すぐObsidianアクセス確認
```bash
# Gドライブアクセステスト
powershell.exe -Command "Test-Path 'G:\\マイドライブ\\Obsidian Vault'" 
./mcp_bridge_extended.sh obsidian_search "TAL"
```

**意味**: ローカル記録は一時的、Obsidianが永続的知識基盤
**目的**: セッション間での知識継承、体系的知識管理
**効果**: 真の「記録は宝」システムの実現