#!/usr/bin/env python3
"""
Claude Code 完全自動起動システム
==============================
記録は宝 - 自動記録・自動活用の完全システム

起動時に必ず実行すべき最重要システム:
1. 脳みそ（Obsidian）への自動記録開始
2. 継続的活動監視
3. 過去の知識の強制的活用
4. リアルタイム記録システム

これがClaude起動時に自動で起動すべき真のシステム
"""

import subprocess
import os
import sys
import time
from datetime import datetime
from pathlib import Path
import threading

class ClaudeAutoStartComplete:
    def __init__(self):
        self.tool_path = Path("/mnt/c/Claude Code/tool")
        os.chdir(self.tool_path)
        
        self.start_time = datetime.now()
        self.pids = {}  # 起動したプロセスのPID管理

    def show_startup_header(self):
        """起動ヘッダー表示"""
        print("🚀 Claude Code 完全自動起動システム")
        print("=" * 60)
        print(f"📅 {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎯 記録は宝 - 自動記録・自動活用開始")
        print()

    def start_brain_system(self):
        """脳みそ（Obsidian）システム開始 - 最重要"""
        print("🧠 Obsidian脳みそシステム起動中...")
        try:
            from obsidian_brain_system import ObsidianBrainSystem
            
            # 脳みそシステム初期化
            brain = ObsidianBrainSystem()
            
            # 強制的知識レビュー
            brain.force_knowledge_review()
            
            # バックグラウンド監視開始
            brain.start_continuous_brain_monitoring()
            
            print("✅ 脳みそシステム起動完了")
            
            # 起動成功を記録
            brain.record_insight("システム起動", "Claude Code完全自動起動システム開始", 
                f"PID: {os.getpid()}, 時刻: {self.start_time}")
            
            return brain
            
        except Exception as e:
            print(f"❌ 脳みそシステム起動エラー: {e}")
            return None

    def start_git_monitoring(self):
        """Git自動監視開始"""
        print("📝 Git自動監視システム起動中...")
        try:
            # smart_git_auto_commit daemon起動
            proc = subprocess.Popen([
                "python3", "smart_git_auto_commit.py", "daemon"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            self.pids['git_daemon'] = proc.pid
            print(f"✅ Git自動監視起動完了 (PID: {proc.pid})")
            
        except Exception as e:
            print(f"❌ Git監視起動エラー: {e}")

    def start_continuous_recorder(self):
        """継続記録システム開始"""
        print("📊 継続記録システム起動中...")
        try:
            # continuous_recorder をバックグラウンドで起動
            proc = subprocess.Popen([
                "python3", "continuous_recorder.py"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            self.pids['continuous_recorder'] = proc.pid
            print(f"✅ 継続記録システム起動完了 (PID: {proc.pid})")
            
        except Exception as e:
            print(f"❌ 継続記録起動エラー: {e}")

    def perform_startup_analysis(self):
        """起動時分析実行"""
        print("📊 起動時システム分析実行中...")
        try:
            # git_quick_insight実行
            result = subprocess.run([
                "python3", "git_quick_insight.py"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("📈 開発状況分析:")
                # 重要な部分のみ表示
                lines = result.stdout.split('\n')
                for line in lines:
                    if '未コミット変更' in line or '推奨アクション' in line or 'コミット数' in line:
                        print(f"   {line.strip()}")
                        
            else:
                print("⚠️ Git分析でエラーが発生")
                
        except Exception as e:
            print(f"⚠️ 起動時分析エラー: {e}")

    def check_system_health(self):
        """システム健全性チェック"""
        print("🏥 システム健全性チェック...")
        try:
            py_files = len(list(self.tool_path.glob("*.py")))
            sh_files = len(list(self.tool_path.glob("*.sh")))
            total = py_files + sh_files
            
            print(f"📊 現在のシステム数: {total}個 (Python: {py_files}, Shell: {sh_files})")
            
            if total > 80:
                print("⚠️ システム数が多すぎます - 整理を検討")
            elif total > 70:
                print("🔔 システム数がやや多めです")
            else:
                print("✅ システム数は適切です")
                
        except Exception as e:
            print(f"⚠️ システムチェックエラー: {e}")

    def show_quick_commands(self):
        """よく使うコマンド表示"""
        print()
        print("💡 今すぐ使えるコマンド:")
        print("   python3 git_quick_insight.py      # 開発状況再分析")
        print("   python3 smart_git_auto_commit.py  # 手動コミット判定") 
        print("   ./mcp_bridge_extended.sh          # Obsidian操作")
        print("   python3 claude_session_reminder.py # 重要事項確認")
        print()

    def create_pid_file(self):
        """PIDファイル作成"""
        try:
            pid_info = {
                "main_pid": os.getpid(),
                "start_time": self.start_time.isoformat(),
                "child_pids": self.pids
            }
            
            with open(".claude_auto_start.pid", 'w') as f:
                import json
                json.dump(pid_info, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ PIDファイル作成エラー: {e}")

    def run_complete_startup(self):
        """完全自動起動実行"""
        self.show_startup_header()
        
        # 1. 最重要: 脳みそシステム起動
        brain = self.start_brain_system()
        
        # 2. Git自動監視開始
        self.start_git_monitoring()
        
        # 3. 継続記録システム開始
        self.start_continuous_recorder()
        
        # 4. 起動時分析実行
        self.perform_startup_analysis()
        
        # 5. システム健全性確認
        self.check_system_health()
        
        # 6. PIDファイル作成
        self.create_pid_file()
        
        # 7. 完了メッセージ
        print()
        print("🎉 Claude Code 完全自動起動完了！")
        print("=" * 60)
        print("📝 すべての記録システムが稼働中")
        print("🧠 Obsidianで今日の記録を確認可能")
        print("🔄 バックグラウンドで継続的監視実行中")
        
        # 8. よく使うコマンド表示
        self.show_quick_commands()
        
        print("🚀 開発作業を開始できます！")
        print()
        
        return brain

def main():
    """メイン実行"""
    startup_system = ClaudeAutoStartComplete()
    
    try:
        brain = startup_system.run_complete_startup()
        
        # 記録システムが稼働中であることを定期的に確認
        print("📝 記録システム監視中... (Ctrl+C で停止)")
        
        while True:
            time.sleep(300)  # 5分間隔でチェック
            
            # プロセス生存確認
            for name, pid in startup_system.pids.items():
                try:
                    os.kill(pid, 0)  # プロセス存在確認
                except OSError:
                    print(f"⚠️ {name} (PID: {pid}) が停止しています")
            
    except KeyboardInterrupt:
        print("\n🛑 自動起動システム停止指示受信")
        
        # 各プロセスの停止
        for name, pid in startup_system.pids.items():
            try:
                os.kill(pid, 15)  # SIGTERM
                print(f"🔄 {name} (PID: {pid}) に停止シグナル送信")
            except OSError:
                pass
        
        # PIDファイル削除
        try:
            os.remove(".claude_auto_start.pid")
        except:
            pass
            
        print("✅ 自動起動システム停止完了")

if __name__ == "__main__":
    main()