# 🗂️ Auto File Organizer 完全設定ガイド

## ✅ 最適化完了済み設定

### 📁 拡張子別自動分類
**画像ファイル → Assets/Images/**
- `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`

**添付ファイル → Assets/Attachments/**
- `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`

**音声ファイル → Assets/Audio/**
- `.mp3`, `.wav`, `.m4a`, `.flac`

**動画ファイル → Assets/Video/**
- `.mp4`, `.avi`, `.mov`, `.mkv`

**アーカイブ → Assets/Archives/**
- `.zip`, `.rar`, `.7z`

### 🏷️ タグベース分類
**デイリーノート → Daily Notes/**
- `#daily`, `#日記`

**プロジェクト → Projects/**
- `#project`, `#プロジェクト`

**AI関連 → AI/**
- `#AI`, `#claude`

**技術関連 → Tech/**
- `#tech`, `#技術`

**リサーチ → Research/**
- `#research`, `#リサーチ`

**テンプレート → Templates/**
- `#template`, `#テンプレート`

## 🛡️ 保護される既存フォルダ
以下のフォルダ内のファイルは移動されません：
- `.obsidian/` - Obsidian設定
- `Templates/` - テンプレートファイル
- `Assets/` - 既に整理済みファイル
- `100_*`, `20_*`, `30_*`, `40_*`, `90_*`, `95_*` - 既存の番号フォルダ
- `MCP/`, `scripts/` - 技術ファイル

## 🎯 使用方法

### 自動整理（推奨）
1. **新ファイル追加時**: 自動的に適切なフォルダに移動
2. **タグ付け**: ノートに適切なタグを付けると自動分類

### 手動整理
1. **Ctrl+P** → 「Auto File Organizer: Organize all files」
2. 全ファイルを一括整理

### 設定確認・変更
1. **Settings** → **Community plugins** → **Auto File Organizer** → **Options**
2. 必要に応じてルール追加・削除

## ⚙️ 現在の設定詳細

### 有効な機能
- ✅ **拡張子ベース分類**: 有効
- ✅ **タグベース分類**: 有効  
- ✅ **新ファイル作成時の自動整理**: 有効
- ✅ **フォルダ自動作成**: 有効
- ✅ **通知表示**: 有効

### 無効な機能
- ❌ **起動時自動整理**: 無効（安全のため）
- ❌ **編集時自動整理**: 無効（安全のため）
- ❌ **DefaultFolder**: 完全無効化

## 🔧 カスタマイズ例

### 新しい拡張子追加
```json
"txt": "Documents",
"csv": "Data"
```

### 新しいタグ追加
```json
"#meeting": "Meetings",
"#idea": "Ideas"
```

## 🎉 メリット

### Before（整理前）
- Vaultルートにファイルが散乱
- ファイル発見が困難
- 管理が煩雑

### After（整理後）
- **Assets/**: メディアファイルが整理
- **Projects/**: プロジェクト関連が集約
- **AI/**: AI関連知識が集中
- **構造化**: 目的別フォルダで効率的管理

---
**設定完了日**: 2025-06-04
**ステータス**: ✅ 本格運用開始可能