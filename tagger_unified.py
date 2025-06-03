#!/usr/bin/env python3
"""
Simple Tagger
============
シンプルな画像タグ付けツール（複雑な12KBシステムの代替）
"""

import os
import json
from datetime import datetime

class SimpleTagger:
    def __init__(self):
        # 売れ筋タグデータベース（実データから）
        self.popular_tags = {
            "キャラクター": ["美少女", "かわいい", "クール", "エレガント"],
            "スタイル": ["アニメ風", "リアル", "イラスト", "デジタルアート"],
            "品質": ["高画質", "最高品質", "詳細", "鮮明"],
            "サイズ": ["A4", "A3", "B4", "ポスターサイズ"],
            "特徴": ["限定", "オリジナル", "手描き風", "プロ仕様"]
        }
        
        self.market_tags = [
            "masterpiece", "best quality", "detailed", "high resolution",
            "beautiful", "cute", "anime style", "digital art", "poster"
        ]
    
    def analyze_filename(self, filename):
        """ファイル名からタグ推測"""
        
        tags = []
        filename_lower = filename.lower()
        
        # キーワード検出
        keywords = {
            "anime": ["アニメ風", "anime style"],
            "girl": ["美少女", "girl"],
            "cute": ["かわいい", "cute"],
            "poster": ["ポスター", "poster"],
            "art": ["アート", "digital art"],
            "high": ["高画質", "high quality"],
            "detailed": ["詳細", "detailed"]
        }
        
        for key, tag_list in keywords.items():
            if key in filename_lower:
                tags.extend(tag_list)
        
        return tags
    
    def generate_market_tags(self, base_concept="美少女"):
        """市場向けタグ生成"""
        
        # ベースタグ
        tags = [base_concept, "高画質", "詳細"]
        
        # ランダムに追加
        import random
        tags.extend(random.sample(self.market_tags, 3))
        
        # 人気タグからランダム選択
        for category, tag_list in self.popular_tags.items():
            if random.random() > 0.5:  # 50%の確率で追加
                tags.append(random.choice(tag_list))
        
        return list(set(tags))  # 重複除去
    
    def create_wildcard(self, tags, filename="output"):
        """ワイルドカード形式で保存"""
        
        # SD用プロンプト形式
        positive_prompt = ", ".join(tags + ["masterpiece", "best quality"])
        negative_prompt = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality"
        
        wildcard_content = f"""# {filename} Wildcard
        
__positive_tags__
{positive_prompt}

__negative_tags__
{negative_prompt}

__style_variants__
anime style
realistic style
digital art style
illustration style

__quality_boost__
masterpiece, best quality, ultra detailed, 8k, high resolution
"""
        
        with open(f"{filename}_wildcard.txt", 'w', encoding='utf-8') as f:
            f.write(wildcard_content)
        
        return f"{filename}_wildcard.txt"
    
    def quick_tag(self, image_path=None, concept="美少女 ポスター"):
        """クイックタグ付け"""
        
        if image_path and os.path.exists(image_path):
            # ファイル名解析
            filename_tags = self.analyze_filename(os.path.basename(image_path))
            print(f"📁 ファイル名タグ: {filename_tags}")
        else:
            filename_tags = []
        
        # 市場タグ生成
        market_tags = self.generate_market_tags(concept)
        
        # 統合
        all_tags = list(set(filename_tags + market_tags))
        
        print(f"🏷️ 生成タグ ({len(all_tags)}個):")
        for i, tag in enumerate(all_tags, 1):
            print(f"  {i}. {tag}")
        
        # ワイルドカード作成
        wildcard_file = self.create_wildcard(all_tags, "quick_tags")
        print(f"✅ ワイルドカード保存: {wildcard_file}")
        
        # JSON保存
        result = {
            'timestamp': datetime.now().isoformat(),
            'concept': concept,
            'image_path': image_path,
            'filename_tags': filename_tags,
            'market_tags': market_tags,
            'all_tags': all_tags
        }
        
        with open('simple_tagger_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"💾 結果保存: simple_tagger_result.json")
        
        return all_tags

def main():
    """メイン実行"""
    
    import sys
    
    tagger = SimpleTagger()
    
    # 引数チェック
    if len(sys.argv) > 1:
        concept = sys.argv[1]
    else:
        concept = "美少女 アニメ ポスター"
    
    print(f"🎨 Simple Tagger 起動")
    print(f"💡 コンセプト: {concept}")
    print("=" * 40)
    
    # クイックタグ実行
    tags = tagger.quick_tag(concept=concept)
    
    print(f"\n🎯 Stable Diffusion用プロンプト:")
    print(", ".join(tags + ["masterpiece", "best quality"]))

if __name__ == "__main__":
    main()