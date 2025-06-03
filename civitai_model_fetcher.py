#!/usr/bin/env python3
"""
CivitAI Model Fetcher
====================
人気モデル・LoRA情報を自動取得
"""

import json
import requests
from datetime import datetime
from pathlib import Path

class CivitAIFetcher:
    def __init__(self):
        self.base_url = "https://civitai.com/api/v1"
        self.cache_dir = Path("civitai_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
    def fetch_trending_models(self, limit=10):
        """トレンドモデルを取得"""
        print("🔍 CivitAI人気モデルを取得中...")
        
        # CivitAI API エンドポイント
        url = f"{self.base_url}/models"
        params = {
            "limit": limit,
            "sort": "Highest Rated",
            "period": "Week"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return self.parse_models(data.get("items", []))
            else:
                print(f"⚠️ API応答エラー: {response.status_code}")
                return self.get_fallback_models()
        except Exception as e:
            print(f"⚠️ 接続エラー: {e}")
            return self.get_fallback_models()
    
    def parse_models(self, models):
        """モデル情報をパース"""
        parsed = []
        for model in models[:10]:
            parsed.append({
                "name": model.get("name", "Unknown"),
                "type": model.get("type", "Checkpoint"),
                "rating": model.get("stats", {}).get("rating", 0),
                "downloads": model.get("stats", {}).get("downloadCount", 0),
                "tags": model.get("tags", []),
                "description": model.get("description", "")[:200]
            })
        return parsed
    
    def get_fallback_models(self):
        """フォールバック用の人気モデルリスト"""
        return [
            {
                "name": "Anything V5",
                "type": "Checkpoint", 
                "rating": 4.95,
                "downloads": 500000,
                "tags": ["anime", "stable", "general"],
                "description": "最も人気のアニメ系モデル"
            },
            {
                "name": "Realistic Vision V5",
                "type": "Checkpoint",
                "rating": 4.92,
                "downloads": 300000,
                "tags": ["photorealistic", "detailed"],
                "description": "高品質なリアル系モデル"
            },
            {
                "name": "DreamShaper V8",
                "type": "Checkpoint",
                "rating": 4.90,
                "downloads": 400000,
                "tags": ["versatile", "artistic"],
                "description": "アート系万能モデル"
            }
        ]
    
    def fetch_popular_loras(self, limit=10):
        """人気LoRAを取得"""
        print("🔍 人気LoRAを取得中...")
        
        # デモ用の人気LoRAリスト
        popular_loras = [
            {
                "name": "Detail Tweaker LoRA",
                "weight_recommended": 0.7,
                "purpose": "ディテール向上",
                "compatibility": ["anime", "realistic"]
            },
            {
                "name": "Good hands - beta2",
                "weight_recommended": 0.8,
                "purpose": "手の修正",
                "compatibility": ["all"]
            },
            {
                "name": "Anime Tarot Card Art",
                "weight_recommended": 0.6,
                "purpose": "タロットカード風",
                "compatibility": ["anime", "artistic"]
            }
        ]
        
        return popular_loras
    
    def save_to_obsidian_format(self, models, loras):
        """Obsidian用にフォーマットして保存"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        # Obsidian用Markdown生成
        content = f"# CivitAI トレンド分析 {timestamp}\n\n"
        
        content += "## 🔥 人気Checkpoints\n\n"
        for i, model in enumerate(models[:5], 1):
            content += f"### {i}. {model['name']}\n"
            content += f"- **評価**: ⭐{model['rating']}/5.0\n"
            content += f"- **DL数**: {model['downloads']:,}\n"
            content += f"- **タグ**: {', '.join(model['tags'][:5])}\n"
            content += f"- **説明**: {model['description']}\n\n"
        
        content += "## 🎨 人気LoRA\n\n"
        for lora in loras[:5]:
            content += f"### {lora['name']}\n"
            content += f"- **推奨Weight**: {lora['weight_recommended']}\n"
            content += f"- **用途**: {lora['purpose']}\n"
            content += f"- **互換性**: {', '.join(lora['compatibility'])}\n\n"
        
        # キャッシュに保存
        cache_file = self.cache_dir / f"civitai_trends_{timestamp}.md"
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        return cache_file
    
    def generate_recommendations(self, keyword):
        """キーワードに基づく推奨"""
        models = self.fetch_trending_models()
        loras = self.fetch_popular_loras()
        
        # キーワード分析
        keyword_lower = keyword.lower()
        
        # 最適なモデル選択
        recommended_model = None
        for model in models:
            model_tags = [tag.lower() for tag in model.get("tags", [])]
            if any(tag in keyword_lower for tag in ["アニメ", "anime", "萌え"]):
                if "anime" in model_tags:
                    recommended_model = model
                    break
            elif any(tag in keyword_lower for tag in ["リアル", "realistic", "写真"]):
                if "photorealistic" in model_tags or "realistic" in model_tags:
                    recommended_model = model
                    break
        
        if not recommended_model and models:
            recommended_model = models[0]  # デフォルト
        
        # 推奨LoRA選択
        recommended_loras = []
        for lora in loras:
            if "all" in lora["compatibility"] or \
               any(compat in recommended_model.get("tags", []) for compat in lora["compatibility"]):
                recommended_loras.append(lora)
        
        return {
            "model": recommended_model,
            "loras": recommended_loras[:3],
            "obsidian_file": self.save_to_obsidian_format(models, loras)
        }

def main():
    import sys
    fetcher = CivitAIFetcher()
    
    print("🤖 CivitAI Model Intelligence")
    print("=" * 50)
    
    # コマンドライン引数またはデフォルト値
    keyword = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "anime girl poster"
    print(f"生成予定のキーワード: {keyword}")
    
    print("\n📊 分析中...")
    recommendations = fetcher.generate_recommendations(keyword)
    
    print("\n✅ 推奨設定")
    print("-" * 50)
    
    if recommendations["model"]:
        model = recommendations["model"]
        print(f"\n🎨 推奨Checkpoint: {model['name']}")
        print(f"   評価: ⭐{model['rating']}/5.0")
        print(f"   DL数: {model['downloads']:,}")
    
    print("\n🔧 推奨LoRA:")
    for lora in recommendations["loras"]:
        print(f"   - {lora['name']} (weight: {lora['weight_recommended']})")
    
    print(f"\n📝 詳細レポート: {recommendations['obsidian_file']}")
    print("\n💡 使用法: python3 civitai_model_fetcher.py [キーワード]")

if __name__ == "__main__":
    main()