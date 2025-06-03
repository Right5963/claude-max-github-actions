#!/usr/bin/env python3
"""
Thinking Core Simple
==================
32KB巨大システムから核心機能のみ抽出（73行版）
"""

import json
import re
from datetime import datetime

class ThinkingCore:
    def __init__(self):
        self.thought_history = []
        self.assumptions = []
        self.insights = []
    
    def detect_assumptions(self, text):
        """思い込み検出（シンプル版）"""
        
        assumption_patterns = [
            r'(絶対|必ず|当然|常に|決して|間違いなく)',
            r'(すべての|みんな|誰も|全員|一人もいない)',
            r'(のはず|に違いない|べきである|はずだ)'
        ]
        
        assumptions = []
        for pattern in assumption_patterns:
            matches = re.findall(pattern, text)
            if matches:
                assumptions.extend(matches)
        
        self.assumptions.extend(assumptions)
        return assumptions
    
    def analyze_problem(self, problem_text):
        """問題分析（エッセンス版）"""
        
        # 思い込み検出
        assumptions = self.detect_assumptions(problem_text)
        
        # 質問生成
        questions = self.generate_questions(problem_text)
        
        # 洞察抽出
        insights = self.extract_insights(problem_text)
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'problem': problem_text,
            'assumptions_found': assumptions,
            'key_questions': questions,
            'potential_insights': insights,
            'next_actions': self.suggest_actions(assumptions, questions)
        }
        
        self.thought_history.append(analysis)
        return analysis
    
    def generate_questions(self, text):
        """重要な質問生成"""
        
        # 基本的な探究質問
        base_questions = [
            f"なぜ{text[:20]}...なのか？",
            "本当にそうだろうか？",
            "別の見方はないか？",
            "何が見落とされているか？",
            "実際のデータは何を示すか？"
        ]
        
        return base_questions[:3]  # 3つに絞る
    
    def extract_insights(self, text):
        """洞察抽出（簡易版）"""
        
        # テキストの長さで洞察パターンを判定
        word_count = len(text.split())
        
        if word_count < 10:
            insight_level = "表面的"
        elif word_count < 50:
            insight_level = "基本的"
        else:
            insight_level = "詳細"
        
        insights = [
            f"分析レベル: {insight_level}",
            f"文字数: {len(text)}文字",
            "さらなる深掘りが必要" if word_count < 30 else "十分な情報あり"
        ]
        
        return insights
    
    def suggest_actions(self, assumptions, questions):
        """次のアクション提案"""
        
        actions = []
        
        if assumptions:
            actions.append(f"思い込み検証: {assumptions[0]}を確認する")
        
        if questions:
            actions.append(f"質問調査: {questions[0]}")
        
        actions.append("追加データ収集")
        actions.append("別の視点で再考")
        
        return actions
    
    def save_session(self, filename="thinking_session.json"):
        """セッション保存"""
        
        session_data = {
            'session_date': datetime.now().isoformat(),
            'thought_history': self.thought_history,
            'total_assumptions': len(self.assumptions),
            'total_insights': len(self.insights)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        return filename

def main():
    """思考分析実行"""
    
    import sys
    
    thinking = ThinkingCore()
    
    # 問題文取得
    if len(sys.argv) > 1:
        problem = " ".join(sys.argv[1:])
    else:
        problem = "売上が伸びない理由がわからない。きっと価格が高すぎるのだろう。"
    
    print(f"🧠 思考分析開始")
    print(f"📝 問題: {problem}")
    print("=" * 50)
    
    # 分析実行
    result = thinking.analyze_problem(problem)
    
    # 結果表示
    print(f"🚨 思い込み発見: {len(result['assumptions_found'])}個")
    for assumption in result['assumptions_found']:
        print(f"  ⚠️ {assumption}")
    
    print(f"\n❓ 重要な質問:")
    for question in result['key_questions']:
        print(f"  • {question}")
    
    print(f"\n💡 洞察:")
    for insight in result['potential_insights']:
        print(f"  💡 {insight}")
    
    print(f"\n🎯 次のアクション:")
    for action in result['next_actions']:
        print(f"  □ {action}")
    
    # セッション保存
    session_file = thinking.save_session()
    print(f"\n💾 セッション保存: {session_file}")

if __name__ == "__main__":
    main()