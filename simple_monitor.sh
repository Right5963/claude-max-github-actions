#!/bin/bash
# シンプルセッション監視
# ===================
# セッション監視のみ実行（Simple First原則）

cd "$(dirname "$0")"

case "${1:-}" in
    start)
        # 既に実行中かチェック
        if [ -f .monitor.pid ] && kill -0 $(cat .monitor.pid) 2>/dev/null; then
            echo "✅ 既に実行中です"
            exit 0
        fi
        
        # バックグラウンドで開始
        echo "🚀 セッション監視を開始..."
        nohup python3 session_auto_monitor.py start > monitor.log 2>&1 &
        echo $! > .monitor.pid
        sleep 2
        
        if kill -0 $(cat .monitor.pid) 2>/dev/null; then
            echo "✅ 監視開始 (PID: $(cat .monitor.pid))"
        else
            echo "❌ 起動失敗"
            rm -f .monitor.pid
        fi
        ;;
        
    stop)
        if [ -f .monitor.pid ]; then
            kill $(cat .monitor.pid) 2>/dev/null
            rm -f .monitor.pid
            echo "⏹️ 監視停止"
        else
            echo "監視は実行されていません"
        fi
        ;;
        
    status)
        if [ -f .monitor.pid ] && kill -0 $(cat .monitor.pid) 2>/dev/null; then
            echo "✅ 監視実行中 (PID: $(cat .monitor.pid))"
            echo ""
            echo "最新のログ:"
            tail -5 session_monitor.log 2>/dev/null || echo "ログなし"
        else
            echo "❌ 監視停止中"
            rm -f .monitor.pid 2>/dev/null
        fi
        ;;
        
    *)
        echo "使用方法: $0 {start|stop|status}"
        $0 status
        ;;
esac