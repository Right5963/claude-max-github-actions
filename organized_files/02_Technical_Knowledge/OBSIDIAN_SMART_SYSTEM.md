# 🧠 Obsidian活用スマートシステム - Simple First

## 🔌 活用可能プラグイン（脳みそから確認済み）

### 1. Dataview - 自動インデックス生成
```dataview
TABLE 
FROM #claude-code/learning
SORT file.mtime DESC
LIMIT 10
```

### 2. Templater - テンプレート自動適用
- セッション記録用テンプレート
- 学習記録用テンプレート
- システム構築記録用テンプレート

### 3. Auto Note Mover - タグベース自動整理
- #claude-code/session → 30_Permanent/35_AI/Claude_Code/Sessions/
- #claude-code/learning → 30_Permanent/35_AI/Claude_Code/Learning/
- #claude-code/failure → 30_Permanent/35_AI/Claude_Code/Failures/

### 4. Local REST API - 外部アクセス
- MCPブリッジ経由での記録・検索自動化

## 📋 情報整理・更新戦略

### 古い情報の特定
```dataview
LIST
FROM ""
WHERE file.mtime < date("2025-01-01")
AND contains(file.path, "Claude")
SORT file.mtime ASC
```

### 情報の更新ルール
1. **日付確認**: 2025年以前の情報は検証必須
2. **タグ統一**: 古いタグを新基準に統一
3. **リンク修正**: 無効リンクの修正
4. **重複削除**: 同内容ファイルの統合

## 🎯 Simple First実装

### テンプレート例（Templater用）
```markdown
# {{title}} #claude-code/{{type}}

## 📅 記録日時
{{date}} {{time}}

## 🎯 概要
{{概要を一行で}}

## 📝 詳細内容
{{具体的内容}}

## 🔗 関連知識
- [[Simple First原則]]
- [[記録は宝]]

## 🏷️ タグ
#claude-code/{{type}} #{{date}}
```

### Dataview自動ダッシュボード
```dataview
TABLE WITHOUT ID
file.link as "記録",
type as "種別", 
date as "日付"
FROM #claude-code
WHERE date >= date(today) - dur(7 days)
SORT date DESC
```

## 🔄 自動化フロー

### 記録作成（Templater使用）
1. Hotkey → テンプレート選択
2. 自動的にメタデータ入力
3. 適切なフォルダに配置

### 知識検索（Dataview使用）
1. タグクエリで関連知識表示
2. 時系列での学習経過確認
3. 失敗→成功パターンの可視化

### 整理実行（Auto Note Mover使用）
1. タグに基づく自動分類
2. 重複ファイルの検出
3. 古い情報のアーカイブ

## 📊 知識可視化

### 学習進捗ダッシュボード
```dataview
TABLE 
count(rows) as "記録数"
FROM #claude-code
GROUP BY type
```

### 失敗パターン分析
```dataview
LIST
FROM #claude-code/failure
WHERE contains(lower(file.name), "simple first")
```

## 🛠️ 実装優先順位

### Phase 1: テンプレート整備
- セッション記録テンプレート
- 学習記録テンプレート
- 失敗記録テンプレート

### Phase 2: 自動化設定
- Auto Note Mover設定
- Dataviewダッシュボード作成
- タグ統一スクリプト

### Phase 3: 古い情報整理
- 2025年以前ファイルの検証
- 重複ファイルの統合
- リンク修正

## 💡 Simple First実践

**複雑なプラグイン設定 → 直感的な使用体験**
- 内部: 高機能なDataview、Templater連携
- 外部: ワンクリックでの記録・検索・整理
- 価値: 複雑な知識管理を簡単操作に変換