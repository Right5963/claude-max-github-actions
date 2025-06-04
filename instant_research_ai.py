#!/usr/bin/env python3
"""
Instant Research AI - Perplexity MCP × Claude 瞬間リサーチシステム
================================================================
Simple First: 外部1コマンド、内部高機能
"""

import os
import sys
import json
import requests
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

class InstantResearchAI:
    """瞬間リサーチAI - Simple First設計"""
    
    def __init__(self):
        self.repo_path = "/mnt/c/Claude Code/tool"
        self.obsidian_vault = "G:\\マイドライブ\\Obsidian Vault"
        self.research_db = "research_history.db"
        self.api_key = os.getenv("PERPLEXITY_API_KEY", "")
        
        # SQLite初期化
        self._init_database()
    
    def _init_database(self):
        """研究履歴データベース初期化"""
        try:
            conn = sqlite3.connect(self.research_db)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS research_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    query TEXT NOT NULL,
                    type TEXT NOT NULL,
                    result_summary TEXT,
                    obsidian_path TEXT,
                    tags TEXT
                )
            """)
            
            # 使用量追跡テーブル追加
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usage_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    total_tokens INTEGER DEFAULT 0,
                    daily_requests INTEGER DEFAULT 0,
                    monthly_tokens INTEGER DEFAULT 0,
                    monthly_requests INTEGER DEFAULT 0,
                    UNIQUE(date)
                )
            """)
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ データベース初期化エラー: {e}")
    
    def perplexity_search(self, query, model="llama-3.1-sonar-large-128k-online"):
        """Perplexity APIで検索実行 (無料枠管理付き)"""
        if not self.api_key:
            print("❌ PERPLEXITY_API_KEY が設定されていません")
            print("設定方法: export PERPLEXITY_API_KEY=your_api_key")
            return None
        
        # 無料枠チェック
        if not self._check_free_tier_limits():
            return None
        
        print(f"🔍 Perplexity検索中: {query}")
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "あなたは日本語で回答する専門的なリサーチャーです。正確で構造化された情報を提供してください。"
                    },
                    {
                        "role": "user", 
                        "content": query
                    }
                ],
                "max_tokens": 4000,
                "temperature": 0.2,
                "top_p": 0.9,
                "search_domain_filter": ["perplexity.ai"],
                "return_images": False,
                "return_related_questions": True,
                "search_recency_filter": "month",
                "top_k": 0,
                "stream": False,
                "presence_penalty": 0,
                "frequency_penalty": 1
            }
            
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                if content:
                    usage = result.get("usage", {})
                    # 使用量記録
                    self._record_usage(usage)
                    print("✅ 検索完了")
                    return {
                        "content": content,
                        "usage": usage,
                        "model": model,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    print("❌ 空の結果")
                    return None
            else:
                print(f"❌ API エラー: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 検索エラー: {e}")
            return None
    
    def instant_search(self, query):
        """瞬間検索 - 最速回答"""
        print("⚡ 瞬間検索モード")
        
        result = self.perplexity_search(query, "llama-3.1-sonar-small-128k-online")
        
        if result:
            # 結果表示
            print(f"\n📊 検索結果:")
            print("=" * 60)
            print(result["content"])
            print("=" * 60)
            
            # 履歴保存
            self._save_to_history(query, "instant", result["content"])
            
            return result
        else:
            print("❌ 検索に失敗しました")
            return None
    
    def deep_research(self, topic):
        """深層リサーチ - 構造化された詳細分析"""
        print("🔬 深層リサーチモード")
        
        # 拡張プロンプト作成
        enhanced_query = f"""
        「{topic}」について、以下の観点で包括的にリサーチして、構造化された報告書を作成してください：

        ## 1. 基本概要
        - 定義と重要性
        - 現在の状況

        ## 2. 最新動向
        - 最近の発展
        - 注目すべき変化

        ## 3. 技術的詳細
        - 主要な技術要素
        - 実装方法

        ## 4. 市場・業界動向
        - 市場規模と成長
        - 主要プレイヤー

        ## 5. 将来展望
        - 予想される発展
        - 課題と機会

        各セクションは具体的で実用的な情報を含めてください。
        """
        
        result = self.perplexity_search(enhanced_query, "llama-3.1-sonar-large-128k-online")
        
        if result:
            # 結果表示
            print(f"\n📋 深層リサーチ結果: {topic}")
            print("=" * 80)
            print(result["content"])
            print("=" * 80)
            
            # Obsidianに保存
            obsidian_path = self._save_to_obsidian(topic, result["content"], "deep_research")
            
            # 履歴保存
            self._save_to_history(topic, "deep_research", result["content"], obsidian_path)
            
            return result
        else:
            print("❌ 深層リサーチに失敗しました")
            return None
    
    def research_session(self, theme):
        """包括的リサーチセッション - 5つの観点で並列調査"""
        print(f"🎯 包括的リサーチセッション: {theme}")
        
        perspectives = [
            f"{theme} の基本概念と定義",
            f"{theme} の最新技術動向",
            f"{theme} の市場分析と競合",
            f"{theme} の実用例と事例研究",
            f"{theme} の将来展望と課題"
        ]
        
        results = []
        
        for i, perspective in enumerate(perspectives, 1):
            print(f"\n📖 観点 {i}/5: {perspective}")
            
            result = self.perplexity_search(perspective)
            
            if result:
                results.append({
                    "perspective": perspective,
                    "content": result["content"],
                    "timestamp": result["timestamp"]
                })
                
                print(f"✅ 観点 {i} 完了")
            else:
                print(f"❌ 観点 {i} 失敗")
        
        if results:
            # 統合レポート作成
            integrated_report = self._create_integrated_report(theme, results)
            
            # Obsidianに保存
            obsidian_path = self._save_to_obsidian(theme, integrated_report, "research_session")
            
            # 履歴保存
            self._save_to_history(theme, "research_session", f"{len(results)}個の観点で調査完了", obsidian_path)
            
            print(f"\n🎉 包括的リサーチ完了: {len(results)}個の観点")
            print(f"📝 保存先: {obsidian_path}")
            
            return results
        else:
            print("❌ 包括的リサーチに失敗しました")
            return None
    
    def _create_integrated_report(self, theme, results):
        """統合レポート作成"""
        report = f"""# {theme} - 包括的リサーチレポート

*生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*情報源: Perplexity AI × Claude 瞬間リサーチシステム*

## 📊 調査概要
- **テーマ**: {theme}
- **調査観点**: {len(results)}個
- **調査日**: {datetime.now().strftime('%Y年%m月%d日')}

---

"""
        
        for i, result in enumerate(results, 1):
            report += f"""## 📖 観点{i}: {result['perspective']}

{result['content']}

---

"""
        
        report += f"""## 🎯 まとめ

このレポートは{len(results)}つの異なる観点から「{theme}」について包括的に調査した結果です。

### 🏷️ タグ
#{theme.replace(' ', '_')} #瞬間リサーチAI #包括的調査 #Perplexity_MCP

### 🔗 関連リンク
- [[Research History]]
- [[{theme} - Follow-up]]

*このレポートは Perplexity MCP × Claude 瞬間リサーチAI によって自動生成されました。*
"""
        
        return report
    
    def _save_to_obsidian(self, topic, content, research_type):
        """Obsidianに保存"""
        try:
            # ファイル名生成（安全な文字のみ）
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{safe_topic}_{research_type}_{timestamp}.md"
            
            # 保存パス
            research_dir = f"{self.obsidian_vault}\\Research\\AI_Generated"
            
            # PowerShellで保存（文字エンコーディング改善）
            # 特殊文字を安全にエスケープ
            safe_content = content.replace("'", "''").replace("`", "``")
            
            ps_command = f"""
$obsidianPath = "{research_dir}"
New-Item -ItemType Directory -Force -Path $obsidianPath | Out-Null
$content = @'
{safe_content}
'@
$filename = "{filename}"
[System.IO.File]::WriteAllText("$obsidianPath\\$filename", $content, [System.Text.Encoding]::UTF8)
Write-Host "Saved: $filename"
"""
            
            result = subprocess.run([
                "powershell.exe", "-Command", ps_command
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                obsidian_path = f"Research\\AI_Generated\\{filename}"
                print(f"📝 Obsidianに保存: {obsidian_path}")
                return obsidian_path
            else:
                print(f"⚠️ Obsidian保存エラー: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"⚠️ Obsidian保存エラー: {e}")
            return None
    
    def _save_to_history(self, query, research_type, result_summary, obsidian_path=None):
        """履歴データベースに保存"""
        try:
            conn = sqlite3.connect(self.research_db)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO research_history 
                (timestamp, query, type, result_summary, obsidian_path, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                query,
                research_type,
                result_summary[:500] + "..." if len(result_summary) > 500 else result_summary,
                obsidian_path,
                f"#{research_type} #AI_research"
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ 履歴保存エラー: {e}")
    
    def _check_free_tier_limits(self):
        """無料枠制限チェック"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            month = datetime.now().strftime('%Y-%m')
            
            conn = sqlite3.connect(self.research_db)
            cursor = conn.cursor()
            
            # 今日の使用量取得
            cursor.execute("""
                SELECT daily_requests, total_tokens FROM usage_tracking 
                WHERE date = ?
            """, (today,))
            
            today_usage = cursor.fetchone()
            daily_requests = today_usage[0] if today_usage else 0
            daily_tokens = today_usage[1] if today_usage else 0
            
            # 今月の使用量取得
            cursor.execute("""
                SELECT SUM(monthly_requests), SUM(monthly_tokens) FROM usage_tracking 
                WHERE date LIKE ?
            """, (f"{month}%",))
            
            month_usage = cursor.fetchone()
            monthly_requests = month_usage[0] if month_usage and month_usage[0] else 0
            monthly_tokens = month_usage[1] if month_usage and month_usage[1] else 0
            
            conn.close()
            
            # Perplexity Pro制限 ($5/月クレジット)
            DAILY_REQUEST_LIMIT = 100    # 1日100リクエスト (Pro想定)
            MONTHLY_TOKEN_LIMIT = 200000  # 月間200,000トークン ($5相当)
            MONTHLY_REQUEST_LIMIT = 2000  # 月間2000リクエスト
            
            # 制限チェック
            if daily_requests >= DAILY_REQUEST_LIMIT:
                print(f"❌ 1日のリクエスト制限に達しました ({daily_requests}/{DAILY_REQUEST_LIMIT})")
                print("明日まで待つか、有料プランにアップグレードしてください")
                return False
            
            if monthly_requests >= MONTHLY_REQUEST_LIMIT:
                print(f"❌ 月間リクエスト制限に達しました ({monthly_requests}/{MONTHLY_REQUEST_LIMIT})")
                print("来月まで待つか、有料プランにアップグレードしてください")
                return False
            
            if monthly_tokens >= MONTHLY_TOKEN_LIMIT:
                print(f"❌ 月間トークン制限に達しました ({monthly_tokens}/{MONTHLY_TOKEN_LIMIT})")
                print("来月まで待つか、有料プランにアップグレードしてください")
                return False
            
            # 警告表示
            if daily_requests >= DAILY_REQUEST_LIMIT * 0.8:
                print(f"⚠️ 1日制限の80%に達しました ({daily_requests}/{DAILY_REQUEST_LIMIT})")
            
            if monthly_requests >= MONTHLY_REQUEST_LIMIT * 0.8:
                print(f"⚠️ 月間リクエスト制限の80%に達しました ({monthly_requests}/{MONTHLY_REQUEST_LIMIT})")
            
            if monthly_tokens >= MONTHLY_TOKEN_LIMIT * 0.8:
                print(f"⚠️ 月間トークン制限の80%に達しました ({monthly_tokens}/{MONTHLY_TOKEN_LIMIT})")
            
            return True
            
        except Exception as e:
            print(f"⚠️ 制限チェックエラー: {e}")
            return True  # エラー時は実行を続行
    
    def _record_usage(self, usage):
        """使用量記録"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            total_tokens = usage.get('total_tokens', 0)
            
            conn = sqlite3.connect(self.research_db)
            cursor = conn.cursor()
            
            # 既存レコード確認
            cursor.execute("""
                SELECT daily_requests, total_tokens, monthly_requests, monthly_tokens 
                FROM usage_tracking WHERE date = ?
            """, (today,))
            
            existing = cursor.fetchone()
            
            if existing:
                # 更新
                cursor.execute("""
                    UPDATE usage_tracking 
                    SET daily_requests = daily_requests + 1,
                        total_tokens = total_tokens + ?,
                        monthly_requests = monthly_requests + 1,
                        monthly_tokens = monthly_tokens + ?
                    WHERE date = ?
                """, (total_tokens, total_tokens, today))
            else:
                # 新規作成
                cursor.execute("""
                    INSERT INTO usage_tracking 
                    (date, daily_requests, total_tokens, monthly_requests, monthly_tokens)
                    VALUES (?, 1, ?, 1, ?)
                """, (today, total_tokens, total_tokens))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ 使用量記録エラー: {e}")
    
    def show_usage_stats(self):
        """使用量統計表示"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            month = datetime.now().strftime('%Y-%m')
            
            conn = sqlite3.connect(self.research_db)
            cursor = conn.cursor()
            
            # 今日の使用量
            cursor.execute("""
                SELECT daily_requests, total_tokens FROM usage_tracking 
                WHERE date = ?
            """, (today,))
            
            today_usage = cursor.fetchone()
            daily_requests = today_usage[0] if today_usage else 0
            daily_tokens = today_usage[1] if today_usage else 0
            
            # 今月の使用量
            cursor.execute("""
                SELECT SUM(monthly_requests), SUM(monthly_tokens) FROM usage_tracking 
                WHERE date LIKE ?
            """, (f"{month}%",))
            
            month_usage = cursor.fetchone()
            monthly_requests = month_usage[0] if month_usage and month_usage[0] else 0
            monthly_tokens = month_usage[1] if month_usage and month_usage[1] else 0
            
            conn.close()
            
            # Perplexity Pro制限
            DAILY_REQUEST_LIMIT = 100
            MONTHLY_TOKEN_LIMIT = 200000
            MONTHLY_REQUEST_LIMIT = 2000
            
            print("📊 Perplexity API 使用量統計 (Pro プラン - $5/月)")
            print("=" * 50)
            print(f"📅 今日 ({today}):")
            print(f"   リクエスト: {daily_requests}/{DAILY_REQUEST_LIMIT} ({daily_requests/DAILY_REQUEST_LIMIT*100:.1f}%)")
            print(f"   トークン: {daily_tokens}")
            print()
            print(f"📆 今月 ({month}):")
            print(f"   リクエスト: {monthly_requests}/{MONTHLY_REQUEST_LIMIT} ({monthly_requests/MONTHLY_REQUEST_LIMIT*100:.1f}%)")
            print(f"   トークン: {monthly_tokens}/{MONTHLY_TOKEN_LIMIT} ({monthly_tokens/MONTHLY_TOKEN_LIMIT*100:.1f}%)")
            print()
            
            # 残り制限計算
            remaining_daily = DAILY_REQUEST_LIMIT - daily_requests
            remaining_monthly_req = MONTHLY_REQUEST_LIMIT - monthly_requests
            remaining_monthly_tok = MONTHLY_TOKEN_LIMIT - monthly_tokens
            
            print("🎯 残り制限:")
            print(f"   今日のリクエスト: {remaining_daily}回")
            print(f"   今月のリクエスト: {remaining_monthly_req}回")
            print(f"   今月のトークン: {remaining_monthly_tok}トークン")
            
            if remaining_daily <= 5:
                print("⚠️ 今日の制限に近づいています")
            if remaining_monthly_req <= 50:
                print("⚠️ 今月のリクエスト制限に近づいています")
            if remaining_monthly_tok <= 5000:
                print("⚠️ 今月のトークン制限に近づいています")
                
        except Exception as e:
            print(f"⚠️ 統計取得エラー: {e}")
    
    def show_history(self, limit=10):
        """履歴表示"""
        try:
            conn = sqlite3.connect(self.research_db)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT timestamp, query, type, obsidian_path 
                FROM research_history 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            results = cursor.fetchall()
            conn.close()
            
            if results:
                print(f"📚 最近のリサーチ履歴 (最新{len(results)}件)")
                print("=" * 60)
                
                for timestamp, query, research_type, obsidian_path in results:
                    dt = datetime.fromisoformat(timestamp)
                    print(f"🕒 {dt.strftime('%m/%d %H:%M')} [{research_type}] {query}")
                    if obsidian_path:
                        print(f"   📝 {obsidian_path}")
                    print()
            else:
                print("📚 履歴がありません")
                
        except Exception as e:
            print(f"⚠️ 履歴取得エラー: {e}")
    
    def test_connection(self):
        """API接続テスト"""
        print("🔧 Perplexity API 接続テスト")
        
        if not self.api_key:
            print("❌ PERPLEXITY_API_KEY が設定されていません")
            print("設定方法:")
            print("export PERPLEXITY_API_KEY=your_actual_api_key")
            return False
        
        test_result = self.perplexity_search("Hello, this is a connection test.", "llama-3.1-sonar-small-128k-online")
        
        if test_result:
            print("✅ 接続テスト成功")
            print(f"💰 使用トークン: {test_result.get('usage', {})}")
            return True
        else:
            print("❌ 接続テスト失敗")
            return False

def main():
    """Simple First: 瞬間リサーチAI - 1コマンド実行"""
    import sys
    
    ai = InstantResearchAI()
    
    print("⚡ Perplexity MCP × Claude 瞬間リサーチAI")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("🔧 使用方法:")
        print("  python3 instant_research_ai.py instant \"検索クエリ\"")
        print("  python3 instant_research_ai.py deep \"深層リサーチテーマ\"")
        print("  python3 instant_research_ai.py session \"包括的リサーチテーマ\"")
        print("  python3 instant_research_ai.py history")
        print("  python3 instant_research_ai.py usage")
        print("  python3 instant_research_ai.py test")
        print()
        print("🔑 API設定:")
        print("  export PERPLEXITY_API_KEY=your_actual_api_key")
        print()
        print("💡 Perplexity Pro制限:")
        print("  - 1日100リクエスト")
        print("  - 月間2,000リクエスト") 
        print("  - 月間200,000トークン ($5相当)")
        return
    
    command = sys.argv[1]
    
    if command == "test":
        ai.test_connection()
    elif command == "history":
        ai.show_history()
    elif command == "usage":
        ai.show_usage_stats()
    elif command == "instant" and len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        ai.instant_search(query)
    elif command == "deep" and len(sys.argv) > 2:
        topic = " ".join(sys.argv[2:])
        ai.deep_research(topic)
    elif command == "session" and len(sys.argv) > 2:
        theme = " ".join(sys.argv[2:])
        ai.research_session(theme)
    else:
        print("❌ 無効なコマンドまたは引数不足")
        print("ヘルプ: python3 instant_research_ai.py")

if __name__ == "__main__":
    main()