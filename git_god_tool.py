#!/usr/bin/env python3
"""
Git God Tool - TAL思考による神ツール
==================================
複雑性を力に変える：日常使用される高度な開発支援
"""

import subprocess
import os
import json
from datetime import datetime
from pathlib import Path

class GitGodTool:
    def __init__(self):
        self.repo_path = "/mnt/c/Claude Code/tool"
        self.obsidian_templates = self._load_obsidian_templates()
        
    def _load_obsidian_templates(self):
        """Obsidianテンプレートの活用"""
        return {
            "commit_patterns": {
                "fix": "🐛 Fix: ",
                "feature": "✨ Feature: ",
                "refactor": "🔧 Refactor: ",
                "docs": "📚 Docs: ",
                "style": "💄 Style: ",
                "test": "🧪 Test: ",
                "perf": "⚡ Perf: ",
                "security": "🔒 Security: "
            }
        }
    
    def smart_status(self):
        """神ツール機能1: 状況認識とアクション提案"""
        print("🎯 Git神ツール - 状況分析")
        print("=" * 40)
        
        # TAL思考フレームワーク適用
        situation = self._analyze_situation()
        decisions = self._provide_decision_framework(situation)
        actions = self._suggest_actions(situation, decisions)
        
        return {
            "situation": situation,
            "decisions": decisions, 
            "actions": actions
        }
    
    def _analyze_situation(self):
        """SITUATION_AWARENESS: 現在の状況を完全把握"""
        print("📊 SITUATION_AWARENESS")
        
        # 現在のブランチ
        branch = subprocess.run(
            ["git", "branch", "--show-current"], 
            capture_output=True, text=True, cwd=self.repo_path
        ).stdout.strip()
        
        # 変更状況
        status = subprocess.run(
            ["git", "status", "--porcelain"], 
            capture_output=True, text=True, cwd=self.repo_path
        ).stdout.strip()
        
        # 同期状況
        try:
            ahead_behind = subprocess.run(
                ["git", "rev-list", "--count", "--left-right", "HEAD...origin/main"],
                capture_output=True, text=True, cwd=self.repo_path
            ).stdout.strip()
            ahead, behind = ahead_behind.split('\t') if ahead_behind else ("0", "0")
        except:
            ahead, behind = "?", "?"
        
        # 最近のコミット
        recent_commits = subprocess.run(
            ["git", "log", "--oneline", "-5"],
            capture_output=True, text=True, cwd=self.repo_path
        ).stdout.strip().split('\n')
        
        situation = {
            "branch": branch,
            "changes": len(status.split('\n')) if status else 0,
            "ahead": ahead,
            "behind": behind,
            "recent_commits": recent_commits
        }
        
        print(f"  📍 Branch: {branch}")
        print(f"  📝 Changes: {situation['changes']} files")
        print(f"  ⬆️  Ahead: {ahead} commits")
        print(f"  ⬇️  Behind: {behind} commits")
        
        return situation
    
    def _provide_decision_framework(self, situation):
        """DECISION_FRAMEWORK: TAL思考による意思決定支援"""
        print("\n🤔 DECISION_FRAMEWORK")
        
        decisions = {}
        
        # 1. コミット判断
        if situation["changes"] > 0:
            if situation["changes"] < 5:
                decisions["commit"] = "推奨: 小さな変更、今すぐコミット"
                commit_priority = "high"
            elif situation["changes"] < 15:
                decisions["commit"] = "検討: 中規模変更、機能単位で分割を検討"
                commit_priority = "medium"
            else:
                decisions["commit"] = "注意: 大規模変更、必ず分割してコミット"
                commit_priority = "low"
        else:
            decisions["commit"] = "不要: 変更なし"
            commit_priority = "none"
        
        # 2. 同期判断
        if int(situation["behind"]) > 0:
            decisions["sync"] = f"必須: {situation['behind']}コミット遅れ、pullが必要"
        elif int(situation["ahead"]) > 0:
            decisions["sync"] = f"推奨: {situation['ahead']}コミット先行、pushを検討"
        else:
            decisions["sync"] = "同期済み"
        
        # 3. ブランチ判断
        if situation["branch"] == "main":
            if situation["changes"] > 0:
                decisions["branch"] = "注意: mainブランチで作業中、featureブランチを検討"
            else:
                decisions["branch"] = "安全: mainブランチ、変更なし"
        else:
            decisions["branch"] = f"適切: {situation['branch']}ブランチで作業中"
        
        for key, decision in decisions.items():
            print(f"  🎯 {key.title()}: {decision}")
        
        return decisions
    
    def _suggest_actions(self, situation, decisions):
        """ACTION_GUIDANCE: 具体的なアクション提案"""
        print("\n⚡ ACTION_GUIDANCE")
        
        actions = []
        
        # 優先度付きアクション生成
        if int(situation["behind"]) > 0:
            actions.append({
                "priority": 1,
                "action": "git pull",
                "reason": "リモートの変更を取得",
                "command": "git pull origin main"
            })
        
        if situation["changes"] > 0:
            # スマートコミットメッセージ提案
            smart_message = self._generate_smart_commit_message()
            actions.append({
                "priority": 2,
                "action": "smart_commit",
                "reason": "変更をコミット",
                "command": f'git add . && git commit -m "{smart_message}"'
            })
        
        if int(situation["ahead"]) > 0:
            actions.append({
                "priority": 3,
                "action": "git push",
                "reason": "変更をリモートに反映",
                "command": "git push origin main"
            })
        
        # アクション表示
        for i, action in enumerate(actions, 1):
            print(f"  {i}. {action['action']}: {action['reason']}")
            print(f"     💻 {action['command']}")
        
        return actions
    
    def _generate_smart_commit_message(self):
        """神ツール機能2: 変更内容からスマートなコミットメッセージ生成"""
        # ファイル変更の分析
        diff_stat = subprocess.run(
            ["git", "diff", "--stat"],
            capture_output=True, text=True, cwd=self.repo_path
        ).stdout
        
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=self.repo_path
        ).stdout
        
        # 変更パターンの認識
        patterns = []
        if ".py" in status:
            patterns.append("feature")
        if ".md" in status:
            patterns.append("docs")
        if "fix" in status.lower() or "bug" in status.lower():
            patterns.append("fix")
        
        # スマートメッセージ生成
        if patterns:
            main_pattern = patterns[0]
            prefix = self.obsidian_templates["commit_patterns"][main_pattern]
        else:
            prefix = "📝 Update: "
        
        # ファイル数による詳細度調整
        file_count = len([line for line in status.split('\n') if line.strip()])
        if file_count == 1:
            message = f"{prefix}Single file modification"
        elif file_count <= 5:
            message = f"{prefix}Multiple file updates ({file_count} files)"
        else:
            message = f"{prefix}Large-scale changes ({file_count} files)"
        
        return message
    
    def execute_action(self, action_index=1):
        """神ツール機能3: ワンクリック実行"""
        analysis = self.smart_status()
        
        if action_index <= len(analysis["actions"]):
            action = analysis["actions"][action_index - 1]
            print(f"\n🚀 実行中: {action['action']}")
            print(f"💻 Command: {action['command']}")
            
            # 実際のコマンド実行
            result = subprocess.run(
                action['command'], 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=self.repo_path
            )
            
            if result.returncode == 0:
                print("✅ 実行完了!")
                
                # Obsidianに実行記録を保存
                self._save_to_obsidian(action, result.stdout)
                
                return True
            else:
                print(f"❌ 実行エラー: {result.stderr}")
                return False
        else:
            print("❌ 無効なアクション番号です")
            return False
    
    def _save_to_obsidian(self, action, output):
        """神ツール機能4: Obsidian知識統合"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        note_content = f"""# Git操作記録 - {timestamp}

