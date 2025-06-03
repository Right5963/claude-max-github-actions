#!/bin/bash
# Claude Code セッション復元スクリプト
# Cursor再起動後にこのスクリプトを実行して前回セッションの継続

set -e

SESSION_DIR="/mnt/c/Claude Code/tool/sessions"
CURRENT_SESSION_FILE="/mnt/c/Claude Code/tool/.current_session"

echo "🔄 Claude Code セッション復元システム"
echo "========================================"

# 現在のセッションID取得
if [ -f "$CURRENT_SESSION_FILE" ]; then
    CURRENT_ID=$(cat "$CURRENT_SESSION_FILE")
    echo "📋 前回セッション: $CURRENT_ID"
    
    # セッション継続コンテキスト表示
    echo ""
    echo "🎯 前回セッションの継続:"
    python3 "/mnt/c/Claude Code/tool/session_manager.py" continue
    echo ""
    
    # Obsidianに保存されたセッション情報の場所
    echo "📚 詳細記録: Obsidian/Sessions/Claude Session *-$CURRENT_ID.md"
    echo ""
    
    # 継続確認
    read -p "このセッションを継続しますか？ (y/n): " -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "✅ セッション継続開始"
        echo ""
        echo "💡 継続のヒント:"
        echo "   - 'Claude Usage Stats拡張機能のインストール済み'"
        echo "   - 'ステータスバーで使用量確認可能'"
        echo "   - '次のタスク: Cursor再起動して動作確認'"
        echo ""
    else
        echo "🆕 新しいセッションを開始"
        # 新しいセッションID生成
        NEW_ID=$(python3 -c "import hashlib, datetime; print(hashlib.md5(datetime.datetime.now().isoformat().encode()).hexdigest()[:8])")
        echo "$NEW_ID" > "$CURRENT_SESSION_FILE"
        echo "📋 新セッション: $NEW_ID"
    fi
else
    echo "⚠️  前回セッションが見つかりません"
    echo "🆕 新しいセッションを開始します"
    
    # 新しいセッションID生成
    NEW_ID=$(python3 -c "import hashlib, datetime; print(hashlib.md5(datetime.datetime.now().isoformat().encode()).hexdigest()[:8])")
    echo "$NEW_ID" > "$CURRENT_SESSION_FILE"
    echo "📋 新セッション: $NEW_ID"
fi

echo ""
echo "🎯 利用可能なコマンド:"
echo "   python3 session_manager.py save          # セッション保存"
echo "   python3 session_manager.py list          # セッション一覧"
echo "   python3 session_manager.py continue      # 継続コンテキスト表示"
echo "   ./session_restore.sh                     # セッション復元（このスクリプト）"
echo ""
echo "✅ セッション管理システム準備完了"