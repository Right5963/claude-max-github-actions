# 自動化システム統合環境

## 概要
Claude Code起動時に自動的に全ての監視・自動化システムが起動する統合環境です。

## 実装済み自動化システム

### 1. セッション監視 (session_monitor)
- **機能**: Claude Codeのセッションを5分ごとに自動保存
- **バックアップ**: sessions/フォルダに履歴保存
- **起動**: 自動

### 2. Git自動コミット (git_auto)
- **機能**: 10分ごとに変更を検出して自動コミット
- **対象**: /mnt/c/Claude Code/toolディレクトリ
- **除外**: ログファイル、PIDファイルなど
- **起動**: 自動（プッシュは手動）

### 3. Obsidian同期 (obsidian_sync)
- **機能**: 15分ごとにObsidian Vaultと同期
- **内容**: セッション情報、日次サマリーを自動作成
- **バックアップ**: obsidian-cache/に保存
- **起動**: 自動

### 4. ヘルスチェック (health_check)
- **機能**: 1時間ごとにシステム診断
- **項目**: ディスク、メモリ、プロセス、Git状態など
- **自動修復**: 一部の問題は自動修復
- **起動**: 自動

### 5. 日次レポート (daily_report)
- **機能**: 毎日23:55に日次レポート生成
- **内容**: 活動、コミット、ファイル変更、生産性分析
- **保存先**: daily_reports/とObsidian
- **起動**: 自動

## 使い方

### Claude起動時（自動）
```bash
# WSLで通常通りclaudeコマンドを実行
claude

# 自動的に：
# 1. 全自動システムの状態確認
# 2. 未起動システムの自動起動
# 3. セッション情報表示
# 4. Claude起動
```

### 手動管理
```bash
# 全システムの状態確認
./auto_systems_launcher.sh status

# 全システム起動
./auto_systems_launcher.sh start

# 全システム停止
./auto_systems_launcher.sh stop

# 全システム再起動
./auto_systems_launcher.sh restart

# 特定システムのログ確認
./auto_systems_launcher.sh log session_monitor
./auto_systems_launcher.sh log git_auto
./auto_systems_launcher.sh log obsidian_sync
./auto_systems_launcher.sh log health_check
./auto_systems_launcher.sh log daily_report
```

## ディレクトリ構造
```
/mnt/c/Claude Code/tool/
├── auto_systems_logs/      # 各システムのログ
├── .auto_pids/            # PIDファイル
├── sessions/              # セッションバックアップ
├── obsidian-cache/        # Obsidianバックアップ
├── daily_reports/         # 日次レポート
└── system_health_report.json  # 最新のヘルスレポート
```

## トラブルシューティング

### システムが起動しない
```bash
# ログを確認
./auto_systems_launcher.sh log [システム名]

# 手動で個別起動を試す
python3 [スクリプト名].py
```

### 全システムリセット
```bash
# 全システム停止
./auto_systems_launcher.sh stop

# PIDファイルをクリア
rm -f .auto_pids/*.pid

# 再起動
./auto_systems_launcher.sh start
```

## 拡張方法

新しい自動化システムを追加するには：

1. スクリプトを作成（daemonモード対応）
2. auto_systems_launcher.shのSYSTEMSに追加
3. テスト実行

## 現在の状態
✅ 全ての自動化システムが統合完了
✅ Claude起動時の自動起動設定済み
✅ 統合管理スクリプト完成