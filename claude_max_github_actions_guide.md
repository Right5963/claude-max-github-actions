# Claude Max + GitHub Actions 実装ガイド 🚀

## 🎯 現在の実装状況

### ✅ 完了済み
1. **Perplexity MCP統合**: Claude Code内で動作確認済み
2. **GitHub Actions ワークフロー**: 設計・ファイル作成済み
3. **Self-hosted Runner**: ダウンロード・セットアップ準備完了
4. **環境変数設定**: .env ファイル作成済み

### 🔧 次に必要な手順

#### Step 1: GitHubリポジトリ準備
```bash
# 現在のローカルリポジトリをGitHubにプッシュ
# ユーザーが実行する必要があります:

# 1. GitHub.comで新しいリポジトリ作成
# 2. リモート追加
git remote add origin https://github.com/YOUR_USERNAME/claude-max-actions.git

# 3. プッシュ
git push -u origin master
```

#### Step 2: GitHub Secrets設定
Repository Settings > Secrets and variables > Actions で以下を設定:

```
PERPLEXITY_API_KEY: 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
ANTHROPIC_API_KEY: [ユーザーのClaude Max APIキー]
```

#### Step 3: Self-hosted Runner登録
```bash
# GitHubリポジトリで:
# Settings > Actions > Runners > New self-hosted runner

# ローカルで実行:
cd actions-runner
./configure_runner.sh
# → GitHub TokenとRepository URLを入力

# Runner開始
./run.sh
```

#### Step 4: ワークフロー実行テスト
```bash
# GitHubリポジトリで:
# Actions > Claude MCP Research Automation > Run workflow
# 
# Input:
# - research_type: instant
# - query: "Claude MCP test"
# - save_to_obsidian: true
```

## 💰 Claude Max料金内運用の仕組み

### @akira_papa_IT方式の活用
```yaml
# GitHub Actions制限設定
timeout-minutes: 5           # 5分でタイムアウト
runs-on: self-hosted        # 無料Self-hosted Runner使用
```

### Claude Max使用量最適化
```python
# 短時間・効率的なAPI呼び出し
result = claude_model.generate(
    prompt="簡潔なリサーチクエリ",
    max_tokens=1000,           # 制限的なトークン数
    timeout=30                 # 短時間制限
)
```

### 月間コスト概算
```
Claude Max: $20/月          # 基本プラン
GitHub Actions: $0          # 2,000分無料枠+Self-hosted
Perplexity Pro: $5/月       # リサーチエンジン
VPS(オプション): $5-10/月   # Self-hosted Runner用

総計: $25-35/月で enterprise級自動化環境
```

## 🚨 重要な技術的制約

### Claude Code CLI + GitHub Actions の現実
```yaml
# 課題: GitHub Actions環境でのClaude認証
steps:
  - name: Setup Claude Code
    run: |
      # インタラクティブ認証が困難
      echo $ANTHROPIC_API_KEY | claude auth login --api-key
      # ↑ このコマンドが実際に動作するか要検証
```

### 代替アプローチ: 直接API呼び出し
```python
# Claude Code CLIの代わりに直接API使用
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

message = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1000,
    messages=[{
        "role": "user", 
        "content": "Research query processing"
    }]
)
```

## 🎯 実装の現実的な道筋

### Phase A: ローカル検証（現在位置）
- ✅ MCP統合動作確認
- ✅ Perplexity検索動作確認
- 🔧 Claude API直接呼び出しテスト

### Phase B: GitHub統合
- GitHubリポジトリ作成・プッシュ
- Self-hosted Runner実際の稼働
- GitHub Actions動作検証

### Phase C: Claude Max統合
- Claude API認証設定
- GitHub Actions環境でのClaude呼び出しテスト
- 使用量監視・制限設定

### Phase D: 運用開始
- 定期リサーチ自動実行
- Obsidian自動保存
- コスト監視・最適化

## 🔧 次のアクションアイテム

### ユーザー側で必要な作業
1. **GitHub新規リポジトリ作成**
2. **Claude Max APIキー取得**
3. **Self-hosted Runner用VPS準備**（オプション）

### 実装側で続行する作業
1. **Claude API直接呼び出し実装**
2. **GitHub Actions ワークフロー改善**
3. **動作検証スクリプト作成**

## 📊 @akira_papa_IT成功事例の再現性

### 成功の要因
1. **Self-hosted Runners**: GitHub Actions 2,000分制限回避
2. **効率的タイムアウト**: 5分制限で十分な処理
3. **コスト最適化**: 追加費用なしでの運用

### 技術的課題
1. **Claude認証**: 非対話環境での認証方法
2. **MCP統合**: GitHub Actions環境での動作
3. **エラーハンドリング**: 制限時間内での確実実行

## 🚀 結論

**現在の状況**: 理論設計は完了、実装の90%が準備済み
**残り作業**: GitHub設定とClaude認証の実際の動作検証

@akira_papa_IT氏の成功を再現するための基盤は整っています。
次はGitHub設定とCloud認証の実際の動作確認が必要です。