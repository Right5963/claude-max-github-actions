# 自動監視付きセッション管理システム

## 概要
session_manager_simple.pyをベースに、5分ごとの自動保存機能を追加した監視システムです。

## 構成ファイル
- `session_auto_monitor.py` - 自動監視デーモン
- `session_monitor_launcher.sh` - 起動/停止/状態確認スクリプト
- `claude_quick_launch.bat` - Claude Code起動時に自動で監視開始（更新済み）

## 使い方

### 1. 手動で監視を開始/停止
```bash
# 監視開始（バックグラウンド実行）
./session_monitor_launcher.sh start

# 監視停止
./session_monitor_launcher.sh stop

# 状態確認
./session_monitor_launcher.sh status

# ログ確認
./session_monitor_launcher.sh log
```

### 2. Claude Code起動時に自動開始
`claude_quick_launch.bat`を実行すると自動的に監視が開始されます。

## 機能
- 5分ごとに自動保存
- セッションファイルのバックアップ（sessions/フォルダ）
- 活動記録の自動追加
- プロセス監視とPID管理
- 詳細なログ記録

## ログファイル
- `session_monitor.log` - 監視ログ
- `session_monitor_daemon.log` - デーモンプロセスログ

## 現在の状態
✅ 監視プロセス実行中 (PID: 1588)
✅ 自動保存動作確認済み
✅ Claude Code起動時の自動開始設定済み