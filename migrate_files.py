#!/usr/bin/env python3
"""
整理済みファイルをGドライブObsidian Vaultに移行
"""

import os
import subprocess
import shutil
from pathlib import Path

def main():
    source_base = Path("/mnt/c/Claude Code/tool/organized_files")
    
    # カテゴリとファイル数を確認
    categories = {
        "01_Market_Research": [],
        "02_Technical_Knowledge": [],
        "03_Strategy_Planning": [],
        "04_Execution_Records": [],
        "05_Success_Cases": [],
        "00_Extracted_Insights": [],
        "99_Uncategorized": []
    }
    
    total_files = 0
    
    for category, files in categories.items():
        category_path = source_base / category
        if category_path.exists():
            md_files = list(category_path.glob("*.md"))
            # _index.mdとGドライブパスのファイルを除外
            md_files = [f for f in md_files if f.name != "_index.md" and not f.name.startswith("G:")]
            categories[category] = md_files
            total_files += len(md_files)
            print(f"{category}: {len(md_files)} ファイル")
    
    print(f"\n総ファイル数: {total_files}")
    
    # PowerShellコマンドでファイルをコピー
    print("\n=== ファイル移行開始 ===")
    
    for category, files in categories.items():
        if not files:
            continue
            
        target_category = category
        if category == "00_Extracted_Insights" or category == "99_Uncategorized":
            target_category = "00_Knowledge_Hub"
            
        for file_path in files:
            try:
                target_path = f"G:\\マイドライブ\\Obsidian Vault\\AI_Generated_Content_Business\\{target_category}\\{file_path.name}"
                
                # PowerShell経由でコピー
                cmd = [
                    'powershell.exe', '-Command',
                    f'Copy-Item "{file_path.as_posix()}" "{target_path}" -Force'
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✓ {file_path.name} → {target_category}/")
                else:
                    print(f"✗ エラー: {file_path.name}")
                    
            except Exception as e:
                print(f"✗ 例外: {file_path.name} - {e}")
    
    print("\n=== 移行完了 ===")
    
    # 結果確認
    cmd = [
        'powershell.exe', '-Command',
        '''
        $base = "G:\\マイドライブ\\Obsidian Vault\\AI_Generated_Content_Business"
        $categories = @("01_Market_Research", "02_Technical_Knowledge", "03_Strategy_Planning", "04_Execution_Records", "05_Success_Cases", "00_Knowledge_Hub")
        
        $total = 0
        foreach ($cat in $categories) {
            $path = Join-Path $base $cat
            if (Test-Path $path) {
                $count = (Get-ChildItem -Path $path -Filter "*.md" -ErrorAction SilentlyContinue).Count
                Write-Host "$cat`: $count files"
                $total += $count
            }
        }
        Write-Host ""
        Write-Host "Total: $total files migrated"
        '''
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    main()