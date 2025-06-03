#!/usr/bin/env python3
"""
スマートGit自動コミットシステム (パフォーマンス最適化版)
======================================================
目標: 24秒 → 3秒以下
"""

import os
import json
import time
import hashlib
import subprocess
import re
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import threading

class OptimizedSmartGitAutoCommit:
    def __init__(self):
        self.work_dir = "/mnt/c/Claude Code/tool"
        self.state_file = ".smart_git_state.json"
        self.interval = 1800  # 30分
        self.min_change_threshold = 3  # 最低3ファイルの変更
        
        # パフォーマンス最適化用キャッシュ
        self.git_status_cache = None
        self.ignored_files_cache = None
        self.cache_timestamp = 0
        self.cache_duration = 30  # 30秒キャッシュ
        
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
        """Git コマンドを実行"""
        try:
            result = subprocess.run(
                command,
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                shell=True,
                timeout=10  # タイムアウト追加
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timeout"
        except Exception as e:
            return False, "", str(e)
    
    def get_git_status_optimized(self):
        """最適化されたGitステータス取得"""
        current_time = time.time()
        
        # キャッシュチェック
        if (self.git_status_cache and 
            current_time - self.cache_timestamp < self.cache_duration):
            return self.git_status_cache
        
        # git status --porcelain で変更ファイル一覧を高速取得
        success, stdout, stderr = self.run_git_command("git status --porcelain")
        if not success:
            return {}
        
        changes = {
            'new': [],
            'modified': [],
            'deleted': []
        }
        
        for line in stdout.strip().split('\n'):
            if not line:
                continue
            
            status = line[:2]
            filepath = line[3:]
            
            if status[0] == 'A' or status[1] == 'A' or status == '??':
                changes['new'].append(filepath)
            elif status[0] == 'M' or status[1] == 'M':
                changes['modified'].append(filepath)
            elif status[0] == 'D' or status[1] == 'D':
                changes['deleted'].append(filepath)
        
        # キャッシュ更新
        self.git_status_cache = changes
        self.cache_timestamp = current_time
        
        return changes
    
    def get_ignored_files_optimized(self, files):
        """一括でgit check-ignoreを実行"""
        if not files:
            return set()
        
        # ファイルリストを一時ファイルに書き込み
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                for file in files:
                    f.write(file + '\n')
                temp_file = f.name
            
            # git check-ignore --stdin で一括チェック
            success, stdout, stderr = self.run_git_command(
                f"git check-ignore --stdin < {temp_file}"
            )
            
            # 一時ファイル削除
            os.unlink(temp_file)
            
            if success:
                return set(stdout.strip().split('\n'))
            else:
                return set()
                
        except Exception:
            # フォールバック: 個別チェック（しかし制限付き）
            ignored = set()
            for file in files[:20]:  # 最大20ファイルまで
                success, stdout, stderr = self.run_git_command(f"git check-ignore '{file}'")
                if success:
                    ignored.add(file)
            return ignored
    
    def get_file_hash_batch(self, files):
        """複数ファイルのハッシュを効率的に計算"""
        def compute_hash(filepath):
            try:
                with open(os.path.join(self.work_dir, filepath), 'rb') as f:
                    return filepath, hashlib.md5(f.read()).hexdigest()
            except:
                return filepath, None
        
        # 並列処理でハッシュ計算
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(compute_hash, files))
        
        return {filepath: hash_val for filepath, hash_val in results if hash_val}
    
    def check_sensitive_info_batch(self, files):
        """複数ファイルの機密情報を並列チェック"""
        def check_single_file(filepath):
            try:
                full_path = os.path.join(self.work_dir, filepath)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for pattern in self.sensitive_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            return filepath
            except:
                pass
            return None
        
        # 並列処理で機密情報チェック
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(check_single_file, files))
        
        return [f for f in results if f]
    
    def analyze_changes_optimized(self):
        """最適化された変更分析"""
        print("🔍 高速変更分析開始...")
        start_time = time.time()
        
        # 1. Gitステータスを高速取得
        git_changes = self.get_git_status_optimized()
        print(f"  📊 Git状態取得: {time.time() - start_time:.2f}秒")
        
        all_files = git_changes['new'] + git_changes['modified']
        
        if not all_files:
            print("  ✅ 変更なし")
            return {'new': [], 'modified': [], 'deleted': [], 'sensitive': []}, {}
        
        # 2. 無視ファイルを一括チェック
        ignored_files = self.get_ignored_files_optimized(all_files)
        filtered_files = [f for f in all_files if f not in ignored_files]
        print(f"  🚫 無視ファイル除外: {time.time() - start_time:.2f}秒")
        
        # 3. ファイルハッシュを並列計算
        current_hashes = self.get_file_hash_batch(filtered_files)
        print(f"  🔢 ハッシュ計算: {time.time() - start_time:.2f}秒")
        
        # 4. 機密情報を並列チェック
        sensitive_files = self.check_sensitive_info_batch(filtered_files)
        print(f"  🔒 機密情報チェック: {time.time() - start_time:.2f}秒")
        
        # 5. 変更タイプの判定
        state = self.load_state()
        changes = {
            'new': [f for f in git_changes['new'] if f in current_hashes and f not in state["file_hashes"]],
            'modified': [f for f in git_changes['modified'] if f in current_hashes and f in state["file_hashes"] and state["file_hashes"][f] != current_hashes[f]],
            'deleted': git_changes['deleted'],
            'sensitive': sensitive_files
        }
        
        total_time = time.time() - start_time
        print(f"  ⚡ 分析完了: {total_time:.2f}秒")
        
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
        
        message += f"\\n\\nTimestamp: {timestamp}"
        
        return message
    
    def auto_commit_optimized(self, changes, current_hashes):
        """最適化された自動コミット実行"""
        if not self.should_commit(changes):
            return False, "Commit conditions not met"
        
        # git add (変更されたファイルのみ)
        files_to_add = changes['new'] + changes['modified']
        if files_to_add:
            # 一括でgit add
            files_str = "' '".join(files_to_add)
            success, stdout, stderr = self.run_git_command(f"git add '{files_str}'")
            if not success:
                print(f"⚠️ git add failed: {stderr}")
        
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
    
    def monitor_once_optimized(self):
        """1回の最適化監視実行"""
        print(f"🚀 最適化Git自動コミットチェック - {datetime.now().strftime('%H:%M:%S')}")
        start_time = time.time()
        
        # 変更を分析
        changes, current_hashes = self.analyze_changes_optimized()
        
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
        success, message = self.auto_commit_optimized(changes, current_hashes)
        status = "✅" if success else "❌"
        print(f"{status} {message}")
        
        # 知識統合は並列で実行（ブロックしない）
        if success and "Committed" in message:
            def run_knowledge_integration():
                try:
                    from git_knowledge_connector import GitKnowledgeConnector
                    print("🧠 自動Git-Knowledge統合開始...")
                    connector = GitKnowledgeConnector()
                    connector.process_commit("HEAD")
                    print("🎉 AI最適化知識ノート自動生成完了")
                except Exception as e:
                    print(f"⚠️ Git-Knowledge統合スキップ: {str(e)[:50]}...")
            
            # バックグラウンドで実行
            thread = threading.Thread(target=run_knowledge_integration)
            thread.daemon = True
            thread.start()
        
        total_time = time.time() - start_time
        print(f"⚡ 総実行時間: {total_time:.2f}秒")
        
        return success

def main():
    """メイン関数"""
    import sys
    
    auto_commit = OptimizedSmartGitAutoCommit()
    
    if len(sys.argv) > 1 and sys.argv[1] == "daemon":
        print("🤖 最適化スマートGit自動コミットデーモンを開始")
        print(f"監視間隔: {auto_commit.interval//60}分")
        print("=" * 50)
        
        while True:
            try:
                auto_commit.monitor_once_optimized()
                print("")
                time.sleep(auto_commit.interval)
            except KeyboardInterrupt:
                print("\\n⏹️ 監視を停止しました")
                break
            except Exception as e:
                print(f"❌ エラー: {e}")
                time.sleep(60)  # エラー時は1分待機
    else:
        # 1回だけ実行
        auto_commit.monitor_once_optimized()

if __name__ == "__main__":
    main()