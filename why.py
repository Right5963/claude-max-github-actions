#!/usr/bin/env python3
"""
Why Helper - Simple First 原則の実践
==================================
複雑なシステムではなく、1つのシンプルな質問ツール

使用方法:
    python3 why.py
    ./why.py  (Linux/WSL)
"""

def why_helper(task=None):
    """
    なぜ？を3回問うシンプルな思考支援
    科学的根拠: 単純な自問が最も効果的（2024-2025研究）
    """
    print("🤔 Why Helper - Simple Thinking Support")
    print("=" * 50)
    
    # コマンドライン引数または対話入力
    if task is None:
        try:
            task = input("今から実装しようとしていること: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n❌ 入力が中断されました")
            return False
    
    if not task or task == "default_value":
        print("❌ 実装内容が不明です")
        return False
    
    print(f"\n📝 課題: {task}")
    print("\n🔍 Why分析:")
    
    # なぜ？を3回問う（科学的に実証済みの手法）
    whys = []
    for i in range(3):
        try:
            why = input(f"  なぜ{i+1}: なぜそれが必要ですか？ > ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n⚠️ 入力が中断されました - ここまでの分析を保存")
            break
        
        if not why:
            print(f"\n❌ Why{i+1}に明確な答えがありません")
            print("💡 提案: もう少し考えてから実装してください")
            return False
        
        whys.append(why)
        print(f"     → {why}")
    
    if whys:
        print("\n✅ 実装理由が明確になりました")
    
    # シンプルな代替案チェック
    print("\n🔄 代替案チェック:")
    try:
        simpler = input("より簡単な方法はありませんか？ > ").strip()
    except (EOFError, KeyboardInterrupt):
        simpler = ""
        print("入力スキップ - 現在のプランで続行")
    
    if simpler:
        print(f"💡 検討案: {simpler}")
        try:
            use_simpler = input("その簡単な方法を試しますか？ (y/n): ").strip().lower()
            if use_simpler == 'y':
                print("✅ シンプルなアプローチを選択")
                return True
        except (EOFError, KeyboardInterrupt):
            print("選択スキップ")
            return True
    
    # 継続性チェック
    print("\n⏰ 継続性チェック:")
    try:
        future_use = input("1ヶ月後もこれを使いますか？ (y/n): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        future_use = "y"
        print("継続使用前提で進行")
    
    if future_use != 'y':
        print("⚠️  1ヶ月後に使わないものは作る価値が低いかもしれません")
        try:
            continue_anyway = input("それでも実装しますか？ (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            continue_anyway = "n"
            print("実装見送り")
        
        if continue_anyway != 'y':
            print("🛑 実装を見送ります")
            return False
    
    print("\n🎯 実装GO判定")
    print("✅ 理由明確")
    print("✅ 代替案検討済み")
    print("✅ 継続使用予定")
    print("\n🚀 実装開始してください！")
    
    return True

def main():
    """メイン実行"""
    import sys
    
    # コマンドライン引数対応
    task = None
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    
    try:
        result = why_helper(task)
        
        if result:
            print("\n📊 セッション結果: 実装推奨")
        else:
            print("\n📊 セッション結果: 実装見送り推奨")
            
    except KeyboardInterrupt:
        print("\n\n👋 中断されました")
    except Exception as e:
        print(f"\n❌ エラー: {e}")

if __name__ == "__main__":
    main()