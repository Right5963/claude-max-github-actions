#!/usr/bin/env python3
"""
シンプル統合思考リサーチシステム
================================
依存関係なし、73行で動作するITRS簡易版
"""

import json
from datetime import datetime
import sys

class SimpleITRS:
    def __init__(self):
        self.thoughts = []
        
    def think(self, content):
        """思考を処理して洞察を生成"""
        # 簡易的な思考分析
        questions = [
            f"なぜ{content[:20]}...なのか？",
            "本当にそうだろうか？",
            "別の見方はないか？"
        ]
        
        thought = {
            "content": content,
            "questions": questions,
            "timestamp": datetime.now().isoformat(),
            "confidence": len(content) / 100.0  # 簡易的な信頼度
        }
        
        self.thoughts.append(thought)
        return thought
    
    def analyze_assumptions(self, content):
        """前提条件を分析"""
        # 簡易的な前提条件検出
        assumption_words = ["はず", "当然", "みんな", "すべて", "必ず", "いつも"]
        found = [word for word in assumption_words if word in content]
        
        return {
            "found_assumptions": found,
            "count": len(found),
            "warning": "前提条件に注意" if found else "明確な前提条件なし"
        }
    
    def interactive_mode(self):
        """対話モード"""
        print("🧠 シンプルITRS - 統合思考支援")
        print("コマンド: think, analyze, quit")
        print("-" * 40)
        
        while True:
            try:
                command = input("\nitrs> ").strip()
                
                if command.startswith("quit") or command == "q":
                    print("👋 終了します")
                    break
                    
                elif command.startswith("think "):
                    content = command[6:]
                    thought = self.think(content)
                    print(f"\n✅ 思考を処理しました")
                    print(f"💭 考えるべき質問:")
                    for q in thought["questions"]:
                        print(f"   • {q}")
                        
                elif command.startswith("analyze "):
                    content = command[8:]
                    result = self.analyze_assumptions(content)
                    print(f"\n🔍 前提条件分析")
                    print(f"   発見数: {result['count']}")
                    print(f"   ⚠️  {result['warning']}")
                    if result['found_assumptions']:
                        print(f"   検出: {', '.join(result['found_assumptions'])}")
                        
                else:
                    print("❌ 不明なコマンド。think, analyze, quit が使えます")
                    
            except KeyboardInterrupt:
                print("\n👋 終了します")
                break

def main():
    """73行のシンプルITRS"""
    itrs = SimpleITRS()
    
    if len(sys.argv) > 2:
        command = sys.argv[1]
        content = ' '.join(sys.argv[2:])
        
        if command == "think":
            thought = itrs.think(content)
            print(f"💭 {content}")
            for q in thought["questions"]:
                print(f"   • {q}")
        elif command == "analyze":
            result = itrs.analyze_assumptions(content)
            print(f"🔍 前提条件: {result['count']}個")
            print(f"⚠️  {result['warning']}")
    else:
        # 対話モードを起動
        itrs.interactive_mode()

if __name__ == "__main__":
    main()