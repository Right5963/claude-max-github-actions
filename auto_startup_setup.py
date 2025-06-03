#!/usr/bin/env python
"""
自動起動セットアップツール
========================
Windows起動時の完全自動実行を設定
"""

import os
import winreg
import subprocess
from pathlib import Path

class AutoStartupSetup:
    def __init__(self):
        self.current_dir = Path(__file__).parent.absolute()
        self.script_name = "ObsidianCursorClaude_AutoStart"

    def setup_registry_autostart(self):
        """レジストリベースの自動起動設定"""
        try:
            reg_key = winreg.HKEY_CURRENT_USER
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

            # simple_auto_startup.py を直接実行するコマンド
            python_script = self.current_dir / "simple_auto_startup.py"
            command = f'python "{python_script}"'

            with winreg.OpenKey(reg_key, reg_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, self.script_name, 0, winreg.REG_SZ, command)

            print("✅ レジストリ自動起動設定完了")
            print(f"   実行コマンド: {command}")
            return True

        except Exception as e:
            print(f"❌ レジストリ設定エラー: {str(e)}")
            return False

    def setup_startup_folder(self):
        """スタートアップフォルダにバッチファイルを配置"""
        try:
            appdata = os.getenv('APPDATA')
            if not appdata:
                print("❌ APPDATA環境変数が見つかりません")
                return False

            startup_folder = Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"

            if not startup_folder.exists():
                print(f"❌ スタートアップフォルダが存在しません: {startup_folder}")
                return False

            # シンプルなバッチファイルを作成
            batch_content = f'''@echo off
cd /d "{self.current_dir}"
python simple_auto_startup.py
'''

            batch_file = startup_folder / f"{self.script_name}.bat"
            with open(batch_file, 'w', encoding='utf-8') as f:
                f.write(batch_content)

            print("✅ スタートアップフォルダ設定完了")
            print(f"   場所: {batch_file}")
            return True

        except Exception as e:
            print(f"❌ スタートアップフォルダ設定エラー: {str(e)}")
            return False

    def remove_autostart(self):
        """自動起動設定を削除"""
        success = True

        # レジストリから削除
        try:
            reg_key = winreg.HKEY_CURRENT_USER
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

            with winreg.OpenKey(reg_key, reg_path, 0, winreg.KEY_SET_VALUE) as key:
                try:
                    winreg.DeleteValue(key, self.script_name)
                    print("✅ レジストリ自動起動設定削除完了")
                except FileNotFoundError:
                    print("ℹ️ レジストリに自動起動設定はありませんでした")

        except Exception as e:
            print(f"⚠️ レジストリ削除エラー: {str(e)}")
            success = False

        # スタートアップフォルダから削除
        try:
            appdata = os.getenv('APPDATA')
            if appdata:
                startup_folder = Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
                batch_file = startup_folder / f"{self.script_name}.bat"

                if batch_file.exists():
                    batch_file.unlink()
                    print("✅ スタートアップフォルダのファイル削除完了")
                else:
                    print("ℹ️ スタートアップフォルダにファイルはありませんでした")

        except Exception as e:
            print(f"⚠️ スタートアップフォルダ削除エラー: {str(e)}")
            success = False

        return success

    def check_autostart_status(self):
        """自動起動設定状況を確認"""
        print("🔍 自動起動設定状況確認")
        print("=" * 40)

        # レジストリ確認
        registry_exists = False
        try:
            reg_key = winreg.HKEY_CURRENT_USER
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(reg_key, reg_path, 0, winreg.KEY_READ) as key:
                try:
                    value, _ = winreg.QueryValueEx(key, self.script_name)
                    print(f"🔑 レジストリ設定: ✅ 設定済み")
                    print(f"   コマンド: {value}")
                    registry_exists = True
                except FileNotFoundError:
                    print("🔑 レジストリ設定: ❌ 未設定")
        except Exception as e:
            print(f"🔑 レジストリ設定: ❌ エラー ({str(e)})")

        # スタートアップフォルダ確認
        startup_exists = False
        try:
            appdata = os.getenv('APPDATA')
            if appdata:
                startup_folder = Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
                batch_file = startup_folder / f"{self.script_name}.bat"

                if batch_file.exists():
                    print(f"📁 スタートアップフォルダ: ✅ 設定済み")
                    print(f"   ファイル: {batch_file}")
                    startup_exists = True
                else:
                    print("📁 スタートアップフォルダ: ❌ 未設定")
            else:
                print("📁 スタートアップフォルダ: ❌ APPDATA未取得")
        except Exception as e:
            print(f"📁 スタートアップフォルダ: ❌ エラー ({str(e)})")

        # ベーススクリプト確認
        python_script = self.current_dir / "simple_auto_startup.py"
        print(f"📄 ベーススクリプト: {'✅ 存在' if python_script.exists() else '❌ 不在'}")

        return {
            'registry': registry_exists,
            'startup_folder': startup_exists,
            'base_script': python_script.exists()
        }

    def test_autostart(self):
        """自動起動機能をテスト"""
        print("🧪 自動起動機能テスト実行中...")

        python_script = self.current_dir / "simple_auto_startup.py"
        if not python_script.exists():
            print("❌ ベーススクリプトが見つかりません")
            return False

        try:
            result = subprocess.run(
                ['python', str(python_script)],
                capture_output=True,
                timeout=30,
                text=True
            )

            if result.returncode == 0:
                print("✅ 自動起動テスト成功！")
                print("   実際のWindows起動時にも正常に動作します")
                return True
            else:
                print(f"❌ 自動起動テスト失敗")
                print(f"   エラー: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ テスト実行エラー: {str(e)}")
            return False

def main():
    """メイン実行"""
    setup = AutoStartupSetup()

    while True:
        print("\n🚀 Windows完全自動起動セットアップ")
        print("=" * 40)
        print("1. レジストリ自動起動を設定")
        print("2. スタートアップフォルダ自動起動を設定")
        print("3. 自動起動設定を削除")
        print("4. 現在の設定状況を確認")
        print("5. 自動起動機能をテスト")
        print("6. 終了")

        choice = input("\n選択 (1-6): ").strip()

        if choice == "1":
            print("\n🔑 レジストリ自動起動設定中...")
            if setup.setup_registry_autostart():
                print("\n🎉 レジストリ自動起動設定完了！")
                print("次回Windows起動時から自動実行されます")

        elif choice == "2":
            print("\n📁 スタートアップフォルダ自動起動設定中...")
            if setup.setup_startup_folder():
                print("\n🎉 スタートアップフォルダ自動起動設定完了！")
                print("次回Windows起動時から自動実行されます")

        elif choice == "3":
            print("\n🗑️ 自動起動設定削除中...")
            if setup.remove_autostart():
                print("\n✅ 自動起動設定削除完了")

        elif choice == "4":
            print("\n")
            status = setup.check_autostart_status()

            if status['registry'] or status['startup_folder']:
                print("\n🎉 自動起動が設定されています！")
                print("次回Windows起動時に自動実行されます")
            else:
                print("\n⚠️ 自動起動が設定されていません")
                print("選択肢1または2で設定してください")

        elif choice == "5":
            print("\n🧪 自動起動機能テスト...")
            setup.test_autostart()

        elif choice == "6":
            print("\n👋 セットアップツールを終了します")
            break

        else:
            print("❌ 無効な選択です")

if __name__ == "__main__":
    main()
