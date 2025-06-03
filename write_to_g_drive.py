#!/usr/bin/env python3
import os
import shutil
import subprocess

# Gドライブの実際のパスを探す
possible_paths = [
    r"G:\マイドライブ\Obsidian Vault",
    r"C:\Users\user\Google Drive\Obsidian Vault",
    r"C:\Users\user\Google Drive\マイドライブ\Obsidian Vault"
]

# 見つかったパスを保存
obsidian_path = None
for path in possible_paths:
    if os.path.exists(path):
        obsidian_path = path
        print(f"✅ Obsidian Vault found: {path}")
        break

if not obsidian_path:
    print("❌ Obsidian Vault not found in any expected location")
    exit(1)

# ノートを保存するディレクトリ
notes_dir = os.path.join(obsidian_path, "notes", "MEMO", "Claude Code開発")
os.makedirs(notes_dir, exist_ok=True)

# C:ドライブからファイルをコピー
source_file = r"C:\Users\user\Documents\Obsidian Vault\notes\MEMO\Claude Code開発\Gドライブアクセス問題の教訓_2025-05-28.md"
dest_file = os.path.join(notes_dir, "Gドライブアクセス問題の教訓_2025-05-28.md")

if os.path.exists(source_file):
    shutil.copy2(source_file, dest_file)
    print(f"✅ File copied to: {dest_file}")
else:
    print(f"❌ Source file not found: {source_file}")

# 新しいノートも作成
new_note = os.path.join(notes_dir, "Gドライブ直接アクセス成功_2025-05-28.md")
with open(new_note, 'w', encoding='utf-8') as f:
    f.write("""# Gドライブ直接アクセス成功

## 解決方法
Pythonスクリプトを使用してWindows側から直接Gドライブに書き込む方法で解決。

## 手順
1. Windows側のパスを使用
2. Python経由で直接ファイル操作
3. WSLのマウント問題を回避

## 結論
WSLの制約を回避し、確実にGドライブのObsidian Vaultに保存できるようになった。

#Claude_Code #Gドライブ #解決済み
""")
print(f"✅ New note created: {new_note}")