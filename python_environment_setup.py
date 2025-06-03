#!/usr/bin/env python
"""
Python環境自動設定ツール
======================
Windows環境でのPython実行問題を解決
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path

class PythonEnvironmentSetup:
    def __init__(self):
        self.python_paths = []
        self.working_python = None

    def detect_python_installations(self):
        """Pythonインストール状況を検出"""
        print("🔍 Python環境を検出中...")

        # 標準的な検索場所
        search_paths = [
            r"C:\Python*",
            r"C:\Program Files\Python*",
            r"C:\Program Files (x86)\Python*",
            r"%LOCALAPPDATA%\Programs\Python*",
            r"%APPDATA%\Local\Programs\Python*"
        ]

        # 環境変数からのPython検出
        if 'PYTHONPATH' in os.environ:
            self.python_paths.append(os.environ['PYTHONPATH'])

        # コマンドラインからの検出
        commands = ['python', 'python3', 'py', 'python.exe']

        for cmd in commands:
            try:
                result = subprocess.run(
                    [cmd, '--version'],
                    capture_output=True,
                    timeout=3,
                    text=True
                )
                if result.returncode == 0:
                    print(f"✅ 発見: {cmd} - {result.stdout.strip()}")
                    self.working_python = cmd
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue

        print("❌ 利用可能なPython環境が見つかりません")
        return False

    def fix_python_environment(self):
        """Python環境の修復"""
        print("\n🔧 Python環境の修復を試行...")

        # Windows App Storeアプリ問題の修復
        try:
            # Python Launcherを試行
            result = subprocess.run(
                ['py', '-3', '--version'],
                capture_output=True,
                timeout=3,
                text=True
            )
            if result.returncode == 0:
                print(f"✅ Python Launcher使用可能: {result.stdout.strip()}")
                self.working_python = 'py -3'
                return True
        except:
            pass

        # Microsoft Store版Pythonの回避
        print("⚠️ Microsoft Store版Pythonの問題を回避中...")

        # 従来版Pythonのパス設定を提案
        suggestions = [
            "1. Python.orgから最新版をダウンロード: https://python.org/downloads/",
            "2. インストール時に「Add Python to PATH」をチェック",
            "3. Microsoft Store版Pythonを無効化 (設定 > アプリの実行エイリアス)",
            "4. Cursor/VSCodeを再起動"
        ]

        print("\n📋 推奨修正手順:")
        for suggestion in suggestions:
            print(f"   {suggestion}")

        return False

    def create_python_wrapper(self):
        """Python実行ラッパーを作成"""
        wrapper_content = '''@echo off
REM Python実行ラッパー - Windows環境の問題回避
setlocal

REM Python Launcherを優先
py -3 %*
if %ERRORLEVEL% neq 0 (
    REM フォールバックでpythonコマンドを試行
    python %*
)
'''

        with open('python_wrapper.bat', 'w', encoding='utf-8') as f:
            f.write(wrapper_content)

        print("📦 Python実行ラッパーを作成: python_wrapper.bat")

    def test_python_functionality(self):
        """Python機能のテスト"""
        if not self.working_python:
            return False

        print(f"\n🧪 {self.working_python} の機能テスト...")

        tests = [
            ("基本実行", [self.working_python, '-c', 'print("OK")']),
            ("モジュール実行", [self.working_python, '-m', 'py_compile', __file__]),
            ("ライブラリ", [self.working_python, '-c', 'import json, os, subprocess; print("Libraries OK")'])
        ]

        all_passed = True
        for test_name, cmd in tests:
            try:
                if self.working_python == 'py -3':
                    # py -3の場合は分割して実行
                    cmd = ['py', '-3'] + cmd[1:]

                result = subprocess.run(cmd, capture_output=True, timeout=5, text=True)
                if result.returncode == 0:
                    print(f"✅ {test_name}: 正常")
                else:
                    print(f"❌ {test_name}: 失敗")
                    all_passed = False
            except Exception as e:
                print(f"❌ {test_name}: エラー - {str(e)[:30]}")
                all_passed = False

        return all_passed

def main():
    """メイン実行"""
    print("🐍 Python環境自動設定ツール")
    print("=" * 40)

    setup = PythonEnvironmentSetup()

    # Step 1: Python検出
    if setup.detect_python_installations():
        print("\n✅ Python環境が利用可能です")

        # Step 2: 機能テスト
        if setup.test_python_functionality():
            print("\n🎉 Python環境は正常に動作しています")
            print(f"   使用コマンド: {setup.working_python}")
        else:
            print("\n⚠️ Python環境に問題があります")
            setup.fix_python_environment()
    else:
        print("\n❌ Python環境の修復が必要です")
        setup.fix_python_environment()

    # Step 3: ラッパー作成
    setup.create_python_wrapper()

    print("\n📝 次のステップ:")
    print("1. python_wrapper.bat を使用してPythonスクリプトを実行")
    print("2. 問題が続く場合は、Python再インストールを検討")

if __name__ == "__main__":
    main()
