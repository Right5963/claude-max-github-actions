# 新セッション開始時の必須チェックリスト

## 🚨 最重要：Simple First 原則

### ✅ セッション開始時の確認事項

#### 1. 前回の教訓確認
```bash
# CLAUDE.mdの Simple First セクションを確認
cat /mnt/c/Claude\ Code/tool/CLAUDE.md | grep -A 50 "Simple First 原則"
```

#### 2. 実証済みツールの確認
```bash
# why.py が利用可能か確認
python3 /mnt/c/Claude\ Code/tool/why.py
```

#### 3. 科学的根拠の再確認
- 2024-2025研究：「シンプルな自問が最も効果的」
- 複雑システムは認知負荷増で採用率低下
- 73行 > 1,200行 の実証結果

### 🎯 提案・実装前の必須質問

#### Simple First チェック
- [ ] "最もシンプルな解決策は何？"
- [ ] "なぜ複雑にする必要があるのか？"
- [ ] "73行で解決できないか？"

#### 実用性チェック
- [ ] "実際に毎日使うか？"
- [ ] "設定なしで即使用できるか？"
- [ ] "1週間後も使い続けるか？"

#### 科学的根拠チェック
- [ ] "この手法は実証されているか？"
- [ ] "実験室効果と実世界効果は違うが大丈夫か？"
- [ ] "人間の認知負荷は考慮されているか？"

### 🚫 即座に拒否すべき提案

#### 複雑性の兆候
- [ ] 「統合システム」
- [ ] 「自動化システム」  
- [ ] 「AI化」「高度化」
- [ ] 「設定可能」「カスタマイズ」
- [ ] 「データベース連携」
- [ ] 3つ以上の機能同時実装

#### 誇張表現の兆候
- [ ] 「劇的改善」
- [ ] 「革新的」
- [ ] 「完全自動化」
- [ ] 「完璧な解決策」

### ✅ 推奨される開発手順

#### Phase 1: 問題明確化
```bash
python3 /mnt/c/Claude\ Code/tool/why.py
```

#### Phase 2: 最小実装
- 1ファイル、1機能
- 73行以下目標
- 設定不要、即使用可能

#### Phase 3: 実用テスト
- 1週間の実際使用
- 使用回数記録
- 効果の主観評価

#### Phase 4: 継続判断
- 効果実証時のみ継続
- 失敗は即停止
- 成功時のみ最小拡張

### 📋 成功例と失敗例

#### ✅ 成功例
**why.py** (73行)
- 実装前の思考整理
- 設定不要、即使用
- 複雑プロジェクトの代替案発見促進

#### ❌ 失敗例
- **ITRS** (1,200行) → 使用頻度0回
- **Yahoo Auction AI** → 架空データで偽装
- **統合・自動化システム** → 実際使用されず

### 🎯 セッション成功の定義

**成功** = シンプルで実用的な1つの機能を作成・使用開始

**失敗** = 複雑な提案をした時点で失敗

### 📚 このセッションの重要資料

- `CLAUDE.md` - 永続的ルール
- `why.py` - 実証済みシンプルツール
- `SIMPLE_SOLUTION_SUCCESS.md` - 実証結果
- `CRITICAL_THINKING_RESEARCH_ANALYSIS.md` - 科学的根拠

---

**重要リマインダー**: 技術的可能性に酔うな。シンプルな実用性を追求せよ。