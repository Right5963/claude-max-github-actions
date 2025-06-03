#!/usr/bin/env python3
"""
Image Quality Evaluator
======================
生成画像の商業価値を自動評価
"""

import os
import json
from pathlib import Path
from datetime import datetime
import random

class ImageQualityEvaluator:
    def __init__(self):
        self.evaluation_dir = Path("image_evaluations")
        self.evaluation_dir.mkdir(exist_ok=True)
        
        # 評価基準
        self.criteria = {
            "composition": {
                "weight": 0.25,
                "factors": ["balance", "focal_point", "rule_of_thirds"]
            },
            "technical": {
                "weight": 0.25,
                "factors": ["sharpness", "noise", "artifacts"]
            },
            "aesthetic": {
                "weight": 0.30,
                "factors": ["color_harmony", "mood", "style_consistency"]
            },
            "commercial": {
                "weight": 0.20,
                "factors": ["market_appeal", "uniqueness", "target_match"]
            }
        }
        
    def evaluate_image(self, image_path, metadata=None):
        """画像を評価"""
        print(f"\n🔍 画像評価: {Path(image_path).name}")
        
        # 実際の画像分析（将来実装）
        # 現在はメタデータとルールベースで評価
        
        evaluation = {
            "image": str(image_path),
            "timestamp": datetime.now().isoformat(),
            "scores": {},
            "total_score": 0,
            "commercial_value": "",
            "recommendations": []
        }
        
        # 各カテゴリを評価
        for category, config in self.criteria.items():
            score = self.evaluate_category(category, metadata)
            evaluation["scores"][category] = score
            evaluation["total_score"] += score * config["weight"]
        
        # 商業価値判定
        evaluation["commercial_value"] = self.determine_commercial_value(evaluation["total_score"])
        
        # 改善推奨事項
        evaluation["recommendations"] = self.generate_recommendations(evaluation["scores"])
        
        return evaluation
    
    def evaluate_category(self, category, metadata):
        """カテゴリ別評価（簡易版）"""
        
        if category == "composition":
            # 構図評価
            score = 70  # ベーススコア
            if metadata:
                # キーワードから推測
                if "portrait" in str(metadata).lower():
                    score += 10  # ポートレートは安定
                if "dynamic" in str(metadata).lower():
                    score += 5
                    
        elif category == "technical":
            # 技術的品質
            score = 75
            if metadata and metadata.get("model"):
                # 使用モデルで判定
                if "V5" in metadata["model"] or "V8" in metadata["model"]:
                    score += 10  # 新しいモデルは高品質
                    
        elif category == "aesthetic":
            # 美的評価
            score = 70
            if metadata and metadata.get("tags"):
                quality_tags = ["masterpiece", "best quality", "detailed"]
                matches = sum(1 for tag in quality_tags if tag in metadata.get("tags", []))
                score += matches * 5
                
        elif category == "commercial":
            # 商業的価値
            score = 65
            if metadata and metadata.get("tags"):
                commercial_tags = ["1girl", "anime", "cute", "colorful"]
                matches = sum(1 for tag in commercial_tags if tag in metadata.get("tags", []))
                score += matches * 5
        
        return min(score, 100)  # 100点満点
    
    def determine_commercial_value(self, total_score):
        """商業価値を判定"""
        if total_score >= 85:
            return "Premium (¥2,000+)"
        elif total_score >= 75:
            return "High (¥1,500-2,000)"
        elif total_score >= 65:
            return "Standard (¥1,000-1,500)"
        elif total_score >= 55:
            return "Budget (¥500-1,000)"
        else:
            return "Review needed"
    
    def generate_recommendations(self, scores):
        """改善推奨事項を生成"""
        recommendations = []
        
        # 低スコアの項目を特定
        for category, score in scores.items():
            if score < 70:
                if category == "composition":
                    recommendations.append("構図を改善: 三分割法や黄金比を意識")
                elif category == "technical":
                    recommendations.append("品質向上: より高いステップ数やCFGスケール調整")
                elif category == "aesthetic":
                    recommendations.append("美的改善: カラーバランスやスタイル統一性")
                elif category == "commercial":
                    recommendations.append("市場性向上: トレンド要素の追加")
        
        return recommendations
    
    def batch_evaluate(self, image_folder, top_n=20):
        """フォルダ内の画像を一括評価"""
        print(f"\n📁 一括評価開始: {image_folder}")
        
        # 画像ファイルを取得
        image_files = []
        for ext in ["*.png", "*.jpg", "*.jpeg"]:
            image_files.extend(Path(image_folder).glob(ext))
        
        if not image_files:
            print("❌ 画像が見つかりません")
            return []
        
        print(f"📊 {len(image_files)}枚の画像を評価中...")
        
        # 全画像を評価
        evaluations = []
        for img_path in image_files:
            # 簡易メタデータ（実際は画像から抽出）
            metadata = {
                "model": "Anything V5",
                "tags": ["1girl", "anime", "detailed", "masterpiece"]
            }
            
            eval_result = self.evaluate_image(img_path, metadata)
            evaluations.append(eval_result)
        
        # スコアでソート
        evaluations.sort(key=lambda x: x["total_score"], reverse=True)
        
        # レポート生成
        self.generate_batch_report(evaluations, top_n)
        
        return evaluations[:top_n]
    
    def generate_batch_report(self, evaluations, top_n):
        """一括評価レポート生成"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        report_file = self.evaluation_dir / f"batch_evaluation_{timestamp}.md"
        
        report = f"""# 画像品質評価レポート
