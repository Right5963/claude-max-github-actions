#!/bin/bash
# Perplexity MCP Setup - 瞬間リサーチAI環境構築
# Simple First: 1コマンドで完全セットアップ

echo "🚀 Perplexity MCP × Claude 瞬間リサーチAI セットアップ"
echo "=" * 60

# 1. API キー確認
if [ -z "$PERPLEXITY_API_KEY" ]; then
    echo "⚠️ PERPLEXITY_API_KEY が設定されていません"
    echo ""
    echo "📝 設定方法:"
    echo "1. Perplexity AI アカウント作成: https://www.perplexity.ai/"
    echo "2. API キー取得: https://www.perplexity.ai/settings/api"
    echo "3. 環境変数設定:"
    echo "   export PERPLEXITY_API_KEY=your_actual_api_key"
    echo ""
    echo "🔧 一時的な設定 (現在のセッションのみ):"
    read -p "API キーを入力してください: " temp_api_key
    if [ -n "$temp_api_key" ]; then
        export PERPLEXITY_API_KEY="$temp_api_key"
        echo "✅ API キーを一時設定しました"
    else
        echo "❌ API キーが必要です。セットアップを終了します。"
        exit 1
    fi
else
    echo "✅ PERPLEXITY_API_KEY 設定確認済み"
fi

# 2. 必要なPythonパッケージインストール
echo ""
echo "📦 必要なパッケージをインストール中..."

python3 -c "import requests" 2>/dev/null || {
    echo "🔧 requests パッケージをインストール中..."
    pip3 install requests --user
}

python3 -c "import sqlite3" 2>/dev/null || {
    echo "⚠️ sqlite3 が利用できません（通常はPython標準）"
}

echo "✅ パッケージ確認完了"

# 3. ディレクトリ構造作成
echo ""
echo "📁 ディレクトリ構造を作成中..."

# ローカルディレクトリ
mkdir -p research_results
mkdir -p research_cache

# Obsidian ディレクトリ (PowerShell経由)
powershell.exe -Command "
\$obsidianPath = 'G:\\マイドライブ\\Obsidian Vault\\Research\\AI_Generated'
New-Item -ItemType Directory -Force -Path \$obsidianPath | Out-Null
Write-Host 'Obsidian Research directory created'
" 2>/dev/null

echo "✅ ディレクトリ作成完了"

# 4. 設定ファイル作成
echo ""
echo "⚙️ 設定ファイルを作成中..."

cat > research_config.json << EOF
{
    "api_settings": {
        "default_model": "llama-3.1-sonar-large-128k-online",
        "fast_model": "llama-3.1-sonar-small-128k-online",
        "max_tokens": 4000,
        "temperature": 0.2
    },
    "storage_settings": {
        "obsidian_vault": "G:\\\\マイドライブ\\\\Obsidian Vault",
        "research_dir": "Research\\\\AI_Generated",
        "history_db": "research_history.db"
    },
    "research_types": {
        "instant": {
            "model": "llama-3.1-sonar-small-128k-online",
            "max_tokens": 2000,
            "description": "瞬間検索 - 最速回答"
        },
        "deep": {
            "model": "llama-3.1-sonar-large-128k-online", 
            "max_tokens": 4000,
            "description": "深層リサーチ - 構造化された詳細分析"
        },
        "session": {
            "model": "llama-3.1-sonar-large-128k-online",
            "max_tokens": 4000,
            "description": "包括的リサーチセッション - 多角的分析"
        }
    }
}
EOF

echo "✅ 設定ファイル作成完了"

# 5. ショートカットスクリプト作成
echo ""
echo "🔗 ショートカットスクリプトを作成中..."

cat > research.sh << 'EOF'
#!/bin/bash
# 瞬間リサーチAI ショートカット

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "$1" in
    "help"|""|"-h")
        echo "⚡ 瞬間リサーチAI ショートカット"
        echo "使用方法:"
        echo "  ./research.sh instant \"検索クエリ\"     # 瞬間検索"
        echo "  ./research.sh deep \"テーマ\"          # 深層リサーチ"
        echo "  ./research.sh session \"テーマ\"       # 包括的セッション"
        echo "  ./research.sh history                 # 履歴表示"
        echo "  ./research.sh test                    # 接続テスト"
        ;;
    *)
        python3 "$SCRIPT_DIR/instant_research_ai.py" "$@"
        ;;
esac
EOF

chmod +x research.sh

echo "✅ ショートカット作成完了"

# 6. Claude Desktop MCP設定 (オプション)
echo ""
echo "🔌 Claude Desktop MCP統合..."

CLAUDE_CONFIG_PATH="$HOME/.config/claude/claude_desktop_config.json"
if [ -f "$CLAUDE_CONFIG_PATH" ]; then
    echo "📝 既存のClaude Desktop設定を発見"
    echo "ℹ️ 手動でMCPサーバーを追加することをお勧めします"
    echo ""
    echo "追加する設定例:"
    echo '{
  "mcpServers": {
    "instant-research": {
      "command": "python3",
      "args": ["'$(pwd)'/instant_research_ai.py", "mcp-server"],
      "env": {
        "PERPLEXITY_API_KEY": "'$PERPLEXITY_API_KEY'"
      }
    }
  }
}'
else
    echo "ℹ️ Claude Desktop設定ファイルが見つかりません"
    echo "通常の使用には影響ありません"
fi

# 7. 接続テスト
echo ""
echo "🧪 接続テストを実行中..."

python3 instant_research_ai.py test

# 8. セットアップ完了
echo ""
echo "🎉 Perplexity MCP × Claude 瞬間リサーチAI セットアップ完了！"
echo ""
echo "📚 使用方法:"
echo "  python3 instant_research_ai.py instant \"検索クエリ\""
echo "  python3 instant_research_ai.py deep \"テーマ\""
echo "  python3 instant_research_ai.py session \"テーマ\""
echo ""
echo "🚀 ショートカット:"
echo "  ./research.sh instant \"AIの最新動向\""
echo "  ./research.sh deep \"Stable Diffusion SDXL\""
echo "  ./research.sh session \"Claude MCP プロトコル\""
echo ""
echo "📊 履歴確認:"
echo "  ./research.sh history"
echo ""
echo "💡 ヒント:"
echo "  - 結果は自動的にObsidianに保存されます"
echo "  - 履歴はSQLiteデータベースで管理されます"
echo "  - API使用量を定期的に確認してください"
echo ""
echo "✅ 準備完了 - 瞬間リサーチを開始してください！"