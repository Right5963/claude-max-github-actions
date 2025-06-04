#!/usr/bin/env python3
"""
Git Daily Driver - 神ツール日常運用版
====================================
TAL思考 + Obsidian知識 = 毎日使われる実用ツール
"""

import subprocess
import os
import json
from datetime import datetime

class GitDailyDriver:
    def __init__(self):
        self.repo_path = "/mnt/c/Claude Code/tool"
        
    def quick_commit(self, message=None):
        """1秒コミット: 日常最頻出操作"""
        print("⚡ Quick Commit")
        
        # 変更確認
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=self.repo_path
        ).stdout.strip()
        
        if not status:
            print("📝 変更なし - コミット不要")
            return False
        
        # スマートメッセージ生成
        if not message:
            file_count = len(status.split('\n'))
            timestamp = datetime.now().strftime("%H:%M")
            message = f"Auto-commit: Work in progress ({file_count} files) - {timestamp}"
        
        # 実行
        result = subprocess.run([
            "bash", "-c", f"cd '{self.repo_path}' && git add . && git commit -m '{message}'"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Committed: {message}")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    
    def sync_now(self):
        """1秒同期: push/pull自動判定"""
        print("🔄 Smart Sync")
        
        # リモート状況確認
        subprocess.run(["git", "fetch"], cwd=self.repo_path, capture_output=True)
        
        # ahead/behind確認
        result = subprocess.run([
            "git", "rev-list", "--count", "--left-right", "HEAD...origin/master"
        ], capture_output=True, text=True, cwd=self.repo_path)
        
        if result.stdout.strip():
            ahead, behind = result.stdout.strip().split('\t')
            ahead, behind = int(ahead), int(behind)
            
            if behind > 0:
                print(f"⬇️  Pulling {behind} commits...")
                pull_result = subprocess.run(
                    ["git", "pull"], cwd=self.repo_path, capture_output=True, text=True
                )
                print("✅ Pull completed" if pull_result.returncode == 0 else f"❌ Pull failed: {pull_result.stderr}")
            
            if ahead > 0:
                print(f"⬆️  Pushing {ahead} commits...")
                push_result = subprocess.run(
                    ["git", "push"], cwd=self.repo_path, capture_output=True, text=True
                )
                print("✅ Push completed" if push_result.returncode == 0 else f"❌ Push failed: {push_result.stderr}")
            
            if ahead == 0 and behind == 0:
                print("✅ Already in sync")
        else:
            print("ℹ️  No remote tracking")
    
    def save_session(self):
        """セッション保存: 作業状況をObsidianに記録"""
        print("💾 Saving Session")
        
        # 現在の状況を取得
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, cwd=self.repo_path
        ).stdout.strip()
        
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=self.repo_path
        ).stdout.strip()
        
        recent_commits = subprocess.run(
            ["git", "log", "--oneline", "-3"],
            capture_output=True, text=True, cwd=self.repo_path
        ).stdout.strip()
        
        # セッション記録作成
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        session_data = {
            "timestamp": timestamp,
            "branch": branch,
            "uncommitted_changes": len(status.split('\n')) if status else 0,
            "recent_work": recent_commits.split('\n')
        }
        
        # ローカル保存
        session_file = f"sessions/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs("sessions", exist_ok=True)
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"✅ Session saved: {session_file}")
        
        # Obsidian Daily Note更新
        self._update_daily_note(session_data)
        
        return session_data
    
    def _update_daily_note(self, session_data):
        """Daily Noteに作業記録を追加"""
        today = datetime.now().strftime("%Y-%m-%d")
        note_content = f"""
## Git Session - {session_data['timestamp']}
- **Branch**: {session_data['branch']}
- **Uncommitted**: {session_data['uncommitted_changes']} files
- **Recent Work**:
{chr(10).join(f"  - {commit}" for commit in session_data['recent_work'][:3])}

"""
        
        try:
            # PowerShell経由でObsidian Daily Noteに追記
            ps_command = f"""
$dailyNote = "G:\\マイドライブ\\Obsidian Vault\\Daily Notes\\{today}.md"
$content = @'
{note_content.strip()}
'@
Add-Content -Path $dailyNote -Value $content -Encoding UTF8
"""
            
            subprocess.run([
                "powershell.exe", "-Command", ps_command
            ], capture_output=True)
            
            print(f"📝 Updated Daily Note: {today}.md")
            
        except Exception as e:
            print(f"⚠️ Daily Note update skipped: {str(e)[:30]}...")
    
    def work_status(self):
        """作業状況の1秒確認"""
        print("📊 Work Status")
        
        # 基本情報
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, cwd=self.repo_path
        ).stdout.strip()
        
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=self.repo_path
        ).stdout.strip()
        
        changes = len(status.split('\n')) if status else 0
        
        # 今日のコミット数
        today_commits = subprocess.run([
            "git", "log", "--since=today", "--oneline"
        ], capture_output=True, text=True, cwd=self.repo_path).stdout.strip()
        
        commit_count = len(today_commits.split('\n')) if today_commits else 0
        
        print(f"🌿 Branch: {branch}")
        print(f"📝 Uncommitted: {changes} files")
        print(f"📅 Today's commits: {commit_count}")
        
        # 推奨アクション
        if changes > 0:
            print("💡 Recommended: git-daily quick")
        elif commit_count > 0:
            print("💡 Recommended: git-daily sync")
        else:
            print("✨ All clean!")

def main():
    """メイン: 超シンプルインターフェース"""
    import sys
    
    driver = GitDailyDriver()
    
    if len(sys.argv) < 2:
        print("🚀 Git Daily Driver")
        print("使用方法:")
        print("  git-daily quick [message]  # クイックコミット")
        print("  git-daily sync             # スマート同期") 
        print("  git-daily save             # セッション保存")
        print("  git-daily status           # 作業状況確認")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "quick":
        message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
        driver.quick_commit(message)
    elif cmd == "sync":
        driver.sync_now()
    elif cmd == "save":
        driver.save_session()
    elif cmd == "status":
        driver.work_status()
    else:
        print(f"❌ Unknown command: {cmd}")

if __name__ == "__main__":
    main()