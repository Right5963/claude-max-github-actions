# 🚀 GitHubリポジトリ作成手順

## ✅ 現在の状況
- 自宅PC専用実装完了・コミット済み ✅
- GitHubリポジトリ作成ページが開きました ✅

## 📋 GitHubでの作成手順

### Step 1: リポジトリ基本情報
```
Repository name: claude-max-github-actions
Description: 自宅PC版 Claude Max + GitHub Actions integration with Perplexity MCP - @akira_papa_IT methodology
```

### Step 2: 設定選択
```
✅ Public (推奨) または Private
❌ Add a README file (チェックしない)
❌ Add .gitignore (チェックしない)  
❌ Choose a license (チェックしない)
```

### Step 3: "Create repository" をクリック

## 🔧 リモート追加とプッシュ

### GitHubリポジトリ作成後に実行
```bash
cd "/mnt/c/Claude Code/tool"

# リモート追加（YOUR_USERNAMEを実際のユーザー名に変更）
git remote add origin https://github.com/YOUR_USERNAME/claude-max-github-actions.git

# プッシュ実行
git push -u origin master
```

## 🔑 GitHub Secrets設定

### Repository Settings > Secrets and variables > Actions
```
Name: PERPLEXITY_API_KEY
Value: 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

Name: ANTHROPIC_API_KEY
Value: [あなたのClaude Max APIキー]
```

## 🏃‍♂️ Self-hosted Runner登録

### Repository Settings > Actions > Runners
```
1. "New self-hosted runner" をクリック
2. Operating System: Linux を選択
3. Architecture: x64 を選択
4. Registration Token をコピー
```

### ローカルでRunner設定実行
```bash
cd "/mnt/c/Claude Code/tool/actions-runner"
./configure_home_runner.sh

# 入力内容:
# Repository URL: https://github.com/YOUR_USERNAME/claude-max-github-actions
# Registration Token: [上記でコピーしたToken]
```

## ⚡ Runner起動

### 電力効率化モードで起動（推奨）
```bash
cd "/mnt/c/Claude Code/tool/actions-runner"
./power_efficient_runner.sh
```

### または PM2で自動管理
```bash
pm2 start ecosystem.home.config.js
pm2 status
```

## 🧪 初回テスト実行

### GitHub Actions ワークフロー実行
```
1. GitHub Repository > Actions タブ
2. "Claude MCP Research Automation" をクリック
3. "Run workflow" をクリック
4. Input設定:
   - research_type: instant
   - query: "Claude MCP integration test"
   - save_to_obsidian: true
5. "Run workflow" 実行
```

## 💰 最終コスト構成

```
Claude Code Pro: $100/月 (約15,000円)
Perplexity Pro: $5/月 (約750円)
GitHub Actions: $0 (Self-hosted runners)
電気代追加分: $0 (PC基本つけっぱなし)

月額総額: 約15,750円 🎯
@akira_papa_IT方式でVPS版より月1,000円節約！
```

## 🎉 完成後の自動化機能

### 24時間自動リサーチ
- 毎朝9時: 技術トレンド収集
- 平日昼: 開発情報更新
- 夕方: 投資・副業情報
- 夜間: 学習推奨記事

### GitHub統合
- Issue作成時: 自動解決策調査
- PR作成時: ベストプラクティス提案
- 定期実行: プロジェクト改善提案

### Obsidian統合
- 自動保存: 全リサーチ結果
- 構造化: 日付・カテゴリ別整理
- 検索可能: 過去の調査結果活用

---

**次のアクション**: GitHubリポジトリ作成 → リモート追加・プッシュ → Runner登録 🚀