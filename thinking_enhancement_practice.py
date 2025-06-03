#!/usr/bin/env python3
"""
思考力強化ツール（シンプル版）
==========================
"default_value"  # input()なしで自動実行可能
"""

import json
import sys
from datetime import datetime

class ThinkingEnhancer:
    def __init__(self):
        self.frameworks = [
            "5WHY分析", "SCAMPER法", "オズボーンチェック", "強制連想法"
        ]
    
    def why_five_times(self, problem):
        """5回なぜ法（自動版）"""
        whys = [
            f"なぜ{problem}なのか？",
            "なぜその原因が生じたのか？", 
            "なぜその根本原因があるのか？",
            "なぜそのシステムになっているのか？",
            "なぜ変えられないと思うのか？"
        ]
        return whys
    
    def generate_alternatives(self, problem):
        """代替案生成"""
        alternatives = [
            f"{problem}を逆転させるとどうなるか？",
            f"{problem}を10倍にするとどうなるか？",
            f"{problem}を他の業界ではどう解決するか？",
            f"{problem}をゲーム化するとどうなるか？",
            f"{problem}をAIに任せるとどうなるか？"
        ]
        return alternatives
    
    def creative_constraints_removal(self, problem):
        """制約除去思考"""
        constraints = [
            "お金の制約がなければ？",
            "時間の制約がなければ？",
            "技術の制約がなければ？",
            "人の制約がなければ？",
            "常識の制約がなければ？"
        ]
        return constraints
    
    def analyze_problem(self, problem):
        """問題分析（自動版）"""
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'original_problem': problem,
            'why_analysis': self.why_five_times(problem),
            'alternatives': self.generate_alternatives(problem),
            'constraint_removal': self.creative_constraints_removal(problem),
            'frameworks_used': self.frameworks,
            'insights': [
                "表面的な問題の奥に真の課題あり",
                "制約を疑うことで新しい解決策が見える",
                "他業界の成功事例は参考になる",
                "逆転の発想で突破口が見つかる"
            ]
        }
        
        return analysis
    
    def display_analysis(self, analysis):
        """分析結果表示"""
        
        print(f"🧠 思考力強化分析結果")
        print("=" * 50)
        print(f"課題: {analysis['original_problem']}")
        
        print(f"\n❓ 5WHY分析:")
        for i, why in enumerate(analysis['why_analysis'], 1):
            print(f"  {i}. {why}")
        
        print(f"\n💡 代替案思考:")
        for i, alt in enumerate(analysis['alternatives'], 1):
            print(f"  {i}. {alt}")
        
        print(f"\n🚫 制約除去思考:")
        for i, constraint in enumerate(analysis['constraint_removal'], 1):
            print(f"  {i}. {constraint}")
        
        print(f"\n🎯 洞察:")
        for insight in analysis['insights']:
            print(f"  • {insight}")
    
    def save_session(self, analysis):
        """セッション保存"""
        
        filename = 'thinking_enhancement_session.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        return filename

def main():
    """思考強化実行"""
    
    enhancer = ThinkingEnhancer()
    
    # 問題取得
    if len(sys.argv) > 1:
        problem = " ".join(sys.argv[1:])
    else:
        problem = "売上が思うように伸びない"
    
    # 分析実行
    analysis = enhancer.analyze_problem(problem)
    
    # 結果表示
    enhancer.display_analysis(analysis)
    
    # セッション保存
    session_file = enhancer.save_session(analysis)
    print(f"\n💾 セッション保存: {session_file}")
    print(f"📋 使用法: python thinking_enhancement_simple.py \"あなたの課題\"")

if __name__ == "__main__":
    main()