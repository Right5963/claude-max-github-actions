#!/usr/bin/env python3
"""
Auto File Organizer プラグイン設定・使用ガイド
"""

import json
import os
from pathlib import Path

def create_default_settings():
    """Auto File Organizerのデフォルト設定を作成"""
    
    vault_path = Path(r"G:\マイドライブ\Obsidian Vault")
    plugin_data_path = vault_path / ".obsidian" / "plugins" / "auto-file-organizer" / "data.json"
    
    # 推奨設定
    default_settings = {
        "enabled": True,
        "organizeOnStartup": False,  # 起動時自動実行は慎重に
        "organizeOnFileCreate": True,  # 新ファイル作成時は自動整理
        "organizeOnFileModify": False,  # 編集時の自動整理は無効（誤動作防止）
        "rules": [
            {
                "name": "Images",
                "enabled": True,
                "pattern": "\\.(png|jpg|jpeg|gif|webp|svg)$",
                "destination": "Assets/Images",
                "description": "画像ファイルをAssets/Imagesフォルダに移動"
            },
            {
                "name": "Attachments", 
                "enabled": True,
                "pattern": "\\.(pdf|doc|docx|xls|xlsx|ppt|pptx)$",
                "destination": "Assets/Attachments",
                "description": "添付ファイルをAssets/Attachmentsフォルダに移動"
            },
            {
                "name": "Audio Files",
                "enabled": True,
                "pattern": "\\.(mp3|wav|m4a|flac)$", 
                "destination": "Assets/Audio",
                "description": "音声ファイルをAssets/Audioフォルダに移動"
            },
            {
                "name": "Video Files",
                "enabled": True,
                "pattern": "\\.(mp4|avi|mov|mkv)$",
                "destination": "Assets/Video", 
                "description": "動画ファイルをAssets/Videoフォルダに移動"
            },
            {
                "name": "Daily Notes",
                "enabled": True,
                "pattern": "^\\d{4}-\\d{2}-\\d{2}.*\\.md$",
                "destination": "Daily Notes",
                "description": "YYYY-MM-DD形式のファイルをDaily Notesフォルダに移動"
            },
            {
                "name": "AI Related Notes",
                "enabled": True,
                "pattern": ".*#(AI|claude|chatgpt|機械学習).*",
                "destination": "AI",
                "description": "AI関連タグのノートをAIフォルダに移動"
            },
            {
                "name": "Project Notes", 
                "enabled": True,
                "pattern": ".*#(project|プロジェクト).*",
                "destination": "Projects",
                "description": "プロジェクト関連タグのノートをProjectsフォルダに移動"
            },
            {
                "name": "Research Notes",
                "enabled": True, 
                "pattern": ".*#(research|リサーチ|調査).*",
                "destination": "Research",
                "description": "リサーチ関連タグのノートをResearchフォルダに移動"
            }
        ],
        "excludePatterns": [
            "^\\.obsidian/.*",
            "^Templates/.*",
            "^Archive/.*"
        ],
        "createFolders": True,  # 必要なフォルダを自動作成
        "showNotifications": True,  # 整理時に通知表示
        "logActions": True  # アクション記録
    }
    
    return default_settings, plugin_data_path