生成日: {datetime.now().strftime('%Y-%m-%d %H:%M')}
評価数: {len(evaluations)}枚

## 🏆 TOP {top_n} 高評価画像

"""
        
        for i, eval_data in enumerate(evaluations[:top_n], 1):
            report += f"### {i}. {Path(eval_data['image']).name}\n"
            report += f"- **総合スコア**: {eval_data['total_score']:.1f}/100\n"
            report += f"- **商業価値**: {eval_data['commercial_value']}\n"
            report += f"- **詳細スコア**:\n"
            for cat, score in eval_data['scores'].items():
                report += f"  - {cat}: {score}/100\n"
            
            if eval_data['recommendations']:
                report += f"- **改善点**: {', '.join(eval_data['recommendations'])}\n"
            report += "\n"
        
        # 統計情報
        avg_score = sum(e['total_score'] for e in evaluations) / len(evaluations)
        report += f"\n## 📊 統計情報\n"
        report += f"- 平均スコア: {avg_score:.1f}/100\n"
        report += f"- Premium品質: {sum(1 for e in evaluations if 'Premium' in e['commercial_value'])}枚\n"
        report += f"- High品質: {sum(1 for e in evaluations if 'High' in e['commercial_value'])}枚\n"
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n✅ レポート生成: {report_file}")
        
        return report_file

def main():
    evaluator = ImageQualityEvaluator()
    
    print("🎨 Image Quality Evaluator")
    print("=" * 50)
    print("1. 単一画像を評価")
    print("2. フォルダ一括評価（TOP20選出）")
    print("3. 簡易評価（ファイル名から推測）")
    
    choice = "1"  # 自動モード：単体評価を実行
    
    if choice == "1":
        image_path = "sample_image.jpg"  # デフォルト画像パス
        metadata = {
            "model": "sample_model",
            "tags": ["sample", "tag"]
        }
        
        result = evaluator.evaluate_image(image_path, metadata)
        
        print(f"\n📊 評価結果")
        print(f"総合スコア: {result['total_score']:.1f}/100")
        print(f"商業価値: {result['commercial_value']}")
        
    elif choice == "2":
        folder = input("画像フォルダパス: ")
        top_n = int(input("TOP何枚を選出？ (デフォルト: 20): ") or 20)
        
        top_images = evaluator.batch_evaluate(folder, top_n)
        
        print(f"\n🏆 TOP {len(top_images)} 選出完了！")
        for i, img in enumerate(top_images[:5], 1):
            print(f"{i}. {Path(img['image']).name} - {img['commercial_value']}")
            
    elif choice == "3":
        # 簡易デモ
        evaluator.evaluate_image("demo_image.png", {"tags": ["1girl", "anime"]})

if __name__ == "__main__":
    main()