#!/usr/bin/env python3
"""
シンプルセッション管理（73行版）
==============================
373行の複雑版を25行のシンプル版に置き換え
"""

import json
import os
from datetime import datetime

class SimpleSessionManager:
    def __init__(self):
        self.session_file = "current_session.json"
        self.session_data = self.load_session()
    
    def load_session(self):
        """セッション読み込み"""
        try:
            with open(self.session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                'start_time': datetime.now().isoformat(),
                'activities': [],
                'notes': []
            }
    
    def save_session(self):
        """セッション保存"""
        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, ensure_ascii=False, indent=2)
    
    def add_activity(self, activity):
        """活動記録"""
        self.session_data['activities'].append({
            'time': datetime.now().isoformat(),
            'activity': activity
        })
        self.save_session()
        print(f"✅ 記録: {activity}")
    
    def add_note(self, note):
        """メモ追加"""
        self.session_data['notes'].append({
            'time': datetime.now().isoformat(),
            'note': note
        })
        self.save_session()
        print(f"📝 メモ: {note}")
    
    def show_status(self):
        """状況表示"""
        print("📊 現在のセッション")
        print(f"開始: {self.session_data['start_time']}")
        print(f"活動数: {len(self.session_data['activities'])}")
        print(f"メモ数: {len(self.session_data['notes'])}")
        
        if self.session_data['activities']:
            print("\n📋 最近の活動:")
            for activity in self.session_data['activities'][-3:]:
                time = activity['time'].split('T')[1][:8]
                print(f"  {time} - {activity['activity']}")

def main():
    """メイン実行"""
    import sys
    
    sm = SimpleSessionManager()
    
    if len(sys.argv) < 2:
        sm.show_status()
        print("\n使用方法:")
        print("python3 session_manager_simple.py activity '活動内容'")
        print("python3 session_manager_simple.py note 'メモ内容'")
        print("python3 session_manager_simple.py status")
        return
    
    command = sys.argv[1]
    
    if command == "activity" and len(sys.argv) > 2:
        sm.add_activity(sys.argv[2])
    elif command == "note" and len(sys.argv) > 2:
        sm.add_note(sys.argv[2])
    elif command == "status":
        sm.show_status()
    else:
        print("❌ 無効なコマンド")

if __name__ == "__main__":
    main()