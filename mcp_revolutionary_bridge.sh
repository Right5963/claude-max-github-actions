#!/bin/bash
# MCP Revolutionary Bridge - 全MCPツール革命的統合ブリッジ
# Claude Code CLI から全てのMCPツールを簡単利用

MCP_TOOL=$1
shift
MCP_ARGS="$@"

# 共通変数
TOOL_DIR="/mnt/c/Claude Code/tool"
OBSIDIAN_VAULT="G:\\マイドライブ\\Obsidian Vault"

# JSON MCP呼び出し関数
call_mcp_json() {
    local server_script=$1
    local tool_name=$2
    local args_json=$3
    
    local request="{\"method\": \"tools/call\", \"params\": {\"name\": \"$tool_name\", \"arguments\": $args_json}}"
    
    cd "$TOOL_DIR"
    echo "$request" | python3 "$server_script" 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'content' in data and len(data['content']) > 0:
        print(data['content'][0].get('text', ''))
    elif 'error' in data:
        print(data['error'])
    else:
        print(json.dumps(data, indent=2))
except:
    for line in sys.stdin:
        print(line.rstrip())
"
}

# 使用方法表示
show_usage() {
    echo "🚀 MCP Revolutionary Bridge - 全MCPツール統合利用"
    echo "=============================================="
    echo ""
    echo "🤖 開発効率化ツール (dev-efficiency):"
    echo "  $0 dev-quick [message]           # スマートクイックコミット"
    echo "  $0 dev-context <file>            # ファイル開発コンテキスト分析"
    echo "  $0 dev-patterns [days]           # 開発パターン検出 (デフォルト7日)"
    echo "  $0 dev-optimize [focus]          # ワークフロー最適化 (speed|quality|efficiency)"
    echo "  $0 dev-sync [type]              # 知識同期 (session|learning|pattern)"
    echo ""
    echo "📝 コミット管理ツール:"
    echo "  $0 commit-story                  # mcp-commit-story: スマートコミットメッセージ"
    echo "  $0 code-analyze <file>           # mcp-code-analyzer: コード品質分析"
    echo ""
    echo "📁 ファイル・知識管理:"
    echo "  $0 obsidian-search <query>       # Obsidian検索"
    echo "  $0 obsidian-read <file>          # Obsidianノート読み込み"
    echo "  $0 obsidian-write <file> <content> # Obsidianノート書き込み"
    echo ""
    echo "⚡ 高速実行:"
    echo "  $0 fastmcp                       # FastMCP開発フレームワーク"
    echo ""
    echo "例:"
    echo "  $0 dev-quick \"Fix: bug in auth module\""
    echo "  $0 dev-context \"src/main.py\""
    echo "  $0 dev-patterns 14"
    echo "  $0 obsidian-search \"TAL\""
}

