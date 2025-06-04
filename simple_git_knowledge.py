#!/usr/bin/env python3
"""
Simple Git Knowledge - 真に実用的なGit知識管理
=============================================
複雑性を排除し、本当に必要な機能のみ提供
"""

import subprocess
import json
from datetime import datetime

def get_recent_learnings(days=7):
    """最近のコミットから学習ポイントを抽出"""
    cmd = f'git log --since="{days} days ago" --pretty=format:"%h|%s|%b" --grep="fix\\|learn\\|improve\\|error"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    learnings = []
    for line in result.stdout.strip().split('\n'):
        if line:
            parts = line.split('|')
            if len(parts) >= 2:
                commit, subject = parts[0], parts[1]
                # FIX, LEARN, ERROR などのキーワードがあるコミットのみ
                if any(word in subject.lower() for word in ['fix', 'learn', 'improve', 'error', 'bug']):
                    learnings.append(f"[{commit}] {subject}")
    
    return learnings

def save_weekly_summary():
    """週次サマリーを1ファイルに保存"""
    learnings = get_recent_learnings(7)
    if learnings:
        summary = {
            "week": datetime.now().strftime("%Y-W%V"),
            "learnings": learnings,
            "count": len(learnings)
        }
        
        with open("weekly_learnings.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"📝 今週の学習: {len(learnings)}件")
        for learning in learnings[:5]:  # 最大5件表示
            print(f"  • {learning}")
    else:
        print("📝 今週の明示的な学習コミットはありません")

if __name__ == "__main__":
    save_weekly_summary()