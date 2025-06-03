#!/usr/bin/env python3
"""
Obsidianプロンプト辞典→ワイルドカード変換
=========================================
売れ筋の知識を資産化して即座に活用
"""

import os
import re
from pathlib import Path
from datetime import datetime

def read_obsidian_dictionary(vault_path, category):
    """Obsidianから特定カテゴリの辞典を読み込む"""
    
    # MCPブリッジ経由でObsidianにアクセス
    dict_path = f"PromptDictionary/{category}"
    
    # 簡易実装：ローカルファイルから読み込み
    # 実際はMCPブリッジ使用
    tags = []
    
    # デモ用のビルトイン辞典
    built_in_dict = {
        "character": {
            "基本": ["1girl", "2girls", "1boy", "multiple girls"],
            "髪型": ["long hair", "short hair", "twintails", "ponytail", "blonde hair"],
            "表情": ["smile", "serious", "wink", "open mouth", "closed eyes"],
            "衣装": ["school uniform", "casual", "dress", "kimono", "swimsuit"]
        },
        "style": {
            "画風": ["anime style", "realistic", "watercolor", "oil painting", "sketch"],
            "品質": ["masterpiece", "best quality", "high resolution", "detailed", "8k"],
            "雰囲気": ["vibrant colors", "pastel colors", "monochrome", "dark theme", "bright"]
        },
        "theme": {
            "ジャンル": ["fantasy", "sci-fi", "slice of life", "action", "romance"],
            "背景": ["simple background", "detailed background", "outdoors", "indoors", "nature"],
            "時間帯": ["day", "night", "sunset", "morning", "golden hour"]
        }
    }
    
    return built_in_dict.get(category, {})

def create_smart_wildcard(keyword, use_dictionary=True):
    """キーワードから賢いワイルドカードを生成"""
    
    print(f"\n📚 プロンプト辞典からワイルドカード生成")
    print("=" * 50)
    
    if use_dictionary:
        print("✅ Obsidian辞典モード（売れ筋データ活用）")
        
        # 辞典から読み込み
        characters = read_obsidian_dictionary("", "character")
        styles = read_obsidian_dictionary("", "style")
        themes = read_obsidian_dictionary("", "theme")
        
        # キーワードに応じて最適な組み合わせを選択
        selected_tags = {
            "character_base": characters.get("基本", []),
            "character_hair": characters.get("髪型", []),
            "character_face": characters.get("表情", []),
            "style_art": styles.get("画風", []),
            "style_quality": styles.get("品質", []),
            "theme_genre": themes.get("ジャンル", [])
        }
        
    else:
        print("⚡ クイックモード（基本タグのみ）")
        selected_tags = {
            "character_base": ["1girl", "2girls"],
            "style_quality": ["masterpiece", "best quality"]
        }
    
    # ワイルドカードファイル生成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"wildcard_dict_{keyword.replace(' ', '_')}_{timestamp}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {keyword} - Obsidian辞典ベース\n")
        f.write(f"# 生成日時: {datetime.now()}\n\n")
        
        for category, tags in selected_tags.items():
            if tags:
                f.write(f"# __{category}__\n")
                for tag in tags:
                    f.write(f"{tag}\n")
                f.write("\n")
    
    # 推奨プロンプト生成
    print(f"\n📝 生成されたワイルドカード: {filename}")
    print("\n🎨 推奨プロンプト:")
    print(f"1. __character_base__, __character_hair__, __character_face__, __style_art__, {keyword}")
    print(f"2. __character_base__, __style_quality__, {keyword}, __theme_genre__")
    print(f"3. {keyword}, __style_art__, __style_quality__, detailed")
    
    return filename

def update_dictionary_from_success(sold_item_tags):
    """売れた商品のタグを辞典に追加"""
    print("\n📈 成功パターンを辞典に追加")
    # 実装：MCPブリッジ経由でObsidianに追記
    print(f"  → {len(sold_item_tags)}個のタグを辞典に追加予定")

def main():
    print("🎯 Obsidianプロンプト辞典システム")
    print("\n選択してください:")
    print("1. 辞典からワイルドカード生成（推奨）")
    print("2. クイック生成（辞典なし）")
    print("3. 売れたタグを辞典に追加")
    
    choice = "default_value"  # input("\n選択 (1-3): ").strip()
    
    if choice == "1":
        keyword = "default_value"  # input("キーワード: ")
        create_smart_wildcard(keyword, use_dictionary=True)
    elif choice == "2":
        keyword = "default_value"  # input("キーワード: ")
        create_smart_wildcard(keyword, use_dictionary=False)
    elif choice == "3":
        tags = "default_value"  # input("売れた商品のタグ（カンマ区切り）: ")
        update_dictionary_from_success(tags.split(","))

if __name__ == "__main__":
    main()