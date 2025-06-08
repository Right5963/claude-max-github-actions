#!/usr/bin/env python3
"""
Obsidian Auto File Organizer 設定最適化ツール（改善版）

より詳細で実用的な分類ルールによる智的分類を実現
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter

def analyze_vault_content(vault_path):
    """Vault内のマークダウンファイルを分析"""
    vault = Path(vault_path)
    analysis = {
        'tags': defaultdict(list),
        'folders': defaultdict(list),
        'content_analysis': defaultdict(list)
    }

    for md_file in vault.rglob("*.md"):
        if any(part.startswith('.') for part in md_file.parts):
            continue
        if "Templates" in md_file.parts or "templates" in md_file.parts:
            continue

        try:
            content = md_file.read_text(encoding='utf-8', errors='ignore')
            file_info = {
                'path': str(md_file.relative_to(vault)),
                'folder': md_file.parent.name,
                'filename': md_file.stem,
                'content_sample': content[:500]  # 内容サンプル
            }

            # タグを抽出
            tags = re.findall(r'#([^\s#\[\]]+)', content)
            for tag in tags:
                analysis['tags'][tag].append(file_info)

            # フォルダ情報を収集
            analysis['folders'][file_info['folder']].append(file_info)

        except Exception as e:
            print(f"ファイル読み込みエラー: {md_file} - {e}")
            continue

    return analysis

def generate_enhanced_mapping(analysis):
    """強化された分類ルールでマッピングを生成"""

    # より詳細で実用的な分類ルール
    detailed_folder_mapping = {
        # 開発・技術関連（細分化）
        'cursor': '100_Cursor',
        'claude': '100_Cursor',
        'ai': '100_Cursor',
        'programming': '100_Cursor',
        'development': '100_Cursor',
        'code': '100_Cursor',
        'python': '100_Cursor',
        'javascript': '100_Cursor',
        'typescript': '100_Cursor',
        'tech': '100_Cursor',
        'api': '100_Cursor',
        'openai': '100_Cursor',
        'llm': '100_Cursor',
        'machinelearning': '100_Cursor',

        # ワークフロー・自動化
        'automation': '100_Workflows',
        'workflow': '100_Workflows',
        'setup': '100_Workflows',
        'configuration': '100_Workflows',
        'installation': '100_Workflows',
        'environment': '100_Workflows',
        'script': '100_Workflows',
        'batch': '100_Workflows',
        'powershell': '100_Workflows',
        'cmd': '100_Workflows',

        # 文献・学習関連（詳細分類）
        'book': '20_Literature/21_Books',
        'reading': '20_Literature/21_Books',
        'article': '20_Literature/22_Articles',
        'blog': '20_Literature/22_Articles',
        'paper': '20_Literature/22_Articles',
        'research': '20_Literature/22_Articles',
        'study': '20_Literature/22_Articles',
        'video': '20_Literature/23_Videos',
        'youtube': '20_Literature/23_Videos',
        'lecture': '20_Literature/23_Videos',
        'course': '20_Literature/23_Videos',
        'twitter': '20_Literature/24_SNS',
        'sns': '20_Literature/24_SNS',
        'social': '20_Literature/24_SNS',
        'post': '20_Literature/24_SNS',

        # 知識管理・ノート術
        'moc': '10_MOCs',
        'map': '10_MOCs',
        'index': '90_Index',
        'permanent': '30_Permanent',
        'evergreen': '30_Evergreen',
        'zettelkasten': '30_Permanent',
        'knowledge': '30_Permanent',
        'concept': '30_Permanent',
        'theory': '30_Permanent',
        'principle': '30_Permanent',

        # プロジェクト・分野
        'project': '40_Areas',
        'business': '40_Areas',
        'work': '40_Areas',
        'client': '40_Areas',
        'meeting': '40_Areas',
        'plan': '40_Areas',
        'strategy': '40_Areas',
        'goal': '40_Areas',

        # メタ・管理
        'meta': '00_System',
        'system': '00_System',
        'setting': '00_System',
        'config': '00_System',
        'template': 'Templates',
        'daily': '00_Daily',
        'journal': '30_Journal',
        'diary': '30_Journal',

        # 共有・発信
        'share': '70_Share',
        'publish': '70_Share',
        'public': '70_Share',
        'blog': '70_Share',

        # 学習・記録
        'learning': '20_Literature',
        'note': '20_Literature',
        'memo': '00_Inbox',
        'fleeting': '00_Inbox',
        'inbox': '00_Inbox',
        'temp': '00_Inbox',
        'draft': '00_Inbox',

        # ツール・プラグイン
        'obsidian': '00_System',
        'plugin': '00_System',
        'tool': '00_System',

        # 専門分野
        'design': '40_Areas',
        'ui': '40_Areas',
        'ux': '40_Areas',
        'marketing': '40_Areas',
        'finance': '40_Areas',
        'health': '40_Areas',
        'fitness': '40_Areas',
        'cooking': '40_Areas',
        'travel': '40_Areas',

        # 日本語キーワード
        'プログラミング': '100_Cursor',
        'コード': '100_Cursor',
        '開発': '100_Cursor',
        '技術': '100_Cursor',
        'エンジニアリング': '100_Cursor',
        'ワークフロー': '100_Workflows',
        '自動化': '100_Workflows',
        'セットアップ': '100_Workflows',
        '設定': '00_System',
        '環境構築': '100_Workflows',
        'プロジェクト': '40_Areas',
        '事業': '40_Areas',
        'ビジネス': '40_Areas',
        '学習': '20_Literature',
        '読書': '20_Literature/21_Books',
        '記事': '20_Literature/22_Articles',
        '動画': '20_Literature/23_Videos',
        '知識': '30_Permanent',
        '永続': '30_Permanent',
        'メモ': '00_Inbox',
        '日記': '30_Journal',
        '共有': '70_Share',
        'インデックス': '90_Index',
        '一覧': '90_Index',
        'まとめ': '90_Index',
    }

    # タグマッピングを生成
    tag_mapping = {}

    for tag, files in analysis['tags'].items():
        tag_lower = tag.lower()

        # 直接マッチング（優先度高）
        matched_folder = None

        # 完全一致チェック
        if tag_lower in detailed_folder_mapping:
            matched_folder = detailed_folder_mapping[tag_lower]
        else:
            # 部分一致チェック（より厳密に）
            for keyword, folder in detailed_folder_mapping.items():
                if keyword in tag_lower or tag_lower in keyword:
                    matched_folder = folder
                    break

        # ファイルの実際の配置パターンも考慮
        if not matched_folder and files:
            folder_counter = Counter()
            for file_info in files:
                current_folder = file_info['folder']
                # より詳細なフォルダ判定
                if current_folder.startswith('100_'):
                    if 'cursor' in current_folder.lower() or 'code' in current_folder.lower():
                        folder_counter['100_Cursor'] += 1
                    else:
                        folder_counter['100_Workflows'] += 1
                elif current_folder.startswith('20_'):
                    folder_counter['20_Literature'] += 1
                elif current_folder.startswith('30_'):
                    if 'permanent' in current_folder.lower():
                        folder_counter['30_Permanent'] += 1
                    elif 'evergreen' in current_folder.lower():
                        folder_counter['30_Evergreen'] += 1
                    else:
                        folder_counter['30_Journal'] += 1
                elif current_folder.startswith('40_'):
                    folder_counter['40_Areas'] += 1
                elif current_folder.startswith('70_'):
                    folder_counter['70_Share'] += 1
                elif current_folder.startswith('90_'):
                    folder_counter['90_Index'] += 1
                elif current_folder.startswith('10_'):
                    folder_counter['10_MOCs'] += 1
                elif current_folder.startswith('00_'):
                    if 'daily' in current_folder.lower():
                        folder_counter['00_Daily'] += 1
                    elif 'system' in current_folder.lower():
                        folder_counter['00_System'] += 1
                    else:
                        folder_counter['00_Inbox'] += 1
                else:
                    folder_counter['00_Inbox'] += 1

            if folder_counter:
                matched_folder = folder_counter.most_common(1)[0][0]

        # デフォルトは受信箱（最後の手段）
        tag_mapping[f'#{tag}'] = matched_folder or '00_Inbox'

    return tag_mapping

def analyze_classification_quality(tag_mapping):
    """分類品質を分析"""
    folder_counts = Counter(tag_mapping.values())

    print("\n📊 分類結果の分析:")
    print("-" * 50)
    for folder, count in folder_counts.most_common():
        percentage = (count / len(tag_mapping)) * 100
        print(f"{folder:<30} {count:>3}個 ({percentage:>5.1f}%)")

    inbox_ratio = (folder_counts.get('00_Inbox', 0) / len(tag_mapping)) * 100
    if inbox_ratio > 50:
        print(f"\n⚠️  警告: {inbox_ratio:.1f}%のタグが未分類（Inbox）です")
        print("   分類ルールの改善が必要かもしれません")
    else:
        print(f"\n✅ 良好: 分類済みタグが{100-inbox_ratio:.1f}%です")

    return folder_counts

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
        config['priority'] = 'tag'

        # より詳細な拡張子マッピング
        config['extensionMapping'] = {
            "md": "00_Inbox",
            "pdf": "20_Literature",
            "epub": "20_Literature/21_Books",
            "png": "Assets",
            "jpg": "Assets",
            "jpeg": "Assets",
            "gif": "Assets",
            "svg": "Assets",
            "py": "100_Cursor",
            "js": "100_Cursor",
            "ts": "100_Cursor",
            "html": "100_Cursor",
            "css": "100_Cursor",
            "json": "Config",
            "yaml": "Config",
            "yml": "Config",
            "toml": "Config",
            "sh": "100_Workflows",
            "bat": "100_Workflows",
            "ps1": "100_Workflows",
            "txt": "00_Inbox",
            "docx": "20_Literature",
            "xlsx": "Data"
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

    print("=== Obsidian Auto File Organizer 設定最適化ツール（改善版）===")
    print()

    # Vault内容を分析
    print("📁 Vault内容を詳細分析中...")
    analysis = analyze_vault_content(vault_path)

    print(f"✅ 分析完了:")
    print(f"   - 検出されたタグ数: {len(analysis['tags'])}")
    print(f"   - 分析したフォルダ数: {len(analysis['folders'])}")
    print()

    # 強化された分類マッピングを生成
    print("🎯 強化された分類ルールでマッピング生成中...")
    tag_mapping = generate_enhanced_mapping(analysis)

    # 分類品質を分析
    folder_counts = analyze_classification_quality(tag_mapping)

    # 代表的なマッピング例を表示（先頭50個）
    print(f"\n📋 生成されたタグマッピング（先頭50個）:")
    print("-" * 60)
    for i, (tag, folder) in enumerate(sorted(tag_mapping.items())):
        if i >= 50:
            print(f"... 他 {len(tag_mapping) - 50} 個")
            break
        print(f"{tag:<35} → {folder}")

    print(f"\n📊 合計 {len(tag_mapping)} タグのマッピングを生成しました。")

    # 確認
    print("\n" + "="*60)
    response = input("この改善された設定でAuto File Organizerを更新しますか？ (y/N): ").strip().lower()

    if response in ['y', 'yes']:
        print("\n⚙️ Auto File Organizer設定を更新中...")

        if update_auto_organizer_config(vault_path, tag_mapping):
            print("✅ 設定が正常に更新されました！")
            print("\n🔄 次の手順:")
            print("1. Obsidianを再起動してください")
            print("2. Auto File Organizerプラグインが有効になっていることを確認してください")
            print("3. 新しいファイルが適切なフォルダに分類されることを確認してください")
            print("\n💡 分類結果に不満がある場合は、スクリプト内の")
            print("   detailed_folder_mapping を調整してください")
        else:
            print("❌ 設定の更新に失敗しました。")
    else:
        print("\n❌ キャンセルされました。設定は変更されませんでした。")

if __name__ == "__main__":
    main()
