#!/bin/bash
# Claude起動時の重要リマインダー表示

echo ""
echo "🚨 Claude Code 重要リマインダー"
echo "========================================"

# 1. Simple First原則
echo ""
echo "📋 Simple First原則"
echo "  ✓ 73行 > 1,200行の実証済み"
echo "  ✓ 最もシンプルな解決策を選ぶ"
echo "  ✓ 実際に毎日使うか？を自問"

# 2. 架空データ禁止
echo ""
echo "🚫 絶対禁止事項"
echo "  ✗ 架空のデータで実装"
echo "  ✗ 実現可能性の未検証"
echo "  ✗ ダミーデータでのデモ"
echo "  ✗ 3つ以上の機能同時実装"

# 3. 利用可能なツール
echo ""
echo "🛠️ 利用可能ツール"
echo "  • why.py - 実装前の思考整理（なぜ？を3回）"
echo "  • cu/cu.bat - 使用量追跡"
echo "  • MCPブリッジ - Obsidian/ファイル操作"

# 4. 過去の失敗
echo ""
echo "⚠️ 過去の失敗から学ぶ"
echo "  • Gドライブマウント固執 → MCPブリッジで解決"
echo "  • 架空データで偽装 → 実データ必須"
echo "  • 複雑システム崇拝 → シンプル優先"

# 5. 成功パターン
echo ""
echo "✅ 成功パターン"
echo "  • 1機能1ファイル（73行以下）"
echo "  • 設定不要、即使用可能"
echo "  • 1週間実用テスト後に判断"

echo ""
echo "========================================"
echo "💡 迷ったら: python3 why.py"
echo "========================================"
echo ""

# ファイル数警告
file_count=$(ls -1 /mnt/c/Claude\ Code/tool/*.py 2>/dev/null | wc -l)
if [ $file_count -gt 50 ]; then
    echo "⚠️  警告: Pythonファイルが${file_count}個 - 複雑化の兆候"
    echo ""
fi

# 最近の作業内容表示
if [ -f "/mnt/c/Claude Code/tool/recent_work_summary.sh" ]; then
    /mnt/c/Claude\ Code/tool/recent_work_summary.sh
fi