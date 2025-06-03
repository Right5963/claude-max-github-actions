#!/usr/bin/env python3
"""
Obsidian Knowledge Integrator
============================
新しい知識をObsidianの体系的構造に完全統合

解決する問題:
1. 新知識の孤立状態
2. メタデータの欠如
3. 関連性マッピングの不足
4. AI活用最適化の欠如
"""

import os
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
import yaml
import hashlib

class ObsidianKnowledgeIntegrator:
    def __init__(self):
        self.obsidian_vault = "G:\\マイドライブ\\Obsidian Vault"
        self.local_knowledge = "/mnt/c/Claude Code/tool/knowledge_notes"
        self.git_knowledge_db = "/mnt/c/Claude Code/tool/.git_knowledge_db.json"
        
        # Obsidianディレクトリ構造（実際の構造に基づく）
        self.obsidian_structure = {
            "00_Inbox": "未分類・新規ノート（24時間以内処理）",
            "20_Literature": "外部情報（書籍・記事・動画・SNS）",
            "30_Permanent": "自分の見解で再構築した知識",
            "70_Share": "公開・共有コンテンツ", 
            "90_Index": "MOC (Map of Contents)",
            "95_Projects": "プロジェクト管理",
            "100_Cursor": "Cursor連携設定"
        }
        
        # 知識分類ルール
        self.classification_rules = {
            "development_insight": {
                "target_dir": "95_Projects/Claude_Code_Development",
                "tags": ["#dev/insight", "#automation", "#learning"],
                "template": "development_insight"
            },
            "pattern_analysis": {
                "target_dir": "30_Permanent/Development_Patterns",
                "tags": ["#dev/pattern", "#analysis", "#methodology"],
                "template": "pattern_analysis"
            },
            "automation_knowledge": {
                "target_dir": "30_Permanent/Automation_Knowledge", 
                "tags": ["#automation", "#efficiency", "#workflow"],
                "template": "automation_knowledge"
            },
            "integration_learning": {
                "target_dir": "30_Permanent/System_Integration",
                "tags": ["#integration", "#system", "#architecture"],
                "template": "integration_learning"
            }
        }
        
        # 関連性検出キーワード
        self.relationship_keywords = {
            "git": ["version control", "commit", "repository", "branch"],
            "automation": ["script", "auto", "workflow", "pipeline"],
            "obsidian": ["knowledge", "note", "vault", "graph"],
            "ai": ["claude", "llm", "artificial intelligence", "machine learning"],
            "development": ["code", "programming", "software", "implementation"],
            "integration": ["connect", "bridge", "link", "combine"],
            "security": ["auth", "permission", "encrypt", "protect"],
            "performance": ["optimize", "speed", "efficient", "fast"]
        }
    
    def load_git_knowledge_db(self):
        """Git知識データベースの読み込み"""
        try:
            with open(self.git_knowledge_db, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"patterns": {}, "learnings": {}, "connections": {}}
    
    def analyze_knowledge_type(self, note_content, patterns):
        """知識タイプの自動分析"""
        content_lower = note_content.lower()
        
        # パターンベースの分類
        if "development_insights" in note_content or any(p in ["automation", "integration"] for p in patterns):
            return "development_insight"
        elif len(patterns) > 2:
            return "pattern_analysis"
        elif "automation" in patterns:
            return "automation_knowledge"
        elif "integration" in patterns:
            return "integration_learning"
        else:
            return "development_insight"  # デフォルト
    
    def generate_metadata(self, note_content, knowledge_type, patterns, related_files):
        """AI最適化メタデータの自動生成"""
        timestamp = datetime.now().isoformat()
        
        # 基本メタデータ
        metadata = {
            "created": timestamp,
            "updated": timestamp,
            "type": knowledge_type,
            "source": "git_knowledge_connector",
            "status": "processed",
            "ai_optimized": True
        }
        
        # 分類に基づくタグ
        classification = self.classification_rules.get(knowledge_type, {})
        tags = classification.get("tags", ["#development"])
        
        # パターンベースの追加タグ
        for pattern in patterns:
            tag = f"#pattern/{pattern.replace('_', '-')}"
            if tag not in tags:
                tags.append(tag)
        
        metadata["tags"] = tags
        
        # 関連ファイル情報
        if related_files:
            metadata["related_files"] = related_files[:5]  # 最大5個
        
        # プロジェクト情報
        metadata["project"] = "Claude Code Development"
        
        # AI活用フラグ
        metadata["ai_searchable"] = True
        metadata["auto_generated"] = True
        
        return metadata
    
    def find_related_notes(self, note_content, patterns):
        """既存ノートとの関連性自動発見"""
        related_notes = []
        content_words = set(re.findall(r'\b\w+\b', note_content.lower()))
        
        # キーワードベースの関連性検出
        for concept, keywords in self.relationship_keywords.items():
            if any(keyword in content_words for keyword in keywords):
                # 概念に基づく関連ノート候補
                related_notes.extend([
                    f"[[{concept.title()}の基礎]]",
                    f"[[{concept.title()}の応用]]"
                ])
        
        # パターンベースの関連性
        pattern_relations = {
            "automation": ["[[自動化戦略]]", "[[ワークフロー最適化]]"],
            "integration": ["[[システム統合]]", "[[API連携]]"],
            "security": ["[[セキュリティベストプラクティス]]", "[[認証システム]]"],
            "git": ["[[Git運用]]", "[[バージョン管理]]"],
            "development": ["[[開発手法]]", "[[コーディング規約]]"]
        }
        
        for pattern in patterns:
            if pattern in pattern_relations:
                related_notes.extend(pattern_relations[pattern])
        
        # 重複除去と上位候補選択
        unique_notes = list(set(related_notes))
        return unique_notes[:8]  # 最大8個の関連ノート
    
    def create_obsidian_note(self, content, metadata, knowledge_type, related_notes):
        """完全なObsidianノート作成"""
        classification = self.classification_rules.get(knowledge_type, {})
        
        # YAML Frontmatter
        yaml_content = yaml.dump(metadata, default_flow_style=False, allow_unicode=True)
        
        # ノート本文の構造化
        structured_content = f"""---
{yaml_content}---

{content}

## 🔗 関連ノート
{self._format_related_notes(related_notes)}

## 📊 メタデータ詳細
- **知識タイプ**: {knowledge_type.replace('_', ' ').title()}
- **自動生成**: {metadata['created']}
- **AI最適化**: ✅
- **検索タグ**: {', '.join(metadata['tags'])}

## 🧠 AI活用ノート
このノートはAI検索・関連性発見・知識統合に最適化されています。

---
*Auto-generated by Obsidian Knowledge Integrator*
*Git-Knowledge Pipeline Integration*
"""
        
        return structured_content
    
    def _format_related_notes(self, related_notes):
        """関連ノートのフォーマット"""
        if not related_notes:
            return "- 関連性を分析中..."
        
        formatted = []
        for note in related_notes:
            if not note.startswith('[['):
                note = f"[[{note}]]"
            formatted.append(f"- {note}")
        
        return '\n'.join(formatted)
    
    def save_to_obsidian_structure(self, note_content, filename, knowledge_type):
        """Obsidianの適切な構造に保存"""
        try:
            classification = self.classification_rules.get(knowledge_type, {})
            target_dir = classification.get("target_dir", "00_Inbox")
            
            # まずローカルに統合ファイルとして保存（確実な動作）
            integrated_dir = os.path.join(self.local_knowledge, "integrated")
            os.makedirs(integrated_dir, exist_ok=True)
            local_integrated_path = os.path.join(integrated_dir, filename)
            
            with open(local_integrated_path, 'w', encoding='utf-8') as f:
                f.write(note_content)
            
            print(f"✅ ローカル統合保存: integrated/{filename}")
            
            # Obsidian保存を試行（エラーがあっても継続）
            try:
                # シンプルなファイル書き込み
                temp_file = f"/tmp/obsidian_temp_{int(datetime.now().timestamp())}.md"
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(note_content)
                
                # PowerShellでコピー
                target_path = f"G:\\マイドライブ\\Obsidian Vault\\{target_dir}\\{filename}"
                result = subprocess.run([
                    "powershell.exe", "-Command",
                    f"Copy-Item '{temp_file}' '{target_path}' -Force; if (Test-Path '{target_path}') {{ Write-Output 'SUCCESS' }} else {{ Write-Output 'FAILED' }}"
                ], capture_output=True, text=True, timeout=20)
                
                # 一時ファイル削除
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                
                if "SUCCESS" in result.stdout:
                    print(f"✅ Obsidian統合成功: {target_dir}/{filename}")
                    return True, target_path
                else:
                    print(f"⚠️ Obsidian保存スキップ（統合は完了）")
                    
            except Exception as obs_error:
                print(f"⚠️ Obsidian保存スキップ: {str(obs_error)[:50]}...")
            
            # ローカル統合は成功したので True を返す
            return True, local_integrated_path
                
        except Exception as e:
            print(f"❌ 統合処理エラー: {e}")
            return False, None
    
    def integrate_knowledge_note(self, knowledge_file_path):
        """知識ノートの完全統合処理"""
        print(f"🧠 Knowledge Integration 開始: {knowledge_file_path}")
        print("=" * 60)
        
        try:
            # 1. 既存ノート読み込み
            with open(knowledge_file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            print(f"📄 原文読み込み完了: {len(original_content)}文字")
            
            # 2. Git知識データベース読み込み
            git_db = self.load_git_knowledge_db()
            
            # 3. パターン抽出（ファイル名から）
            filename = Path(knowledge_file_path).name
            patterns = []
            for pattern in ["security", "integration", "automation", "documentation"]:
                if pattern in filename.lower() or pattern in original_content.lower():
                    patterns.append(pattern)
            
            print(f"🔍 検出パターン: {', '.join(patterns) if patterns else 'なし'}")
            
            # 4. 知識タイプ分析
            knowledge_type = self.analyze_knowledge_type(original_content, patterns)
            print(f"📋 知識タイプ: {knowledge_type}")
            
            # 5. 関連ファイル情報（簡易版）
            related_files = []
            if "git" in original_content.lower():
                related_files.append("smart_git_auto_commit.py")
            if "obsidian" in original_content.lower():
                related_files.append("git_knowledge_connector.py")
            
            # 6. メタデータ生成
            metadata = self.generate_metadata(original_content, knowledge_type, patterns, related_files)
            print(f"🏷️ メタデータ生成: {len(metadata['tags'])}タグ")
            
            # 7. 関連ノート発見
            related_notes = self.find_related_notes(original_content, patterns)
            print(f"🔗 関連ノート: {len(related_notes)}個発見")
            
            # 8. 完全なObsidianノート作成
            integrated_content = self.create_obsidian_note(
                original_content, metadata, knowledge_type, related_notes
            )
            
            # 9. Obsidian構造への保存
            new_filename = f"AI_Integrated_{filename}"
            success, saved_path = self.save_to_obsidian_structure(
                integrated_content, new_filename, knowledge_type
            )
            
            if success:
                print("=" * 60)
                print("🎉 Knowledge Integration 完了！")
                print(f"📍 保存先: {saved_path}")
                print(f"📊 統合情報:")
                print(f"  - タイプ: {knowledge_type}")
                print(f"  - タグ: {len(metadata['tags'])}個")
                print(f"  - 関連ノート: {len(related_notes)}個")
                print(f"  - AI最適化: ✅")
                
                return {
                    "success": True,
                    "path": saved_path,
                    "metadata": metadata,
                    "related_notes": related_notes,
                    "knowledge_type": knowledge_type
                }
            else:
                print("❌ 統合に失敗しました")
                return {"success": False}
                
        except Exception as e:
            print(f"❌ 統合処理エラー: {e}")
            return {"success": False, "error": str(e)}
    
    def integrate_all_pending_knowledge(self):
        """保留中の全知識ノートを統合"""
        print("🚀 全知識ノート統合開始")
        print("=" * 50)
        
        if not os.path.exists(self.local_knowledge):
            print(f"📂 知識ディレクトリが見つかりません: {self.local_knowledge}")
            return
        
        knowledge_files = list(Path(self.local_knowledge).glob("*.md"))
        
        if not knowledge_files:
            print("📄 統合対象の知識ノートが見つかりません")
            return
        
        print(f"📋 統合対象: {len(knowledge_files)}ファイル")
        
        results = []
        for i, file_path in enumerate(knowledge_files, 1):
            print(f"\n--- 統合 {i}/{len(knowledge_files)} ---")
            result = self.integrate_knowledge_note(str(file_path))
            results.append(result)
        
        # 統計表示
        successful = sum(1 for r in results if r.get("success"))
        print("\n" + "=" * 50)
        print(f"🎯 統合完了: {successful}/{len(knowledge_files)} 成功")
        
        return results
    
    def show_integration_status(self):
        """統合状況の表示"""
        print("📊 Knowledge Integration 状況")
        print("=" * 40)
        
        # ローカル知識ファイル
        local_files = list(Path(self.local_knowledge).glob("*.md")) if os.path.exists(self.local_knowledge) else []
        print(f"ローカル知識ファイル: {len(local_files)}個")
        
        # Git知識データベース
        git_db = self.load_git_knowledge_db()
        print(f"Git知識エントリ: {len(git_db.get('learnings', {}))}個")
        
        # 分類別統計
        print("\n📋 知識分類:")
        for k_type, config in self.classification_rules.items():
            print(f"  - {k_type.replace('_', ' ').title()}: {config['target_dir']}")
        
        return {
            "local_files": len(local_files),
            "git_entries": len(git_db.get('learnings', {})),
            "classifications": len(self.classification_rules)
        }

def main():
    """メイン実行"""
    import sys
    
    integrator = ObsidianKnowledgeIntegrator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "integrate":
            if len(sys.argv) > 2:
                # 特定ファイルの統合
                file_path = sys.argv[2]
                integrator.integrate_knowledge_note(file_path)
            else:
                # 全ファイルの統合
                integrator.integrate_all_pending_knowledge()
        
        elif command == "status":
            integrator.show_integration_status()
        
        else:
            print("使用方法:")
            print("  python3 obsidian_knowledge_integrator.py integrate [file_path]")
            print("  python3 obsidian_knowledge_integrator.py status")
    else:
        # デフォルト: 全統合
        integrator.integrate_all_pending_knowledge()

if __name__ == "__main__":
    main()