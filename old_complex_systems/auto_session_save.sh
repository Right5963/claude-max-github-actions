#!/bin/bash
# Claude Code セッション自動保存スクリプト
# バックグラウンドで常駐し、セッションを自動保存

cd "/mnt/c/Claude Code/tool"

# 既存のモニタープロセスをチェック
if pgrep -f "session_manager.py monitor" > /dev/null; then
    echo "⚠️ セッション自動保存は既に実行中です"
    exit 1
fi

# バックグラウンドで自動保存開始
echo "🚀 Claude Code セッション自動保存を開始します..."
nohup python3 session_manager.py monitor > session_monitor.log 2>&1 &
PID=$!

echo "✅ 自動保存プロセス開始 (PID: $PID)"
echo "📝 ログファイル: session_monitor.log"
echo ""
echo "停止する場合: kill $PID"

# PIDファイルに保存
echo $PID > .session_monitor.pid