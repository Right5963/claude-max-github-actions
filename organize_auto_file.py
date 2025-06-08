#!/usr/bin/env python3
"""
Obsidian Auto File Organizer 設定最適化ツール

現在のVault内容を分析して、適切なタグとフォルダのマッピングを提案・適用します。
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter

def analyze_vault_content(vault_path):
    """Vault内のマークダウンファイルを分析"""
    vault = Path(vault_path)
    analysis = {
        'tags': defaultdict(list),  # タグ -> ファイルリスト
        'folders': defaultdict(list),  # フォルダ -> ファイルリスト
        'keywords': defaultdict(list)  # キーワード -> ファイルリスト
    }

    # マークダウンファイルを検索
    for md_file in vault.rglob("*.md"):
        # 隠しフォルダとテンプレートを除外
        if any(part.startswith('.') for part in md_file.parts):
            continue
        if "Templates" in md_file.parts or "templates" in md_file.parts:
            continue

        try:
            content = md_file.read_text(encoding='utf-8', errors='ignore')
            file_info = {
                'path': str(md_file.relative_to(vault)),
                'folder': md_file.parent.name,
                'filename': md_file.stem
            }

            # タグを抽出
            tags = re.findall(r'#([^\s#\[\]]+)', content)
            for tag in tags:
                analysis['tags'][tag].append(file_info)

            # フォルダ情報を収集
            analysis['folders'][file_info['folder']].append(file_info)

            # キーワード分析（タイトルと内容から）
            text = (file_info['filename'] + ' ' + content).lower()

            # 技術キーワード
            tech_keywords = ['python', 'javascript', 'typescript', 'code', 'programming', 'cursor', 'claude', 'ai', 'automation']
            for keyword in tech_keywords:
                if keyword in text:
                    analysis['keywords'][keyword].append(file_info)

        except Exception as e:
            print(f"ファイル読み込みエラー: {md_file} - {e}")
            continue

    return analysis

def generate_optimal_mapping(analysis):
    """分析結果から最適なマッピングを生成"""

    # Obsidianのフォルダ構造に基づくマッピング
    folder_mapping = {
        # 技術・開発関連
        'cursor': '100_Cursor',
        'claude': '100_Cursor',
        'ai': '100_Cursor',
        'code': '100_Cursor',
        'programming': '100_Cursor',
        'development': '100_Cursor',
        'automation': '100_Workflows',
        'workflow': '100_Workflows',

        # 学習・文献関連
        'article': '20_Literature/22_Articles',
        'book': '20_Literature/21_Books',
        'video': '20_Literature/23_Videos',
        'twitter': '20_Literature/24_SNS',
        'sns': '20_Literature/24_SNS',

        # プロジェクト・分野
        'project': '40_Areas',
        'business': '40_Areas',
        'research': '40_Areas',

        # その他
        'index': '90_Index',
        'moc': '10_MOCs',
        'permanent': '30_Permanent',
        'evergreen': '30_Evergreen',
        'share': '70_Share'
    }

    # タグマッピングを生成
    tag_mapping = {}

    for tag, files in analysis['tags'].items():
        # タグ名から適切なフォルダを推測
        tag_lower = tag.lower()

        # 直接マッチング
        matched_folder = None
        for keyword, folder in folder_mapping.items():
            if keyword in tag_lower:
                matched_folder = folder
                break

        # ファイルが実際に配置されているフォルダも考慮
        if not matched_folder and files:
            folder_counter = Counter()
            for file_info in files:
                current_folder = file_info['folder']
                # 既存フォルダから適切なマッピングを推測
                if current_folder.startswith('100_'):
                    folder_counter['100_Cursor'] += 1
                elif current_folder.startswith('20_'):
                    folder_counter['20_Literature'] += 1
                elif current_folder.startswith('30_'):
                    folder_counter['30_Permanent'] += 1
                elif current_folder.startswith('40_'):
                    folder_counter['40_Areas'] += 1
                else:
                    folder_counter['00_Inbox'] += 1

            if folder_counter:
                matched_folder = folder_counter.most_common(1)[0][0]

        # デフォルトは受信箱
        tag_mapping[f'#{tag}'] = matched_folder or '00_Inbox'

    return tag_mapping

def update_auto_organizer_config(vault_path, tag_mapping):
    """Auto File Organizerの設定を更新"""
    config_path = Path(vault_path) / ".obsidian" / "plugins" / "auto-file-organizer" / "data.json"

    if not config_path.exists():
        print(f"Auto File Organizerの設定ファイルが見つかりません: {config_path}")
        return False

    try:
        # 現在の設定を読み込み
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # バックアップを作成
        backup_path = config_path.with_suffix('.json.backup')
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"設定をバックアップしました: {backup_path}")

        # タグマッピングを更新
        config['tagMapping'] = tag_mapping

        # 基本設定も最適化
        config['tagEnabled'] = True
        config['priority'] = 'tag'  # タグ優先にする

        # 拡張子マッピングも改善
        config['extensionMapping'] = {
            "md": "00_Inbox",
            "pdf": "20_Literature",
            "png": "Assets",
            "jpg": "Assets",
            "jpeg": "Assets",
            "py": "100_Cursor",
            "js": "100_Cursor",
            "ts": "100_Cursor",
            "json": "Config",
            "sh": "100_Workflows",
            "bat": "100_Workflows",
            "ps1": "100_Workflows"
        }

        # 設定を保存
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        return True

    except Exception as e:
        print(f"設定更新エラー: {e}")
        return False

def main():
    vault_path = r"G:\マイドライブ\Obsidian Vault"

    print("=== Obsidian Auto File Organizer 設定最適化ツール ===")
    print()

    # Vault内容を分析
    print("📁 Vault内容を分析中...")
    analysis = analyze_vault_content(vault_path)

    print(f"✅ 分析完了:")
    print(f"   - 検出されたタグ数: {len(analysis['tags'])}")
    print(f"   - 分析したフォルダ数: {len(analysis['folders'])}")
    print()

    # 最適なマッピングを生成
    print("🎯 最適なタグマッピングを生成中...")
    tag_mapping = generate_optimal_mapping(analysis)

    # プレビューを表示
    print("\n📋 生成されたタグマッピング:")
    print("-" * 50)
    for tag, folder in sorted(tag_mapping.items()):
        print(f"{tag:<30} → {folder}")

    print(f"\n📊 合計 {len(tag_mapping)} タグのマッピングを生成しました。")

    # 確認
    print("\n" + "="*50)
    response = input("この設定でAuto File Organizerを更新しますか？ (y/N): ").strip().lower()

    if response in ['y', 'yes']:
        print("\n⚙️ Auto File Organizer設定を更新中...")

        if update_auto_organizer_config(vault_path, tag_mapping):
            print("✅ 設定が正常に更新されました！")
            print("\n🔄 次の手順:")
            print("1. Obsidianを再起動してください")
            print("2. Auto File Organizerプラグインが有効になっていることを確認してください")
            print("3. 新しいファイルが自動的に適切なフォルダに分類されることを確認してください")
        else:
            print("❌ 設定の更新に失敗しました。")
    else:
        print("\n❌ キャンセルされました。設定は変更されませんでした。")

if __name__ == "__main__":
    main()
