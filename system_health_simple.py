#!/usr/bin/env python3
"""
システム健全性チェック（Windows対応版）
=====================================
Windows環境でも正確に動作する高速ヘルスチェックツール
"""

import os
import subprocess
import platform
from datetime import datetime
from typing import Optional, Dict, List

class SystemHealthAdvanced:
    def __init__(self):
        self.systems = self.get_python_systems()
        self.results = {}
        self.python_cmd = self.get_python_command()
        self.os_type = platform.system()

    def get_python_command(self):
        """環境に応じたPythonコマンドを取得"""
        commands = ['python', 'python3', 'py']

        for cmd in commands:
            try:
                result = subprocess.run(
                    [cmd, '--version'],
                    capture_output=True,
                    timeout=3,
                    text=True
                )
                if result.returncode == 0:
                    print(f"🐍 Python実行コマンド: {cmd}")
                    print(f"🐍 Python版本: {result.stdout.strip()}")
                    return cmd
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue

        print("❌ Python環境が見つかりません")
        return None

    def get_python_systems(self):
        """Pythonシステムのみ取得（高速化）"""
        systems = []
        current_file = os.path.basename(__file__)

        for file in os.listdir('.'):
            if file.endswith('.py') and file != current_file:
                systems.append(file)
        return sorted(systems)

    def advanced_test(self, filename: str) -> str:
        """高度なテスト（syntax + 簡単実行チェック）"""
        if not self.python_cmd:
            return "🚨 Python環境なし"

        try:
            # Step 1: Syntax check
            result = subprocess.run(
                [self.python_cmd, '-m', 'py_compile', filename],
                capture_output=True,
                timeout=5,
                text=True
            )

            if result.returncode != 0:
                error_msg = result.stderr.strip()[:50] if result.stderr else "構文エラー"
                return f"❌ Syntax Error: {error_msg}"

            # Step 2: Import test (if possible)
            try:
                # ファイル名からモジュール名を取得
                module_name = filename[:-3]  # .pyを除去

                result = subprocess.run(
                    [self.python_cmd, '-c', f'import {module_name}; print("OK")'],
                    capture_output=True,
                    timeout=3,
                    text=True,
                    cwd='.'
            )

            if result.returncode == 0:
                    return "✅ Perfect"
            else:
                    return "⚠️ Import Issues"

            except Exception:
                return "✅ Syntax OK"

        except subprocess.TimeoutExpired:
            return "⏰ Timeout"
        except Exception as e:
            return f"🚨 Error: {str(e)[:30]}"

    def check_all_systems(self):
        """全システムの健全性チェック"""
        print("🔍 システム健全性チェック（Windows対応版）")
        print(f"🖥️ OS: {self.os_type}")
        print(f"📁 対象: {len(self.systems)}システム")
        print("=" * 60)

        perfect_count = 0
        ok_count = 0
        warning_count = 0
        error_count = 0

        for system in self.systems:
            result = self.advanced_test(system)
            self.results[system] = result

            if "Perfect" in result:
                perfect_count += 1
                print(f"✅ {system} - {result}")
            elif "Syntax OK" in result:
                ok_count += 1
                print(f"✅ {system} - {result}")
            elif "Import Issues" in result or "Warning" in result:
                warning_count += 1
                print(f"⚠️ {system} - {result}")
            else:
                error_count += 1
                print(f"❌ {system} - {result}")

        total = perfect_count + ok_count + warning_count + error_count
        working = perfect_count + ok_count

        print(f"\n📊 詳細結果:")
        print(f"✅ 完全正常: {perfect_count}個")
        print(f"✅ 構文正常: {ok_count}個")
        print(f"⚠️ 警告: {warning_count}個")
        print(f"❌ エラー: {error_count}個")
        print(f"🎯 基本健全性: {working/total*100:.1f}%" if total > 0 else "🎯 基本健全性: 0%")

        return self.results

    def save_detailed_report(self):
        """詳細レポート保存"""
        report = {
            'check_date': datetime.now().isoformat(),
            'os_type': self.os_type,
            'python_command': self.python_cmd,
            'total_systems': len(self.systems),
            'results': self.results,
            'summary': {
                'perfect': sum(1 for r in self.results.values() if "Perfect" in r),
                'syntax_ok': sum(1 for r in self.results.values() if "Syntax OK" in r),
                'warnings': sum(1 for r in self.results.values() if "Warning" in r or "Import Issues" in r),
                'errors': sum(1 for r in self.results.values() if "❌" in r)
            }
        }

        with open('system_health_report_detailed.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(report, f, ensure_ascii=False, indent=2)

        print("📄 詳細レポート保存: system_health_report_detailed.json")

    def python_environment_fix(self):
        """Python環境の修正提案"""
        if not self.python_cmd:
            print("\n🚨 Python環境修正が必要です:")
            print("1. Python 3.12.3をインストール")
            print("2. 環境変数PATHにPythonを追加")
            print("3. Cursor/VSCodeを再起動")
            return False
        return True

def main():
    """メイン実行"""
    health = SystemHealthAdvanced()

    if health.python_environment_fix():
    health.check_all_systems()
        health.save_detailed_report()
    else:
        print("❌ Python環境の修正が必要です")

if __name__ == "__main__":
    main()
