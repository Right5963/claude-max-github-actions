#!/usr/bin/env python3
"""
Obsidian自動同期システム
========================
Obsidian Vaultの変更を監視し、自動的にバックアップ・同期
"""

import os
import json
import time
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

class ObsidianAutoSync:
    def __init__(self):
        self.obsidian_path = "G:\\マイドライブ\\Obsidian Vault"
        self.backup_dir = "/mnt/c/Claude Code/tool/obsidian-cache"
        self.state_file = ".obsidian_sync_state.json"
        self.interval = 900  # 15分ごと
        self.important_dirs = [
            "Projects",
            "Daily Notes",
            "20_Stock/AI",
            "00_Core_Knowledge"
        ]
        
    def load_state(self):
        """前回の同期状態を読み込み"""
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except:
            return {"last_sync": None, "synced_files": {}}
    
    def save_state(self, state):
        """同期状態を保存"""
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def get_file_mtime(self, filepath):
        """ファイルの更新時刻を取得"""
        try:
            # PowerShell経由でWindows側のファイル情報を取得
            cmd = f'powershell.exe -Command "(Get-Item -Path \\"{filepath}\\").LastWriteTime.ToString(\\"yyyy-MM-dd HH:mm:ss\\")"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def list_obsidian_files(self):
        """Obsidian内の重要ファイルをリスト"""
        files = []
        
        # MCPブリッジ経由でファイル一覧を取得
        for important_dir in self.important_dirs:
            cmd = ["./mcp_bridge_extended.sh", "obsidian_list", important_dir]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    # 出力からファイルパスを抽出
                    for line in result.stdout.split('\n'):
                        if line.strip() and line.endswith('.md'):
                            files.append(line.strip())
            except:
                pass
        
        return files
    
    def sync_file(self, filepath):
        """個別ファイルを同期"""
        try:
            # MCPブリッジ経由でファイルを読み込み
            cmd = ["./mcp_bridge_extended.sh", "obsidian_read", filepath]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # バックアップディレクトリに保存
                backup_path = os.path.join(self.backup_dir, filepath)
                os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(result.stdout)
                
                return True
        except Exception as e:
            print(f"同期エラー: {filepath} - {e}")
        return False
    
    def check_claude_session(self):
        """Claude Codeのセッション情報をObsidianに保存"""
        try:
            # 現在のセッション情報を読み込み
            with open("current_session.json", 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            # Obsidianノートを作成
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            note_content = f"""# Claude Code セッション - {timestamp}

## セッション情報
- 開始時刻: {session_data.get('start_time', 'N/A')}
- 活動数: {len(session_data.get('activities', []))}
- メモ数: {len(session_data.get('notes', []))}

## 最近の活動
"""
            
            # 最新の活動を追加
            for activity in session_data.get('activities', [])[-5:]:
                time = activity['time'].split('T')[1][:8]
                note_content += f"- {time} - {activity['activity']}\n"
            
            if session_data.get('notes'):
                note_content += "\n## メモ\n"
                for note in session_data.get('notes', [])[-3:]:
                    time = note['time'].split('T')[1][:8]
                    note_content += f"- {time} - {note['note']}\n"
            
            # Obsidianに保存
            date_str = datetime.now().strftime("%Y-%m-%d")
            note_path = f"Daily Notes/{date_str}_Claude_Session.md"
            
            cmd = ["./mcp_bridge_extended.sh", "obsidian_write", note_path, note_content]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ セッション情報をObsidianに保存: {note_path}")
                return True
            
        except Exception as e:
            print(f"❌ セッション保存エラー: {e}")
        
        return False
    
    def sync_once(self):
        """1回の同期実行"""
        try:
            state = self.load_state()
            sync_count = 0
            error_count = 0
            
            print("🔄 Obsidian同期を開始...")
            
            # セッション情報を保存（エラーでも続行）
            try:
                self.check_claude_session()
            except Exception as e:
                print(f"⚠️ セッション保存エラー: {e}")
                error_count += 1
            
            # MCPブリッジの存在確認
            if not os.path.exists("./mcp_bridge_extended.sh"):
                print("❌ MCPブリッジが見つかりません - ローカルバックアップのみ実行")
                return self.local_backup_only()
            
            # 重要ファイルの同期
            try:
                files = self.list_obsidian_files()
                
                for filepath in files[:10]:  # エラー時は少なめに
                    try:
                        mtime = self.get_file_mtime(os.path.join(self.obsidian_path, filepath))
                        
                        # 新規または更新されたファイル
                        if filepath not in state["synced_files"] or \
                           state["synced_files"].get(filepath) != mtime:
                            if self.sync_file(filepath):
                                state["synced_files"][filepath] = mtime
                                sync_count += 1
                    except Exception as e:
                        error_count += 1
                        if error_count > 3:
                            print("⚠️ エラーが多いため同期を中断")
                            break
            except Exception as e:
                print(f"⚠️ ファイルリスト取得エラー: {e}")
            
            # 状態を保存
            state["last_sync"] = datetime.now().isoformat()
            self.save_state(state)
            
            if error_count > 0:
                print(f"⚠️ 同期完了: {sync_count}ファイル更新、{error_count}件のエラー")
            else:
                print(f"✅ 同期完了: {sync_count}ファイルを更新")
            
            return True
            
        except Exception as e:
            print(f"❌ 同期エラー: {e}")
            return False
    
    def local_backup_only(self):
        """ローカルバックアップのみ実行"""
        try:
            # セッション情報をローカルに保存
            if os.path.exists("current_session.json"):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = f"{self.backup_dir}/session_backup_{timestamp}.json"
                shutil.copy2("current_session.json", backup_file)
                print(f"✅ ローカルバックアップ完了: {backup_file}")
                return True
        except Exception as e:
            print(f"❌ バックアップエラー: {e}")
        return False
    
    def daily_summary(self):
        """日次サマリーをObsidianに作成"""
        try:
            # 今日の作業内容を集計
            summary = f"""# 日次サマリー - {datetime.now().strftime('%Y-%m-%d')}

## 本日の活動
"""
            
            # recent_work_summary.shの出力を取得
            result = subprocess.run(["./recent_work_summary.sh"], capture_output=True, text=True)
            if result.returncode == 0:
                summary += result.stdout
            
            # Obsidianに保存
            date_str = datetime.now().strftime("%Y-%m-%d")
            note_path = f"Daily Notes/{date_str}_Summary.md"
            
            cmd = ["./mcp_bridge_extended.sh", "obsidian_write", note_path, summary]
            subprocess.run(cmd, capture_output=True, text=True)
            
            print(f"✅ 日次サマリーを作成: {note_path}")
            
        except Exception as e:
            print(f"❌ サマリー作成エラー: {e}")

def main():
    """メイン関数"""
    import sys
    
    sync = ObsidianAutoSync()
    
    if len(sys.argv) > 1 and sys.argv[1] == "daemon":
        print("🤖 Obsidian自動同期デーモンを開始")
        print(f"同期間隔: {sync.interval}秒")
        
        while True:
            try:
                sync.sync_once()
                
                # 1日1回、23:50に日次サマリーを作成
                if datetime.now().strftime("%H:%M") == "23:50":
                    sync.daily_summary()
                
                time.sleep(sync.interval)
            except KeyboardInterrupt:
                print("\n⏹️ 同期を停止しました")
                break
            except Exception as e:
                print(f"❌ エラー: {e}")
                time.sleep(60)
    else:
        # 1回だけ実行
        sync.sync_once()

if __name__ == "__main__":
    main()