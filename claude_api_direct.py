#!/usr/bin/env python3
"""
Claude API Direct Integration for GitHub Actions
===============================================
GitHub Actions環境でClaude Code CLIの代替として使用
@akira_papa_IT方式での実装を可能にする
"""

import os
import sys
import json
import requests
from datetime import datetime
from instant_research_ai import InstantResearchAI

class ClaudeAPIGitHubActions:
    """GitHub Actions環境でのClaude Max統合"""
    
    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
        self.research_ai = InstantResearchAI()
        
        if not self.anthropic_api_key:
            print("⚠️ ANTHROPIC_API_KEY not found. Claude features disabled.")
        if not self.perplexity_api_key:
            print("⚠️ PERPLEXITY_API_KEY not found. Research features disabled.")
    
    def claude_research_analysis(self, research_data, query):
        """Claude APIでリサーチデータを分析"""
        if not self.anthropic_api_key:
            return {"error": "Claude API key not available"}
        
        try:
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": self.anthropic_api_key,
                "anthropic-version": "2023-06-01"
            }
            
            analysis_prompt = f"""
以下のPerplexity検索結果を分析し、構造化された洞察を提供してください：

**検索クエリ**: {query}

**検索結果**:
{research_data}

**分析内容**:
1. 主要なポイント（3-5個）
2. 技術的考察
3. 実用的な示唆
4. 今後のアクション提案

マークダウン形式で構造化して回答してください。
"""
            
            payload = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 2000,
                "messages": [
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ]
            }
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result["content"][0]["text"]
                
                return {
                    "analysis": analysis,
                    "usage": result.get("usage", {}),
                    "model": "claude-3-sonnet-20240229",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "error": f"Claude API error: {response.status_code}",
                    "details": response.text
                }
                
        except Exception as e:
            return {"error": f"Claude analysis failed: {str(e)}"}
    
    def integrated_research_workflow(self, query, research_type="instant"):
        """統合リサーチワークフロー: Perplexity + Claude分析"""
        print(f"🚀 統合リサーチ開始: {research_type} - {query}")
        
        # Phase 1: Perplexity検索
        if research_type == "instant":
            research_result = self.research_ai.instant_search(query)
        elif research_type == "deep":
            research_result = self.research_ai.deep_research(query)
        elif research_type == "session":
            research_result = self.research_ai.research_session(query)
        else:
            research_result = self.research_ai.instant_search(query)
        
        if not research_result:
            return {"error": "Perplexity research failed"}
        
        research_content = research_result.get("content", "")
        
        # Phase 2: Claude分析（API利用可能な場合）
        claude_analysis = None
        if self.anthropic_api_key:
            print("🧠 Claude分析実行中...")
            claude_result = self.claude_research_analysis(research_content, query)
            if "error" not in claude_result:
                claude_analysis = claude_result
        
        # Phase 3: 統合レポート生成
        integrated_report = self._create_integrated_report(
            query, research_type, research_result, claude_analysis
        )
        
        return {
            "query": query,
            "research_type": research_type,
            "perplexity_result": research_result,
            "claude_analysis": claude_analysis,
            "integrated_report": integrated_report,
            "timestamp": datetime.now().isoformat()
        }
    
    def _create_integrated_report(self, query, research_type, research_result, claude_analysis):
        """統合レポート作成"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""# 統合リサーチレポート: {query}

*生成日時: {timestamp}*
*生成システム: Perplexity MCP × Claude API (GitHub Actions)*

## 📊 検索情報
- **クエリ**: {query}
- **タイプ**: {research_type}
- **実行環境**: GitHub Actions Self-hosted Runner

---

## 🔍 Perplexity検索結果

{research_result.get('content', 'No content available')}

---
"""
        
        if claude_analysis and "analysis" in claude_analysis:
            report += f"""## 🧠 Claude分析・洞察

{claude_analysis['analysis']}

### 📊 使用量情報
- **Perplexity**: {research_result.get('usage', {})}
- **Claude**: {claude_analysis.get('usage', {})}

---
"""
        else:
            report += """## 🧠 Claude分析
Claude API利用不可 - Perplexity結果のみ

---
"""
        
        report += f"""## 🏷️ メタデータ
- **生成日時**: {timestamp}
- **研究タイプ**: {research_type}
- **GitHub Actions**: Self-hosted Runner
- **コスト最適化**: @akira_papa_IT方式

*このレポートはClaude Max + GitHub Actions統合システムによって自動生成されました。*
"""
        
        return report
    
    def save_to_github_actions_artifacts(self, data, filename):
        """GitHub Actions Artifactsに保存"""
        try:
            artifacts_dir = os.getenv("GITHUB_WORKSPACE", "./github_artifacts")
            os.makedirs(artifacts_dir, exist_ok=True)
            
            filepath = os.path.join(artifacts_dir, filename)
            
            if isinstance(data, dict):
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(data))
            
            print(f"📁 Artifacts保存: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"⚠️ Artifacts保存エラー: {e}")
            return None

def main():
    """GitHub Actions環境での実行エントリポイント"""
    print("🚀 Claude Max + GitHub Actions 統合システム")
    print("参考: @akira_papa_IT - Claude Code GitHub Actions on Self-hosted Runners")
    print("=" * 60)
    
    if len(sys.argv) < 3:
        print("使用方法:")
        print("  python3 claude_api_direct.py <research_type> <query>")
        print("  research_type: instant, deep, session")
        print("  query: 検索クエリ")
        return
    
    research_type = sys.argv[1]
    query = " ".join(sys.argv[2:])
    
    # GitHub Actions環境変数チェック
    is_github_actions = os.getenv("GITHUB_ACTIONS") == "true"
    if is_github_actions:
        print("🔧 GitHub Actions環境で実行中")
        print(f"📂 Workspace: {os.getenv('GITHUB_WORKSPACE', 'N/A')}")
        print(f"🏃‍♂️ Runner: {os.getenv('RUNNER_NAME', 'N/A')}")
    
    # 統合リサーチ実行
    integration = ClaudeAPIGitHubActions()
    result = integration.integrated_research_workflow(query, research_type)
    
    if "error" in result:
        print(f"❌ エラー: {result['error']}")
        sys.exit(1)
    
    # 結果出力
    print("\n" + "="*60)
    print("📊 統合リサーチ完了")
    print("="*60)
    print(result["integrated_report"])
    
    # GitHub Actions環境での保存
    if is_github_actions:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON結果保存
        json_filename = f"research_result_{timestamp}.json"
        integration.save_to_github_actions_artifacts(result, json_filename)
        
        # マークダウンレポート保存
        md_filename = f"research_report_{timestamp}.md"
        integration.save_to_github_actions_artifacts(
            result["integrated_report"], md_filename
        )
        
        # GitHub Actions Outputに設定
        print(f"::set-output name=report_file::{md_filename}")
        print(f"::set-output name=research_success::true")
    
    print("\n✅ 処理完了")

if __name__ == "__main__":
    main()