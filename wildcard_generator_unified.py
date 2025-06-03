#!/usr/bin/env python3
"""
シンプルワイルドカード生成 - 単一テキストファイル形式
既存のyaml1ファイルと同じ形式で生成
"""

import os
import sys
from collections import Counter
from pathlib import Path
from datetime import datetime

def extract_tags_from_directory(tagger_dir):
    """ディレクトリからタグを抽出"""
    all_tags = []
    tagged_path = Path(tagger_dir)
    
    if not tagged_path.exists():
        print(f"❌ ディレクトリが見つかりません: {tagger_dir}")
        return all_tags
    
    txt_files = list(tagged_path.glob("*.txt"))
    print(f"📁 {len(txt_files)}個のtxtファイルを処理中...")
    
    for txt_file in txt_files:
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
                tags = [tag.strip() for tag in content.split(',')]
                all_tags.extend(tags)
        except Exception as e:
            print(f"⚠️ ファイル読み込みエラー: {txt_file} - {e}")
    
    return all_tags

def categorize_tags_simple(all_tags):
    """シンプルなカテゴリ分類"""
    tag_counts = Counter(all_tags)
    
    categories = {
        'characterface': [],
        'characterbody': [],
        'clothing': [],
        'poseemotion': [],
        'angle': [],
        'backgrounds': [],
        'style': [],
        'quality': [],
        'general': []
    }
    
    # キーワードベースで分類（日本語と英語両対応）
    category_keywords = {
        'characterface': ['hair', 'eyes', 'face', 'head', 'eyebrows', 'nose', 'mouth', '髪', '目', '顔', 'blonde', 'blue eyes'],
        'characterbody': ['body', 'chest', 'waist', 'legs', 'arms', 'skin', 'figure', '体', '胸', '腕'],
        'clothing': ['dress', 'uniform', 'shirt', 'skirt', 'pants', 'jacket', 'outfit', 'clothing', '服', '制服', 'school uniform'],
        'poseemotion': ['standing', 'sitting', 'walking', 'smile', 'happy', 'sad', 'angry', 'pose', 'expression', '笑顔', 'smile'],
        'angle': ['from', 'view', 'angle', 'side', 'front', 'back', 'above', 'below', '正面', '横'],
        'backgrounds': ['background', 'outdoor', 'indoor', 'street', 'room', 'park', 'beach', 'sky', '背景', '室内'],
        'style': ['anime', 'realistic', 'art', 'illustration', 'manga', 'cartoon', 'style', 'digital', 'アニメ', 'digital art'],
        'quality': ['masterpiece', 'best quality', 'detailed', 'high resolution', 'ultra', '8k', '4k', 'HD', '高画質', '詳細']
    }
    
    # すべてのタグを処理（頻度に関係なく）
    for tag in all_tags:
        tag_lower = tag.lower().strip()
        categorized = False
        
        for category, keywords in category_keywords.items():
            if any(keyword in tag_lower for keyword in keywords):
                if tag not in categories[category]:  # 重複を避ける
                    categories[category].append(tag)
                categorized = True
                break
        
        if not categorized:
            if tag not in categories['general']:  # 重複を避ける
                categories['general'].append(tag)
    
    return categories

def create_combinations(tags, max_combinations=25):
    """タグの組み合わせを作成"""
    import random
    
    if len(tags) < 2:
        return tags[:max_combinations]
    
    combinations = []
    
    # 単体タグ（上位の頻出タグ）
    combinations.extend(tags[:5])
    
    # 組み合わせ作成
    for _ in range(max_combinations - len(combinations)):
        if len(tags) >= 2:
            combo_size = random.randint(2, min(5, len(tags)))
            combo = random.sample(tags, combo_size)
            combination = ", ".join(combo)
            combinations.append(combination)
    
    return combinations[:max_combinations]

def generate_simple_wildcard(tagger_dir, theme_name):
    """シンプルワイルドカード生成"""
    print(f"🎯 シンプルワイルドカード生成開始")
    print(f"入力: {tagger_dir}")
    print(f"テーマ: {theme_name}")
    
    # タグ抽出
    all_tags = extract_tags_from_directory(tagger_dir)
    if not all_tags:
        print("❌ タグが見つかりませんでした")
        return None
    
    print(f"📊 総タグ数: {len(all_tags)}個")
    print(f"📊 ユニークタグ数: {len(set(all_tags))}個")
    
    # カテゴリ分類
    categories = categorize_tags_simple(all_tags)
    
    # 出力ファイル名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"wildcards_{theme_name}_{timestamp}.txt"
    # カレントディレクトリのwildcardsフォルダに保存
    output_dir = os.path.join(os.getcwd(), "wildcards")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    
    # ワイルドカード内容生成（シンプルテキスト形式）
    content = f"# Wildcard for {theme_name}\n"
    content += f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    content += f"# Total tags: {len(set(all_tags))}\n\n"
    
    # メインプロンプトテンプレート
    content += "# Main template:\n"
    content += "# 1girl, solo, {characterface}, {characterbody}, {clothing}, {poseemotion}, {angle}, {backgrounds}, {style}\n\n"
    
    for category, tags in categories.items():
        if not tags:
            continue
            
        content += f"# {category.upper()}\n"
        
        # 頻度の高い順に並べる
        tag_counts = Counter(tags)
        sorted_tags = [tag for tag, _ in tag_counts.most_common()]
        
        # 単体タグとして出力
        for tag in sorted_tags[:20]:  # 上位20個のみ
            content += f"{tag}\n"
        
        content += "\n"
    
    # ファイル保存
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ ワイルドカード生成完了: {filename}")
        print(f"📁 保存先: {output_path}")
        
        # カテゴリ統計表示
        print(f"\n📊 カテゴリ別統計:")
        for category, tags in categories.items():
            if tags:
                print(f"   {category}: {len(tags)}個のタグ")
        
        return output_path
        
    except Exception as e:
        print(f"❌ ファイル保存エラー: {e}")
        return None

def main():
    if len(sys.argv) < 3:
        print("使用方法:")
        print(f"{sys.argv[0]} <tagger_directory> <theme_name>")
        print(f"例: {sys.argv[0]} './manual_test_project/tagger_results' '美少女'")
        return
    
    tagger_dir = sys.argv[1]
    theme_name = sys.argv[2]
    
    result = generate_simple_wildcard(tagger_dir, theme_name)
    
    if result:
        print(f"\n🎉 完了！生成されたファイル: {result}")
        print(f"\n📝 使用例:")
        print(f"1. Dynamic Promptsで使用")
        print(f"2. 手動でコピー&ペースト")
        print(f"3. 他のワイルドカードツールで読み込み")

if __name__ == "__main__":
    main()