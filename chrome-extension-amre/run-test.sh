#!/bin/bash

# AMRE自動テストランナー

echo "🚀 AMRE拡張機能自動テスト開始"

# 必要な依存関係をチェック
if ! command -v node &> /dev/null; then
    echo "❌ Node.jsが必要です"
    exit 1
fi

# puppeteerのインストール確認
if ! npm list puppeteer &> /dev/null; then
    echo "📦 Puppeteerをインストール中..."
    npm install puppeteer
fi

# テスト実行
echo "🧪 自動テスト実行中..."
node auto-test.js

# 結果確認
if [ -f "test-report.json" ]; then
    echo "📊 テスト結果:"
    cat test-report.json | jq '.summary'
    
    # 成功率チェック
    SUCCESS_RATE=$(cat test-report.json | jq '.summary.successRate')
    if [ "$SUCCESS_RATE" -ge 80 ]; then
        echo "✅ テスト合格（成功率: ${SUCCESS_RATE}%）"
        exit 0
    else
        echo "❌ テスト不合格（成功率: ${SUCCESS_RATE}%）"
        echo "🔧 修正が必要です"
        exit 1
    fi
else
    echo "❌ テストレポートが生成されませんでした"
    exit 1
fi