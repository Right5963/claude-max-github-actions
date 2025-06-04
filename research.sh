#!/bin/bash
# 瞬間リサーチAI ショートカット (無料枠管理対応)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "$1" in
    "help"|""|"-h")
        echo "⚡ 瞬間リサーチAI ショートカット (無料枠管理付き)"
        echo "使用方法:"
        echo "  ./research.sh instant \"検索クエリ\"     # 瞬間検索"
        echo "  ./research.sh deep \"テーマ\"          # 深層リサーチ"
        echo "  ./research.sh session \"テーマ\"       # 包括的セッション"
        echo "  ./research.sh history                 # 履歴表示"
        echo "  ./research.sh usage                   # 使用量統計"
        echo "  ./research.sh test                    # 接続テスト"
        echo ""
        echo "💡 Perplexity Pro制限:"
        echo "  - 1日100リクエスト"
        echo "  - 月間2,000リクエスト" 
        echo "  - 月間200,000トークン ($5相当)"
        ;;
    *)
        python3 "$SCRIPT_DIR/instant_research_ai.py" "$@"
        ;;
esac