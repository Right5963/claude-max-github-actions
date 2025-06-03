#!/usr/bin/env python3
"""
高度知識抽出システム
==================
抽象的内容 → 実用的洞察への革命
"""

import os
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class AdvancedKnowledgeExtractor:
    def __init__(self):
        self.work_dir = "/mnt/c/Claude Code/tool"
        
        # 開発パターン検出用の詳細規則
        self.pattern_rules = {
            'refactoring': {
                'file_patterns': [r'.*\.py$', r'.*\.js$', r'.*\.ts$'],
                'content_patterns': [
                    r'def\s+\w+\s*\([^)]*\)\s*:',  # 新しい関数定義
                    r'class\s+\w+\s*[\(:]',        # 新しいクラス定義
                    r'import\s+\w+',               # 新しいimport
                    r'from\s+\w+\s+import',        # from import
                ],
                'deletion_patterns': [
                    r'#.*TODO.*',                  # TODO削除
                    r'print\s*\(',                 # print文削除
                    r'console\.log\s*\(',          # console.log削除
                ]
            },
            'optimization': {
                'keywords': ['optimize', 'performance', 'speed', 'fast', 'cache', 'async', 'parallel'],
                'file_types': ['.py', '.js', '.ts', '.sql']
            },
            'bug_fix': {
                'keywords': ['fix', 'bug', 'error', 'exception', 'crash', 'fail'],
                'patterns': [
                    r'try\s*:.*except',            # 例外処理追加
                    r'if\s+.*\s+is\s+None',        # None チェック
                    r'isinstance\s*\(',            # 型チェック
                ]
            },
            'feature_addition': {
                'keywords': ['add', 'new', 'feature', 'implement', 'create'],
                'indicators': [
                    'new_files_ratio',             # 新規ファイル比率
                    'new_functions_count',         # 新規関数数
                    'api_endpoints',               # APIエンドポイント
                ]
            },
            'security_improvement': {
                'keywords': ['security', 'auth', 'permission', 'validate', 'sanitize'],
                'patterns': [
                    r'password.*hash',
                    r'token.*verify',
                    r'input.*validate',
                    r'escape.*html',
                ]
            }
        }
        
        # コード品質メトリクス
        self.quality_metrics = {
            'complexity': ['cyclomatic', 'cognitive', 'nesting'],
            'maintainability': ['readability', 'modularity', 'documentation'],
            'testability': ['coverage', 'mocking', 'isolation']
        }
    
    def analyze_commit_changes(self, commit_hash="HEAD"):
        """コミットの変更を詳細分析"""
        print(f"🔍 高度分析開始: {commit_hash}")
        
        # 1. コミット情報取得
        commit_info = self.get_commit_info(commit_hash)
        
        # 2. 変更ファイル分析
        file_changes = self.analyze_file_changes(commit_hash)
        
        # 3. コードパターン分析
        code_patterns = self.detect_code_patterns(file_changes)
        
        # 4. 品質影響分析
        quality_impact = self.analyze_quality_impact(file_changes)
        
        # 5. 開発洞察生成
        insights = self.generate_development_insights(
            commit_info, file_changes, code_patterns, quality_impact
        )
        
        return {
            'commit_info': commit_info,
            'file_changes': file_changes,
            'code_patterns': code_patterns,
            'quality_impact': quality_impact,
            'insights': insights
        }
    
    def get_commit_info(self, commit_hash):
        """詳細なコミット情報を取得"""
        try:
            # コミット情報
            result = subprocess.run([
                'git', 'show', '--format=%H%n%s%n%an%n%ad%n%B', '--name-status', commit_hash
            ], cwd=self.work_dir, capture_output=True, text=True)
            
            lines = result.stdout.strip().split('\n')
            if len(lines) < 4:
                return {}
            
            return {
                'hash': lines[0],
                'subject': lines[1],
                'author': lines[2],
                'date': lines[3],
                'message': '\n'.join(lines[4:lines.index('') if '' in lines[4:] else len(lines)]),
                'file_status': [line for line in lines if '\t' in line]
            }
        except Exception as e:
            print(f"⚠️ コミット情報取得エラー: {e}")
            return {}
    
    def analyze_file_changes(self, commit_hash):
        """ファイル変更の詳細分析"""
        try:
            # 変更統計
            result = subprocess.run([
                'git', 'show', '--stat', commit_hash
            ], cwd=self.work_dir, capture_output=True, text=True)
            
            stat_lines = result.stdout.strip().split('\n')
            
            # ファイル別変更詳細
            file_details = []
            changes_summary = {'additions': 0, 'deletions': 0, 'files': 0}
            
            for line in stat_lines:
                if '|' in line and ('+' in line or '-' in line):
                    parts = line.split('|')
                    if len(parts) >= 2:
                        filename = parts[0].strip()
                        change_info = parts[1].strip()
                        
                        # 変更数の抽出
                        additions = change_info.count('+')
                        deletions = change_info.count('-')
                        
                        file_details.append({
                            'filename': filename,
                            'additions': additions,
                            'deletions': deletions,
                            'total_changes': additions + deletions,
                            'file_type': Path(filename).suffix,
                            'change_type': self.classify_change_type(filename, additions, deletions)
                        })
                        
                        changes_summary['additions'] += additions
                        changes_summary['deletions'] += deletions
                        changes_summary['files'] += 1
            
            return {
                'summary': changes_summary,
                'files': file_details,
                'file_types': self.analyze_file_types(file_details),
                'change_distribution': self.analyze_change_distribution(file_details)
            }
            
        except Exception as e:
            print(f"⚠️ ファイル変更分析エラー: {e}")
            return {}
    
    def classify_change_type(self, filename, additions, deletions):
        """変更タイプの分類"""
        if deletions == 0:
            return "new_file"
        elif additions == 0:
            return "file_deletion"
        elif additions > deletions * 2:
            return "major_addition"
        elif deletions > additions * 2:
            return "major_reduction"
        else:
            return "modification"
    
    def analyze_file_types(self, file_details):
        """ファイルタイプ別分析"""
        type_stats = defaultdict(lambda: {'count': 0, 'additions': 0, 'deletions': 0})
        
        for file in file_details:
            file_type = file['file_type'] or 'no_extension'
            type_stats[file_type]['count'] += 1
            type_stats[file_type]['additions'] += file['additions']
            type_stats[file_type]['deletions'] += file['deletions']
        
        return dict(type_stats)
    
    def analyze_change_distribution(self, file_details):
        """変更分布の分析"""
        if not file_details:
            return {}
        
        total_changes = sum(f['total_changes'] for f in file_details)
        
        # 最も変更の多いファイル
        most_changed = max(file_details, key=lambda f: f['total_changes'])
        
        # 変更の集中度
        concentration = most_changed['total_changes'] / total_changes if total_changes > 0 else 0
        
        return {
            'most_changed_file': most_changed,
            'change_concentration': concentration,
            'average_changes_per_file': total_changes / len(file_details),
            'change_types': [f['change_type'] for f in file_details]
        }
    
    def detect_code_patterns(self, file_changes):
        """コードパターンの検出"""
        patterns_detected = []
        
        for file_info in file_changes.get('files', []):
            filename = file_info['filename']
            
            # ファイル内容の変更を分析
            patterns = self.analyze_file_content_patterns(filename, file_info)
            patterns_detected.extend(patterns)
        
        return self.consolidate_patterns(patterns_detected)
    
    def analyze_file_content_patterns(self, filename, file_info):
        """ファイル内容のパターン分析"""
        patterns = []
        
        # ファイル拡張子による分類
        file_ext = Path(filename).suffix
        
        # リファクタリングパターン
        if file_info['change_type'] == 'modification' and file_ext in ['.py', '.js', '.ts']:
            if file_info['deletions'] > 0 and file_info['additions'] > 0:
                patterns.append({
                    'type': 'refactoring',
                    'confidence': 0.7,
                    'evidence': f"{file_info['deletions']}行削除、{file_info['additions']}行追加",
                    'description': f"{filename}でコード構造の改善"
                })
        
        # 新機能追加パターン
        if file_info['change_type'] == 'new_file':
            patterns.append({
                'type': 'feature_addition',
                'confidence': 0.9,
                'evidence': f"新規ファイル: {filename}",
                'description': f"{file_ext}ファイルによる新機能実装"
            })
        
        # 最適化パターン
        if file_info['additions'] > file_info['deletions'] and 'optimized' in filename.lower():
            patterns.append({
                'type': 'optimization',
                'confidence': 0.8,
                'evidence': f"最適化版ファイル: {filename}",
                'description': "パフォーマンス改善の実装"
            })
        
        return patterns
    
    def consolidate_patterns(self, patterns_detected):
        """パターンの統合と優先順位付け"""
        pattern_groups = defaultdict(list)
        
        for pattern in patterns_detected:
            pattern_groups[pattern['type']].append(pattern)
        
        consolidated = {}
        for pattern_type, pattern_list in pattern_groups.items():
            # 信頼度の平均
            avg_confidence = sum(p['confidence'] for p in pattern_list) / len(pattern_list)
            
            # 証拠の統合
            evidence = [p['evidence'] for p in pattern_list]
            descriptions = [p['description'] for p in pattern_list]
            
            consolidated[pattern_type] = {
                'confidence': avg_confidence,
                'count': len(pattern_list),
                'evidence': evidence,
                'descriptions': descriptions
            }
        
        return consolidated
    
    def analyze_quality_impact(self, file_changes):
        """品質への影響分析"""
        impact = {
            'complexity_change': 'neutral',
            'maintainability_change': 'neutral',
            'testability_change': 'neutral',
            'overall_quality_trend': 'stable'
        }
        
        if not file_changes:
            return impact
        
        summary = file_changes.get('summary', {})
        files = file_changes.get('files', [])
        
        # 複雑性への影響
        if summary.get('additions', 0) > summary.get('deletions', 0) * 1.5:
            impact['complexity_change'] = 'increased'
        elif summary.get('deletions', 0) > summary.get('additions', 0) * 1.5:
            impact['complexity_change'] = 'decreased'
        
        # 保守性への影響
        test_files = [f for f in files if 'test' in f['filename'].lower()]
        doc_files = [f for f in files if f['file_type'] in ['.md', '.txt', '.rst']]
        
        if test_files or doc_files:
            impact['maintainability_change'] = 'improved'
        
        # テスト可能性への影響
        if test_files:
            impact['testability_change'] = 'improved'
        
        # 全体的な品質トレンド
        improvement_factors = sum([
            impact['complexity_change'] == 'decreased',
            impact['maintainability_change'] == 'improved',
            impact['testability_change'] == 'improved'
        ])
        
        if improvement_factors >= 2:
            impact['overall_quality_trend'] = 'improving'
        elif impact['complexity_change'] == 'increased':
            impact['overall_quality_trend'] = 'declining'
        
        return impact
    
    def generate_development_insights(self, commit_info, file_changes, code_patterns, quality_impact):
        """実用的な開発洞察を生成"""
        insights = []
        
        # 1. パフォーマンス洞察
        if 'optimization' in code_patterns:
            opt_pattern = code_patterns['optimization']
            insights.append(f"パフォーマンス最適化: {opt_pattern['count']}箇所で改善実装 - {', '.join(opt_pattern['evidence'])}")
        
        # 2. コード品質洞察
        if quality_impact['overall_quality_trend'] == 'improving':
            insights.append(f"コード品質向上: 保守性({quality_impact['maintainability_change']}) + テスト性({quality_impact['testability_change']})の改善")
        
        # 3. 開発パターン洞察
        if 'refactoring' in code_patterns:
            refactor = code_patterns['refactoring']
            insights.append(f"リファクタリング実施: {refactor['count']}ファイルで構造改善 - 可読性・保守性の向上")
        
        # 4. 新機能洞察
        if 'feature_addition' in code_patterns:
            feature = code_patterns['feature_addition']
            insights.append(f"新機能開発: {feature['count']}個の新しい機能モジュール追加 - システム拡張")
        
        # 5. 変更規模洞察
        if file_changes and file_changes.get('summary'):
            summary = file_changes['summary']
            if summary.get('files', 0) > 10:
                insights.append(f"大規模変更: {summary['files']}ファイル、{summary['additions']}行追加 - アーキテクチャレベルの改善")
            elif summary.get('additions', 0) > 100:
                insights.append(f"機能拡張: {summary['additions']}行の新規コード - 既存システムの大幅強化")
        
        # 6. 技術負債洞察
        if file_changes and file_changes.get('summary'):
            summary = file_changes['summary']
            if summary.get('deletions', 0) > summary.get('additions', 0):
                insights.append(f"技術負債解消: {summary['deletions']}行削除 - コードベースの整理・最適化")
        
        # 7. デフォルト洞察の回避
        if not insights:
            # より具体的なデフォルト洞察
            if commit_info and commit_info.get('subject'):
                subject = commit_info['subject']
                if 'Auto-commit' in subject:
                    insights.append(f"開発効率化: 自動コミットシステムによる継続的な変更管理の実現")
                else:
                    insights.append(f"開発推進: {subject}による機能向上・問題解決の実装")
        
        return insights

# メイン使用例
def main():
    extractor = AdvancedKnowledgeExtractor()
    
    # 最新コミットを分析
    analysis = extractor.analyze_commit_changes("HEAD")
    
    print("🧠 高度知識抽出結果:")
    print("=" * 50)
    
    if analysis['insights']:
        print("💡 開発洞察:")
        for i, insight in enumerate(analysis['insights'], 1):
            print(f"  {i}. {insight}")
    
    if analysis['code_patterns']:
        print("\n🔍 検出されたパターン:")
        for pattern_type, pattern_data in analysis['code_patterns'].items():
            print(f"  {pattern_type}: 信頼度{pattern_data['confidence']:.1f} ({pattern_data['count']}件)")
    
    if analysis['quality_impact']:
        print("\n📊 品質への影響:")
        impact = analysis['quality_impact']
        print(f"  全体的なトレンド: {impact['overall_quality_trend']}")
        print(f"  複雑性: {impact['complexity_change']}")
        print(f"  保守性: {impact['maintainability_change']}")

if __name__ == "__main__":
    main()