#!/usr/bin/env python3
"""
新セッション開始用ガイド
======================
新しいClaude Codeセッション開始時に必ず実行

使用方法:
    python3 start.py
"""

def show_session_checklist():
    """新セッション開始時のチェックリスト表示"""
    print("🚀 Claude Code 新セッション開始")
    print("=" * 50)
    print()
    
    print("🚨 最重要：Simple First 原則")
    print("前回実証: 73行ツール > 1,200行システム")
    print()
    
    print("📋 必須チェック:")
    print("□ CLAUDE.md の Simple First セクションを確認済み")
    print("□ why.py の動作確認済み") 
    print("□ 複雑システム提案の拒否準備済み")
    print()
    
    print("🎯 提案前の必須質問:")
    print("1. 最もシンプルな解決策は何？")
    print("2. なぜ複雑にする必要があるのか？")
    print("3. 73行で解決できないか？")
    print("4. 実際に毎日使うか？")
    print("5. 1週間後も使い続けるか？")
    print()
    
    print("🚫 即座に拒否すべきもの:")
    print("- 統合システム、自動化システム、AI化")
    print("- 設定システム、データベース連携")
    print("- 3つ以上の機能同時実装")
    print("- 「劇的改善」「革新的」等の誇張表現")
    print()
    
    print("✅ 利用可能なツール:")
    print("- why.py: 実装前の思考整理（73行、実証済み）")
    print()
    
    print("📊 セッション成功の定義:")
    print("成功 = シンプルで実用的な1つの機能を作成・使用開始")
    print("失敗 = 複雑な提案をした時点で失敗")
    print()
    
    # インタラクティブな確認
    print("🤔 セッション準備確認:")
    ready = "default_value"  # input("Simple First原則を理解しましたか？ (y/n): ").strip().lower()
    
    if ready == 'y':
        print("✅ セッション開始準備完了")
        print()
        print("💡 推奨最初のアクション:")
        print("1. 解決したい課題を1つ選ぶ")
        print("2. python3 why.py を実行")
        print("3. シンプルな解決策を1つ実装")
        
        # why.py テスト提案
        test_why = "default_value"  # input("\nwhy.py をテスト実行しますか？ (y/n): ").strip().lower()
        if test_why == 'y':
            import subprocess
            try:
                subprocess.run(['python3', '/mnt/c/Claude Code/tool/why.py'], check=True)
            except:
                print("⚠️ why.py の実行に失敗しました")
                print("パスを確認してください: /mnt/c/Claude Code/tool/why.py")
        
    else:
        print("❌ Simple First原則の理解が不十分です")
        print("CLAUDE.md の Simple First セクションを再確認してください")
        return False
    
    return True

def main():
    """メイン実行"""
    try:
        success = show_session_checklist()
        if success:
            print("\n🎉 新セッション開始準備完了!")
            print("シンプルで実用的な開発をお楽しみください。")
        
    except KeyboardInterrupt:
        print("\n\n👋 セッション準備を中断しました")
    except Exception as e:
        print(f"\n❌ エラー: {e}")

if __name__ == "__main__":
    main()