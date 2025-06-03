#!/bin/bash
# セッション監視起動スクリプト
# =========================
# バックグラウンドで監視プロセスを起動

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# ログファイル
LOG_FILE="session_monitor_daemon.log"

# 監視ステータス確認関数
check_status() {
    python3 session_auto_monitor.py status
}

# 監視開始関数
start_monitor() {
    echo "🚀 セッション監視を開始します..."
    
    # 既存のプロセスチェック
    if [ -f .session_monitor.pid ]; then
        PID=$(cat .session_monitor.pid)
        if ps -p $PID > /dev/null 2>&1; then
            echo "⚠️ 監視プロセスは既に実行中です (PID: $PID)"
            check_status
            return 1
        else
            echo "古いPIDファイルを削除します"
            rm -f .session_monitor.pid
        fi
    fi
    
    # バックグラウンドで起動
    nohup python3 session_auto_monitor.py start > "$LOG_FILE" 2>&1 &
    NEW_PID=$!
    
    # 起動確認（3秒待機）
    sleep 3
    
    if ps -p $NEW_PID > /dev/null 2>&1; then
        echo "✅ 監視プロセスをバックグラウンドで起動しました (PID: $NEW_PID)"
        echo ""
        check_status
    else
        echo "❌ 監視プロセスの起動に失敗しました"
        echo "ログを確認してください: $LOG_FILE"
        tail -10 "$LOG_FILE"
        return 1
    fi
}

# 監視停止関数
stop_monitor() {
    echo "🛑 セッション監視を停止します..."
    python3 session_auto_monitor.py stop
}

# メイン処理
case "${1:-}" in
    start)
        start_monitor
        ;;
    stop)
        stop_monitor
        ;;
    restart)
        stop_monitor
        sleep 2
        start_monitor
        ;;
    status)
        check_status
        ;;
    log)
        if [ -f "$LOG_FILE" ]; then
            echo "📋 監視ログ ($LOG_FILE):"
            tail -20 "$LOG_FILE"
        else
            echo "ログファイルが見つかりません"
        fi
        ;;
    *)
        echo "🤖 セッション監視ランチャー"
        echo ""
        echo "使用方法:"
        echo "  $0 start    # 監視開始（バックグラウンド）"
        echo "  $0 stop     # 監視停止"
        echo "  $0 restart  # 監視再起動"
        echo "  $0 status   # 状態確認"
        echo "  $0 log      # ログ表示"
        echo ""
        echo "現在の状態:"
        check_status
        ;;
esac