#!/usr/bin/env python3
"""
Obsidian日本語ライター - 確実に日本語を書き込むツール
====================================================
研究結果: PowerShell + UTF8エンコーディングが最も確実
"""

import os
import subprocess
import json
from pathlib import Path

class ObsidianJapaneseWriter:
    def __init__(self):
        self.vault_path = r"G:\マイドライブ\Obsidian Vault"
        self.fallback_path = r"C:\Users\user\Documents\Obsidian Vault"
        
    def write_japanese_text(self, file_path, content):
        """日本語テキストを確実にObsidianに書き込む
        
        Args:
            file_path (str): Vault内のファイルパス（例: "Projects/test.md"）
            content (str): 書き込むコンテンツ（日本語を含む）
        
        Returns:
            bool: 成功したかどうか
        """
        
        # 方法1: PowerShell経由でUTF8書き込み（最も確実）
        try:
            full_path = f"{self.vault_path}\\{file_path}"
            
            # エスケープ処理
            escaped_content = content.replace("'", "''").replace('"', '`"')
            
            # PowerShellコマンド実行
            ps_command = f"""
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$content = @'
{content}
'@
Set-Content -Path '{full_path}' -Value $content -Encoding UTF8
"""
            
            result = subprocess.run([
                'powershell.exe', '-Command', ps_command
            ], capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                print(f"✅ PowerShell UTF8方式で書き込み成功: {file_path}")
                return True
            else:
                print(f"❌ PowerShell書き込みエラー: {result.stderr}")
                
        except Exception as e:
            print(f"❌ PowerShell方式失敗: {e}")
        
        # 方法2: Python直接書き込み（Windows側パス）
        try:
            windows_path = Path(self.vault_path) / file_path
            windows_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(windows_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Python直接書き込み成功: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Python直接書き込み失敗: {e}")
        
        # 方法3: フォールバック先への書き込み
        try:
            fallback_path = Path(self.fallback_path) / file_path
            fallback_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(fallback_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"⚠️ フォールバック先に書き込み: {fallback_path}")
            return True
            
        except Exception as e:
            print(f"❌ 全ての方法が失敗: {e}")
            return False
    
    def read_japanese_text(self, file_path):
        """日本語テキストをObsidianから読み込む
        
        Args:
            file_path (str): Vault内のファイルパス
            
        Returns:
            str: ファイル内容（読み込み失敗時はNone）
        """
        
        # 方法1: PowerShell経由でUTF8読み込み
        try:
            full_path = f"{self.vault_path}\\{file_path}"
            
            ps_command = f"""
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Get-Content '{full_path}' -Encoding UTF8 -Raw
"""
            
            result = subprocess.run([
                'powershell.exe', '-Command', ps_command
            ], capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                print(f"✅ PowerShell UTF8方式で読み込み成功: {file_path}")
                return result.stdout
            else:
                print(f"❌ PowerShell読み込みエラー: {result.stderr}")
                
        except Exception as e:
            print(f"❌ PowerShell読み込み失敗: {e}")
        
        # 方法2: Python直接読み込み
        for base_path in [self.vault_path, self.fallback_path]:
            try:
                full_path = Path(base_path) / file_path
                
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print(f"✅ Python直接読み込み成功: {full_path}")
                return content
                
            except Exception as e:
                print(f"❌ Python読み込み失敗 ({base_path}): {e}")
        
        return None
    
    def test_japanese_writing(self):
        """日本語書き込みテスト"""
        test_content = """# 日本語テスト

## 概要
これは日本語文字の書き込みテストです。

## 内容
- ひらがな: あいうえお
- カタカナ: アイウエオ  
- 漢字: 日本語文字化けテスト
- 記号: 「」、。・

## 技術要素
- UTF-8エンコーディング
- PowerShell UTF8出力
- Obsidian Vault統合

## 結論
この方法で日本語が正しく書き込まれていれば成功です。

#日本語 #テスト #UTF8 #Obsidian
"""
        
        test_file = "Tests/japanese_test.md"
        
        print("🧪 日本語書き込みテストを実行中...")
        success = self.write_japanese_text(test_file, test_content)
        
        if success:
            print("📖 書き込んだ内容を読み戻してテスト...")
            read_content = self.read_japanese_text(test_file)
            
            if read_content and "日本語" in read_content:
                print("✅ 日本語テスト完全成功！")
                return True
            else:
                print("❌ 読み戻しで文字化けが発生")
                return False
        else:
            print("❌ 書き込みテスト失敗")
            return False

def main():
    """メイン関数"""
    import sys
    
    writer = ObsidianJapaneseWriter()
    
    if len(sys.argv) == 1:
        # テストモード
        writer.test_japanese_writing()
    elif len(sys.argv) == 3:
        # 書き込みモード
        file_path = sys.argv[1]
        content = sys.argv[2]
        writer.write_japanese_text(file_path, content)
    elif len(sys.argv) == 2 and sys.argv[1] == "read":
        # 読み込みテスト
        content = writer.read_japanese_text("Tests/japanese_test.md")
        if content:
            print("📄 読み込み内容:")
            print(content)
    else:
        print("""
日本語Obsidianライター

使用方法:
  python3 obsidian_japanese_writer.py                    # テスト実行
  python3 obsidian_japanese_writer.py "path.md" "内容"    # ファイル書き込み
  python3 obsidian_japanese_writer.py read               # テストファイル読み込み
""")

if __name__ == "__main__":
    main()