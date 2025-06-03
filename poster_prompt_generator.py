#!/usr/bin/env python3
"""
ポスター用プロンプト生成ツール
============================
売れ筋スタイルのプロンプトを瞬時に生成
"""

import random

# 売れ筋の要素（実際の落札データから）
styles = ["anime style", "detailed illustration", "vibrant colors", "high quality"]
themes = ["cute girl", "cool character", "fantasy scene", "cyberpunk", "traditional japanese"]
moods = ["cheerful", "mysterious", "dynamic", "peaceful", "dramatic"]

def generate_prompts(base_keyword, count=3):
    """売れ筋プロンプトを生成"""
    prompts = []
    
    for i in range(count):
        style = random.choice(styles)
        theme = random.choice(themes)
        mood = random.choice(moods)
        
        prompt = f"{base_keyword}, {theme}, {mood}, {style}, masterpiece, best quality, poster art"
        prompts.append(prompt)
    
    return prompts

if __name__ == "__main__":
    import sys
    
    # コマンドライン引数またはデフォルト使用
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    else:
        keyword = "アニメ ポスター"  # デフォルト
    
    print(f"\n🎨 {keyword} 用の売れ筋プロンプト\n")
    prompts = generate_prompts(keyword, 5)
    
    for i, prompt in enumerate(prompts, 1):
        print(f"{i}. {prompt}")
    
    print(f"\n💡 ヒント: これらをStable Diffusionにコピペして使用")
    print(f"📋 使用法: python poster_prompt_generator.py \"美少女 イラスト\"")
    
    # JSON出力も追加
    import json
    with open('poster_prompts.json', 'w', encoding='utf-8') as f:
        json.dump({
            'keyword': keyword,
            'prompts': prompts,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ プロンプト保存: poster_prompts.json")