#!/usr/bin/env python3
"""
日次レポート自動生成システム
============================
毎日の活動を自動的に集計してレポート生成
"""

import os
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

class DailyReportAuto:
    def __init__(self):
        self.report_dir = "daily_reports"
        self.valuable_output_dir = "valuable_systems_output"
        os.makedirs(self.report_dir, exist_ok=True)
        
    def get_session_activities(self):
        """今日のセッション活動を取得"""
        activities = []
        today = datetime.now().date()
        
        # current_session.jsonから
        try:
            with open("current_session.json", 'r', encoding='utf-8') as f:
                session_data = json.load(f)
                
            for activity in session_data.get('activities', []):
                activity_time = datetime.fromisoformat(activity['time'].replace('T', ' '))
                if activity_time.date() == today:
                    activities.append({
                        'time': activity_time.strftime('%H:%M:%S'),
                        'activity': activity['activity']
                    })
        except:
            pass
        
        # sessionsフォルダから過去のセッションも確認
        sessions_dir = Path("sessions")
        if sessions_dir.exists():
            for session_file in sessions_dir.glob("session_*.json"):
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    for activity in data.get('activities', []):
                        activity_time = datetime.fromisoformat(activity['time'].replace('T', ' '))
                        if activity_time.date() == today:
                            activities.append({
                                'time': activity_time.strftime('%H:%M:%S'),
                                'activity': activity['activity']
                            })
                except:
                    continue
        
        return sorted(activities, key=lambda x: x['time'])
    
    def get_git_commits(self):
        """今日のGitコミットを取得"""
        commits = []
        
        try:
            # 今日のコミットを取得
            cmd = ["git", "log", "--since=midnight", "--pretty=format:%H|||%s|||%an|||%ai"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout:
                for line in result.stdout.strip().split('\n'):
                    parts = line.split('|||')
                    if len(parts) >= 4:
                        commits.append({
                            'hash': parts[0][:7],
                            'message': parts[1],
                            'author': parts[2],
                            'time': parts[3].split()[1][:5]
                        })
        except:
            pass
        
        return commits
    
    def get_file_changes(self):
        """今日変更されたファイルを取得"""
        changes = {
            'created': [],
            'modified': [],
            'deleted': []
        }
        
        try:
            # 今日の0時からの変更を取得
            cmd = ["find", ".", "-type", "f", "-mtime", "-1", "-not", "-path", "./.git/*"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                today = datetime.now().date()
                
                for filepath in result.stdout.strip().split('\n'):
                    if filepath:
                        try:
                            stat = os.stat(filepath)
                            mtime = datetime.fromtimestamp(stat.st_mtime)
                            
                            if mtime.date() == today:
                                # 作成日時と変更日時を比較
                                ctime = datetime.fromtimestamp(stat.st_ctime)
                                
                                if ctime.date() == today:
                                    changes['created'].append(filepath[2:])  # ./を除去
                                else:
                                    changes['modified'].append(filepath[2:])
                        except:
                            continue
        except:
            pass
        
        return changes
    
    def get_python_scripts_run(self):
        """実行されたPythonスクリプトを取得"""
        scripts = []
        
        # ログファイルやセッションデータから実行履歴を推測
        log_files = ["session_monitor.log", "claude_usage.log"]
        
        for log_file in log_files:
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Pythonスクリプト実行の痕跡を探す
                    import re
                    pattern = r'python3?\s+(\S+\.py)'
                    matches = re.findall(pattern, content)
                    scripts.extend(matches)
                except:
                    pass
        
        return list(set(scripts))  # 重複を除去
    
    def get_health_status(self):
        """最新のヘルスチェック結果を取得"""
        try:
            with open("system_health_report.json", 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            return report.get('summary', {})
        except:
            return None
    
    def analyze_productivity(self):
        """生産性分析"""
        activities = self.get_session_activities()
        commits = self.get_git_commits()
        
        # 活動時間の分布
        hour_distribution = {}
        for activity in activities:
            hour = int(activity['time'].split(':')[0])
            hour_distribution[hour] = hour_distribution.get(hour, 0) + 1
        
        # 最も活発な時間帯
        if hour_distribution:
            peak_hour = max(hour_distribution, key=hour_distribution.get)
            peak_activity = hour_distribution[peak_hour]
        else:
            peak_hour = "N/A"
            peak_activity = 0
        
        return {
            'total_activities': len(activities),
            'total_commits': len(commits),
            'peak_hour': f"{peak_hour}:00",
            'peak_activity_count': peak_activity,
            'activity_hours': len(hour_distribution)
        }
    
    def generate_report(self):
        """日次レポートを生成"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        time_str = datetime.now().strftime('%H:%M:%S')
        
        print(f"📊 日次レポート生成中... ({date_str})")
        
        # データ収集
        activities = self.get_session_activities()
        commits = self.get_git_commits()
        file_changes = self.get_file_changes()
        scripts_run = self.get_python_scripts_run()
        health_status = self.get_health_status()
        productivity = self.analyze_productivity()
        
        # Markdownレポート作成
        report = f"""# 日次レポート - {date_str}

生成時刻: {time_str}

## 📈 生産性サマリー

- **総活動数**: {productivity['total_activities']}件
- **Gitコミット数**: {productivity['total_commits']}件
- **最も活発な時間帯**: {productivity['peak_hour']} ({productivity['peak_activity_count']}件の活動)
- **活動時間**: {productivity['activity_hours']}時間

## 🎯 本日の活動

### セッション活動 ({len(activities)}件)
"""
        
        # 活動リスト
        for activity in activities[-10:]:  # 最新10件
            report += f"- {activity['time']} - {activity['activity']}\n"
        
        if len(activities) > 10:
            report += f"\n*...他 {len(activities) - 10}件の活動*\n"
        
        # Gitコミット
        report += f"\n### Gitコミット ({len(commits)}件)\n"
        for commit in commits[:5]:
            report += f"- {commit['time']} [{commit['hash']}] {commit['message']}\n"
        
        # ファイル変更
        total_changes = len(file_changes['created']) + len(file_changes['modified'])
        report += f"\n### ファイル変更 ({total_changes}件)\n"
        
        if file_changes['created']:
            report += f"\n**新規作成 ({len(file_changes['created'])}件)**\n"
            for file in file_changes['created'][:5]:
                report += f"- {file}\n"
        
        if file_changes['modified']:
            report += f"\n**変更 ({len(file_changes['modified'])}件)**\n"
            for file in file_changes['modified'][:5]:
                report += f"- {file}\n"
        
        # 実行スクリプト
        if scripts_run:
            report += f"\n### 実行されたPythonスクリプト ({len(scripts_run)}件)\n"
            for script in scripts_run[:10]:
                report += f"- {script}\n"
        
        # システムヘルス
        if health_status:
            report += f"\n## 🏥 システムヘルス\n"
            report += f"- **健全**: {health_status.get('healthy', 0)}項目\n"
            report += f"- **警告**: {health_status.get('warning', 0)}項目\n"
            report += f"- **重大**: {health_status.get('critical', 0)}項目\n"
        
        # 明日への推奨事項
        report += f"\n## 💡 明日への推奨事項\n\n"
        
        if productivity['total_activities'] < 10:
            report += "- 活動が少なめです。タスクの優先順位を明確にしましょう\n"
        
        if health_status and health_status.get('critical', 0) > 0:
            report += "- システムに重大な問題があります。health_check_auto.py fixを実行してください\n"
        
        if not commits:
            report += "- 今日はコミットがありません。変更を定期的にコミットしましょう\n"
        
        report += "\n---\n*このレポートは自動生成されました*"
        
        # レポートを保存
        report_path = os.path.join(self.report_dir, f"daily_report_{date_str}.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ レポート生成完了: {report_path}")
        
        # Obsidianにも保存
        try:
            note_path = f"Daily Notes/{date_str}_Report.md"
            cmd = ["./mcp_bridge_extended.sh", "obsidian_write", note_path, report]
            subprocess.run(cmd, capture_output=True)
            print(f"✅ Obsidianに保存: {note_path}")
        except:
            pass
        
        return report_path

def main():
    """メイン関数"""
    import sys
    import time
    
    reporter = DailyReportAuto()
    
    if len(sys.argv) > 1 and sys.argv[1] == "daemon":
        print("🤖 日次レポート自動生成デーモンを開始")
        print("毎日23:55にレポートを生成します")
        
        while True:
            try:
                current_time = datetime.now().strftime("%H:%M")
                
                # 23:55に実行
                if current_time == "23:55":
                    reporter.generate_report()
                    time.sleep(70)  # 重複実行を防ぐ
                
                time.sleep(30)  # 30秒ごとにチェック
                
            except KeyboardInterrupt:
                print("\n⏹️ 停止しました")
                break
    else:
        # 即座に実行
        reporter.generate_report()

if __name__ == "__main__":
    main()