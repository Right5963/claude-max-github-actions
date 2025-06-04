#!/usr/bin/env python3
"""
MCP Auto Manager - 効率化特化MCPツール自動管理システム
=====================================================
TAL思考による開発効率化の革命的自動化
"""

import subprocess
import json
import requests
import re
import os
from datetime import datetime
from pathlib import Path

class MCPAutoManager:
    def __init__(self):
        self.repo_path = "/mnt/c/Claude Code/tool"
        self.mcp_registry = {}
        self.efficiency_categories = {
            "code_analysis": ["code", "ast", "lint", "format", "analyze"],
            "file_operations": ["file", "directory", "search", "edit"],
            "ai_integration": ["ai", "llm", "openai", "anthropic", "completion"],
            "database": ["database", "sql", "sqlite", "postgres", "mongo"],
            "web_automation": ["web", "browser", "scrape", "automation"],
            "documentation": ["docs", "readme", "markdown", "wiki"],
            "testing": ["test", "mock", "assert", "coverage"],
            "monitoring": ["monitor", "log", "metrics", "health"],
            "security": ["security", "auth", "encrypt", "secret"],
            "productivity": ["todo", "calendar", "note", "time"]
        }
        
    def discover_mcp_ecosystem(self):
        """SITUATION_AWARENESS: MCPエコシステムの自動発見"""
        print("🔍 MCP Ecosystem Discovery")
        print("=" * 40)
        
        discovered_tools = {}
        
        # GitHub/npm検索による最新MCPツール発見
        search_terms = [
            "mcp-server", "model-context-protocol", 
            "@modelcontextprotocol", "claude-mcp",
            "mcp-", "model-context"
        ]
        
        for term in search_terms:
            try:
                # npm search API (制限付きだが基本情報取得可能)
                npm_results = self._search_npm_packages(term)
                discovered_tools.update(npm_results)
                
                # GitHub API search（レート制限あり）
                github_results = self._search_github_repos(term)
                discovered_tools.update(github_results)
                
            except Exception as e:
                print(f"⚠️ Search error for {term}: {str(e)[:50]}...")
        
        # 効率化特化ツールの分類
        categorized = self._categorize_efficiency_tools(discovered_tools)
        
        print(f"✅ 発見ツール数: {len(discovered_tools)}")
        for category, tools in categorized.items():
            if tools:
                print(f"  📁 {category}: {len(tools)}個")
        
        return categorized
    
    def _search_npm_packages(self, term):
        """npm パッケージ検索（公開API使用）"""
        try:
            url = f"https://registry.npmjs.org/-/v1/search?text={term}&size=20"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                packages = {}
                
                for obj in data.get("objects", []):
                    package = obj.get("package", {})
                    name = package.get("name", "")
                    description = package.get("description", "")
                    
                    if self._is_mcp_relevant(name, description):
                        packages[name] = {
                            "source": "npm",
                            "description": description,
                            "version": package.get("version", ""),
                            "install_cmd": f"npx -y {name}",
                            "keywords": package.get("keywords", [])
                        }
                
                return packages
                
        except Exception as e:
            print(f"⚠️ npm search failed: {e}")
            return {}
    
    def _search_github_repos(self, term):
        """GitHub リポジトリ検索（制限付き）"""
        try:
            # GitHub search APIは認証が必要だが、限定的に使用
            url = f"https://api.github.com/search/repositories?q={term}+mcp&sort=updated&per_page=10"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                repos = {}
                
                for repo in data.get("items", []):
                    name = repo.get("name", "")
                    description = repo.get("description", "")
                    
                    if self._is_mcp_relevant(name, description):
                        repos[name] = {
                            "source": "github",
                            "description": description,
                            "url": repo.get("html_url", ""),
                            "stars": repo.get("stargazers_count", 0),
                            "updated": repo.get("updated_at", "")
                        }
                
                return repos
                
        except Exception as e:
            print(f"⚠️ GitHub search limited: {e}")
            return {}
    
    def _is_mcp_relevant(self, name, description):
        """MCPツールの関連性判定"""
        text = f"{name} {description}".lower()
        
        mcp_indicators = [
            "mcp", "model-context", "claude", "protocol",
            "server", "tool", "integration"
        ]
        
        return any(indicator in text for indicator in mcp_indicators)
    
    def _categorize_efficiency_tools(self, tools):
        """効率化特化ツールの分類"""
        categorized = {category: [] for category in self.efficiency_categories}
        
        for tool_name, tool_info in tools.items():
            text = f"{tool_name} {tool_info.get('description', '')}".lower()
            
            for category, keywords in self.efficiency_categories.items():
                if any(keyword in text for keyword in keywords):
                    categorized[category].append({
                        "name": tool_name,
                        "info": tool_info
                    })
                    break
            else:
                # 未分類のツールも保持
                if "other" not in categorized:
                    categorized["other"] = []
                categorized["other"].append({
                    "name": tool_name,
                    "info": tool_info
                })
        
        return categorized
    
    def analyze_efficiency_impact(self, categorized_tools):
        """DECISION_FRAMEWORK: 効率化インパクト分析"""
        print("\n🤔 EFFICIENCY IMPACT ANALYSIS")
        print("=" * 40)
        
        high_impact_tools = []
        current_gaps = []
        
        # 現在のMCP設定を取得
        current_mcps = self._get_current_mcps()
        
        # ギャップ分析
        for category, keywords in self.efficiency_categories.items():
            category_tools = categorized_tools.get(category, [])
            current_in_category = [mcp for mcp in current_mcps if any(kw in mcp.lower() for kw in keywords)]
            
            if not current_in_category and category_tools:
                current_gaps.append({
                    "category": category,
                    "missing_capability": keywords[0],
                    "available_tools": len(category_tools),
                    "priority": self._calculate_priority(category)
                })
        
        # 高インパクトツールの特定
        for category, tools in categorized_tools.items():
            for tool in tools:
                impact_score = self._calculate_impact_score(tool, category)
                if impact_score > 7:  # 8点以上を高インパクトとする
                    high_impact_tools.append({
                        "tool": tool,
                        "category": category,
                        "impact_score": impact_score
                    })
        
        # 結果表示
        print(f"📊 現在のMCPツール数: {len(current_mcps)}")
        print(f"🔍 発見された新ツール数: {sum(len(tools) for tools in categorized_tools.values())}")
        print(f"🎯 高インパクトツール数: {len(high_impact_tools)}")
        print(f"⚠️  機能ギャップ数: {len(current_gaps)}")
        
        return {
            "high_impact_tools": high_impact_tools,
            "current_gaps": current_gaps,
            "recommendation": self._generate_recommendations(high_impact_tools, current_gaps)
        }
    
    def _get_current_mcps(self):
        """現在のMCP設定を取得"""
        try:
            result = subprocess.run(
                ["claude", "mcp", "list"],
                capture_output=True, text=True, cwd=self.repo_path
            )
            return result.stdout.strip().split('\n') if result.stdout else []
        except:
            return []
    
    def _calculate_priority(self, category):
        """カテゴリの優先度計算"""
        priority_map = {
            "code_analysis": 9,
            "file_operations": 8,
            "ai_integration": 9,
            "productivity": 8,
            "testing": 7,
            "documentation": 6,
            "web_automation": 7,
            "database": 6,
            "monitoring": 5,
            "security": 8
        }
        return priority_map.get(category, 5)
    
    def _calculate_impact_score(self, tool, category):
        """ツールのインパクトスコア計算"""
        base_score = self._calculate_priority(category)
        
        # GitHubスター数による補正
        stars = tool["info"].get("stars", 0)
        if stars > 100:
            base_score += 1
        elif stars > 500:
            base_score += 2
        
        # 最新性による補正
        updated = tool["info"].get("updated", "")
        if "2024" in updated or "2025" in updated:
            base_score += 1
        
        return min(base_score, 10)  # 最大10点
    
    def _generate_recommendations(self, high_impact_tools, gaps):
        """推奨アクション生成"""
        recommendations = []
        
        # 高インパクトツールの優先インストール
        for tool_data in sorted(high_impact_tools, key=lambda x: x["impact_score"], reverse=True)[:5]:
            recommendations.append({
                "action": "install",
                "tool": tool_data["tool"]["name"],
                "reason": f"高インパクト({tool_data['impact_score']}/10) - {tool_data['category']}強化",
                "priority": "high"
            })
        
        # ギャップ解消の推奨
        for gap in sorted(gaps, key=lambda x: x["priority"], reverse=True)[:3]:
            recommendations.append({
                "action": "fill_gap",
                "category": gap["category"],
                "reason": f"機能ギャップ解消 - {gap['missing_capability']}機能",
                "priority": "medium"
            })
        
        return recommendations
    
    def auto_install_system(self, recommendations):
        """ACTION_GUIDANCE: 自動インストールシステム"""
        print("\n⚡ AUTO INSTALL SYSTEM")
        print("=" * 40)
        
        installed = []
        failed = []
        
        for rec in recommendations:
            if rec["action"] == "install":
                tool_name = rec["tool"]
                print(f"📦 Installing: {tool_name}")
                
                success = self._install_mcp_tool(tool_name)
                
                if success:
                    installed.append(tool_name)
                    print(f"✅ {tool_name} インストール完了")
                    
                    # Obsidianに記録
                    self._log_to_obsidian("install", tool_name, rec["reason"])
                else:
                    failed.append(tool_name)
                    print(f"❌ {tool_name} インストール失敗")
        
        # インストール結果の統計
        print(f"\n📊 インストール結果:")
        print(f"  ✅ 成功: {len(installed)}")
        print(f"  ❌ 失敗: {len(failed)}")
        
        return {
            "installed": installed,
            "failed": failed,
            "success_rate": len(installed) / (len(installed) + len(failed)) if (installed or failed) else 0
        }
    
    def _install_mcp_tool(self, tool_name):
        """MCPツールの自動インストール"""
        try:
            # まず npm パッケージとして試行
            result = subprocess.run([
                "claude", "mcp", "add", tool_name, "--",
                "npx", "-y", tool_name
            ], capture_output=True, text=True, cwd=self.repo_path, timeout=60)
            
            if result.returncode == 0:
                return True
            
            # uvx での試行
            result = subprocess.run([
                "claude", "mcp", "add", tool_name, "--",
                "uvx", tool_name
            ], capture_output=True, text=True, cwd=self.repo_path, timeout=60)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"⚠️ Install error: {e}")
            return False
    
    def _log_to_obsidian(self, action, tool_name, reason):
        """Obsidian活動記録"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        log_content = f"""
