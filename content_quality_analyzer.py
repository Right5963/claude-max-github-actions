#!/usr/bin/env python3
"""
ファイル内容を精査して品質を評価するスクリプト
デマ、架空データ、実用性のない内容を検出
"""

import os
import re
from pathlib import Path
from datetime import datetime

# 問題のあるパターン
PROBLEMATIC_PATTERNS = {
    "架空データ": [
        r"ダミーデータ", r"モックデータ", r"サンプルデータ", r"テストデータ",
        r"dummy", r"mock", r"sample", r"placeholder", r"TODO", r"FIXME"
    ],
    "未実装・未完成": [
        r"実装予定", r"未実装", r"作成中", r"準備中", r"開発中",
        r"not implemented", r"coming soon", r"under construction", r"WIP"
    ],
    "エラー・失敗": [
        r"失敗", r"エラー", r"動作しない", r"機能しない", r"壊れて",
        r"error", r"failed", r"broken", r"not working", r"deprecated"
    ],
    "重複・冗長": [
        r"テスト版", r"旧版", r"old", r"backup", r"copy", r"duplicate",
        r"_v\d+", r"_old", r"_backup", r"_test"
    ],
    "低品質の兆候": [
        r"適当", r"とりあえず", r"雑に", r"簡単に", r"ざっくり",
        r"quick and dirty", r"temporary", r"temp", r"rough"
    ]
}

# 価値の高いキーワード
HIGH_VALUE_KEYWORDS = [
    "成功", "完了", "実証済み", "動作確認済み", "本番環境",
    "success", "complete", "verified", "production", "working",
    "revenue", "profit", "実績", "売上"
]

