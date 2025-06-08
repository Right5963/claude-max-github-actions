#!/usr/bin/env python3
"""
Obsidian脳みそ自動記録・活用システム
=================================
記録は宝 = データ作成 + データ利用の完全自動化

問題:
- 脳みそ（Obsidian）に記録されない
- 記録されても活用されない
- セッション間で知識が断絶

解決策:
- リアルタイム自動記録
- 自動的な知識検索・提示
- 過去の経験の強制的活用
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path
import threading
import time
import hashlib

class ObsidianBrainSystem:
    def __init__(self):
        self.tool_path = Path("/mnt/c/Claude Code/tool")
        self.obsidian_path = "G:\\マイドライブ\\Obsidian Vault"
        self.today = datetime.now().strftime("%Y%m%d")
        
        # 今日の主要記録ファイル
        self.daily_record = f"{self.obsidian_path}\\Claude_Brain_Record_{self.today}.md"
        self.activity_record = f"{self.obsidian_path}\\Activity_Log_{self.today}.md"
        self.knowledge_index = f"{self.obsidian_path}\\Knowledge_Index_{self.today}.md"
        
        # 脳みその初期化
        self.initialize_brain()

    def initialize_brain(self):
        """脳みその初期化 - 今日の記録開始"""
        print("🧠 Obsidian脳みそシステム初期化中...")
        
        brain_header = f"""# 🧠 Claude Code 脳みそ記録 {self.today}

## 📋 セッション開始情報
- 開始時刻: {datetime.now().strftime('%H:%M:%S')}
- PID: {os.getpid()}
- 作業ディレクトリ: {self.tool_path}

## 🎯 今日の重要発見
> 自動記録システムがここに重要な発見を追記します

## 📝 リアルタイム活動ログ
"""
        
        self.write_to_obsidian(self.daily_record, brain_header, mode='w')
        
        # 知識インデックス初期化
        knowledge_header = f"""# 📚 知識インデックス {self.today}

## 🔍 今日参照すべき過去の知識
{self.get_relevant_past_knowledge()}

## 💡 今日の新しい学び
> システムが自動的に学びを記録します

## ⚠️ 回避すべき過去の失敗
{self.get_past_failures()}
"""
        
        self.write_to_obsidian(self.knowledge_index, knowledge_header, mode='w')
        print("✅ 脳みそ初期化完了")

    def write_to_obsidian(self, file_path, content, mode='a'):
        """Obsidianへの書き込み（PowerShell経由）"""
        try:
            if mode == 'w':
                ps_command = f'''
                Set-Content -Path "{file_path}" -Value @"
{content}
"@ -Encoding UTF8
                '''
            else:
                ps_command = f'''
                Add-Content -Path "{file_path}" -Value @"
{content}
"@ -Encoding UTF8
                '''
            
            result = subprocess.run([
                "powershell.exe", "-Command", ps_command
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                print(f"⚠️ Obsidian書き込みエラー: {result.stderr}")
                
        except Exception as e:
            print(f"⚠️ Obsidian書き込み例外: {e}")

    def get_relevant_past_knowledge(self):
        """過去の関連知識を自動取得"""
        try:
            # MCP経由でObsidian検索
            search_terms = [
                "Simple First", "git_quick_insight", "smart_git_auto_commit",
                "記録は宝", "why.py", "システム削除", "失敗"
            ]
            
            relevant_knowledge = []
            
            for term in search_terms:
                try:
                    result = subprocess.run([
                        "./mcp_bridge_extended.sh", "obsidian_search", term
                    ], cwd=self.tool_path, capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0 and result.stdout.strip():
                        files = result.stdout.strip().split('\n')[:3]  # 上位3件
                        for file_path in files:
                            if ':' in file_path:
                                file_name = file_path.split(':')[0].split('\\')[-1]
                                relevant_knowledge.append(f"- [{term}] {file_name}")
                                
                except:
                    continue
            
            if relevant_knowledge:
                return '\n'.join(relevant_knowledge[:10])  # 最大10件
            else:
                return "- まだ蓄積された知識がありません"
                
        except Exception as e:
            return f"- 知識取得エラー: {e}"

    def get_past_failures(self):
        """過去の失敗を自動取得"""
        failure_keywords = [
            "削除", "失敗", "エラー", "問題", "アーカイブ", "なぜダメだった"
        ]
        
        failures = []
        for keyword in failure_keywords:
            try:
                result = subprocess.run([
                    "./mcp_bridge_extended.sh", "obsidian_search", keyword
                ], cwd=self.tool_path, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0 and result.stdout.strip():
                    files = result.stdout.strip().split('\n')[:2]  # 上位2件
                    for file_path in files:
                        if ':' in file_path:
                            file_name = file_path.split(':')[0].split('\\')[-1]
                            failures.append(f"- ⚠️ {file_name}")
                            
            except:
                continue
        
        return '\n'.join(failures[:5]) if failures else "- 記録された失敗がありません"

    def record_command_execution(self, command, output=None, error=None):
        """コマンド実行の自動記録"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        record = f"""
### {timestamp} - コマンド実行
```bash
{command}
```
"""
        
        if output:
            record += f"""
**出力:**
```
{output[:500]}  # 最初の500文字のみ
```
"""
        
        if error:
            record += f"""
**エラー:**
```
{error[:200]}
```
"""
        
        self.write_to_obsidian(self.activity_record, record)

    def record_file_change(self, change_type, file_path, details=None):
        """ファイル変更の自動記録"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        record = f"""
