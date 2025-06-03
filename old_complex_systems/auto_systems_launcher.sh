#!/bin/bash
# 統合自動システム起動スクリプト
# ================================
# 全ての自動化システムを一括管理

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# ログディレクトリ
LOG_DIR="auto_systems_logs"
mkdir -p "$LOG_DIR"

# PIDファイル
PID_DIR=".auto_pids"
mkdir -p "$PID_DIR"

# 色付き出力
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# システムリスト
declare -A SYSTEMS=(
    ["session_monitor"]="セッション監視|./session_monitor_launcher.sh start|5分ごと自動保存"
    ["git_auto"]="Git自動コミット|python3 git_auto_commit.py daemon|10分ごと変更検出"
    ["obsidian_sync"]="Obsidian同期|python3 obsidian_auto_sync.py daemon|15分ごと同期"
    ["health_check"]="ヘルスチェック|python3 health_check_auto.py daemon|1時間ごと診断"
    ["daily_report"]="日次レポート|python3 daily_report_auto.py daemon|23:55に生成"
)

# 関数: システム状態チェック
check_system_status() {
    local system=$1
    local pid_file="$PID_DIR/${system}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo "running"
            return 0
        fi
    fi
    echo "stopped"
    return 1
}

# 関数: システム起動
start_system() {
    local system=$1
    local info="${SYSTEMS[$system]}"
    IFS='|' read -r name command description <<< "$info"
    
    echo -e "${GREEN}[起動]${NC} $name - $description"
    
    # 既に起動している場合はスキップ
    if [ "$(check_system_status $system)" = "running" ]; then
        echo -e "${YELLOW}  → 既に起動中${NC}"
        return 0
    fi
    
    # バックグラウンドで起動
    nohup $command > "$LOG_DIR/${system}.log" 2>&1 &
    local pid=$!
    echo $pid > "$PID_DIR/${system}.pid"
    
    # 起動確認
    sleep 2
    if ps -p $pid > /dev/null 2>&1; then
        echo -e "${GREEN}  ✓ 起動成功 (PID: $pid)${NC}"
    else
        echo -e "${RED}  ✗ 起動失敗${NC}"
        rm -f "$PID_DIR/${system}.pid"
        return 1
    fi
}

# 関数: システム停止
stop_system() {
    local system=$1
    local info="${SYSTEMS[$system]}"
    IFS='|' read -r name command description <<< "$info"
    
    echo -e "${RED}[停止]${NC} $name"
    
    local pid_file="$PID_DIR/${system}.pid"
    if [ ! -f "$pid_file" ]; then
        echo -e "${YELLOW}  → 起動していません${NC}"
        return 0
    fi
    
    local pid=$(cat "$pid_file")
    
    # 特殊処理: session_monitorは専用コマンドで停止
    if [ "$system" = "session_monitor" ]; then
        ./session_monitor_launcher.sh stop
    else
        kill $pid 2>/dev/null
    fi
    
    rm -f "$pid_file"
    echo -e "${GREEN}  ✓ 停止完了${NC}"
}

# 関数: 全システムの状態表示
show_status() {
    echo "🤖 自動システム状態"
    echo "===================="
    
    for system in "${!SYSTEMS[@]}"; do
        local info="${SYSTEMS[$system]}"
        IFS='|' read -r name command description <<< "$info"
        
        local status=$(check_system_status $system)
        if [ "$status" = "running" ]; then
            local pid=$(cat "$PID_DIR/${system}.pid")
            echo -e "${GREEN}✅${NC} $name (PID: $pid) - $description"
        else
            echo -e "${RED}❌${NC} $name - 停止中"
        fi
    done
    
    echo ""
    echo "ログファイル: $LOG_DIR/"
}

# 関数: 全システム起動
start_all() {
    echo "🚀 全自動システムを起動中..."
    echo ""
    
    # 優先順位順に起動
    start_system "session_monitor"
    start_system "health_check"
    start_system "obsidian_sync"
    start_system "git_auto"
    start_system "daily_report"
    
    echo ""
    echo "✅ 起動処理完了"
    echo ""
    show_status
}

# 関数: 全システム停止
stop_all() {
    echo "🛑 全自動システムを停止中..."
    echo ""
    
    for system in "${!SYSTEMS[@]}"; do
        stop_system $system
    done
    
    echo ""
    echo "✅ 停止処理完了"
}

# 関数: ログ表示
show_logs() {
    local system=$1
    
    if [ -z "$system" ]; then
        echo "利用可能なシステム:"
        for s in "${!SYSTEMS[@]}"; do
            echo "  - $s"
        done
        return
    fi
    
    local log_file="$LOG_DIR/${system}.log"
    if [ -f "$log_file" ]; then
        echo "📋 $system のログ (最新20行):"
        tail -20 "$log_file"
    else
        echo "❌ ログファイルが見つかりません: $log_file"
    fi
}

# メイン処理
case "${1:-}" in
    start)
        start_all
        ;;
    stop)
        stop_all
        ;;
    restart)
        stop_all
        sleep 3
        start_all
        ;;
    status)
        show_status
        ;;
    log)
        show_logs "${2:-}"
        ;;
    help|--help|-h)
        echo "🤖 統合自動システムランチャー"
        echo ""
        echo "使用方法:"
        echo "  $0 start    # 全システム起動"
        echo "  $0 stop     # 全システム停止"
        echo "  $0 restart  # 全システム再起動"
        echo "  $0 status   # 状態確認"
        echo "  $0 log [システム名] # ログ表示"
        echo ""
        echo "自動化システム一覧:"
        for system in "${!SYSTEMS[@]}"; do
            local info="${SYSTEMS[$system]}"
            IFS='|' read -r name command description <<< "$info"
            echo "  - $system: $name ($description)"
        done
        ;;
    *)
        # 引数なしの場合は状態表示
        show_status
        echo "ヘルプ: $0 help"
        ;;
esac