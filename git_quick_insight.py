#!/usr/bin/env python3
"""
Git Quick Insight - 即座に価値を提供する開発状況分析
==================================================
73行以下のシンプルツール / 設定不要 / 即使用可能
"""

import subprocess
import re
from datetime import datetime, timedelta
from collections import defaultdict

def run_git(command):
    """Git コマンド実行"""
    try:
        result = subprocess.run(
            f"git {command}", shell=True, 
            capture_output=True, text=True, cwd="/mnt/c/Claude Code/tool"
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except:
        return ""

def analyze_recent_commits():
    """最近5コミットの即座分析"""
    print("🔍 Git Quick Insight - 開発状況即座分析")
    print("=" * 50)
    
    # 最近5コミット取得
    log_output = run_git("log --oneline -5")
    if not log_output:
        print("❌ Gitリポジトリが見つかりません")
        return
    
    commits = log_output.split('\n')
    print(f"📊 最近のコミット数: {len(commits)}")
    
    # コミットメッセージパターン分析
    patterns = defaultdict(int)
    files_changed = 0
    
    for commit in commits:
        message = commit[8:].lower()  # ハッシュ除去
        
        # パターン検出
        if any(word in message for word in ['add', 'new', 'create']):
            patterns['新機能'] += 1
        elif any(word in message for word in ['fix', 'error', 'bug']):
            patterns['バグ修正'] += 1
        elif any(word in message for word in ['update', 'modify', 'change']):
            patterns['改善'] += 1
        elif any(word in message for word in ['auto', 'commit']):
            patterns['自動化'] += 1
        else:
            patterns['その他'] += 1
    
    # 最新コミットの詳細
    latest_stats = run_git("show --stat HEAD --format=''")
    if latest_stats:
        files_changed = len([line for line in latest_stats.split('\n') if '|' in line])
    
    # 結果表示
    print("\n🔍 開発パターン分析:")
    for pattern, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
        print(f"  {pattern}: {count}回")
    
    print(f"\n📁 最新コミット変更ファイル数: {files_changed}")
    
    # 直近の作業状況
    status = run_git("status --porcelain")
    uncommitted = len(status.split('\n')) if status else 0
    print(f"💼 未コミット変更: {uncommitted}ファイル")
    
    # 今日の作業量
    today = datetime.now().strftime("%Y-%m-%d")
    today_commits = run_git(f"log --since='{today}' --oneline")
    today_count = len(today_commits.split('\n')) if today_commits else 0
    print(f"🗓️ 今日のコミット数: {today_count}")
    
    # 推奨アクション
    print(f"\n💡 推奨アクション:")
    if uncommitted > 0:
        print(f"  ⚡ {uncommitted}個の変更をコミット検討")
    if patterns['新機能'] > patterns['バグ修正']:
        print("  🚀 新機能開発が活発 - テスト強化推奨")
    if today_count == 0:
        print("  📝 今日はまだコミットなし - 作業開始？")
    
    print(f"\n✅ 分析完了 ({datetime.now().strftime('%H:%M:%S')})")

if __name__ == "__main__":
    analyze_recent_commits()