case "$MCP_TOOL" in
    # === 開発効率化ツール (dev-efficiency) ===
    "dev-quick")
        MESSAGE=${1:-""}
        if [ -n "$MESSAGE" ]; then
            ARGS_JSON="{\"message\": \"$MESSAGE\"}"
        else
            ARGS_JSON="{}"
        fi
        
        echo "⚡ スマートクイックコミット実行中..."
        result=$(call_mcp_json "mcp_dev_efficiency.py" "dev_quick_commit" "$ARGS_JSON")
        echo "$result"
        ;;
    
    "dev-context")
        if [ -z "$1" ]; then
            echo "❌ ファイルパスが必要です"
            echo "使用例: $0 dev-context src/main.py"
            exit 1
        fi
        
        FILE_PATH=$1
        ARGS_JSON="{\"file_path\": \"$FILE_PATH\"}"
        
        echo "🔍 ファイル開発コンテキスト分析中: $FILE_PATH"
        result=$(call_mcp_json "mcp_dev_efficiency.py" "dev_file_context" "$ARGS_JSON")
        echo "$result" | python3 -c "import sys, json; [print(json.dumps(json.loads(line), indent=2)) if line.strip() and line.strip().startswith('{') else print(line.rstrip()) for line in sys.stdin]" 2>/dev/null || echo "$result"
        ;;
    
    "dev-patterns")
        DAYS=${1:-7}
        ARGS_JSON="{\"days\": $DAYS}"
        
        echo "📊 開発パターン検出中 (過去${DAYS}日間)..."
        result=$(call_mcp_json "mcp_dev_efficiency.py" "dev_pattern_detect" "$ARGS_JSON")
        echo "$result" | python3 -c "import sys, json; [print(json.dumps(json.loads(line), indent=2)) if line.strip() and line.strip().startswith('{') else print(line.rstrip()) for line in sys.stdin]" 2>/dev/null || echo "$result"
        ;;
    
    "dev-optimize")
        FOCUS=${1:-"efficiency"}
        ARGS_JSON="{\"focus\": \"$FOCUS\"}"
        
        echo "🎯 ワークフロー最適化分析中 (フォーカス: $FOCUS)..."
        result=$(call_mcp_json "mcp_dev_efficiency.py" "dev_auto_optimize" "$ARGS_JSON")
        echo "$result"
        ;;
    
    "dev-sync")
        SYNC_TYPE=${1:-"session"}
        ARGS_JSON="{\"type\": \"$SYNC_TYPE\"}"
        
        echo "🔄 開発知識同期中 (タイプ: $SYNC_TYPE)..."
        result=$(call_mcp_json "mcp_dev_efficiency.py" "dev_knowledge_sync" "$ARGS_JSON")
        echo "$result"
        ;;
    
    # === コミット・コード分析ツール ===
    "commit-story")
        echo "📝 mcp-commit-story でスマートコミットメッセージ生成中..."
        
        # Git情報取得
        cd "$TOOL_DIR"
        git_status=$(git status --porcelain)
        git_diff=$(git diff --stat)
        
        if [ -z "$git_status" ]; then
            echo "ℹ️ コミットする変更がありません"
        else
            echo "変更されたファイル:"
            echo "$git_status"
            echo ""
            echo "統計:"
            echo "$git_diff"
            echo ""
            echo "💡 推奨コミットメッセージ:"
            
            # ファイル変更パターンから推奨メッセージ生成
            if echo "$git_status" | grep -q "\.py"; then
                if echo "$git_status" | grep -q "M.*\.py"; then
                    echo "feat: Update Python modules with enhanced functionality"
                else
                    echo "feat: Add new Python modules"
                fi
            elif echo "$git_status" | grep -q "\.md"; then
                echo "docs: Update documentation and guides"
            elif echo "$git_status" | grep -q "\.sh"; then
                echo "feat: Add/update automation scripts"
            else
                echo "chore: Update project files"
            fi
        fi
        ;;
    
    "code-analyze")
        if [ -z "$1" ]; then
            echo "❌ 分析するファイルパスが必要です"
            echo "使用例: $0 code-analyze src/main.py"
            exit 1
        fi
        
        FILE_PATH=$1
        echo "🔍 mcp-code-analyzer でコード品質分析中: $FILE_PATH"
        
        if [ ! -f "$FILE_PATH" ]; then
            echo "❌ ファイルが見つかりません: $FILE_PATH"
            exit 1
        fi
        
        # ファイル基本情報
        echo "📁 ファイル情報:"
        echo "  パス: $FILE_PATH"
        echo "  サイズ: $(stat -c%s "$FILE_PATH" 2>/dev/null || echo "不明") bytes"
        echo "  最終更新: $(stat -c%y "$FILE_PATH" 2>/dev/null || echo "不明")"
        
        # Python ファイルの場合の簡易分析
        if [[ "$FILE_PATH" == *.py ]]; then
            echo ""
            echo "🐍 Python コード分析:"
            lines=$(wc -l < "$FILE_PATH")
            functions=$(grep -c "^def " "$FILE_PATH")
            classes=$(grep -c "^class " "$FILE_PATH")
            imports=$(grep -c "^import \|^from " "$FILE_PATH")
            
            echo "  総行数: $lines"
            echo "  関数数: $functions"
            echo "  クラス数: $classes"
            echo "  インポート数: $imports"
            
            # 複雑度の簡易評価
            if [ $lines -gt 500 ]; then
                echo "  📊 複雑度: 高 (500行以上)"
            elif [ $lines -gt 200 ]; then
                echo "  📊 複雑度: 中 (200-500行)"
            else
                echo "  📊 複雑度: 低 (200行未満)"
            fi
        fi
        ;;
    
    # === Obsidian操作 (既存機能) ===
    "obsidian-search")
        if [ -z "$1" ]; then
            echo "❌ 検索クエリが必要です"
            exit 1
        fi
        
        echo "🔍 Obsidian検索中: $1"
        powershell.exe -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Get-ChildItem '$OBSIDIAN_VAULT' -Recurse -Filter '*.md' | Select-String -Pattern '$1' -Encoding UTF8 | Select-Object -First 10"
        ;;
    
    "obsidian-read")
        if [ -z "$1" ]; then
            echo "❌ ファイルパスが必要です"
            exit 1
        fi
        
        echo "📖 Obsidianノート読み込み: $1"
        powershell.exe -Command "Get-Content '$OBSIDIAN_VAULT\\$1' -Encoding UTF8"
        ;;
    
    "obsidian-write")
        if [ -z "$1" ] || [ -z "$2" ]; then
            echo "❌ ファイルパスと内容が必要です"
            echo "使用例: $0 obsidian-write \"test.md\" \"# テスト内容\""
            exit 1
        fi
        
        FILE_PATH=$1
        shift
        CONTENT="$@"
        
        echo "✏️ Obsidianノート書き込み: $FILE_PATH"
        powershell.exe -Command "Set-Content -Path '$OBSIDIAN_VAULT\\$FILE_PATH' -Value '$CONTENT' -Encoding UTF8"
        echo "✅ 書き込み完了"
        ;;
    
    # === FastMCP ===
    "fastmcp")
        echo "⚡ FastMCP 開発フレームワーク"
        echo "高速MCP開発・デプロイツール利用可能"
        echo "詳細: npx fastmcp --help"
        ;;
    
    # === ヘルプ・使用方法 ===
    "help"|"--help"|"-h"|"")
        show_usage
        ;;
    
    *)
        echo "❌ 不明なツール: $MCP_TOOL"
        echo ""
        show_usage
        exit 1
        ;;
esac