## 実行アクション
- **操作**: {action['action']}
- **理由**: {action['reason']}
- **コマンド**: `{action['command']}`

## 実行結果
```
{output}
```

## タグ
#git #automation #daily-workflow

---
*Git神ツールによる自動記録*
"""
        
        # ローカルとObsidian両方に保存
        try:
            # ローカル保存
            os.makedirs("git_operations_log", exist_ok=True)
            local_path = f"git_operations_log/git_op_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(local_path, 'w', encoding='utf-8') as f:
                f.write(note_content)
            
            # Obsidian保存（PowerShell経由）
            obsidian_path = f"Daily Notes/Git Operations/git_op_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            subprocess.run([
                "powershell.exe", "-Command",
                f"New-Item -ItemType Directory -Force -Path 'G:\\マイドライブ\\Obsidian Vault\\Daily Notes\\Git Operations'; $content = @'`n{note_content}`n'@; $content | Out-File -FilePath 'G:\\マイドライブ\\Obsidian Vault\\{obsidian_path}' -Encoding UTF8"
            ], capture_output=True)
            
            print(f"📝 操作記録をObsidianに保存: {obsidian_path}")
            
        except Exception as e:
            print(f"⚠️ Obsidian保存スキップ: {str(e)[:30]}...")

def main():
    """メイン実行: 神ツールインターフェース"""
    import sys
    
    tool = GitGodTool()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            tool.smart_status()
        elif sys.argv[1] == "execute":
            action_num = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            tool.execute_action(action_num)
        else:
            print("使用方法:")
            print("  python3 git_god_tool.py status    # 状況分析とアクション提案")
            print("  python3 git_god_tool.py execute 1 # 推奨アクション実行")
    else:
        # デフォルト: インタラクティブモード
        print("🎯 Git神ツール - Interactive Mode")
        analysis = tool.smart_status()
        
        if analysis["actions"]:
            print(f"\n実行しますか？ (1-{len(analysis['actions'])}, q=quit): ", end="")
            choice = input()
            
            if choice.isdigit() and 1 <= int(choice) <= len(analysis["actions"]):
                tool.execute_action(int(choice))
            elif choice.lower() != 'q':
                print("無効な選択です")

if __name__ == "__main__":
    main()