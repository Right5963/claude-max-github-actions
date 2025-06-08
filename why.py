#!/usr/bin/env python3
"""
なぜ？を3回問う思考支援ツール
Simple First の実践例
"""

def ask_why_three_times(topic):
    """なぜ？を3回問うことで本質に迫る"""
    print(f"🤔 テーマ: {topic}")
    print("=" * 50)
    
    why1 = input("🔍 なぜ？(1回目): ")
    print(f"   → {why1}")
    print()
    
    why2 = input("🔍 なぜ？(2回目): ")
    print(f"   → {why2}")
    print()
    
    why3 = input("🔍 なぜ？(3回目): ")
    print(f"   → {why3}")
    print()
    
    print("💡 本質的な気づき:")
    insight = input("   → ")
    
    return {
        "topic": topic,
        "why1": why1,
        "why2": why2, 
        "why3": why3,
        "insight": insight
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("🎯 何について考えますか？: ")
    
    result = ask_why_three_times(topic)
    
    print("\n" + "=" * 50)
    print("📋 思考の記録:")
    print(f"テーマ: {result['topic']}")
    print(f"なぜ1: {result['why1']}")
    print(f"なぜ2: {result['why2']}")
    print(f"なぜ3: {result['why3']}")
    print(f"洞察: {result['insight']}")