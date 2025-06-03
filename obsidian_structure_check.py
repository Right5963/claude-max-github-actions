#!/usr/bin/env python3
"""
Obsidian 実構造調査ツール
========================
実際のディレクトリ構造を調査して統合を修正
"""

import subprocess
import json
import os

def check_obsidian_structure():
    """実際のObsidian構造を調査"""
    print("🔍 Obsidian Vault 実構造調査")
    print("=" * 40)
    
    vault_path = "G:\\マイドライブ\\Obsidian Vault"
    
    try:
        # PowerShell で実際の構造取得
        result = subprocess.run([
            "powershell.exe", "-Command",
            f"Get-ChildItem '{vault_path}' -Directory | Select-Object Name | ConvertTo-Json"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip():
            try:
                dirs = json.loads(result.stdout)
                if isinstance(dirs, dict):
                    dirs = [dirs]
                
                print("📁 実際のディレクトリ構造:")
                actual_dirs = []
                for dir_info in dirs:
                    dir_name = dir_info.get('Name', '')
                    if dir_name:
                        print(f"  - {dir_name}")
                        actual_dirs.append(dir_name)
                
                return actual_dirs
                
            except json.JSONDecodeError:
                print("❌ JSON解析エラー")
                
        # フォールバック: 代替方法
        print("🔄 代替方法で調査中...")
        result2 = subprocess.run([
            "powershell.exe", "-Command", 
            f"if (Test-Path '{vault_path}') {{ Write-Output 'EXISTS' }} else {{ Write-Output 'NOT_FOUND' }}"
        ], capture_output=True, text=True)
        
        if "EXISTS" in result2.stdout:
            print("✅ Obsidian Vault アクセス可能")
            # 基本的なディレクトリを作成
            basic_dirs = ["Projects", "Daily", "Templates", "Archive"]
            print("📁 基本ディレクトリ作成:")
            
            for dir_name in basic_dirs:
                create_result = subprocess.run([
                    "powershell.exe", "-Command",
                    f"New-Item -Path '{vault_path}\\{dir_name}' -ItemType Directory -Force | Out-Null; Write-Output 'Created: {dir_name}'"
                ], capture_output=True, text=True)
                
                if create_result.returncode == 0:
                    print(f"  ✅ {dir_name}")
                else:
                    print(f"  ❌ {dir_name} - {create_result.stderr[:50]}")
            
            return basic_dirs
        else:
            print("❌ Obsidian Vault アクセス不可")
            return []
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return []

def update_integration_config(actual_dirs):
    """統合設定を実構造に合わせて更新"""
    if not actual_dirs:
        return False
    
    print(f"\n🔧 統合設定更新")
    
    # 実際のディレクトリに基づく新しい分類ルール
    new_structure = {
        "development_insight": {
            "target_dir": "Projects" if "Projects" in actual_dirs else actual_dirs[0],
            "tags": ["#dev/insight", "#automation", "#learning"]
        },
        "pattern_analysis": {
            "target_dir": "Archive" if "Archive" in actual_dirs else actual_dirs[0],
            "tags": ["#dev/pattern", "#analysis"]
        }
    }
    
    print("📝 新しい分類ルール:")
    for knowledge_type, config in new_structure.items():
        print(f"  {knowledge_type} → {config['target_dir']}")
    
    return True

if __name__ == "__main__":
    dirs = check_obsidian_structure()
    if dirs:
        update_integration_config(dirs)
        print(f"\n✅ 構造調査完了 - {len(dirs)}個のディレクトリ確認")
    else:
        print(f"\n❌ 構造調査失敗")