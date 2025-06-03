#!/usr/bin/env python
"""
自動起動設定ツール
==================
Windows起動時の自動実行設定を管理
"""

import os
import shutil
import winreg
from pathlib import Path
import subprocess

class StartupConfigurator:
    def __init__(self):
        self.current_dir = Path(__file__).parent.absolute()
        self.startup_folder = Path(os.getenv('APPDATA')) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        self.script_name = "ObsidianCursorClaude_AutoStart"

    def create_startup_shortcut(self):
        """スタートアップフォルダにショートカットを作成"""
        try:
            # PowerShellスクリプトのパス
            ps_script = self.current_dir / "auto_startup.ps1"

            # ショートカット作成用のVBScript
            vbs_content = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{self.startup_folder}\\{self.script_name}.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "powershell.exe"
oLink.Arguments = "-WindowStyle Hidden -ExecutionPolicy Bypass -File ""{ps_script}"" -Auto -Silent"
oLink.WorkingDirectory = "{self.current_dir}"
oLink.Description = "Obsidian-Cursor-Claude Code 自動起動"
oLink.IconLocation = "powershell.exe,0"
oLink.Save
'''

            # 一時的なVBSファイルを作成して実行
            vbs_file = self.current_dir / "create_shortcut.vbs"
            with open(vbs_file, 'w', encoding='utf-8') as f:
                f.write(vbs_content)

            result = subprocess.run(['cscript', str(vbs_file), '//Nologo'],
                                  capture_output=True, text=True)

            # 一時ファイル削除
            vbs_file.unlink()

            if result.returncode == 0:
                print("✅ スタートアップショートカット作成完了")
                print(f"   場所: {self.startup_folder}")
                return True
            else:
                print(f"❌ ショートカット作成失敗: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ ショートカット作成エラー: {str(e)}")
            return False

    def remove_startup_shortcut(self):
        """スタートアップショートカットを削除"""
        shortcut_path = self.startup_folder / f"{self.script_name}.lnk"

        try:
            if shortcut_path.exists():
                shortcut_path.unlink()
                print("✅ スタートアップショートカット削除完了")
                return True
            else:
                print("ℹ️ スタートアップショートカットは存在しません")
                return True

        except Exception as e:
            print(f"❌ ショートカット削除エラー: {str(e)}")
            return False

    def add_to_registry(self):
        """レジストリに自動起動を追加"""
        try:
            reg_key = winreg.HKEY_CURRENT_USER
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            ps_script = self.current_dir / "auto_startup.ps1"

            command = f'powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File "{ps_script}" -Auto -Silent'

            with winreg.OpenKey(reg_key, reg_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, self.script_name, 0, winreg.REG_SZ, command)

            print("✅ レジストリ自動起動設定完了")
            return True

        except Exception as e:
            print(f"❌ レジストリ設定エラー: {str(e)}")
            return False

    def remove_from_registry(self):
        """レジストリから自動起動を削除"""
        try:
            reg_key = winreg.HKEY_CURRENT_USER
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

            with winreg.OpenKey(reg_key, reg_path, 0, winreg.KEY_SET_VALUE) as key:
                try:
                    winreg.DeleteValue(key, self.script_name)
                    print("✅ レジストリ自動起動設定削除完了")
                    return True
                except FileNotFoundError:
                    print("ℹ️ レジストリに自動起動設定はありません")
                    return True

        except Exception as e:
            print(f"❌ レジストリ削除エラー: {str(e)}")
            return False

    def check_startup_status(self):
        """現在の自動起動設定状況を確認"""
        print("🔍 自動起動設定状況確認")
        print("=" * 40)

        # ショートカット確認
        shortcut_path = self.startup_folder / f"{self.script_name}.lnk"
        shortcut_exists = shortcut_path.exists()
        print(f"📁 スタートアップフォルダ: {'✅ 設定済み' if shortcut_exists else '❌ 未設定'}")

        # レジストリ確認
        registry_exists = False
        try:
            reg_key = winreg.HKEY_CURRENT_USER
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(reg_key, reg_path, 0, winreg.KEY_READ) as key:
                try:
                    winreg.QueryValueEx(key, self.script_name)
                    registry_exists = True
                except FileNotFoundError:
                    pass
        except:
            pass

        print(f"🔑 レジストリ設定: {'✅ 設定済み' if registry_exists else '❌ 未設定'}")

        # ファイル存在確認
        ps_script = self.current_dir / "auto_startup.ps1"
        bat_script = self.current_dir / "auto_startup.bat"

        print(f"📄 PowerShellスクリプト: {'✅ 存在' if ps_script.exists() else '❌ 不在'}")
        print(f"📄 バッチファイル: {'✅ 存在' if bat_script.exists() else '❌ 不在'}")

        return {
            'shortcut': shortcut_exists,
            'registry': registry_exists,
            'ps_script': ps_script.exists(),
            'bat_script': bat_script.exists()
        }

    def create_desktop_shortcut(self):
        """デスクトップに手動起動用ショートカットを作成"""
        try:
            desktop = Path(os.path.expanduser("~/Desktop"))
            ps_script = self.current_dir / "auto_startup.ps1"

            vbs_content = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{desktop}\\{self.script_name}.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "powershell.exe"
oLink.Arguments = "-ExecutionPolicy Bypass -File ""{ps_script}"""
oLink.WorkingDirectory = "{self.current_dir}"
oLink.Description = "Obsidian-Cursor-Claude Code 起動"
oLink.IconLocation = "powershell.exe,0"
oLink.Save
'''

            vbs_file = self.current_dir / "create_desktop_shortcut.vbs"
            with open(vbs_file, 'w', encoding='utf-8') as f:
                f.write(vbs_content)

            result = subprocess.run(['cscript', str(vbs_file), '//Nologo'],
                                  capture_output=True, text=True)
            vbs_file.unlink()

            if result.returncode == 0:
                print("✅ デスクトップショートカット作成完了")
                return True
            else:
                print(f"❌ デスクトップショートカット作成失敗: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ デスクトップショートカット作成エラー: {str(e)}")
            return False

def main():
    """メイン実行"""
    configurator = StartupConfigurator()

    while True:
        print("\n🚀 自動起動設定ツール")
        print("=" * 30)
        print("1. 自動起動を有効にする（スタートアップフォルダ）")
        print("2. 自動起動を有効にする（レジストリ）")
        print("3. 自動起動を無効にする")
        print("4. 現在の設定状況を確認")
        print("5. デスクトップショートカット作成")
        print("6. 終了")

        choice = input("\n選択 (1-6): ").strip()

        if choice == "1":
            print("\n📁 スタートアップフォルダに設定中...")
            configurator.create_startup_shortcut()

        elif choice == "2":
            print("\n🔑 レジストリに設定中...")
            configurator.add_to_registry()

        elif choice == "3":
            print("\n🗑️ 自動起動設定を削除中...")
            configurator.remove_startup_shortcut()
            configurator.remove_from_registry()

        elif choice == "4":
            print("\n")
            configurator.check_startup_status()

        elif choice == "5":
            print("\n🖥️ デスクトップショートカット作成中...")
            configurator.create_desktop_shortcut()

        elif choice == "6":
            print("\n👋 設定ツールを終了します")
            break

        else:
            print("❌ 無効な選択です")

if __name__ == "__main__":
    main()
