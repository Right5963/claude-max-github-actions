# 🚀 GitHub Repository Push Instructions

## ✅ 現在の状況
- GitHubリポジトリ作成完了: https://github.com/Right5963/claude-max-github-actions ✅
- リモートURLの設定完了 ✅
- 認証設定が必要 🔧

## 🔑 GitHub認証設定

### Option 1: Personal Access Token使用（推奨）
```bash
# 1. GitHub Personal Access Token作成
# https://github.com/settings/tokens にアクセス
# "Generate new token (classic)" をクリック
# Scope: repo (Full control of private repositories) にチェック
# Tokenを生成・コピー

# 2. 認証情報でプッシュ
cd "/mnt/c/Claude Code/tool"
git push -u origin master
# Username: Right5963
# Password: [生成したPersonal Access Token]
```

### Option 2: GitHub CLI使用
```bash
# GitHub CLI認証
gh auth login
# Browser認証を選択

# プッシュ実行
git push -u origin master
```

### Option 3: SSH Key使用
```bash
# SSH Key生成・設定後
git remote set-url origin git@github.com:Right5963/claude-max-github-actions.git
git push -u origin master
```

## 📋 推奨手順：Personal Access Token

### Step 1: Token作成
1. https://github.com/settings/tokens にアクセス
2. "Generate new token (classic)" をクリック
3. Note: "Claude Max GitHub Actions"
4. Expiration: 30 days (または適切な期間)
5. Scopes: `repo` にチェック ✅
6. "Generate token" をクリック
7. **Token をコピー・保存** 📋

### Step 2: プッシュ実行
```bash
cd "/mnt/c/Claude Code/tool"
git push -u origin master

# 認証プロンプトで入力:
# Username: Right5963
# Password: [コピーしたPersonal Access Token]
```

## 🔑 次のステップ（プッシュ成功後）

### 1. GitHub Secrets設定
```
Repository: https://github.com/Right5963/claude-max-github-actions
Settings > Secrets and variables > Actions > "New repository secret"

Secret 1:
Name: PERPLEXITY_API_KEY
Value: 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

Secret 2:
Name: ANTHROPIC_API_KEY  
Value: [あなたのClaude Max APIキー]
```

### 2. Self-hosted Runner登録
```
Repository Settings > Actions > Runners > "New self-hosted runner"
Operating System: Linux
Architecture: x64
Registration Token をコピー
```

### 3. ローカルでRunner設定
```bash
cd "/mnt/c/Claude Code/tool/actions-runner"
./configure_home_runner.sh

# 入力内容:
Repository URL: https://github.com/Right5963/claude-max-github-actions
Registration Token: [上記でコピーしたToken]
```

### 4. Runner起動
```bash
# 電力効率化モード（推奨）
./power_efficient_runner.sh

# または PM2自動管理
pm2 start ecosystem.home.config.js
```

## 🧪 初回テスト

### GitHub Actions実行テスト
```
1. Repository > Actions タブ
2. "Claude MCP Research Automation"
3. "Run workflow"
4. Input:
   - research_type: instant
   - query: "Claude MCP test"
   - save_to_obsidian: true
5. 実行確認
```

## ⚡ トラブルシューティング

### プッシュ認証エラー
```bash
# リモートURL確認
git remote -v

# 認証情報再設定
git config --global user.name "Right5963"
git config --global user.email "your-email@example.com"
```

### 依存関係エラー（必要に応じて）
```bash
# GitHub Actions Runner依存関係
cd "/mnt/c/Claude Code/tool/actions-runner"
sudo ./bin/installdependencies.sh

# PM2インストール
sudo npm install -g pm2
```

---

**次のアクション**: Personal Access Token作成 → プッシュ実行 🚀