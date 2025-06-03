#!/usr/bin/env python3
"""
スマートGit自動コミットシステム
==============================
意味のある変更のみを適切なタイミングでコミット
"""

import os
import json
import time
import hashlib
import subprocess
import re
from datetime import datetime
from pathlib import Path

class SmartGitAutoCommit:
    def __init__(self):
        self.work_dir = "/mnt/c/Claude Code/tool"
        self.state_file = ".smart_git_state.json"
        self.interval = 1800  # 30分
        self.min_change_threshold = 3  # 最低3ファイルの変更
        
        # 除外パターン
        self.ignored_patterns = [
            r'.*\.log$',
            r'.*\.pid$',
            r'sessions/.*',
            r'auto_systems_logs/.*',
            r'.*\.pyc$',
            r'__pycache__/.*',
        ]
        
        # 機密情報パターン
        self.sensitive_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
        ]
        
    def load_state(self):
        """前回の状態を読み込み"""
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except:
            return {
                "last_commit": None,
                "file_hashes": {},
                "commit_count": 0
            }
    
    def save_state(self, state):
        """状態を保存"""
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def run_git_command(self, command):
        """Gitコマンドを実行"""
        try:
            result = subprocess.run(
                command,
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                shell=True
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def get_file_hash(self, filepath):
        """ファイルのハッシュを取得"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def is_ignored(self, filepath):
        """無視すべきファイルかチェック"""
        for pattern in self.ignored_patterns:
            if re.match(pattern, filepath):
                return True
        return False
    
    def check_sensitive_info(self, filepath):
        """機密情報が含まれているかチェック"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                for pattern in self.sensitive_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        return True
        except:
            pass
        return False
    
    def analyze_changes(self):
        """変更を分析"""
        state = self.load_state()
        changes = {
            'new': [],
            'modified': [],
            'deleted': [],
            'sensitive': []
        }
        current_hashes = {}
        
        # 現在のファイルをチェック
        for root, dirs, files in os.walk(self.work_dir):
            # .gitディレクトリをスキップ
            if '.git' in root:
                continue
                
            for file in files:
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, self.work_dir)
                
                if self.is_ignored(rel_path):
                    continue
                
                current_hash = self.get_file_hash(filepath)
                if not current_hash:
                    continue
                
                current_hashes[rel_path] = current_hash
                
                # 機密情報チェック
                if self.check_sensitive_info(filepath):
                    changes['sensitive'].append(rel_path)
                    continue
                
                # 変更タイプを判定
                if rel_path not in state["file_hashes"]:
                    changes['new'].append(rel_path)
                elif state["file_hashes"][rel_path] != current_hash:
                    changes['modified'].append(rel_path)
        
        # 削除されたファイルをチェック
        for rel_path in state["file_hashes"]:
            if rel_path not in current_hashes:
                changes['deleted'].append(rel_path)
        
        return changes, current_hashes
    
    def should_commit(self, changes):
        """コミットすべきかどうか判定"""
        # 機密情報が含まれている場合はコミットしない
        if changes['sensitive']:
            print(f"⚠️ 機密情報が検出されました: {changes['sensitive']}")
            return False
        
        # 変更の総数をチェック
        total_changes = len(changes['new']) + len(changes['modified']) + len(changes['deleted'])
        if total_changes < self.min_change_threshold:
            print(f"変更が少なすぎます（{total_changes}件）")
            return False
        
        # Python構文エラーチェック
        for file in changes['new'] + changes['modified']:
            if file.endswith('.py'):
                result = subprocess.run(
                    ['python3', '-m', 'py_compile', file],
                    cwd=self.work_dir,
                    capture_output=True
                )
                if result.returncode != 0:
                    print(f"⚠️ Python構文エラー: {file}")
                    return False
        
        return True
    
    def generate_commit_message(self, changes):
        """インテリジェントなコミットメッセージを生成"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 変更の分類
        new_count = len(changes['new'])
        mod_count = len(changes['modified'])
        del_count = len(changes['deleted'])
        
        # 主要な変更タイプを特定
        main_action = ""
        if new_count > mod_count and new_count > del_count:
            main_action = "Add"
        elif del_count > mod_count:
            main_action = "Remove"
        else:
            main_action = "Update"
        
        # ファイルタイプの分析
        file_types = {}
        all_files = changes['new'] + changes['modified']
        for file in all_files:
            ext = Path(file).suffix or 'no-ext'
            file_types[ext] = file_types.get(ext, 0) + 1
        
        # 最も変更の多いファイルタイプ
        if file_types:
            main_type = max(file_types, key=file_types.get)
            if main_type == '.py':
                type_desc = "Python scripts"
            elif main_type == '.md':
                type_desc = "documentation"
            elif main_type == '.sh':
                type_desc = "shell scripts"
            elif main_type == '.json':
                type_desc = "configuration"
            else:
                type_desc = f"{main_type} files"
        else:
            type_desc = "files"
        
        # メッセージ構築
        if new_count > 0 and mod_count > 0:
            message = f"Auto-commit: {main_action} and modify {type_desc}"
        else:
            message = f"Auto-commit: {main_action} {type_desc}"
        
        # 詳細を追加
        details = []
        if new_count > 0:
            details.append(f"{new_count} new")
        if mod_count > 0:
            details.append(f"{mod_count} modified")
        if del_count > 0:
            details.append(f"{del_count} deleted")
        
        if details:
            message += f" ({', '.join(details)})"
        
        # 主要な変更ファイルを追加（最大3個）
        important_files = []
        for file in (changes['new'] + changes['modified'])[:3]:
            if not file.startswith('sessions/') and not file.endswith('.log'):
                important_files.append(Path(file).name)
        
        if important_files:
            message += f"\n\nKey files: {', '.join(important_files)}"
        
        message += f"\n\nTimestamp: {timestamp}"
        
        return message
    
    def auto_commit(self, changes, current_hashes):
        """自動コミット実行"""
        if not self.should_commit(changes):
            return False, "Commit conditions not met"
        
        # git add (変更されたファイルのみ)
        files_to_add = changes['new'] + changes['modified']
        if files_to_add:
            for file in files_to_add:
                success, stdout, stderr = self.run_git_command(f"git add '{file}'")
                if not success:
                    print(f"⚠️ git add failed for {file}: {stderr}")
        
        # 削除されたファイルの処理
        for file in changes['deleted']:
            success, stdout, stderr = self.run_git_command(f"git rm '{file}'")
            # ファイルが既に削除されている場合はエラーを無視
        
        # コミットメッセージ生成
        commit_message = self.generate_commit_message(changes)
        
        # git commit
        success, stdout, stderr = self.run_git_command(
            f"git commit -m \"{commit_message.replace('\"', '\\\"')}\""
        )
        
        if not success:
            if "nothing to commit" in stderr:
                return True, "Nothing to commit"
            return False, f"git commit failed: {stderr}"
        
        # 状態を更新
        state = self.load_state()
        state["file_hashes"] = current_hashes
        state["last_commit"] = datetime.now().isoformat()
        state["commit_count"] = state.get("commit_count", 0) + 1
        self.save_state(state)
        
        total_changes = len(changes['new']) + len(changes['modified']) + len(changes['deleted'])
        return True, f"Committed {total_changes} changes (commit #{state['commit_count']})"
    
    def monitor_once(self):
        """1回の監視実行"""
        print(f"🔍 Git自動コミットチェック - {datetime.now().strftime('%H:%M:%S')}")
        
        # 変更を分析
        changes, current_hashes = self.analyze_changes()
        
        # 結果を表示
        total_changes = len(changes['new']) + len(changes['modified']) + len(changes['deleted'])
        if total_changes == 0:
            print("✅ 変更なし")
            return True
        
        print(f"📝 検出された変更: {total_changes}件")
        if changes['new']:
            print(f"  新規: {len(changes['new'])}件")
        if changes['modified']:
            print(f"  更新: {len(changes['modified'])}件")
        if changes['deleted']:
            print(f"  削除: {len(changes['deleted'])}件")
        
        # コミット実行
        success, message = self.auto_commit(changes, current_hashes)
        status = "✅" if success else "❌"
        print(f"{status} {message}")
        
        # Git-Knowledge統合（コミット成功時）
        if success and "Committed" in message:
            try:
                from git_knowledge_connector import GitKnowledgeConnector
                print("")
                print("🧠 自動Git-Knowledge統合開始...")
                
                connector = GitKnowledgeConnector()
                connector.process_commit("HEAD")
                print("🎉 AI最適化知識ノート自動生成完了")
                
            except Exception as e:
                print(f"⚠️ Git-Knowledge統合スキップ: {str(e)[:50]}...")
        
        return success

def main():
    """メイン関数"""
    import sys
    
    auto_commit = SmartGitAutoCommit()
    
    if len(sys.argv) > 1 and sys.argv[1] == "daemon":
        print("🤖 スマートGit自動コミットデーモンを開始")
        print(f"監視間隔: {auto_commit.interval//60}分")
        print("=" * 50)
        
        while True:
            try:
                auto_commit.monitor_once()
                print("")
                time.sleep(auto_commit.interval)
            except KeyboardInterrupt:
                print("\n⏹️ 監視を停止しました")
                break
            except Exception as e:
                print(f"❌ エラー: {e}")
                time.sleep(60)  # エラー時は1分待機
    else:
        # 1回だけ実行
        auto_commit.monitor_once()

if __name__ == "__main__":
    main()