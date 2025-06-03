#!/usr/bin/env python
"""
日常ワークフロー最適化ツール
===========================
Obsidian知識ベースとCursorを活用した効率的な作業フロー
"""

import os
import json
import subprocess
from datetime import datetime, date
from pathlib import Path

class DailyWorkflowOptimizer:
    def __init__(self):
        self.vault_path = Path(r"G:\マイドライブ\Obsidian Vault")
        self.workspace_path = Path(".")
        self.today = date.today()

    def start_daily_session(self):
        """日次セッションを開始"""
        print("🌅 Obsidian-Cursor 日次ワークフロー開始")
        print("=" * 50)

        # Step 1: システム健全性チェック
        print("📊 システム健全性チェック...")
        self.quick_health_check()

        # Step 2: 知識ベース接続確認
        print("\n🔗 知識ベース接続確認...")
        self.check_knowledge_base()

        # Step 3: 今日の作業環境準備
        print(f"\n📅 {self.today} の作業環境準備...")
        self.setup_daily_environment()

        # Step 4: 推奨アクション提案
        print("\n💡 今日の推奨アクション...")
        self.suggest_daily_actions()

    def quick_health_check(self):
        """高速健全性チェック"""
        try:
            result = subprocess.run(
                ['python', 'system_health_simple.py'],
                capture_output=True,
                timeout=10,
                text=True
            )

            if result.returncode == 0:
                lines = result.stdout.split('\n')
                health_line = [line for line in lines if '基本健全性:' in line]
                if health_line:
                    print(f"✅ {health_line[0].split('🎯 ')[1]}")
                else:
                    print("✅ システム正常動作中")
            else:
                print("⚠️ 軽微な問題あり（詳細はsystem_health_simple.pyで確認）")

        except Exception as e:
            print(f"❌ ヘルスチェック実行エラー: {str(e)[:50]}")

    def check_knowledge_base(self):
        """知識ベース接続状況確認"""
        if self.vault_path.exists():
            # 主要フォルダの存在確認
            folders = ["10_Inbox", "20_Literature", "30_Permanent", "100_Cursor"]
            existing = [f for f in folders if (self.vault_path / f).exists()]

            print(f"✅ Vault接続: {len(existing)}/{len(folders)} フォルダ確認")

            # 最近更新されたファイルを確認
            recent_files = self.get_recent_vault_updates()
            if recent_files:
                print(f"📝 最近更新: {len(recent_files)}ファイル")

        else:
            print("❌ Obsidian Vault未接続")

    def get_recent_vault_updates(self, days=7):
        """最近更新されたVaultファイルを取得"""
        recent_files = []
        if not self.vault_path.exists():
            return recent_files

        try:
            from datetime import datetime, timedelta
            cutoff = datetime.now() - timedelta(days=days)

            for md_file in self.vault_path.rglob("*.md"):
                if md_file.stat().st_mtime > cutoff.timestamp():
                    recent_files.append(md_file)

            return recent_files[:10]  # 最新10ファイル

        except Exception:
            return []

    def setup_daily_environment(self):
        """今日の作業環境セットアップ"""
        # 今日のセッションファイル作成
        session_file = f"session_{self.today.strftime('%Y%m%d')}.json"

        session_data = {
            'date': str(self.today),
            'start_time': datetime.now().isoformat(),
            'workspace': str(self.workspace_path.absolute()),
            'vault_connection': self.vault_path.exists(),
            'tasks': [],
            'insights': [],
            'files_accessed': []
        }

        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

        print(f"📄 セッションファイル作成: {session_file}")

        # Inboxファイル確認
        if self.vault_path.exists():
            inbox_path = self.vault_path / "10_Inbox"
            if inbox_path.exists():
                inbox_files = list(inbox_path.glob("*.md"))
                if inbox_files:
                    print(f"📥 Inbox処理推奨: {len(inbox_files)}ファイル")
                else:
                    print("📭 Inbox: 整理済み")

    def suggest_daily_actions(self):
        """今日の推奨アクション提案"""
        suggestions = [
            "🔍 python system_health_simple.py で詳細システム状況確認",
            "📚 Obsidian Vaultの新規ノート作成・既存ノート更新",
            "🤖 Claude-Cursor連携でのコード開発・レビュー",
            "📊 why.py でプロジェクトの課題分析",
            "💡 simple_itrs.py で統合思考リサーチ"
        ]

        # Inboxファイルがある場合の提案追加
        if self.vault_path.exists():
            inbox_path = self.vault_path / "10_Inbox"
            if inbox_path.exists() and list(inbox_path.glob("*.md")):
                suggestions.insert(1, "📥 python obsidian_integration_enhanced.py で Inbox整理")

        print("📋 推奨アクション:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"   {i}. {suggestion}")

        print(f"\n🎯 今日の目標: Obsidian知識ベースを活用した高効率AI開発")

    def create_daily_summary(self):
        """今日のセッションサマリーを作成"""
        session_file = f"session_{self.today.strftime('%Y%m%d')}.json"

        if os.path.exists(session_file):
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)

            # 終了時間追加
            session_data['end_time'] = datetime.now().isoformat()
            session_data['duration_hours'] = round(
                (datetime.now() - datetime.fromisoformat(session_data['start_time'])).total_seconds() / 3600, 2
            )

            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)

            print(f"📊 セッションサマリー更新: {session_file}")
            print(f"⏱️ 作業時間: {session_data['duration_hours']}時間")

    def obsidian_quick_access(self):
        """Obsidianへのクイックアクセス機能"""
        if not self.vault_path.exists():
            print("❌ Obsidian Vault未接続")
            return

        print("🚀 Obsidianクイックアクセス")
        print("=" * 30)

        # 最近のファイル
        recent_files = self.get_recent_vault_updates(days=3)
        if recent_files:
            print("📝 最近更新されたファイル:")
            for i, file in enumerate(recent_files[:5], 1):
                rel_path = file.relative_to(self.vault_path)
                print(f"   {i}. {rel_path}")

        # フォルダ構造概要
        main_folders = ["10_Inbox", "20_Literature", "30_Permanent", "70_Share", "90_Index"]
        print("\n📁 主要フォルダ:")
        for folder in main_folders:
            folder_path = self.vault_path / folder
            if folder_path.exists():
                file_count = len(list(folder_path.rglob("*.md")))
                print(f"   📂 {folder}: {file_count}ファイル")

def main():
    """メイン実行"""
    optimizer = DailyWorkflowOptimizer()

    print("🎯 日常ワークフロー最適化ツール")
    print("選択してください:")
    print("1. 日次セッション開始")
    print("2. Obsidianクイックアクセス")
    print("3. セッションサマリー作成")
    print("4. 自動実行（セッション開始）")

    choice = input("\n選択 (1-4): ").strip()

    if choice == "1":
        optimizer.start_daily_session()
    elif choice == "2":
        optimizer.obsidian_quick_access()
    elif choice == "3":
        optimizer.create_daily_summary()
    else:
        # デフォルト：自動実行
        optimizer.start_daily_session()

if __name__ == "__main__":
    main()
