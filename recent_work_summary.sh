#!/bin/bash
# 最近の作業内容サマリー表示

echo ""
echo "📂 最近の作業内容"
echo "-------------------"

# 最近変更されたファイル（24時間以内）
echo "• 24時間以内の変更:"
find /mnt/c/Claude\ Code/tool -name "*.py" -mtime -1 -type f 2>/dev/null | head -5 | while read file; do
    basename "$file"
done

# セッション情報
if [ -d "/mnt/c/Claude Code/tool/sessions" ]; then
    latest_session=$(ls -t /mnt/c/Claude\ Code/tool/sessions/*.json 2>/dev/null | head -1)
    if [ -n "$latest_session" ]; then
        echo ""
        echo "• 最新セッション: $(basename $latest_session)"
    fi
fi

# 現在のプロジェクト数警告
project_dirs=$(find /mnt/c/Claude\ Code/tool -maxdepth 1 -type d -name "*_system" -o -name "*-system" -o -name "*_project" 2>/dev/null | wc -l)
if [ $project_dirs -gt 3 ]; then
    echo ""
    echo "⚠️  並行プロジェクト数: ${project_dirs}個 - 簡略化を検討"
fi

echo "-------------------"