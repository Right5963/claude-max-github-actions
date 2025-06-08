#!/usr/bin/env python3
"""
散乱したファイルを効率的に整理するスクリプト
ファイル名とキーワードからカテゴリを自動判定
"""

import os
import shutil
from pathlib import Path

# ファイル分類ルール
FILE_CATEGORIES = {
    "01_Market_Research": [
        "fanza", "dmm", "doujin", "yahoo", "auction", "market", "research",
        "popular", "trend", "sales", "ranking", "hidden_gems", "visual_impression"
    ],
    "02_Technical_Knowledge": [
        "mcp", "claude", "llm", "ollama", "api", "github", "git", "code",
        "workflow", "technical", "development", "tal", "system", "automation",
        "integration", "bridge", "setup", "guide", "implementation"
    ],
    "03_Strategy_Planning": [
        "strategy", "plan", "analysis", "optimization", "tal_thinking",
        "decision", "framework", "roadmap", "approach"
    ],
    "04_Execution_Records": [
        "record", "log", "session", "report", "status", "progress",
        "test", "result", "execution", "daily", "tracker"
    ],
    "05_Success_Cases": [
        "success", "complete", "achievement", "milestone", "working",
        "verified", "proven", "case", "example"
    ]
}

def categorize_file(filename):
    """ファイル名から適切なカテゴリを判定"""
    filename_lower = filename.lower()
    
    # 各カテゴリのキーワードをチェック
    best_category = None
    best_score = 0
    
    for category, keywords in FILE_CATEGORIES.items():
        score = sum(1 for keyword in keywords if keyword in filename_lower)
        if score > best_score:
            best_score = score
            best_category = category
            
    # スコアが0の場合はデフォルトカテゴリ
    if best_score == 0:
        best_category = "99_Uncategorized"
        
    return best_category

def organize_files():
    """散乱したファイルを整理"""
    source_dir = Path("/mnt/c/Claude Code/tool")
    target_base = Path("/mnt/c/Claude Code/tool/organized_files")
    
    # ターゲットディレクトリを作成
    target_base.mkdir(exist_ok=True)
    
    # カテゴリディレクトリを作成
    for category in FILE_CATEGORIES.keys():
        (target_base / category).mkdir(exist_ok=True)
    (target_base / "99_Uncategorized").mkdir(exist_ok=True)
    
    # 統計
    stats = {
        "total": 0,
        "organized": 0,
        "skipped": 0
    }
    
    # MDファイルのみを対象
    md_files = list(source_dir.glob("*.md"))
    
    print(f"=== ファイル整理開始 ===")
    print(f"対象ファイル数: {len(md_files)}")
    
    for file_path in md_files:
        stats["total"] += 1
        
        # 重要なシステムファイルはスキップ
        if file_path.name in ["CLAUDE.md", "README.md"]:
            print(f"スキップ: {file_path.name} (システムファイル)")
            stats["skipped"] += 1
            continue
            
        # カテゴリを判定
        category = categorize_file(file_path.name)
        
        # ターゲットパスを作成
        target_path = target_base / category / file_path.name
        
        # ファイルをコピー（元のファイルは残す）
        try:
            shutil.copy2(file_path, target_path)
            print(f"✓ {file_path.name} → {category}/")
            stats["organized"] += 1
        except Exception as e:
            print(f"✗ エラー: {file_path.name} - {e}")
            
    # 統計を表示
    print(f"\n=== 整理完了 ===")
    print(f"総ファイル数: {stats['total']}")
    print(f"整理済み: {stats['organized']}")
    print(f"スキップ: {stats['skipped']}")
    
    # カテゴリ別統計
    print(f"\n=== カテゴリ別統計 ===")
    for category in os.listdir(target_base):
        category_path = target_base / category
        if category_path.is_dir():
            file_count = len(list(category_path.glob("*.md")))
            if file_count > 0:
                print(f"{category}: {file_count}ファイル")
    
    return target_base

def create_category_index(target_base):
    """各カテゴリのインデックスファイルを作成"""
    print(f"\n=== インデックス作成 ===")
    
    for category_dir in target_base.iterdir():
        if not category_dir.is_dir():
            continue
            
        md_files = list(category_dir.glob("*.md"))
        if not md_files:
            continue
            
        index_content = f"# {category_dir.name} Index\n\n"
        index_content += f"総ファイル数: {len(md_files)}\n\n"
        index_content += "## ファイル一覧\n\n"
        
        for file_path in sorted(md_files):
            index_content += f"- [[{file_path.stem}]]\n"
            
        index_path = category_dir / "_index.md"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
            
        print(f"✓ インデックス作成: {category_dir.name}/_index.md")

if __name__ == "__main__":
    # ファイルを整理
    target_base = organize_files()
    
    # インデックスを作成
    create_category_index(target_base)
    
    print("\n整理されたファイルは organized_files/ ディレクトリに保存されました。")
    print("Gドライブへの移動は手動で行ってください。")