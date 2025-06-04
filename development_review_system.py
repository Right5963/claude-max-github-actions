#!/usr/bin/env python3
"""
Development Review System - 開発後自動レビューシステム
===================================================
「問題点はないか？しっかり考えて」を自動化
開発・実装後の批判的レビューと改善提案を自動実行
"""

import os
import sys
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path

class DevelopmentReviewSystem:
    def __init__(self):
        self.repo_path = "/mnt/c/Claude Code/tool"
        self.review_db = "development_reviews.json"
        
    def critical_review_checklist(self, file_path):
        """批判的レビューチェックリスト + 強制知識参照"""
        issues = []
        improvements = []
        
        if not os.path.exists(file_path):
            issues.append(f"❌ ファイルが存在しない: {file_path}")
            return {"issues": issues, "improvements": improvements}
        
        print(f"🔍 批判的レビュー開始: {file_path}")
        
        # 🔥 強制知識参照チェック - Simple First原則の確認
        print("📚 CLAUDE.md 重要原則確認中...")
        self._verify_simple_first_knowledge()
        
        print("📚 Simple First原則: 複雑な機能を直感的な1コマンドに包む")
        
        # 1. ファイル基本分析
        file_stats = self._analyze_file_basics(file_path)
        
        # 2. Simple First 原則チェック
        simplicity_check = self._check_simplicity_principle(file_path, file_stats)
        issues.extend(simplicity_check["issues"])
        improvements.extend(simplicity_check["improvements"])
        
        # 3. 依存性分析
        dependency_check = self._check_dependencies(file_path)
        issues.extend(dependency_check["issues"])
        improvements.extend(dependency_check["improvements"])
        
        # 4. 実用性分析
        practicality_check = self._check_practicality(file_path, file_stats)
        issues.extend(practicality_check["issues"])
        improvements.extend(practicality_check["improvements"])
        
        # 5. エラーハンドリング分析
        error_handling_check = self._check_error_handling(file_path)
        issues.extend(error_handling_check["issues"])
        improvements.extend(error_handling_check["improvements"])
        
        # 6. ドキュメント分析
        documentation_check = self._check_documentation(file_path)
        issues.extend(documentation_check["issues"])
        improvements.extend(documentation_check["improvements"])
        
        return {
            "issues": issues,
            "improvements": improvements,
            "file_stats": file_stats
        }
    
    def _analyze_file_basics(self, file_path):
        """ファイル基本分析"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            stats = {
                "lines": len(content.split('\n')),
                "size_kb": len(content.encode('utf-8')) / 1024,
                "functions": len(re.findall(r'def\s+\w+\(', content)),
                "classes": len(re.findall(r'class\s+\w+', content)),
                "imports": len(re.findall(r'^(import|from)\s+', content, re.MULTILINE)),
                "comments": len(re.findall(r'#.*', content)),
                "docstrings": len(re.findall(r'"""[\s\S]*?"""', content))
            }
            
            return stats
            
        except Exception as e:
            return {"error": str(e)}
    
    def _check_simplicity_principle(self, file_path, file_stats):
        """Simple First 原則チェック - 外部シンプル、内部複雑OK"""
        issues = []
        improvements = []
        
        # Simple First: 内部の複雑性は価値があれば許容
        # チェック対象: 外部インターフェースの分かりやすさ
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # メイン関数の外部インターフェースチェック
            if 'if __name__ == "__main__"' in content:
                # 外部から見た使いやすさの評価
                if 'def main()' in content:
                    improvements.append("💡 外部インターフェース良好 - Simple Firstに準拠")
                else:
                    issues.append("⚠️ メイン関数不明確 - 外部インターフェース改善必要")
            
            # 内部複雑性は価値創造なら推奨
            lines = file_stats.get("lines", 0)
            functions = file_stats.get("functions", 0)
            
            if lines > 300 and functions > 10:
                improvements.append(f"💡 高機能システム: {lines}行、{functions}関数 - 内部複雑性は価値創造")
            
        except Exception as e:
            issues.append(f"❌ Simple First チェックエラー: {e}")
        
        # インポート数チェック
        if file_stats.get("imports", 0) > 15:
            issues.append(f"⚠️ 依存過多: {file_stats['imports']}個のインポート")
            improvements.append("💡 依存関係整理 - 必要最小限のインポートに削減")
        
        return {"issues": issues, "improvements": improvements}
    
    def _check_dependencies(self, file_path):
        """依存性分析 - 実際の危険な依存のみチェック"""
        issues = []
        improvements = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 実際のsubprocess呼び出しで危険なコマンドをチェック
            subprocess_calls = re.findall(r'subprocess\.(run|call|Popen)\([^)]*["\']([^"\']*(?:jq|curl|wget|apt-get)[^"\']*)["\']', content)
            
            if subprocess_calls:
                for call_type, command in subprocess_calls:
                    issues.append(f"🚨 実際の外部依存: {command} (subprocess経由)")
                    improvements.append(f"💡 {command.split()[0]}をPython標準ライブラリで代替")
            
            # subprocess の適切な使用量チェック
            all_subprocess = re.findall(r'subprocess\.(run|call|Popen)', content)
            if len(all_subprocess) > 8:
                improvements.append(f"💡 subprocess使用多め: {len(all_subprocess)}箇所 - 必要に応じて最適化検討")
            
        except Exception as e:
            issues.append(f"❌ 依存性分析エラー: {e}")
        
        return {"issues": issues, "improvements": improvements}
    
    def _check_practicality(self, file_path, file_stats):
        """実用性分析"""
        issues = []
        improvements = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 即座に使用可能かチェック
            if 'if __name__ == "__main__"' not in content and file_path.endswith('.py'):
                issues.append("⚠️ メイン実行ブロックなし - 直接実行不可")
                improvements.append("💡 if __name__ == '__main__': ブロック追加")
            
            # 実際の設定ファイル読み込みチェック  
            config_reads = re.findall(r'(open|load|read)[^)]*["\']([^"\']*(?:config|settings|\.env)[^"\']*)["\']', content)
            for operation, config_file in config_reads:
                if not re.search(r'if\s+.*exists', content):  # 存在チェックなしの場合のみ警告
                    issues.append(f"⚠️ 設定ファイル依存: {config_file} (存在チェックなし)")
                    improvements.append("💡 設定ファイル存在チェック追加またはデフォルト値設定")
            
            # ハードコードパスチェック
            hardcoded_paths = re.findall(r'["\'](/[a-zA-Z0-9/_-]+|[A-Z]:\\\\[^"\']+)["\']', content)
            if len(hardcoded_paths) > 3:
                issues.append(f"⚠️ ハードコードパス多用: {len(hardcoded_paths)}箇所")
                improvements.append("💡 相対パス・環境変数使用に変更")
            
        except Exception as e:
            issues.append(f"❌ 実用性分析エラー: {e}")
        
        return {"issues": issues, "improvements": improvements}
    
    def _check_error_handling(self, file_path):
        """エラーハンドリング分析"""
        issues = []
        improvements = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # try-except 比率チェック
            function_count = len(re.findall(r'def\s+\w+\(', content))
            try_count = len(re.findall(r'try:', content))
            
            if function_count > 0:
                error_handling_ratio = try_count / function_count
                if error_handling_ratio < 0.3:  # 30%未満
                    issues.append(f"⚠️ エラーハンドリング不足: {error_handling_ratio:.1%}")
                    improvements.append("💡 主要関数にtry-except追加")
            
            # 素のexceptチェック
            bare_except = len(re.findall(r'except:\s*$', content, re.MULTILINE))
            if bare_except > 0:
                issues.append(f"⚠️ 素のexcept使用: {bare_except}箇所")
                improvements.append("💡 具体的例外クラス指定に変更")
            
        except Exception as e:
            issues.append(f"❌ エラーハンドリング分析エラー: {e}")
        
        return {"issues": issues, "improvements": improvements}
    
    def _check_documentation(self, file_path):
        """ドキュメント分析"""
        issues = []
        improvements = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # docstring比率チェック
            function_count = len(re.findall(r'def\s+\w+\(', content))
            docstring_count = len(re.findall(r'def\s+\w+\([^)]*\):\s*"""', content))
            
            if function_count > 0:
                doc_ratio = docstring_count / function_count
                if doc_ratio < 0.5:  # 50%未満
                    issues.append(f"⚠️ ドキュメント不足: {doc_ratio:.1%}")
                    improvements.append("💡 主要関数にdocstring追加")
            
            # 使用例チェック
            if '使用例' not in content and 'example' not in content.lower():
                issues.append("⚠️ 使用例なし")
                improvements.append("💡 実用的な使用例を追加")
                
        except Exception as e:
            issues.append(f"❌ ドキュメント分析エラー: {e}")
        
        return {"issues": issues, "improvements": improvements}
    
    def _verify_simple_first_knowledge(self):
        """Simple First 原則の強制知識確認"""
        try:
            claude_md_path = os.path.join(self.repo_path, "CLAUDE.md")
            with open(claude_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple First の定義を抽出
            lines = content.split('\n')
            in_simple_first = False
            principles = []
            
            for line in lines:
                if "Simple First の進化" in line:
                    in_simple_first = True
                elif in_simple_first and line.startswith("#### "):
                    break
                elif in_simple_first and line.strip().startswith("- "):
                    principles.append(line.strip())
            
            if principles:
                print("📝 Simple First 原則 (CLAUDE.md より):")
                for principle in principles:
                    print(f"  {principle}")
                print()
            else:
                print("⚠️ Simple First 原則が見つかりません")
                
        except Exception as e:
            print(f"⚠️ CLAUDE.md 読み込みエラー: {e}")
            print("📝 フォールバック - Simple First: 複雑な機能を直感的な1コマンドに包む")
    
    def auto_fix_issues(self, file_path, review_result):
        """問題の自動修正"""
        fixed = []
        
        print(f"🔧 自動修正開始: {file_path}")
        
        # 1. メイン実行ブロック追加
        if "メイン実行ブロックなし" in str(review_result.get("issues", [])):
            if self._add_main_block(file_path):
                fixed.append("✅ メイン実行ブロック追加")
        
        # 2. 基本docstring追加
        if "ドキュメント不足" in str(review_result.get("issues", [])):
            if self._add_basic_docstrings(file_path):
                fixed.append("✅ 基本docstring追加")
        
        # 3. エラーハンドリング強化
        if "エラーハンドリング不足" in str(review_result.get("issues", [])):
            if self._improve_error_handling(file_path):
                fixed.append("✅ エラーハンドリング強化")
        
        return fixed
    
    def _add_main_block(self, file_path):
        """メイン実行ブロック追加"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'if __name__ == "__main__"' not in content and file_path.endswith('.py'):
                # 最後に追加
                main_block = '''
if __name__ == "__main__":
    # メイン実行
    print("🚀 実行開始")
    # TODO: メイン処理を実装
'''
                content += main_block
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return True
        except Exception as e:
            print(f"⚠️ メインブロック追加エラー: {e}")
        
        return False
    
    def _add_basic_docstrings(self, file_path):
        """基本docstring追加"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            modified = False
            new_lines = []
            
            for i, line in enumerate(lines):
                new_lines.append(line)
                
                # 関数定義の後にdocstringがない場合
                if re.match(r'\s*def\s+\w+\(', line):
                    # 次の行がdocstringでない場合
                    if i + 1 < len(lines) and '"""' not in lines[i + 1]:
                        indent = len(line) - len(line.lstrip())
                        docstring = ' ' * (indent + 4) + '"""機能説明TODO"""\n'
                        new_lines.append(docstring)
                        modified = True
            
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                return True
                
        except Exception as e:
            print(f"⚠️ docstring追加エラー: {e}")
        
        return False
    
    def _improve_error_handling(self, file_path):
        """エラーハンドリング改善"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 素のexceptを具体的に変更
            improved_content = re.sub(
                r'except:\s*\n', 
                'except Exception as e:\n', 
                content
            )
            
            if content != improved_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(improved_content)
                return True
                
        except Exception as e:
            print(f"⚠️ エラーハンドリング改善エラー: {e}")
        
        return False
    
    def full_development_review(self, target_files=None):
        """完全開発レビュー"""
        print("🔍 完全開発レビューシステム開始")
        print("=" * 50)
        
        if target_files is None:
            # 最近変更されたファイルを対象
            try:
                result = subprocess.run(
                    ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
                    capture_output=True, text=True, cwd=self.repo_path
                )
                target_files = [f for f in result.stdout.split('\n') if f.endswith(('.py', '.sh'))]
            except Exception as e:
                print(f"⚠️ Git差分取得エラー: {e}")
                target_files = ['git_daily_driver.py', 'mcp_dev_efficiency.py', 'auto_research_system.py']
        
        all_reviews = {}
        total_issues = 0
        total_improvements = 0
        
        for file_path in target_files:
            full_path = os.path.join(self.repo_path, file_path)
            
            print(f"\n📂 レビュー対象: {file_path}")
            
            review_result = self.critical_review_checklist(full_path)
            all_reviews[file_path] = review_result
            
            issues = review_result.get("issues", [])
            improvements = review_result.get("improvements", [])
            
            total_issues += len(issues)
            total_improvements += len(improvements)
            
            # 問題表示
            if issues:
                print("❌ 発見された問題:")
                for issue in issues:
                    print(f"  {issue}")
            
            # 改善提案表示
            if improvements:
                print("💡 改善提案:")
                for improvement in improvements:
                    print(f"  {improvement}")
            
            # 自動修正実行
            if issues or improvements:
                fixed = self.auto_fix_issues(full_path, review_result)
                if fixed:
                    print("🔧 自動修正完了:")
                    for fix in fixed:
                        print(f"  {fix}")
            else:
                print("✅ 問題なし - 良好な実装")
        
        # サマリー
        print(f"\n📊 レビューサマリー")
        print(f"対象ファイル: {len(target_files)}個")
        print(f"発見問題: {total_issues}個")
        print(f"改善提案: {total_improvements}個")
        
        # レビュー結果保存
        self._save_review_results(all_reviews)
        
        return all_reviews
    
    def _save_review_results(self, reviews):
        """レビュー結果保存"""
        try:
            review_record = {
                "timestamp": datetime.now().isoformat(),
                "reviews": reviews,
                "summary": {
                    "files_reviewed": len(reviews),
                    "total_issues": sum(len(r.get("issues", [])) for r in reviews.values()),
                    "total_improvements": sum(len(r.get("improvements", [])) for r in reviews.values())
                }
            }
            
            # 既存レビューに追加
            all_reviews = []
            if os.path.exists(self.review_db):
                with open(self.review_db, 'r') as f:
                    all_reviews = json.load(f)
            
            all_reviews.append(review_record)
            
            # 最新10件のみ保持
            all_reviews = all_reviews[-10:]
            
            with open(self.review_db, 'w') as f:
                json.dump(all_reviews, f, indent=2, ensure_ascii=False)
            
            print(f"📝 レビュー結果を保存: {self.review_db}")
            
        except Exception as e:
            print(f"⚠️ レビュー結果保存エラー: {e}")

def main():
    """Simple First: 問題点はないか？しっかり考えて - 1コマンド実行"""
    import sys
    
    reviewer = DevelopmentReviewSystem()
    
    print("🤔 「問題点はないか？しっかり考えて」自動実行")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # 特定ファイルの問題点チェック
        file_path = sys.argv[1]
        print(f"📂 対象ファイル: {file_path}")
        
        # 1. 批判的レビュー（内部で472行の複雑な分析）
        review_result = reviewer.critical_review_checklist(file_path)
        
        # 2. 問題点と改善点の表示
        issues = review_result.get("issues", [])
        improvements = review_result.get("improvements", [])
        
        if issues:
            print("\n❌ 発見された問題点:")
            for issue in issues:
                print(f"  {issue}")
        
        if improvements:
            print("\n💡 改善提案:")
            for improvement in improvements:
                print(f"  {improvement}")
        
        # 3. 自動修正実行
        if issues or improvements:
            print("\n🔧 自動修正中...")
            fixed = reviewer.auto_fix_issues(file_path, review_result)
            if fixed:
                print("✅ 修正完了:")
                for fix in fixed:
                    print(f"  {fix}")
            else:
                print("ℹ️ 手動対応が必要な項目です")
        else:
            print("\n🎉 完璧です！問題点なし")
            
    else:
        # 最近の開発を全てチェック
        print("📊 最近の開発内容を自動チェック中...")
        reviewer.full_development_review()

if __name__ == "__main__":
    main()