### {timestamp} - ファイル変更
- **タイプ:** {change_type}
- **ファイル:** {file_path}
"""
        
        if details:
            record += f"- **詳細:** {details}\n"
        
        self.write_to_obsidian(self.activity_record, record)

    def record_insight(self, insight_type, description, context=None):
        """洞察・学びの自動記録"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        insight = f"""
## 💡 {timestamp} - {insight_type}

{description}
"""
        
        if context:
            insight += f"""
**文脈:**
{context}
"""
        
        insight += f"""
**タグ:** #学び #{insight_type} #{self.today}

---
"""
        
        self.write_to_obsidian(self.knowledge_index, insight)

    def auto_retrieve_context(self, current_task):
        """現在のタスクに関連する文脈を自動取得"""
        print(f"🔍 '{current_task}' に関連する過去の知識を検索中...")
        
        try:
            # 関連する過去の記録を検索
            search_result = subprocess.run([
                "./mcp_bridge_extended.sh", "obsidian_search", current_task
            ], cwd=self.tool_path, capture_output=True, text=True, timeout=30)
            
            if search_result.returncode == 0 and search_result.stdout.strip():
                files = search_result.stdout.strip().split('\n')[:3]
                
                context_record = f"""
## 🔍 {datetime.now().strftime('%H:%M:%S')} - 自動文脈取得

**現在のタスク:** {current_task}

**関連する過去の記録:**
"""
                
                for file_path in files:
                    if ':' in file_path:
                        file_name = file_path.split(':')[0].split('\\')[-1]
                        line_content = file_path.split(':', 1)[1] if ':' in file_path else ""
                        context_record += f"- {file_name}: {line_content[:100]}...\n"
                
                context_record += f"""
**活用方法:** 上記の過去の経験を参考に現在のタスクを効率化
"""
                
                self.write_to_obsidian(self.daily_record, context_record)
                
                print(f"✅ {len(files)}件の関連記録を発見・記録")
                return files
            else:
                print("📝 関連する過去の記録が見つかりませんでした")
                return []
                
        except Exception as e:
            print(f"⚠️ 文脈取得エラー: {e}")
            return []

    def force_knowledge_review(self):
        """強制的な知識レビュー - セッション開始時に必ず実行"""
        print("🧠 強制的知識レビュー開始...")
        
        # 昨日以降の重要な記録を強制表示
        yesterday_keywords = [
            "重要", "失敗", "成功", "学び", "Simple First", "記録"
        ]
        
        review_content = f"""
## 🚨 {datetime.now().strftime('%H:%M:%S')} - 強制知識レビュー

**必ず確認すべき過去の重要事項:**

"""
        
        for keyword in yesterday_keywords:
            try:
                result = subprocess.run([
                    "./mcp_bridge_extended.sh", "obsidian_search", keyword
                ], cwd=self.tool_path, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0 and result.stdout.strip():
                    files = result.stdout.strip().split('\n')[:2]  # 上位2件
                    review_content += f"\n### {keyword}関連:\n"
                    
                    for file_path in files:
                        if ':' in file_path:
                            file_name = file_path.split(':')[0].split('\\')[-1]
                            review_content += f"- {file_name}\n"
                            
            except:
                continue
        
        review_content += f"""
**⚠️ 作業開始前に上記の記録を必ず確認してください**

**今セッションの改善点:**
- 過去の失敗を繰り返さない
- 成功パターンを積極活用
- Simple First原則の徹底

---
"""
        
        self.write_to_obsidian(self.daily_record, review_content)
        print("✅ 強制知識レビュー完了 - Obsidianを確認してください")

    def start_continuous_brain_monitoring(self):
        """継続的脳みそ監視開始"""
        print("🔄 継続的脳みそ監視開始...")
        
        def monitor_loop():
            while True:
                try:
                    # 10分ごとの生存確認
                    if int(time.time()) % 600 == 0:  # 10分 = 600秒
                        self.record_insight("システム稼働", "Obsidian脳みそシステム稼働中")
                    
                    # 1時間ごとの知識整理
                    if int(time.time()) % 3600 == 0:  # 1時間 = 3600秒
                        self.auto_knowledge_consolidation()
                    
                    time.sleep(60)  # 1分間隔でチェック
                    
                except Exception as e:
                    print(f"⚠️ 脳みそ監視エラー: {e}")
                    time.sleep(60)
        
        # バックグラウンドで監視開始
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()

    def auto_knowledge_consolidation(self):
        """自動知識整理"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        consolidation = f"""
## 📚 {timestamp} - 自動知識整理

**この1時間の活動サマリー:**
- ファイル変更監視実行
- Git状態確認
- システム稼働状況記録

**次の1時間で意識すべきこと:**
- Simple First原則の継続適用
- 記録の継続（この記録も含む）
- 過去の失敗パターン回避

---
"""
        
        self.write_to_obsidian(self.daily_record, consolidation)

def main():
    """メイン実行 - Claude起動時に必ず実行"""
    brain = ObsidianBrainSystem()
    
    print("🧠 Obsidian脳みそシステム開始")
    print(f"📝 今日の記録: {brain.daily_record}")
    print(f"📚 知識インデックス: {brain.knowledge_index}")
    
    # 強制的知識レビュー実行
    brain.force_knowledge_review()
    
    # 継続監視開始
    brain.start_continuous_brain_monitoring()
    
    print("✅ 脳みそシステム完全起動")
    print("🎯 Obsidianで今日の記録を確認してください")
    
    return brain

if __name__ == "__main__":
    brain_system = main()
    
    try:
        print("📝 脳みそシステム稼働中... (Ctrl+C で停止)")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 脳みそシステム停止")
        brain_system.record_insight("システム停止", "Obsidian脳みそシステム手動停止")