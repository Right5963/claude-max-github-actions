#!/bin/bash
# Gitリポジトリ初期化ヘルパー
# =========================
# 現在のディレクトリをGitリポジトリ化するかの判断支援

echo "🔍 Git自動コミット導入アシスタント"
echo "==================================="
echo ""

# 現在の状況確認
if [ -d .git ]; then
    echo "✅ すでにGitリポジトリです"
    git status --short
    exit 0
fi

echo "❌ Gitリポジトリではありません"
echo ""

# ディレクトリ分析
echo "📊 ディレクトリ分析:"
echo "-------------------"
file_count=$(find . -type f -not -path '*/\.*' | wc -l)
total_size=$(du -sh . 2>/dev/null | cut -f1)
echo "ファイル数: $file_count"
echo "合計サイズ: $total_size"

# 主要なファイルタイプ
echo ""
echo "📝 主要なファイルタイプ:"
find . -type f -not -path '*/\.*' -name '*.*' | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10

# Git化のメリット評価
echo ""
echo "🤔 このディレクトリをGit化すべきか？"
echo "===================================="

score=0
reasons=()

# Python/JavaScript プロジェクト
if [ -f "package.json" ] || [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
    score=$((score + 30))
    reasons+=("✓ プログラミングプロジェクトです")
fi

# 多数のソースファイル
py_count=$(find . -name "*.py" | wc -l)
js_count=$(find . -name "*.js" | wc -l)
if [ $py_count -gt 5 ] || [ $js_count -gt 5 ]; then
    score=$((score + 20))
    reasons+=("✓ 多数のソースコードファイルがあります")
fi

# ドキュメント
md_count=$(find . -name "*.md" | wc -l)
if [ $md_count -gt 3 ]; then
    score=$((score + 10))
    reasons+=("✓ ドキュメントが整備されています")
fi

# 既存のバックアップシステム
if [ -d "sessions" ] || [ -d "backup" ]; then
    score=$((score + 20))
    reasons+=("✓ バックアップの必要性が高いです")
fi

# スコア表示
echo ""
echo "📈 Git化推奨スコア: $score/100"
echo ""
for reason in "${reasons[@]}"; do
    echo "  $reason"
done

# 推奨事項
echo ""
echo "💡 推奨事項:"
if [ $score -ge 50 ]; then
    echo "✅ Git化を推奨します"
    echo ""
    echo "実行するには:"
    echo "  git init"
    echo "  echo '*.log' >> .gitignore"
    echo "  echo '*.pid' >> .gitignore"
    echo "  echo '__pycache__/' >> .gitignore"
    echo "  echo 'sessions/' >> .gitignore"
    echo "  git add ."
    echo "  git commit -m 'Initial commit'"
    echo ""
    echo "その後、Git自動コミットを有効化できます"
elif [ $score -ge 30 ]; then
    echo "⚠️ Git化を検討してください"
    echo "プロジェクトが成長したら導入を推奨"
else
    echo "❌ 現時点ではGit化は不要です"
    echo "より多くのコードを書いてから検討してください"
fi

# 注意事項
echo ""
echo "⚠️ 注意事項:"
echo "- 機密情報（APIキー等）を含まないか確認"
echo "- 大きなバイナリファイルは除外推奨"
echo "- 個人情報を含むファイルに注意"