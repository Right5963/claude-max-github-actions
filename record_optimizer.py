#!/usr/bin/env python3
"""
記録整理・最適化システム
====================
蓄積された記録の継続的整理・最適化・管理

機能:
- 重複記録の除去
- 古い記録のアーカイブ
- 記録の要約・圧縮
- 検索インデックス作成
- ストレージ使用量監視
- 重要度による分類
"""

import os
import json
import shutil
import hashlib
import gzip
from datetime import datetime, timedelta
from pathlib import Path
import threading
import time
import subprocess

class RecordOptimizer:
    def __init__(self):
        self.tool_path = Path("/mnt/c/Claude Code/tool")
        self.obsidian_path = Path("G:/マイドライブ/Obsidian Vault")
        
        # アーカイブディレクトリ
        self.archive_dir = self.tool_path / "record_archive"
        self.compressed_dir = self.archive_dir / "compressed"
        self.index_dir = self.archive_dir / "indices"
        
        # 設定
        self.max_daily_records = 100  # 1日最大100記録
        self.archive_after_days = 30  # 30日後にアーカイブ
        self.compress_after_days = 7   # 7日後に圧縮
        self.max_storage_mb = 500     # 最大500MB
        
        self.setup_directories()
        self.start_optimization()

    def setup_directories(self):
        """ディレクトリ構造作成"""
        self.archive_dir.mkdir(exist_ok=True)
        self.compressed_dir.mkdir(exist_ok=True)
        self.index_dir.mkdir(exist_ok=True)
        
        print(f"📁 記録整理ディレクトリ準備完了: {self.archive_dir}")

    def start_optimization(self):
        """記録整理開始"""
        print("🔄 記録整理・最適化システム開始")
        
        # 初回の全体整理
        self.perform_full_optimization()
        
        # 継続的監視開始
        self.start_continuous_monitoring()

    def perform_full_optimization(self):
        """全体最適化実行"""
        print("🧹 記録全体最適化実行中...")
        
        # 1. 重複除去
        duplicates_removed = self.remove_duplicates()
        
        # 2. 古い記録のアーカイブ
        archived_count = self.archive_old_records()
        
        # 3. 記録の圧縮 (無効化)
        compressed_count = 0  # 圧縮は無効
        
        # 4. インデックス作成
        self.create_search_index()
        
        # 5. ストレージ使用量チェック
        storage_info = self.check_storage_usage()
        
        # 結果記録
        optimization_result = {
            "timestamp": datetime.now().isoformat(),
            "duplicates_removed": duplicates_removed,
            "archived_count": archived_count,
            "compressed_count": compressed_count,
            "storage_info": storage_info
        }
        
        self.log_optimization_result(optimization_result)
        
        print(f"✅ 全体最適化完了: 重複除去{duplicates_removed}件, アーカイブ{archived_count}件")

    def remove_duplicates(self):
        """重複記録除去"""
        print("🔍 重複記録検出・除去中...")
        
        duplicates_removed = 0
        seen_hashes = set()
        
        # JSONファイルの重複チェック
        for json_file in self.tool_path.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                content_hash = hashlib.md5(content.encode()).hexdigest()
                
                if content_hash in seen_hashes:
                    # 重複ファイル削除
                    backup_path = self.archive_dir / f"duplicate_{json_file.name}"
                    shutil.move(json_file, backup_path)
                    duplicates_removed += 1
                    print(f"  重複除去: {json_file.name}")
                else:
                    seen_hashes.add(content_hash)
                    
            except Exception as e:
                print(f"⚠️ 重複チェックエラー {json_file}: {e}")
        
        # ログファイルの重複行除去
        for log_file in self.tool_path.glob("*.log"):
            try:
                duplicates_removed += self.remove_duplicate_lines(log_file)
            except Exception as e:
                print(f"⚠️ ログ重複除去エラー {log_file}: {e}")
        
        return duplicates_removed

    def remove_duplicate_lines(self, log_file):
        """ログファイルの重複行除去"""
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            unique_lines = []
            seen_lines = set()
            removed_count = 0
            
            for line in lines:
                line_hash = hashlib.md5(line.strip().encode()).hexdigest()
                if line_hash not in seen_lines:
                    unique_lines.append(line)
                    seen_lines.add(line_hash)
                else:
                    removed_count += 1
            
            if removed_count > 0:
                # バックアップ作成
                backup_path = self.archive_dir / f"{log_file.name}.backup"
                shutil.copy2(log_file, backup_path)
                
                # 重複除去版で上書き
                with open(log_file, 'w', encoding='utf-8') as f:
                    f.writelines(unique_lines)
                
                print(f"  {log_file.name}: {removed_count}行の重複除去")
            
            return removed_count
            
        except Exception as e:
            print(f"⚠️ {log_file}の重複行除去エラー: {e}")
            return 0

    def archive_old_records(self):
        """古い記録のアーカイブ"""
        print("📦 古い記録アーカイブ中...")
        
        cutoff_date = datetime.now() - timedelta(days=self.archive_after_days)
        archived_count = 0
        
        # 古いJSONファイルをアーカイブ
        for json_file in self.tool_path.glob("*.json"):
            try:
                file_mtime = datetime.fromtimestamp(json_file.stat().st_mtime)
                
                if file_mtime < cutoff_date:
                    archive_path = self.archive_dir / json_file.name
                    shutil.move(json_file, archive_path)
                    archived_count += 1
                    print(f"  アーカイブ: {json_file.name}")
                    
            except Exception as e:
                print(f"⚠️ アーカイブエラー {json_file}: {e}")
        
        # 古いログファイルをアーカイブ
        for log_file in self.tool_path.glob("*.log"):
            try:
                file_mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                
                if file_mtime < cutoff_date and log_file.stat().st_size > 1024 * 1024:  # 1MB以上
                    archive_path = self.archive_dir / log_file.name
                    shutil.move(log_file, archive_path)
                    archived_count += 1
                    print(f"  大容量ログアーカイブ: {log_file.name}")
                    
            except Exception as e:
                print(f"⚠️ ログアーカイブエラー {log_file}: {e}")
        
        return archived_count

    def compress_old_records(self):
        """古い記録の圧縮 (無効化)"""
        print("🚫 圧縮機能は無効化されています")
        return 0  # 圧縮は実行しない

    def create_search_index(self):
        """検索インデックス作成"""
        print("🔍 検索インデックス作成中...")
        
        try:
            index_data = {
                "created": datetime.now().isoformat(),
                "files": {},
                "keywords": {},
                "daily_summary": {}
            }
            
            # 現在のファイルをインデックス化
            for json_file in self.tool_path.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        content = json.load(f)
                    
                    file_info = {
                        "size": json_file.stat().st_size,
                        "modified": datetime.fromtimestamp(json_file.stat().st_mtime).isoformat(),
                        "type": "session" if "session" in json_file.name else "data",
                        "activities_count": len(content.get("activities", [])) if isinstance(content, dict) else 0
                    }
                    
                    index_data["files"][json_file.name] = file_info
                    
                except Exception as e:
                    print(f"⚠️ インデックス化エラー {json_file}: {e}")
            
            # インデックス保存
            index_file = self.index_dir / f"search_index_{datetime.now().strftime('%Y%m%d')}.json"
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 検索インデックス作成完了: {index_file}")
            
        except Exception as e:
            print(f"⚠️ インデックス作成エラー: {e}")

    def check_storage_usage(self):
        """ストレージ使用量チェック"""
        total_size = 0
        file_count = 0
        
        # tool ディレクトリのサイズ
        for file_path in self.tool_path.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
                file_count += 1
        
        storage_info = {
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "file_count": file_count,
            "max_size_mb": self.max_storage_mb,
            "usage_percent": round((total_size / (1024 * 1024)) / self.max_storage_mb * 100, 1)
        }
        
        print(f"💾 ストレージ使用量: {storage_info['total_size_mb']}MB ({storage_info['usage_percent']}%)")
        
        # 使用量が上限を超えている場合の警告
        if storage_info["usage_percent"] > 80:
            print(f"⚠️ ストレージ使用量が{storage_info['usage_percent']}%に達しています")
            self.emergency_cleanup()
        
        return storage_info

    def emergency_cleanup(self):
        """緊急クリーンアップ"""
        print("🚨 緊急クリーンアップ実行中...")
        
        # 大きなログファイルを強制アーカイブ
        for log_file in self.tool_path.glob("*.log"):
            if log_file.stat().st_size > 10 * 1024 * 1024:  # 10MB以上
                archive_path = self.archive_dir / f"emergency_{log_file.name}"
                shutil.move(log_file, archive_path)
                print(f"  緊急アーカイブ: {log_file.name}")
        
        # 古いセッションファイルを強制削除
        for session_file in self.tool_path.glob("session_*.json"):
            file_age = datetime.now() - datetime.fromtimestamp(session_file.stat().st_mtime)
            if file_age.days > 3:  # 3日以上古い
                session_file.unlink()
                print(f"  古いセッション削除: {session_file.name}")

    def log_optimization_result(self, result):
        """最適化結果記録"""
        try:
            log_file = self.tool_path / "record_optimization.log"
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{json.dumps(result, ensure_ascii=False)}\n")
            
            # Obsidianにも記録
            self.log_to_obsidian(result)
            
        except Exception as e:
            print(f"⚠️ 最適化結果記録エラー: {e}")

    def log_to_obsidian(self, result):
        """Obsidian記録"""
        try:
            today = datetime.now().strftime("%Y%m%d")
            obsidian_file = f"G:\\マイドライブ\\Obsidian Vault\\Record_Optimization_{today}.md"
            
            optimization_record = f"""
## {datetime.now().strftime('%H:%M:%S')} - 記録最適化実行

**実行結果:**
- 重複除去: {result['duplicates_removed']}件
- アーカイブ: {result['archived_count']}件  
- 圧縮: {result['compressed_count']}件
- ストレージ使用量: {result['storage_info']['total_size_mb']}MB ({result['storage_info']['usage_percent']}%)

**効果:**
- 記録の品質向上
- ストレージ効率化
- 検索性能向上

---
"""
            
            ps_command = f'''
            Add-Content -Path "{obsidian_file}" -Value @"
{optimization_record}
"@ -Encoding UTF8
            '''
            
            subprocess.run([
                "powershell.exe", "-Command", ps_command
            ], capture_output=True, timeout=30)
            
        except Exception as e:
            print(f"⚠️ Obsidian記録エラー: {e}")

    def start_continuous_monitoring(self):
        """継続的監視開始"""
        print("🔄 継続的記録監視開始...")
        
        def monitoring_loop():
            while True:
                try:
                    # 1時間ごとの軽量最適化
                    if int(time.time()) % 3600 == 0:  # 1時間
                        self.light_optimization()
                    
                    # 24時間ごとの全体最適化
                    if int(time.time()) % 86400 == 0:  # 24時間
                        self.perform_full_optimization()
                    
                    time.sleep(300)  # 5分間隔でチェック
                    
                except Exception as e:
                    print(f"⚠️ 監視ループエラー: {e}")
                    time.sleep(300)
        
        # バックグラウンドで監視開始
        monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitor_thread.start()

    def light_optimization(self):
        """軽量最適化"""
        try:
            # 重複除去のみ実行
            duplicates = self.remove_duplicates()
            if duplicates > 0:
                print(f"🧹 軽量最適化: {duplicates}件の重複除去")
                
        except Exception as e:
            print(f"⚠️ 軽量最適化エラー: {e}")

def main():
    """メイン実行"""
    print("🔧 記録整理・最適化システム開始")
    
    optimizer = RecordOptimizer()
    
    try:
        print("📝 記録整理システム稼働中... (Ctrl+C で停止)")
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n🛑 記録整理システム停止")

if __name__ == "__main__":
    main()