def setup_auto_file_organizer():
    """Auto File Organizer プラグインのセットアップ"""
    print("🗂️ Auto File Organizer プラグイン設定開始...")
    
    settings, settings_path = create_default_settings()
    
    try:
        # 設定ファイル作成
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
            
        print(f"✅ 設定ファイル作成完了: {settings_path}")
        
        # 必要なフォルダ作成
        vault_path = Path(r"G:\マイドライブ\Obsidian Vault")
        folders_to_create = [
            "Assets/Images",
            "Assets/Attachments", 
            "Assets/Audio",
            "Assets/Video",
            "Daily Notes",
            "AI",
            "Projects", 
            "Research"
        ]
        
        for folder in folders_to_create:
            folder_path = vault_path / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 フォルダ作成: {folder}")
            
        print("\n🎯 設定内容:")
        print("- 新ファイル作成時に自動整理")
        print("- 画像→Assets/Images")
        print("- 添付ファイル→Assets/Attachments") 
        print("- デイリーノート→Daily Notes")
        print("- タグ別分類 (#AI, #project, #research)")
        print("- 通知とログ記録有効")
        
        print("\n⚠️ 重要:")
        print("1. Obsidianを再起動してプラグインを有効化")
        print("2. Settings → Community plugins → Auto File Organizer で設定確認")
        print("3. 既存ファイルの整理は手動実行が必要")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def create_usage_guide():
    """使用方法ガイド作成"""
    guide_path = Path(r"G:\マイドライブ\Obsidian Vault") / "Auto_File_Organizer_使用方法.md"
    
    guide_content = """# 🗂️ Auto File Organizer 使用方法

## ✅ プラグイン有効化手順

1. **Obsidianを再起動**
2. **Settings** (⚙️) → **Community plugins** 
3. **Auto File Organizer** を探して **Enable** をクリック
4. **Options** で設定確認・調整

## 🎯 現在の設定

### 自動整理ルール
- **画像ファイル** (.png, .jpg, .gif等) → `Assets/Images/`
- **添付ファイル** (.pdf, .doc等) → `Assets/Attachments/`
- **音声ファイル** (.mp3, .wav等) → `Assets/Audio/`
- **動画ファイル** (.mp4, .avi等) → `Assets/Video/`
- **デイリーノート** (YYYY-MM-DD形式) → `Daily Notes/`

### タグ別分類
- **#AI, #claude, #chatgpt, #機械学習** → `AI/`
- **#project, #プロジェクト** → `Projects/`
- **#research, #リサーチ, #調査** → `Research/`

## 🚀 使用方法

### 自動整理（推奨）
- 新しいファイル作成時に自動で適切なフォルダに移動
- 設定変更不要で即使用可能

### 手動整理
1. **Command Palette** (Ctrl+P) を開く
2. `Auto File Organizer: Organize all files` を実行
3. 既存の全ファイルが整理される

## ⚙️ 設定調整

### プラグイン設定画面
- **Settings** → **Community plugins** → **Auto File Organizer** → **Options**

### 主要設定項目
- `Organize on file create`: 新ファイル作成時の自動整理 (推奨: ON)
- `Organize on file modify`: ファイル編集時の自動整理 (推奨: OFF)
- `Show notifications`: 整理時の通知表示 (推奨: ON)
- `Create folders`: 必要フォルダの自動作成 (推奨: ON)

## 🔧 カスタムルール追加

設定画面で新しいルールを追加可能:

### 例：技術ノート分類
- **Pattern**: `.*#(tech|技術|プログラミング).*`
- **Destination**: `Tech/`
- **Description**: 技術関連ノートをTechフォルダに移動

### 例：特定プロジェクト
- **Pattern**: `.*プロジェクトX.*`
- **Destination**: `Projects/ProjectX/`
- **Description**: プロジェクトX関連ファイルを専用フォルダに移動

## ⚠️ 注意事項

1. **重要ファイルのバックアップ**: 大量整理前は必ずバックアップ
2. **段階的テスト**: 新しいルールは小規模テストから
3. **除外設定**: `.obsidian/`, `Templates/`, `Archive/` フォルダは自動除外済み
4. **手動確認**: 重要なファイル移動は結果を確認

## 🎯 効果的な活用

### ワークフロー例
1. 新しい画像やPDFをVaultに保存
2. 自動で適切なフォルダに移動
3. ノートにタグ付け (#AI, #project等)
4. 定期的に手動整理コマンド実行で全体最適化

### ファイル命名のコツ
- デイリーノート: `2025-06-04.md` 形式で自動分類
- プロジェクト: `プロジェクト名_YYYY-MM-DD.md` で識別しやすく
- 画像: `screenshot_機能名.png` で用途明確化

---

*Auto File Organizer v1.0.8 設定ガイド*
*更新日: 2025-06-04*
"""
    
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
        
    print(f"📋 使用方法ガイド作成: {guide_path.name}")

def main():
    print("🚀 Auto File Organizer セットアップ開始")
    print("=" * 50)
    
    if setup_auto_file_organizer():
        create_usage_guide()
        print("\n✅ セットアップ完了!")
        print("\n次のステップ:")
        print("1. Obsidianを再起動")
        print("2. Community plugins で Auto File Organizer を有効化") 
        print("3. 'Auto_File_Organizer_使用方法.md' で詳細確認")
    else:
        print("\n❌ セットアップ失敗")

if __name__ == "__main__":
    main()