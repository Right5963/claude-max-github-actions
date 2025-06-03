#!/bin/bash
# 自動化レベル管理
# ================
# 必要に応じて自動化レベルを選択

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 設定ファイル
CONFIG_FILE=".auto_level_config"
LOG_DIR="auto_systems_logs"
mkdir -p "$LOG_DIR"

# 現在のレベルを取得
get_current_level() {
    if [ -f "$CONFIG_FILE" ]; then
        cat "$CONFIG_FILE"
    else
        echo "minimal"
    fi
}

# レベルを設定
set_level() {
    local level=$1
    echo "$level" > "$CONFIG_FILE"
    echo "✅ 自動化レベルを「$level」に設定しました"
}

# システム起動
start_systems() {
    local level=$(get_current_level)
    
    echo "🚀 自動化レベル「$level」で起動中..."
    
    # 常に起動（全レベル）
    ./simple_monitor.sh start
    
    case "$level" in
        balanced)
            # バランスモード
            echo "⚖️ バランスモードで起動"
            
            # ヘルスチェック（1時間ごと、静かに）
            if [ ! -f .health_check.pid ] || ! kill -0 $(cat .health_check.pid 2>/dev/null) 2>&1; then
                (
                    while true; do
                        python3 health_check_auto.py quiet
                        sleep 3600
                    done
                ) > "$LOG_DIR/health_check.log" 2>&1 &
                echo $! > .health_check.pid
                echo "  ✓ ヘルスチェック起動（1時間ごと）"
            fi
            
            # 日次レポート（18:00に生成）
            if [ ! -f .daily_report.pid ] || ! kill -0 $(cat .daily_report.pid 2>/dev/null) 2>&1; then
                (
                    while true; do
                        current_hour=$(date +%H)
                        if [ "$current_hour" = "18" ]; then
                            python3 daily_report_auto.py
                            sleep 3700  # 次の18:00まで待機
                        fi
                        sleep 60
                    done
                ) > "$LOG_DIR/daily_report.log" 2>&1 &
                echo $! > .daily_report.pid
                echo "  ✓ 日次レポート起動（18:00生成）"
            fi
            ;;
            
        full)
            # フル自動化
            echo "🚀 フル自動化モードで起動"
            
            # バランスモードの機能を含む
            $0 balanced > /dev/null 2>&1
            
            # Obsidian同期（15分ごと）
            if [ ! -f .obsidian_sync.pid ] || ! kill -0 $(cat .obsidian_sync.pid 2>/dev/null) 2>&1; then
                nohup python3 obsidian_auto_sync.py daemon > "$LOG_DIR/obsidian_sync.log" 2>&1 &
                echo $! > .obsidian_sync.pid
                echo "  ✓ Obsidian同期起動（15分ごと）"
            fi
            
            # Git自動コミット（30分ごと）
            if [ ! -f .git_auto_commit.pid ] || ! kill -0 $(cat .git_auto_commit.pid 2>/dev/null) 2>&1; then
                nohup python3 smart_git_auto_commit.py daemon > "$LOG_DIR/git_auto_commit.log" 2>&1 &
                echo $! > .git_auto_commit.pid
                echo "  ✓ Git自動コミット起動（30分ごと）"
            fi
            ;;
            
        minimal|*)
            # ミニマルモード（デフォルト）
            echo "📦 ミニマルモードで起動（セッション監視のみ）"
            ;;
    esac
    
    echo ""
    echo "✅ 起動完了"
}

# システム停止
stop_systems() {
    echo "🛑 全自動システムを停止中..."
    
    # 全PIDファイルを処理
    for pid_file in .*.pid; do
        if [ -f "$pid_file" ]; then
            pid=$(cat "$pid_file")
            if kill $pid 2>/dev/null; then
                echo "  ✓ $(basename $pid_file .pid) 停止"
            fi
            rm -f "$pid_file"
        fi
    done
    
    # simple_monitorも停止
    ./simple_monitor.sh stop
    
    echo "✅ 停止完了"
}

# 状態表示
show_status() {
    echo "🤖 自動化システム状態"
    echo "===================="
    echo "現在のレベル: $(get_current_level)"
    echo ""
    
    # 各システムの状態
    echo "📊 稼働中のシステム:"
    
    # セッション監視
    if [ -f .monitor.pid ] && kill -0 $(cat .monitor.pid 2>/dev/null) 2>&1; then
        echo "  ✅ セッション監視 (PID: $(cat .monitor.pid))"
    else
        echo "  ❌ セッション監視"
    fi
    
    # ヘルスチェック
    if [ -f .health_check.pid ] && kill -0 $(cat .health_check.pid 2>/dev/null) 2>&1; then
        echo "  ✅ ヘルスチェック (PID: $(cat .health_check.pid))"
    fi
    
    # 日次レポート
    if [ -f .daily_report.pid ] && kill -0 $(cat .daily_report.pid 2>/dev/null) 2>&1; then
        echo "  ✅ 日次レポート (PID: $(cat .daily_report.pid))"
    fi
    
    # Obsidian同期
    if [ -f .obsidian_sync.pid ] && kill -0 $(cat .obsidian_sync.pid 2>/dev/null) 2>&1; then
        echo "  ✅ Obsidian同期 (PID: $(cat .obsidian_sync.pid))"
    fi
    
    # Git自動コミット
    if [ -f .git_auto_commit.pid ] && kill -0 $(cat .git_auto_commit.pid 2>/dev/null) 2>&1; then
        echo "  ✅ Git自動コミット (PID: $(cat .git_auto_commit.pid))"
    fi
}

# ヘルプ
show_help() {
    cat << EOF
🎛️ 自動化レベル管理システム

使用方法:
  $0 level {minimal|balanced|full}  # レベル設定
  $0 start                          # 現在のレベルで起動
  $0 stop                           # 全停止
  $0 status                         # 状態確認
  $0 help                           # このヘルプ

レベル説明:
  minimal   - セッション監視のみ（デフォルト）
  balanced  - セッション監視 + ヘルスチェック + 日次レポート
  full      - 全機能（Obsidian同期 + Git自動コミット含む）

例:
  $0 level balanced  # バランスモードに設定
  $0 start          # 起動
EOF
}

# メイン処理
case "${1:-}" in
    level)
        if [ -z "$2" ]; then
            echo "現在のレベル: $(get_current_level)"
        else
            case "$2" in
                minimal|balanced|full)
                    set_level "$2"
                    ;;
                *)
                    echo "❌ 無効なレベル: $2"
                    echo "有効なレベル: minimal, balanced, full"
                    ;;
            esac
        fi
        ;;
    start)
        start_systems
        ;;
    stop)
        stop_systems
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_status
        echo ""
        echo "ヘルプ: $0 help"
        ;;
esac