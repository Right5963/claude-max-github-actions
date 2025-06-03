#!/bin/bash
# シンプルヘルスチェック
# =====================
# 必要な時だけ手動実行

echo "🏥 システムヘルスチェック"
echo "======================="

# ディスク使用量
echo -n "💾 ディスク: "
df -h / | awk 'NR==2 {print $5 " 使用 (" $4 " 空き)"}'

# メモリ使用量
echo -n "🧠 メモリ: "
free -h | awk 'NR==2 {printf "%.1f%% 使用 (%.1fG/%.1fG)\n", $3/$2*100, $3, $2}'

# セッション監視状態
echo -n "📝 セッション監視: "
if [ -f .monitor.pid ] && kill -0 $(cat .monitor.pid) 2>/dev/null; then
    echo "✅ 稼働中"
else
    echo "❌ 停止中"
fi

# セッションファイル
if [ -f current_session.json ]; then
    echo -n "📋 セッション: "
    python3 -c "
import json
with open('current_session.json') as f:
    data = json.load(f)
    print(f\"{len(data.get('activities', []))}件の活動\")
"
fi

# 最新のバックアップ
echo -n "💾 最新バックアップ: "
ls -t sessions/session_*.json 2>/dev/null | head -1 | xargs -r basename || echo "なし"

echo ""
echo "実行完了"