## MCP Auto Install - {timestamp}
- **Action**: {action}
- **Tool**: {tool_name}  
- **Reason**: {reason}

#mcp #automation #efficiency

---
"""
        
        try:
            # PowerShell経由でObsidian Daily Noteに追記
            ps_command = f"""
$dailyNote = "G:\\マイドライブ\\Obsidian Vault\\Daily Notes\\MCP_Auto_Installs.md"
$content = @'
{log_content.strip()}
'@
Add-Content -Path $dailyNote -Value $content -Encoding UTF8
"""
            
            subprocess.run([
                "powershell.exe", "-Command", ps_command
            ], capture_output=True, timeout=10)
            
        except Exception:
            # エラーでも継続
            pass
    
    def create_efficiency_dashboard(self):
        """効率化ダッシュボードの作成"""
        print("\n📊 EFFICIENCY DASHBOARD")
        print("=" * 40)
        
        current_mcps = self._get_current_mcps()
        
        dashboard_data = {
            "timestamp": datetime.now().isoformat(),
            "total_mcps": len(current_mcps),
            "categories": {},
            "recommendations": [],
            "next_check": datetime.now().strftime("%Y-%m-%d")
        }
        
        # カテゴリ別MCP分析
        for category, keywords in self.efficiency_categories.items():
            category_mcps = [mcp for mcp in current_mcps if any(kw in mcp.lower() for kw in keywords)]
            dashboard_data["categories"][category] = {
                "count": len(category_mcps),
                "tools": category_mcps,
                "coverage": "good" if len(category_mcps) > 0 else "missing"
            }
        
        # ダッシュボード保存
        with open("mcp_efficiency_dashboard.json", "w") as f:
            json.dump(dashboard_data, f, indent=2)
        
        print("✅ 効率化ダッシュボード作成完了")
        return dashboard_data

def main():
    """メイン実行: MCP自動管理システム"""
    import sys
    
    manager = MCPAutoManager()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "discover":
            # MCPエコシステム発見
            categorized = manager.discover_mcp_ecosystem()
            analysis = manager.analyze_efficiency_impact(categorized)
            
            print("\n🎯 RECOMMENDATIONS:")
            for rec in analysis["recommendation"][:5]:
                print(f"  • {rec['action']}: {rec.get('tool', rec.get('category'))} - {rec['reason']}")
                
        elif cmd == "auto-install":
            # 自動インストール実行
            categorized = manager.discover_mcp_ecosystem()
            analysis = manager.analyze_efficiency_impact(categorized)
            result = manager.auto_install_system(analysis["recommendation"])
            
            print(f"\n🎉 自動インストール完了: {result['success_rate']:.1%} 成功率")
            
        elif cmd == "dashboard":
            # 効率化ダッシュボード作成
            manager.create_efficiency_dashboard()
            
        else:
            print("使用方法:")
            print("  python3 mcp_auto_manager.py discover      # MCPエコシステム発見")
            print("  python3 mcp_auto_manager.py auto-install  # 推奨ツール自動インストール")
            print("  python3 mcp_auto_manager.py dashboard     # 効率化ダッシュボード作成")
    else:
        # デフォルト: 完全自動実行
        print("🚀 MCP Auto Manager - 完全自動実行")
        
        categorized = manager.discover_mcp_ecosystem()
        analysis = manager.analyze_efficiency_impact(categorized)
        result = manager.auto_install_system(analysis["recommendation"])
        dashboard = manager.create_efficiency_dashboard()
        
        print(f"\n🎊 自動処理完了!")
        print(f"  📦 新規インストール: {len(result['installed'])}個")
        print(f"  📊 総MCPツール数: {dashboard['total_mcps']}個")

if __name__ == "__main__":
    main()