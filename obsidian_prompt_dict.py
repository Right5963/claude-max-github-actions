#!/usr/bin/env python3
"""
Obsidianプロンプト辞典 完全版
============================
MCPブリッジ経由でObsidianの辞典を活用
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

class ObsidianPromptDictionary:
    def __init__(self):
        self.mcp_bridge = "/mnt/c/Claude Code/tool/mcp_bridge_extended.sh"
        self.dict_base = "PromptDictionary"
        
    def setup_dictionary(self):
        """Obsidianに辞典構造を初期設定"""
        print("📚 Obsidianプロンプト辞典をセットアップ中...")
        
        # 初期辞典構造
        initial_dict = {
            "Characters/基本属性.md": """# 基本属性
## 人数
- 1girl #売れ筋No1
- 2girls #グループ需要
- 1boy #男性キャラ
- multiple girls #3人以上

## 年齢層
- young girl #10代
- mature female #大人
- chibi #デフォルメ""",
            
            "Characters/人気髪型.md": """# 人気髪型
## 長さ
- long hair #ロング人気
- short hair #ショート
- medium hair #ミディアム

## スタイル  
- twintails #ツインテール
- ponytail #ポニーテール
- braid #三つ編み""",
            
            "Styles/画風.md": """# 画風辞典
## アート系
- anime style #アニメ調
- realistic #リアル系
- watercolor #水彩画風
- digital art #デジタルアート

## 品質タグ
- masterpiece #最高品質
- best quality #高品質
- detailed #詳細
- 8k resolution #超高解像度""",
            
            "Success/売れ筋パターン.md": """# 売れ筋パターン
## 2024年ヒット
- 1girl, school uniform, smile #学園系
- fantasy, magical girl #魔法少女系
- cyberpunk, neon lights #サイバーパンク

## 季節もの
- cherry blossoms, spring #春/桜
- beach, summer #夏/海
- autumn leaves #秋/紅葉
- snow, winter #冬/雪"""
        }
        
        # Obsidianに辞典を作成
        for path, content in initial_dict.items():
            full_path = f"{self.dict_base}/{path}"
            self._write_to_obsidian(full_path, content)
            
        print("✅ 辞典セットアップ完了！")
        
    def _write_to_obsidian(self, path, content):
        """Obsidianにファイルを書き込む"""
        # ファイル内容を一時保存
        temp_file = f"/tmp/obsidian_temp_{datetime.now().timestamp()}.md"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        # MCPブリッジ経由で書き込み
        cmd = f'cat "{temp_file}" | {self.mcp_bridge} obsidian_write "{path}"'
        subprocess.run(cmd, shell=True, capture_output=True)
        os.remove(temp_file)
        
    def search_dictionary(self, keyword):
        """辞典から関連タグを検索"""
        print(f"\n🔍 '{keyword}'に関連するタグを検索中...")
        
        # MCPブリッジで検索
        cmd = f'{self.mcp_bridge} obsidian_search "{keyword}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # 結果をパース
        found_tags = []
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if "#" in line:  # タグを含む行
                    # タグを抽出
                    import re
                    tags = re.findall(r'- ([^#]+)', line)
                    found_tags.extend(tags)
        
        return [tag.strip() for tag in found_tags if tag.strip()]
    
    def generate_wildcard(self, keyword, include_success=True):
        """キーワードからワイルドカード生成"""
        print(f"\n🎯 '{keyword}' のワイルドカード生成開始")
        
        # 関連タグを検索
        related_tags = self.search_dictionary(keyword)
        
        # カテゴリ別に整理
        categories = {
            "character": [],
            "style": [],
            "quality": [],
            "theme": []
        }
        
        # 基本的な売れ筋タグも追加
        if include_success:
            categories["character"].extend(["1girl", "cute", "smile"])
            categories["style"].extend(["anime style", "detailed"])
            categories["quality"].extend(["masterpiece", "best quality", "8k"])
        
        # 検索結果を分類
        for tag in related_tags:
            if any(word in tag for word in ["girl", "boy", "hair", "eyes"]):
                categories["character"].append(tag)
            elif any(word in tag for word in ["style", "art", "painting"]):
                categories["style"].append(tag)
            elif any(word in tag for word in ["quality", "detailed", "resolution"]):
                categories["quality"].append(tag)
            else:
                categories["theme"].append(tag)
        
        # ワイルドカードファイル生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"obsidian_wildcard_{keyword.replace(' ', '_')}_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Obsidian辞典ベース: {keyword}\n")
            f.write(f"# 生成: {datetime.now()}\n\n")
            
            for cat_name, tags in categories.items():
                if tags:
                    # 重複を除去
                    unique_tags = list(set(tags))
                    f.write(f"# __{cat_name}__\n")
                    for tag in unique_tags:
                        f.write(f"{tag}\n")
                    f.write("\n")
        
        print(f"✅ ワイルドカード生成完了: {filename}")
        
        # 推奨プロンプト
        print("\n📝 推奨プロンプト:")
        print(f"1. __character__, __style__, __quality__, {keyword}")
        print(f"2. __character__, {keyword}, __theme__, detailed background")
        print(f"3. {keyword}, __style__, masterpiece, high resolution")
        
        return filename
    
    def add_success_pattern(self, tags, price, notes=""):
        """売れた商品のパターンを辞典に追加"""
        print("\n💰 成功パターンを辞典に追加")
        
        # 現在の日付
        date = datetime.now().strftime("%Y-%m-%d")
        
        # 追記内容
        new_entry = f"\n\n## {date} 追加\n"
        new_entry += f"- {', '.join(tags)} #{price}円で落札\n"
        if notes:
            new_entry += f"  メモ: {notes}\n"
        
        # Success辞典に追記
        success_path = f"{self.dict_base}/Success/売れ筋パターン.md"
        
        # 現在の内容を読み込み
        cmd = f'{self.mcp_bridge} obsidian_read "{success_path}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        current_content = result.stdout if result.returncode == 0 else ""
        updated_content = current_content + new_entry
        
        # 更新
        self._write_to_obsidian(success_path, updated_content)
        
        print(f"✅ 成功パターンを追加しました（{price}円）")

def main():
    """メイン実行"""
    dict_system = ObsidianPromptDictionary()
    
    print("🎨 Obsidianプロンプト辞典システム")
    print("=" * 50)
    print("1. 初期セットアップ（初回のみ）")
    print("2. キーワードからワイルドカード生成")
    print("3. 売れたパターンを辞典に追加")
    print("4. 辞典を検索")
    
    choice = "default_value"  # input("\n選択 (1-4): ").strip()
    
    if choice == "1":
        dict_system.setup_dictionary()
        
    elif choice == "2":
        keyword = "default_value"  # input("キーワード: ")
        dict_system.generate_wildcard(keyword)
        
    elif choice == "3":
        tags = "default_value"  # input("売れたタグ（カンマ区切り）: ").split(",")
        price = "default_value"  # input("落札価格: ")
        notes = "default_value"  # input("メモ（任意）: ")
        dict_system.add_success_pattern(
            [tag.strip() for tag in tags],
            price,
            notes
        )
        
    elif choice == "4":
        keyword = "default_value"  # input("検索キーワード: ")
        results = dict_system.search_dictionary(keyword)
        print(f"\n見つかったタグ: {', '.join(results)}")

if __name__ == "__main__":
    main()