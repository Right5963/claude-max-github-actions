#!/bin/bash
# Claude Code MCP Self-hosted Runner セットアップ
# @akira_papa_IT氏の手法を参考にした実装

echo "🚀 Claude Code MCP Self-hosted Runner セットアップ"
echo "参考: @akira_papa_IT - Claude Code GitHub Actions on Self-hosted Runners"
echo "=" * 60

# 1. 前提条件チェック
echo "📋 前提条件チェック中..."

# Node.js確認
if ! command -v node &> /dev/null; then
    echo "❌ Node.js が必要です"
    echo "インストール: curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -"
    echo "              sudo apt-get install -y nodejs"
    exit 1
fi

# Python確認  
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 が必要です"
    echo "インストール: sudo apt update && sudo apt install python3 python3-pip"
    exit 1
fi

# Claude Code確認
if ! command -v claude &> /dev/null; then
    echo "❌ Claude Code CLI が必要です"
    echo "インストール: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

echo "✅ 前提条件チェック完了"

# 2. GitHub Actions Runner ダウンロード
echo ""
echo "📦 GitHub Actions Runner ダウンロード中..."

RUNNER_VERSION="2.311.0"  # 最新安定版
RUNNER_ARCH="x64"

if [ ! -d "actions-runner" ]; then
    mkdir actions-runner && cd actions-runner
    
    curl -o actions-runner-linux-${RUNNER_ARCH}-${RUNNER_VERSION}.tar.gz \
        -L https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-${RUNNER_ARCH}-${RUNNER_VERSION}.tar.gz
    
    tar xzf ./actions-runner-linux-${RUNNER_ARCH}-${RUNNER_VERSION}.tar.gz
    
    echo "✅ Runner ダウンロード完了"
else
    cd actions-runner
    echo "✅ Runner は既にダウンロード済み"
fi

# 3. 依存関係インストール
echo ""
echo "🔧 依存関係インストール中..."

sudo ./bin/installdependencies.sh

# 4. Runner設定スクリプト作成
echo ""
echo "⚙️ Runner設定スクリプト作成中..."

cat > configure_runner.sh << 'EOF'
#!/bin/bash
# GitHub Actions Runner 設定スクリプト

echo "🔧 GitHub Actions Runner 設定"
echo ""
echo "以下の情報が必要です:"
echo "1. GitHub Repository URL (例: https://github.com/username/repo)"
echo "2. Registration Token (Repository Settings > Actions > Runners から取得)"
echo ""

read -p "Repository URL を入力してください: " REPO_URL
read -p "Registration Token を入力してください: " REG_TOKEN

# Runner設定
./config.sh --url "$REPO_URL" --token "$REG_TOKEN" --name "claude-mcp-runner" --work "_work"

echo ""
echo "✅ Runner設定完了"
echo ""
echo "🚀 Runner開始方法:"
echo "   ./run.sh"
echo ""
echo "🔄 自動起動設定:"
echo "   sudo ./svc.sh install"
echo "   sudo ./svc.sh start"
EOF

chmod +x configure_runner.sh

# 5. Claude Code MCP設定確認
echo ""
echo "🔍 Claude Code MCP設定確認中..."

cd ..  # actions-runnerディレクトリから戻る

# MCP設定確認
if claude mcp list | grep -q "perplexity-research"; then
    echo "✅ Perplexity MCP は既に設定済み"
else
    echo "⚠️ Perplexity MCP が設定されていません"
    echo "設定コマンド:"
    echo "claude mcp add perplexity-research -- python3 $(pwd)/perplexity_mcp_server.py mcp-server"
fi

# 6. PM2設定（@akira_papa_IT推奨）
echo ""
echo "🔄 PM2による自動管理設定..."

if ! command -v pm2 &> /dev/null; then
    echo "📦 PM2をインストール中..."
    sudo npm install -g pm2
fi

# PM2設定ファイル作成
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'claude-mcp-runner',
    cwd: './actions-runner',
    script: './run.sh',
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    }
  }, {
    name: 'perplexity-mcp-server',
    script: './perplexity_mcp_server.py',
    args: 'mcp-server',
    interpreter: 'python3',
    autorestart: true,
    watch: false,
    max_memory_restart: '500M'
  }]
};
EOF

echo "✅ PM2設定ファイル作成完了"

# 7. 環境変数設定テンプレート
echo ""
echo "🔑 環境変数設定テンプレート作成中..."

cat > .env.example << EOF
# Perplexity API Key
PERPLEXITY_API_KEY=your_perplexity_api_key_here

# GitHub Actions Secrets で設定する項目:
# - PERPLEXITY_API_KEY: Perplexity API キー
# - その他必要に応じて追加
EOF

# 8. セットアップ完了
echo ""
echo "🎉 Claude Code MCP Self-hosted Runner セットアップ完了！"
echo ""
echo "📋 次のステップ:"
echo "1. GitHub Repository の Settings > Actions > Runners に移動"
echo "2. 'New self-hosted runner' をクリック"
echo "3. Registration Token を取得"
echo "4. cd actions-runner && ./configure_runner.sh を実行"
echo "5. .env ファイルを作成し、PERPLEXITY_API_KEY を設定"
echo "6. Runner開始: ./run.sh または PM2で管理: pm2 start ecosystem.config.js"
echo ""
echo "🔧 管理コマンド:"
echo "   PM2開始: pm2 start ecosystem.config.js"
echo "   PM2状態: pm2 status"
echo "   PM2停止: pm2 stop all"
echo "   PM2削除: pm2 delete all"
echo ""
echo "📊 GitHub Actions 使用量確認:"
echo "   Repository Settings > Billing > Actions"
echo "   月間2,000分の無料枠を効率活用"
echo ""
echo "🎯 MCP機能テスト:"
echo "   claude --model sonnet -c 'result = mcp__perplexity_research__perplexity_instant_search(\"test\"); print(result)'"
echo ""
echo "参考記事: @akira_papa_IT - Claude Code GitHub Actions on Self-hosted Runners"
echo "Qiita: https://qiita.com/akira_funakoshi/items/c46577970b42166a6666"