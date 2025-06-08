#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto File Organizer 設定自動生成ツール

Obsidian Vaultのファイル内容を分析し、適切なフォルダ・タグマッピングを自動生成します。
"""

import json
import re
from pathlib import Path
from typing import Dict, Set, Tuple, Any
from collections import defaultdict, Counter


class AutoOrganizerConfigGenerator:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.config_path = self.vault_path / ".obsidian" / "plugins" / "auto-file-organizer" / "data.json"

        # フォルダ構造の定義（README.mdに基づく）
        self.folder_structure = {
            "00_Inbox": "新規・未分類ファイル",
            "10_MOCs": "Map of Contents",
            "20_Literature": "参考文献・記事",
            "20_Literature/21_Books": "書籍",
            "20_Literature/22_Articles": "記事",
            "20_Literature/23_Videos": "動画",
            "20_Literature/24_SNS": "SNS投稿",
            "20_Literature/29_Other": "その他文献",
            "30_Permanent": "永続的なノート",
            "30_Evergreen": "エバーグリーンノート",
            "40_Areas": "分野別ノート",
            "70_Share": "共有用ノート",
            "90_Index": "インデックス",
            "100_Cursor": "Cursor関連",
            "100_Workflows": "ワークフロー"
        }

        # キーワードベースの分類ルール
        self.keyword_rules = {
            # 技術関連
            "100_Cursor": ["cursor", "claude", "ai", "コード", "開発", "プログラミング", "vscode"],
            "100_Workflows": ["ワークフロー", "自動化", "automation", "workflow", "手順"],
            "24_Techs": ["python", "javascript", "typescript", "bash", "shell", "tech"],

            # 文献・学習
            "20_Literature/21_Books": ["book", "書籍", "読書", "本"],
            "20_Literature/22_Articles": ["article", "記事", "ブログ", "blog"],
            "20_Literature/23_Videos": ["video", "動画", "youtube", "講座"],
            "20_Literature/24_SNS": ["twitter", "x-twitter", "sns", "ツイート", "投稿"],

            # プロジェクト・分野
            "30_Permanent": ["permanent", "永続", "知識", "コンセプト"],
            "30_Evergreen": ["evergreen", "エバーグリーン", "成長", "発展"],
            "40_Areas": ["project", "プロジェクト", "分野", "領域"],

            # メタ・管理
            "90_Index": ["index", "インデックス", "一覧", "まとめ"],
            "70_Share": ["share", "共有", "公開", "発信"],
            "10_MOCs": ["moc", "map of contents", "マップ", "目次"]
        }

    def analyze_file_content(self, file_path: Path) -> Tuple[Set[str], str]:
        """ファイル内容を分析してタグとカテゴリを抽出"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return set(), "00_Inbox"

        # タグを抽出
        tags = set(re.findall(r'#([^\s#]+)', content))

        # キーワードベースでカテゴリを判定
        content_lower = content.lower()
        title_lower = file_path.stem.lower()

        for folder, keywords in self.keyword_rules.items():
            if any(keyword in content_lower or keyword in title_lower for keyword in keywords):
                return tags, folder

        # デフォルトは受信箱
        return tags, "00_Inbox"

    def scan_vault_files(self) -> Dict[str, Tuple[Set[str], str]]:
        """Vault内のすべてのマークダウンファイルを分析"""
        file_analysis = {}

        for md_file in self.vault_path.rglob("*.md"):
            # 隠しフォルダやテンプレートは除外
            if any(part.startswith('.') for part in md_file.parts):
                continue
            if "Templates" in md_file.parts:
                continue

            tags, category = self.analyze_file_content(md_file)
            relative_path = str(md_file.relative_to(self.vault_path))
            file_analysis[relative_path] = (tags, category)

        return file_analysis

    def generate_tag_mapping(self, file_analysis: Dict[str, Tuple[Set[str], str]]) -> Dict[str, str]:
        """タグマッピングを生成"""
        tag_folder_mapping: defaultdict[str, Counter[str]] = defaultdict(Counter)

        # 各タグがどのフォルダに最も多く出現するかを集計
        for _, (tags, folder) in file_analysis.items():
            for tag in tags:
                tag_folder_mapping[tag][folder] += 1

        # 最も頻度の高いフォルダをタグにマッピング
        tag_mapping: Dict[str, str] = {}
        for tag, folder_counts in tag_folder_mapping.items():
            most_common_folder: str = folder_counts.most_common(1)[0][0]
            tag_mapping[f"#{tag}"] = most_common_folder

        return tag_mapping

    def load_current_config(self) -> Dict[str, Any]:
        """現在の設定を読み込み"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def generate_new_config(self) -> Dict[str, Any]:
        """新しい設定を生成"""
        print("Vault内のファイルを分析中...")
        file_analysis = self.scan_vault_files()

        print(f"分析したファイル数: {len(file_analysis)}")

        # タグマッピングを生成
        tag_mapping = self.generate_tag_mapping(file_analysis)

        print(f"検出されたタグ数: {len(tag_mapping)}")

        # 基本的な拡張子マッピング
        extension_mapping = {
            "md": "00_Inbox",  # デフォルトは受信箱に
            "pdf": "20_Literature",
            "png": "Assets",
            "jpg": "Assets",
            "jpeg": "Assets",
            "gif": "Assets",
            "py": "100_Cursor",
            "js": "100_Cursor",
            "ts": "100_Cursor",
            "json": "Config",
            "sh": "100_Workflows",
            "bat": "100_Workflows",
            "ps1": "100_Workflows"
        }

        # 現在の設定を基に新しい設定を構築
        current_config = self.load_current_config()

        new_config = {
            "tagEnabled": True,
            "extensionEnabled": True,
            "priority": "tag",  # タグ優先
            "extensionMapping": extension_mapping,
            "tagMapping": tag_mapping
        }

        # 既存の設定があれば一部を保持
        if current_config:
            new_config["tagEnabled"] = current_config.get("tagEnabled", True)
            new_config["extensionEnabled"] = current_config.get("extensionEnabled", True)
            new_config["priority"] = current_config.get("priority", "tag")

        return new_config

    def save_config(self, config: Dict, backup: bool = True):
        """設定を保存"""
        if backup and self.config_path.exists():
            backup_path = self.config_path.with_suffix('.json.backup')
            print(f"現在の設定をバックアップ: {backup_path}")
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(self.load_current_config(), f, ensure_ascii=False, indent=2)

        print(f"新しい設定を保存: {self.config_path}")
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def preview_changes(self) -> str:
        """変更内容をプレビュー"""
        current_config = self.load_current_config()
        new_config = self.generate_new_config()

        report = []
        report.append("=== Auto File Organizer 設定変更プレビュー ===\n")

        # タグマッピングの変更
        current_tags = set(current_config.get("tagMapping", {}).keys())
        new_tags = set(new_config["tagMapping"].keys())

        report.append(f"新規タグ数: {len(new_tags - current_tags)}")
        report.append(f"更新タグ数: {len(current_tags & new_tags)}")
        report.append(f"削除タグ数: {len(current_tags - new_tags)}")

        # 新規タグの詳細
        if new_tags - current_tags:
            report.append("\n--- 新規タグマッピング ---")
            for tag in sorted(new_tags - current_tags):
                report.append(f"{tag} → {new_config['tagMapping'][tag]}")

        # 変更されたタグの詳細
        changed_tags = []
        for tag in current_tags & new_tags:
            if current_config["tagMapping"][tag] != new_config["tagMapping"][tag]:
                changed_tags.append(tag)

        if changed_tags:
            report.append("\n--- 変更されたタグマッピング ---")
            for tag in sorted(changed_tags):
                old_folder = current_config["tagMapping"][tag]
                new_folder = new_config["tagMapping"][tag]
                report.append(f"{tag}: {old_folder} → {new_folder}")

        return "\n".join(report)

    def run_interactive(self):
        """対話的に実行"""
        print("Auto File Organizer 設定自動生成ツール")
        print("=" * 50)

        # プレビューを表示
        preview = self.preview_changes()
        print(preview)

        # 確認
        print("\n" + "=" * 50)
        response = input("設定を更新しますか？ (y/N): ").strip().lower()

        if response in ['y', 'yes']:
            new_config = self.generate_new_config()
            self.save_config(new_config)
            print("\n設定が更新されました！")
            print("Obsidianを再起動して変更を反映してください。")
        else:
            print("\nキャンセルされました。")


def main():
    vault_path = r"G:\マイドライブ\Obsidian Vault"
    generator = AutoOrganizerConfigGenerator(vault_path)
    generator.run_interactive()


if __name__ == "__main__":
    main()
