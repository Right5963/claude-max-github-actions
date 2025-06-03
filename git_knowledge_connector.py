#!/usr/bin/env python3
"""
Git-Knowledge Connector (プロトタイプ)
=====================================
GitコミットからObsidian知識ネットワークへの自動統合

革命的機能:
- コミット内容からパターン抽出
- 自動的な学習要素特定
- Obsidian知識ノート生成
- 開発履歴の知識化
"""

import os
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path
import hashlib

class GitKnowledgeConnector:
    def __init__(self, repo_path="/mnt/c/Claude Code/tool"):
        self.repo_path = repo_path
        self.obsidian_bridge_script = "./mcp_bridge_extended.sh"
        self.knowledge_db = ".git_knowledge_db.json"
        self.patterns_db = ".development_patterns.json"
        
        # パターン認識の基準
        self.code_patterns = {
            "refactoring": [r"refactor", r"cleanup", r"reorganize", r"optimize"],
            "feature_addition": [r"add", r"implement", r"create", r"new"],
            "bug_fix": [r"fix", r"bug", r"error", r"issue", r"patch"],
            "documentation": [r"doc", r"readme", r"comment", r"explain"],
            "testing": [r"test", r"spec", r"verify", r"validate"],
            "integration": [r"integrate", r"connect", r"bridge", r"link"],
            "automation": [r"auto", r"script", r"batch", r"daemon"],
            "security": [r"security", r"auth", r"permission", r"encrypt"],
            "performance": [r"performance", r"speed", r"optimize", r"efficient"]
        }
        
        # 学習要素のキーワード
        self.learning_indicators = [
            "learned", "discovered", "found", "realized", "understood",
            "mistake", "error", "problem", "solution", "approach",
            "better", "improved", "enhanced", "optimized"
        ]
    
    def load_knowledge_db(self):
        """知識データベースの読み込み"""
        try:
            with open(self.knowledge_db, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "patterns": {},
                "learnings": {},
                "connections": {},
                "stats": {"total_commits": 0, "patterns_identified": 0}
            }
    
    def save_knowledge_db(self, data):
        """知識データベースの保存"""
        with open(self.knowledge_db, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_commit_info(self, commit_hash="HEAD"):
        """Gitコミット情報の取得"""
        try:
            # コミット情報
            commit_info = subprocess.run([
                "git", "log", "-1", "--format=%H|%s|%B|%an|%ad", commit_hash
            ], cwd=self.repo_path, capture_output=True, text=True).stdout.strip()
            
            if not commit_info:
                return None
                
            parts = commit_info.split('|')
            hash_val, subject, body, author, date = parts[0], parts[1], parts[2], parts[3], parts[4]
            
            # 変更ファイル情報
            files_changed = subprocess.run([
                "git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash
            ], cwd=self.repo_path, capture_output=True, text=True).stdout.strip().split('\n')
            
            # 統計情報
            stats = subprocess.run([
                "git", "diff", "--shortstat", f"{commit_hash}^", commit_hash
            ], cwd=self.repo_path, capture_output=True, text=True).stdout.strip()
            
            return {
                "hash": hash_val,
                "subject": subject,
                "body": body,
                "author": author,
                "date": date,
                "files_changed": [f for f in files_changed if f],
                "stats": stats
            }
        except Exception as e:
            print(f"❌ Gitコミット情報取得エラー: {e}")
            return None
    
    def analyze_commit_patterns(self, commit_info):
        """コミットパターンの分析"""
        if not commit_info:
            return []
        
        full_text = f"{commit_info['subject']} {commit_info['body']}".lower()
        identified_patterns = []
        
        for pattern_name, keywords in self.code_patterns.items():
            for keyword in keywords:
                if re.search(keyword, full_text):
                    identified_patterns.append(pattern_name)
                    break
        
        # ファイル拡張子による追加分析
        file_types = set()
        for file_path in commit_info['files_changed']:
            ext = Path(file_path).suffix
            if ext:
                file_types.add(ext)
        
        # ファイルタイプに基づくパターン推定
        if '.py' in file_types:
            identified_patterns.append('python_development')
        if '.sh' in file_types:
            identified_patterns.append('script_development')
        if '.md' in file_types:
            identified_patterns.append('documentation')
        if '.json' in file_types:
            identified_patterns.append('configuration')
        
        return list(set(identified_patterns))  # 重複除去
    
    def extract_learning_elements(self, commit_info):
        """学習要素の抽出"""
        if not commit_info:
            return []
        
        full_text = f"{commit_info['subject']} {commit_info['body']}"
        learnings = []
        
        # 学習指標の検出
        for indicator in self.learning_indicators:
            if indicator in full_text.lower():
                # 周辺テキストを抽出して学習要素として記録
                sentences = re.split(r'[.!?]', full_text)
                for sentence in sentences:
                    if indicator in sentence.lower():
                        learnings.append(sentence.strip())
        
        # ファイル数や変更規模からの推定
        file_count = len(commit_info['files_changed'])
        if file_count > 10:
            learnings.append(f"大規模変更 ({file_count}ファイル) - プロジェクト構造の理解が進んだ")
        
        if 'fix' in commit_info['subject'].lower():
            learnings.append("問題解決スキルの向上 - バグ修正パターンの習得")
        
        if 'refactor' in commit_info['subject'].lower():
            learnings.append("コード品質向上 - リファクタリング技術の応用")
        
        return learnings
    
    def generate_obsidian_note(self, commit_info, patterns, learnings):
        """Obsidian知識ノートの生成"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        commit_short = commit_info['hash'][:8]
        
        # メインパターンを特定
        main_pattern = patterns[0] if patterns else "general_development"
        
        note_content = f"""# 開発洞察: {commit_info['subject']}

## 📊 基本情報
- **コミット**: `{commit_short}`
- **日時**: {commit_info['date']}
- **作成者**: {commit_info['author']}
- **変更ファイル数**: {len(commit_info['files_changed'])}

## 🔍 識別されたパターン
{self._format_patterns(patterns)}

## 📚 学習要素
{self._format_learnings(learnings)}

## 📁 変更ファイル
{self._format_files(commit_info['files_changed'])}

## 📈 統計
```
{commit_info['stats']}
```

## 🔗 関連知識
{self._generate_knowledge_links(patterns)}

## 💡 今後への示唆
{self._generate_future_insights(patterns, learnings)}

---
*自動生成: Git-Knowledge Connector*
*タイムスタンプ: {timestamp}*
"""
        
        return {
            "filename": f"Development_Insights_{timestamp}_{main_pattern}.md",
            "content": note_content,
            "patterns": patterns,
            "learnings": learnings
        }
    
    def _format_patterns(self, patterns):
        """パターンのフォーマット"""
        if not patterns:
            return "- 一般的な開発作業"
        
        formatted = []
        for pattern in patterns:
            emoji = self._get_pattern_emoji(pattern)
            formatted.append(f"- {emoji} **{pattern.replace('_', ' ').title()}**")
        
        return '\n'.join(formatted)
    
    def _format_learnings(self, learnings):
        """学習要素のフォーマット"""
        if not learnings:
            return "- 継続的な開発経験の蓄積"
        
        formatted = []
        for learning in learnings:
            formatted.append(f"- 💡 {learning}")
        
        return '\n'.join(formatted)
    
    def _format_files(self, files):
        """ファイルリストのフォーマット"""
        if not files:
            return "- なし"
        
        formatted = []
        for file_path in files[:10]:  # 最大10個まで表示
            ext = Path(file_path).suffix
            emoji = self._get_file_emoji(ext)
            formatted.append(f"- {emoji} `{file_path}`")
        
        if len(files) > 10:
            formatted.append(f"- ... 他 {len(files) - 10} ファイル")
        
        return '\n'.join(formatted)
    
    def _generate_knowledge_links(self, patterns):
        """知識リンクの生成"""
        links = []
        
        for pattern in patterns:
            if pattern == "refactoring":
                links.append("- [[リファクタリング手法]]")
                links.append("- [[コード品質向上]]")
            elif pattern == "feature_addition":
                links.append("- [[機能開発プロセス]]")
                links.append("- [[要件分析]]")
            elif pattern == "bug_fix":
                links.append("- [[デバッグ技術]]")
                links.append("- [[エラーハンドリング]]")
            elif pattern == "automation":
                links.append("- [[自動化戦略]]")
                links.append("- [[スクリプト開発]]")
        
        if not links:
            links.append("- [[開発ベストプラクティス]]")
        
        return '\n'.join(links)
    
    def _generate_future_insights(self, patterns, learnings):
        """将来への示唆の生成"""
        insights = []
        
        if "refactoring" in patterns:
            insights.append("- より良いコード構造の探求を継続")
        if "automation" in patterns:
            insights.append("- 自動化の範囲をさらに拡大検討")
        if "integration" in patterns:
            insights.append("- システム間連携の更なる最適化")
        
        if len(learnings) > 2:
            insights.append("- 学習密度が高い - 知識の体系化を検討")
        
        if not insights:
            insights.append("- 継続的改善の機会を探る")
        
        return '\n'.join(insights)
    
    def _get_pattern_emoji(self, pattern):
        """パターン別絵文字"""
        emoji_map = {
            "refactoring": "🔧",
            "feature_addition": "✨",
            "bug_fix": "🐛",
            "documentation": "📚",
            "testing": "🧪",
            "integration": "🔗",
            "automation": "🤖",
            "security": "🔒",
            "performance": "⚡",
            "python_development": "🐍",
            "script_development": "📜"
        }
        return emoji_map.get(pattern, "💻")
    
    def _get_file_emoji(self, ext):
        """ファイル拡張子別絵文字"""
        emoji_map = {
            ".py": "🐍",
            ".sh": "📜",
            ".md": "📝",
            ".json": "📋",
            ".txt": "📄",
            ".yaml": "⚙️",
            ".yml": "⚙️"
        }
        return emoji_map.get(ext, "📁")
    
    def save_to_obsidian(self, note_data):
        """Obsidianへの保存"""
        try:
            # ローカル保存（確実な動作確認）
            local_dir = "knowledge_notes"
            os.makedirs(local_dir, exist_ok=True)
            local_path = os.path.join(local_dir, note_data['filename'])
            
            with open(local_path, 'w', encoding='utf-8') as f:
                f.write(note_data['content'])
            
            print(f"✅ ローカル知識ノート保存: {local_path}")
            
            # Obsidian保存も試行（エラーがあっても継続）
            try:
                obsidian_path = f"Development_Insights/{note_data['filename']}"
                
                # シンプルなファイル作成
                result = subprocess.run([
                    "powershell.exe", "-Command",
                    f"$content = @'\n{note_data['content']}\n'@; $content | Out-File -FilePath 'G:\\マイドライブ\\Obsidian Vault\\{obsidian_path}' -Encoding UTF8 -Force"
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print(f"✅ Obsidianノート保存成功: {obsidian_path}")
                else:
                    print(f"⚠️ Obsidian保存スキップ: アクセス制限")
                    
            except Exception as obs_error:
                print(f"⚠️ Obsidian保存スキップ: {str(obs_error)[:50]}...")
            
            return True
                
        except Exception as e:
            print(f"❌ 知識ノート保存エラー: {e}")
            return False
    
    def update_knowledge_database(self, commit_info, patterns, learnings):
        """知識データベースの更新"""
        db = self.load_knowledge_db()
        
        # 統計更新
        db["stats"]["total_commits"] += 1
        db["stats"]["patterns_identified"] += len(patterns)
        
        # パターン頻度の更新
        for pattern in patterns:
            if pattern not in db["patterns"]:
                db["patterns"][pattern] = {"count": 0, "examples": []}
            db["patterns"][pattern]["count"] += 1
            db["patterns"][pattern]["examples"].append({
                "commit": commit_info['hash'][:8],
                "subject": commit_info['subject'],
                "date": commit_info['date']
            })
        
        # 学習要素の蓄積
        commit_key = commit_info['hash'][:8]
        db["learnings"][commit_key] = {
            "elements": learnings,
            "patterns": patterns,
            "date": commit_info['date']
        }
        
        self.save_knowledge_db(db)
        return db
    
    def process_commit(self, commit_hash="HEAD"):
        """コミットの完全処理"""
        print(f"🔍 Git-Knowledge Connector 開始")
        print(f"処理対象: {commit_hash}")
        print("=" * 50)
        
        # 1. コミット情報取得
        commit_info = self.get_commit_info(commit_hash)
        if not commit_info:
            print("❌ コミット情報の取得に失敗しました")
            return False
        
        print(f"📝 コミット: {commit_info['subject']}")
        print(f"📁 変更ファイル: {len(commit_info['files_changed'])}個")
        
        # 2. パターン分析
        patterns = self.analyze_commit_patterns(commit_info)
        print(f"🔍 識別パターン: {', '.join(patterns) if patterns else 'なし'}")
        
        # 3. 学習要素抽出
        learnings = self.extract_learning_elements(commit_info)
        print(f"💡 学習要素: {len(learnings)}個")
        
        # 4. Obsidianノート生成
        note_data = self.generate_obsidian_note(commit_info, patterns, learnings)
        print(f"📔 ノート生成: {note_data['filename']}")
        
        # 5. Obsidianに保存（基本版）
        if self.save_to_obsidian(note_data):
            print("✅ 基本ノート保存完了")
            
            # 6. AI最適化統合実行
            try:
                from obsidian_knowledge_integrator import ObsidianKnowledgeIntegrator
                print("🧠 AI最適化統合開始...")
                
                integrator = ObsidianKnowledgeIntegrator()
                latest_file = os.path.join("knowledge_notes", note_data['filename'])
                
                integration_result = integrator.integrate_knowledge_note(latest_file)
                
                if integration_result.get("success"):
                    print("🎉 完全AI統合完了！")
                    print(f"📍 統合先: {integration_result.get('path', 'ローカル')}")
                    print(f"🏷️ タグ数: {len(integration_result.get('metadata', {}).get('tags', []))}個")
                    print(f"🔗 関連ノート: {len(integration_result.get('related_notes', []))}個")
                else:
                    print("⚠️ 統合は部分的完了")
                    
            except Exception as integration_error:
                print(f"⚠️ AI統合スキップ: {str(integration_error)[:50]}...")
        
        # 7. 知識データベース更新
        db = self.update_knowledge_database(commit_info, patterns, learnings)
        print(f"📊 累計コミット: {db['stats']['total_commits']}回")
        print(f"🎯 累計パターン: {db['stats']['patterns_identified']}個")
        
        print("=" * 50)
        print("🎉 完全Git-Knowledge統合完了！")
        
        return True
    
    def show_knowledge_stats(self):
        """知識統計の表示"""
        db = self.load_knowledge_db()
        
        print("📊 Git-Knowledge統合統計")
        print("=" * 30)
        print(f"総コミット数: {db['stats']['total_commits']}")
        print(f"識別パターン数: {db['stats']['patterns_identified']}")
        
        if db["patterns"]:
            print("\n🔍 パターン頻度:")
            sorted_patterns = sorted(db["patterns"].items(), 
                                   key=lambda x: x[1]["count"], 
                                   reverse=True)
            
            for pattern, data in sorted_patterns[:10]:
                emoji = self._get_pattern_emoji(pattern)
                print(f"  {emoji} {pattern.replace('_', ' ').title()}: {data['count']}回")
        
        return db

def main():
    """メイン実行"""
    import sys
    
    connector = GitKnowledgeConnector()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "stats":
            connector.show_knowledge_stats()
        elif sys.argv[1] == "process":
            commit_hash = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
            connector.process_commit(commit_hash)
        else:
            print("使用方法:")
            print("  python3 git_knowledge_connector.py process [commit_hash]")
            print("  python3 git_knowledge_connector.py stats")
    else:
        # デフォルトは最新コミットを処理
        connector.process_commit()

if __name__ == "__main__":
    main()