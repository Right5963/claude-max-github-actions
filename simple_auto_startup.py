#!/usr/bin/env python
"""
シンプル自動起動スクリプト
========================
確実に動作する自動起動機能
"""

import sys
import subprocess
from daily_workflow_optimizer import DailyWorkflowOptimizer

def auto_startup():
    """自動起動メイン処理"""
    print("🚀 Obsidian-Cursor-Claude Code システム自動起動")
    print("=" * 50)

    try:
        # DailyWorkflowOptimizerのインスタンス作成
        optimizer = DailyWorkflowOptimizer()

        # 自動セッション開始
        optimizer.start_daily_session()

        print("\n🎉 自動起動完了！")
        print("\n📝 推奨：次に以下のアプリケーションを開いてください")
        print("  - Obsidian (知識ベース)")
        print("  - Cursor (AI開発環境)")

    except Exception as e:
        print(f"❌ 自動起動エラー: {str(e)}")
        print("手動で python daily_workflow_optimizer.py を実行してください")

if __name__ == "__main__":
    auto_startup()
