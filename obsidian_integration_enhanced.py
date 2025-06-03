#!/usr/bin/env python
"""
Obsidian統合強化ツール
====================
知識ベースとの連携を最適化し、正しいフォルダ構造で整理
"""

import os
import shutil
import json
import re
from datetime import datetime
from pathlib import Path

class ObsidianIntegrationEnhanced:
    def __init__(self):
        self.vault_path = Path(r"G:\マイドライブ\Obsidian Vault")
        self.inbox_path = self.vault_path / "10_Inbox"
        self.rules_path = self.vault_path / "100_Cursor"

        # フォルダ構造定義
        self.folder_structure = {
            "10_Inbox": "未分類情報の一時保管",
            "20_Literature": "外部情報ノート",
            "30_Permanent": "恒久的知識（自分の言葉で再構築）",
            "70_Share": "共有・公開用コンテンツ",
            "90_Index": "知識体系の俯瞰（MOC）",
            "100_Cursor": "システム説明とAIルール"
        }

    def check_vault_connection(self):
        """Vaultへの接続確認"""
        if not self.vault_path.exists():
            print(f"❌ Obsidian Vault not found: {self.vault_path}")
            return False

        print(f"✅ Obsidian Vault接続: {self.vault_path}")
        return True

    def analyze_inbox_contents(self):
        """Inboxの内容分析"""
        if not self.inbox_path.exists():
            print("📭 10_Inboxフォルダが存在しません")
            return []

        files = list(self.inbox_path.glob("*.md"))
        print(f"📧 10_Inbox内のファイル: {len(files)}個")

        analyzed = []
        for file in files:
            analysis = self.analyze_file_content(file)
            analyzed.append(analysis)

        return analyzed

    def analyze_file_content(self, file_path):
        """ファイル内容の分析"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            analysis = {
                'file': file_path.name,
                'path': str(file_path),
                'size': file_path.stat().st_size,
                'created': datetime.fromtimestamp(file_path.stat().st_ctime),
                'content_preview': content[:200] + "..." if len(content) > 200 else content,
                'suggested_folder': self.suggest_target_folder(file_path.name, content),
                'tags': self.extract_tags(content),
                'links': self.extract_links(content)
            }

            return analysis

        except Exception as e:
            return {
                'file': file_path.name,
                'error': str(e),
                'suggested_folder': "10_Inbox"
            }

    def suggest_target_folder(self, filename, content):
        """適切な移動先フォルダを提案"""
        # ファイル名パターン
        if "Thread by @" in filename:
            return "20_Literature/22_Articles"
        elif "Claude" in filename or "AI" in filename:
            return "20_Literature/24_Techs"
        elif "tips" in filename.lower():
            return "20_Literature/22_Articles"
        elif "Yahoo" in filename or "auction" in filename.lower():
            return "20_Literature/24_Techs"

        # 内容分析
        content_lower = content.lower()
        if "twitter" in content_lower or "x.com" in content_lower:
            return "20_Literature/22_Articles"
        elif "ai" in content_lower or "claude" in content_lower:
            return "20_Literature/24_Techs"
        elif "プログラミング" in content or "coding" in content_lower:
            return "20_Literature/24_Techs"
        elif "philosophy" in content_lower or "哲学" in content:
            return "20_Literature/Philosophy"

        # デフォルト
        return "20_Literature"

    def extract_tags(self, content):
        """Obsidianタグを抽出"""
        tags = re.findall(r'#[\w\-/]+', content)
        return tags

    def extract_links(self, content):
        """Obsidianリンクを抽出"""
        links = re.findall(r'\[\[(.*?)\]\]', content)
        return links

    def organize_inbox_properly(self, dry_run=True):
        """正しいルールに従ってInboxを整理"""
        analyzed_files = self.analyze_inbox_contents()

        if not analyzed_files:
            print("📭 整理するファイルがありません")
            return

        print(f"\n📋 整理計画 ({'干运行' if dry_run else '実行中'}):")
        print("=" * 60)

        for analysis in analyzed_files:
            if 'error' in analysis:
                print(f"❌ {analysis['file']}: {analysis['error']}")
                continue

            target_folder = analysis['suggested_folder']
            print(f"📄 {analysis['file']}")
            print(f"   → {target_folder}")
            print(f"   📏 サイズ: {analysis['size']} bytes")
            print(f"   🏷️ タグ: {', '.join(analysis['tags']) if analysis['tags'] else 'なし'}")
            print(f"   📝 プレビュー: {analysis['content_preview'][:100]}...")
            print()

            if not dry_run:
                self.move_file_to_folder(analysis['path'], target_folder)

    def move_file_to_folder(self, source_path, target_folder):
        """ファイルを指定フォルダに移動"""
        source = Path(source_path)
        target_dir = self.vault_path / target_folder

        # ターゲットディレクトリ作成
        target_dir.mkdir(parents=True, exist_ok=True)

        # ファイル移動
        target_path = target_dir / source.name

        # 重複回避
        counter = 1
        while target_path.exists():
            name_parts = source.stem, counter, source.suffix
            target_path = target_dir / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
            counter += 1

        try:
            shutil.move(str(source), str(target_path))
            print(f"✅ 移動完了: {source.name} → {target_folder}")
        except Exception as e:
            print(f"❌ 移動失敗: {source.name} - {str(e)}")

    def create_inbox_summary(self):
        """Inbox整理のサマリーを作成"""
        analyzed_files = self.analyze_inbox_contents()

        summary = {
            'date': datetime.now().isoformat(),
            'total_files': len(analyzed_files),
            'files': analyzed_files,
            'folder_distribution': {}
        }

        # フォルダ別集計
        for analysis in analyzed_files:
            if 'error' not in analysis:
                folder = analysis['suggested_folder']
                if folder not in summary['folder_distribution']:
                    summary['folder_distribution'][folder] = 0
                summary['folder_distribution'][folder] += 1

        # サマリー保存
        with open('inbox_analysis_summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2, default=str)

        print("📊 Inbox分析サマリー保存: inbox_analysis_summary.json")
        return summary

    def check_system_integration(self):
        """システム統合状況をチェック"""
        print("🔗 Obsidian-Cursor-Claude統合チェック")
        print("=" * 50)

        checks = [
            ("Obsidian Vault接続", self.vault_path.exists()),
            ("フォルダ構造", all((self.vault_path / folder).exists() for folder in self.folder_structure.keys())),
            ("ルールファイル", (self.rules_path / "101_フォルダ構造.md").exists()),
            ("Cursor設定", (self.vault_path / ".cursor-rules.json").exists()),
            ("MCP設定", (self.vault_path / "MCP").exists())
        ]

        all_good = True
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"{status} {check_name}")
            if not result:
                all_good = False

        if all_good:
            print("\n🎉 システム統合は完璧です！")
        else:
            print("\n⚠️ 一部の統合に問題があります")

        return all_good

def main():
    """メイン実行"""
    print("🔗 Obsidian統合強化ツール")
    print("=" * 40)

    integration = ObsidianIntegrationEnhanced()

    # Step 1: 基本チェック
    if not integration.check_vault_connection():
        return

    # Step 2: システム統合チェック
    integration.check_system_integration()

    # Step 3: Inbox分析
    print("\n" + "=" * 50)
    summary = integration.create_inbox_summary()

    # Step 4: 整理提案（dry run）
    print(f"\n📋 整理提案（{summary['total_files']}ファイル）:")
    integration.organize_inbox_properly(dry_run=True)

    print("\n📝 次のステップ:")
    print("1. 提案内容を確認")
    print("2. integration.organize_inbox_properly(dry_run=False) で実行")
    print("3. システムが正常に統合されていることを確認")

if __name__ == "__main__":
    main()