class ContentAnalyzer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.analysis_results = {
            "削除推奨": [],
            "要確認": [],
            "改善可能": [],
            "高価値": [],
            "保持推奨": []
        }
        
    def analyze_all_files(self):
        """すべてのファイルを分析"""
        print("=== ファイル内容精査開始 ===\n")
        
        # organized_filesディレクトリのすべてのmdファイルを取得
        md_files = list(self.base_path.rglob("*.md"))
        
        for file_path in md_files:
            if file_path.name.startswith("_"):  # インデックスファイルはスキップ
                continue
            self.analyze_single_file(file_path)
            
        # 結果をレポート
        self.generate_report()
        
    def analyze_single_file(self, file_path):
        """単一ファイルの分析"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # ファイルサイズチェック
            file_size = len(content)
            
            # 各種スコアを計算
            scores = {
                "問題スコア": self.calculate_problem_score(content, file_path.name),
                "価値スコア": self.calculate_value_score(content, file_path.name),
                "実装状態": self.check_implementation_status(content),
                "データ品質": self.check_data_quality(content),
                "文書品質": self.check_documentation_quality(content, file_size)
            }
            
            # カテゴリを決定
            category = self.categorize_file(scores, file_path)
            
            # 結果を保存
            self.analysis_results[category].append({
                "path": file_path,
                "scores": scores,
                "size": file_size,
                "reason": self.get_categorization_reason(scores, category)
            })
            
        except Exception as e:
            print(f"エラー: {file_path.name} - {e}")
            
    def calculate_problem_score(self, content, filename):
        """問題スコアを計算（高いほど問題あり）"""
        score = 0
        content_lower = content.lower()
        filename_lower = filename.lower()
        
        for category, patterns in PROBLEMATIC_PATTERNS.items():
            for pattern in patterns:
                # ファイル名での出現
                if re.search(pattern, filename_lower):
                    score += 3
                # 内容での出現
                matches = len(re.findall(pattern, content_lower))
                score += matches * 1
                
        return score
        
    def calculate_value_score(self, content, filename):
        """価値スコアを計算（高いほど価値あり）"""
        score = 0
        content_lower = content.lower()
        
        for keyword in HIGH_VALUE_KEYWORDS:
            matches = len(re.findall(keyword.lower(), content_lower))
            score += matches * 2
            
        # コード例の存在
        if "```" in content:
            score += 5
            
        # 具体的な数値や統計の存在
        if re.search(r'\d+%|\d+円|\$\d+', content):
            score += 3
            
        return score
        
    def check_implementation_status(self, content):
        """実装状態をチェック"""
        if re.search(r'(実装済み|implemented|working|動作確認済み)', content, re.I):
            return "実装済み"
        elif re.search(r'(未実装|not implemented|TODO|準備中)', content, re.I):
            return "未実装"
        else:
            return "不明"
            
    def check_data_quality(self, content):
        """データ品質をチェック"""
        if re.search(r'(ダミー|dummy|mock|sample|テストデータ)', content, re.I):
            return "架空データ"
        elif re.search(r'(実データ|実際の|real|actual|production)', content, re.I):
            return "実データ"
        else:
            return "不明"
            
    def check_documentation_quality(self, content, file_size):
        """文書品質をチェック"""
        # 短すぎる
        if file_size < 100:
            return "内容不足"
        # 構造化されている
        elif "##" in content and "```" in content:
            return "構造化"
        # テキストのみ
        elif file_size < 500:
            return "簡易"
        else:
            return "標準"
            
    def categorize_file(self, scores, file_path):
        """ファイルをカテゴリ分類"""
        problem_score = scores["問題スコア"]
        value_score = scores["価値スコア"]
        impl_status = scores["実装状態"]
        data_quality = scores["データ品質"]
        
        # 削除推奨
        if (problem_score > 10 or 
            data_quality == "架空データ" or
            impl_status == "未実装" and value_score < 5):
            return "削除推奨"
            
        # 要確認
        elif problem_score > 5 or data_quality == "架空データ":
            return "要確認"
            
        # 高価値
        elif value_score > 10 and problem_score < 3:
            return "高価値"
            
        # 改善可能
        elif value_score > 5 and problem_score < 5:
            return "改善可能"
            
        # 保持推奨
        else:
            return "保持推奨"
            
    def get_categorization_reason(self, scores, category):
        """カテゴリ分類の理由を取得"""
        reasons = []
        
        if scores["問題スコア"] > 10:
            reasons.append("問題パターンが多数検出")
        if scores["データ品質"] == "架空データ":
            reasons.append("架空データを含む")
        if scores["実装状態"] == "未実装":
            reasons.append("未実装の機能")
        if scores["価値スコア"] > 10:
            reasons.append("高価値コンテンツ")
        if scores["文書品質"] == "内容不足":
            reasons.append("内容が不十分")
            
        return "、".join(reasons) if reasons else "特記事項なし"
        
    def generate_report(self):
        """分析レポートを生成"""
        report = ["# ファイル内容精査レポート\n"]
        report.append(f"分析日時: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        
        # サマリー
        report.append("## サマリー\n")
        total_files = sum(len(files) for files in self.analysis_results.values())
        report.append(f"- 総ファイル数: {total_files}")
        
        for category, files in self.analysis_results.items():
            percentage = (len(files) / total_files * 100) if total_files > 0 else 0
            report.append(f"- {category}: {len(files)}ファイル ({percentage:.1f}%)")
            
        # カテゴリ別詳細
        for category, files in self.analysis_results.items():
            if not files:
                continue
                
            report.append(f"\n## {category} ({len(files)}ファイル)\n")
            
            # ファイルリスト
            for file_info in sorted(files, key=lambda x: x["scores"]["問題スコア"], reverse=True)[:10]:
                relative_path = file_info["path"].relative_to(self.base_path)
                report.append(f"### {relative_path}")
                report.append(f"- 問題スコア: {file_info['scores']['問題スコア']}")
                report.append(f"- 価値スコア: {file_info['scores']['価値スコア']}")
                report.append(f"- 実装状態: {file_info['scores']['実装状態']}")
                report.append(f"- データ品質: {file_info['scores']['データ品質']}")
                report.append(f"- 理由: {file_info['reason']}")
                report.append("")
                
        # レポートを保存
        report_path = self.base_path.parent / "content_quality_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(report))
            
        print(f"レポート生成完了: {report_path}")
        
        # コンソールにサマリーを表示
        print("\n=== 分析結果サマリー ===")
        for category, files in self.analysis_results.items():
            print(f"{category}: {len(files)}ファイル")
            
        # 削除推奨ファイルの詳細
        if self.analysis_results["削除推奨"]:
            print("\n=== 削除推奨ファイル（上位10件） ===")
            for file_info in self.analysis_results["削除推奨"][:10]:
                print(f"- {file_info['path'].name}: {file_info['reason']}")

def main():
    base_path = Path("/mnt/c/Claude Code/tool/organized_files")
    
    if not base_path.exists():
        print("エラー: organized_filesディレクトリが見つかりません")
        return
        
    analyzer = ContentAnalyzer(base_path)
    analyzer.analyze_all_files()

if __name__ == "__main__":
    main()