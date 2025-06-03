#!/usr/bin/env python3
"""
シンプル日次レポート
==================
手動実行で今日の活動サマリーを表示
"""

import json
import os
from datetime import datetime
from collections import Counter

def main():
    print("📊 日次レポート")
    print("=" * 40)
    
    # 現在のセッション読み込み
    try:
        with open('current_session.json', 'r', encoding='utf-8') as f:
            session = json.load(f)
    except:
        print("❌ セッションファイルが見つかりません")
        return
    
    # 今日の活動を抽出
    today = datetime.now().date()
    today_activities = []
    
    for activity in session.get('activities', []):
        try:
            act_time = datetime.fromisoformat(activity['time'].replace('T', ' '))
            if act_time.date() == today:
                today_activities.append({
                    'time': act_time.strftime('%H:%M'),
                    'activity': activity['activity']
                })
        except:
            continue
    
    # サマリー表示
    print(f"📅 日付: {today}")
    print(f"🎯 活動数: {len(today_activities)}件")
    
    if today_activities:
        # 時間帯分析
        hours = [int(a['time'].split(':')[0]) for a in today_activities]
        hour_counts = Counter(hours)
        peak_hour = max(hour_counts, key=hour_counts.get)
        print(f"⏰ 最も活発な時間: {peak_hour}時台")
        
        # 最新の活動
        print("\n📋 最新の活動:")
        for activity in today_activities[-5:]:
            print(f"  {activity['time']} - {activity['activity']}")
    else:
        print("\n今日の活動はまだありません")
    
    # セッションファイル数
    session_count = len([f for f in os.listdir('sessions') if f.startswith('session_')])
    print(f"\n💾 総バックアップ数: {session_count}個")
    
    print("\n✅ レポート完了")

if __name__ == "__main__":
    main()