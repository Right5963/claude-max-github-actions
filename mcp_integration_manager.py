#!/usr/bin/env python3
"""
MCP Integration Manager - 統合MCPシステム管理
============================================
全MCPツールの統合管理と効率化ダッシュボード
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path

class MCPIntegrationManager:
    def __init__(self):
        self.repo_path = "/mnt/c/Claude Code/tool"
        self.mcp_config_path = os.path.expanduser("~/.config/claude/claude_desktop_config.json")
        
    def setup_custom_mcp_server(self):
        """カスタム開発効率化MCPサーバーの設定"""
        print("🔧 Setting up custom MCP development efficiency server")
        
        # カスタムMCPサーバーの追加
        try:
            result = subprocess.run([
                "claude", "mcp", "add", "dev-efficiency", "--",
                "python3", f"{self.repo_path}/mcp_dev_efficiency.py"
            ], capture_output=True, text=True, cwd=self.repo_path)
            
            if result.returncode == 0:
                print("✅ Custom dev-efficiency MCP server added")
                return True
            else:
                print(f"⚠️ Custom MCP server setup failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Custom MCP server setup error: {e}")
            return False
    
    def install_essential_tools(self):
        """必須効率化ツールの自動インストール"""
        print("📦 Installing essential efficiency tools")
        
        essential_tools = [
            {
                "name": "mcp-commit-story",
                "command": "npx -y mcp-commit-story",
                "description": "Smart commit message generation"
            },
            {
                "name": "fastmcp",
                "command": "npx -y fastmcp",
                "description": "Fast MCP development framework"
            },
            {
                "name": "mcp-code-analyzer",
                "command": "npx -y @mcp-code/analyzer",
                "description": "Code analysis and optimization"
            }
        ]
        
        installed = []
        failed = []
        
        for tool in essential_tools:
            print(f"  📦 Installing {tool['name']}...")
            
            try:
                result = subprocess.run([
                    "claude", "mcp", "add", tool["name"], "--"
                ] + tool["command"].split(), 
                capture_output=True, text=True, cwd=self.repo_path, timeout=120)
                
                if result.returncode == 0:
                    installed.append(tool["name"])
                    print(f"    ✅ {tool['name']} installed")
                else:
                    failed.append(tool["name"])
                    print(f"    ❌ {tool['name']} failed: {result.stderr[:100]}...")
                    
            except subprocess.TimeoutExpired:
                failed.append(tool["name"])
                print(f"    ⏰ {tool['name']} installation timeout")
            except Exception as e:
                failed.append(tool["name"])
                print(f"    ❌ {tool['name']} error: {str(e)[:100]}...")
        
        print(f"\n📊 Installation Summary:")
        print(f"  ✅ Successful: {len(installed)}")
        print(f"  ❌ Failed: {len(failed)}")
        
        return {"installed": installed, "failed": failed}
    
    def create_efficiency_dashboard(self):
        """効率化ダッシュボードの作成"""
        print("📊 Creating MCP efficiency dashboard")
        
        # 現在のMCP設定取得
        current_mcps = self._get_current_mcp_list()
        
        # 効率化カテゴリ分析
        categories = {
            "Development": [],
            "File Operations": [],
            "AI Integration": [],
            "Automation": [],
            "Knowledge": [],
            "Other": []
        }
        
        for mcp in current_mcps:
            categorized = False
            
            if any(keyword in mcp.lower() for keyword in ["dev", "code", "commit", "git"]):
                categories["Development"].append(mcp)
                categorized = True
            elif any(keyword in mcp.lower() for keyword in ["file", "directory", "search"]):
                categories["File Operations"].append(mcp)
                categorized = True
            elif any(keyword in mcp.lower() for keyword in ["ai", "llm", "anthropic", "openai"]):
                categories["AI Integration"].append(mcp)
                categorized = True
            elif any(keyword in mcp.lower() for keyword in ["auto", "daemon", "schedule"]):
                categories["Automation"].append(mcp)
                categorized = True
            elif any(keyword in mcp.lower() for keyword in ["obsidian", "note", "memory", "knowledge"]):
                categories["Knowledge"].append(mcp)
                categorized = True
            
            if not categorized:
                categories["Other"].append(mcp)
        
        # ダッシュボードデータ作成
        dashboard = {
            "timestamp": datetime.now().isoformat(),
            "total_mcps": len(current_mcps),
            "categories": {
                category: {
                    "count": len(tools),
                    "tools": tools,
                    "coverage": "excellent" if len(tools) >= 3 else "good" if len(tools) >= 1 else "missing"
                }
                for category, tools in categories.items()
            },
            "efficiency_score": self._calculate_efficiency_score(categories),
            "recommendations": self._generate_dashboard_recommendations(categories)
        }
        
        # ダッシュボード保存
        with open("mcp_efficiency_dashboard.json", "w") as f:
            json.dump(dashboard, f, indent=2)
        
        # Obsidianレポート作成
        self._create_obsidian_dashboard_report(dashboard)
        
        print(f"✅ Dashboard created with efficiency score: {dashboard['efficiency_score']}/100")
        
        return dashboard
    
    def _get_current_mcp_list(self):
        """現在のMCPリスト取得"""
        try:
            result = subprocess.run(
                ["claude", "mcp", "list"],
                capture_output=True, text=True, cwd=self.repo_path
            )
            
            if result.returncode == 0:
                return [line.split(':')[0].strip() for line in result.stdout.strip().split('\n') if line.strip()]
            else:
                return []
        except:
            return []
    
    def _calculate_efficiency_score(self, categories):
        """効率化スコア計算"""
        weights = {
            "Development": 25,
            "File Operations": 20,
            "AI Integration": 20,
            "Automation": 15,
            "Knowledge": 15,
            "Other": 5
        }
        
        total_score = 0
        
        for category, weight in weights.items():
            tool_count = len(categories.get(category, []))
            
            if tool_count >= 3:
                category_score = 100
            elif tool_count >= 2:
                category_score = 80
            elif tool_count >= 1:
                category_score = 60
            else:
                category_score = 0
            
            total_score += (category_score * weight) / 100
        
        return round(total_score)
    
    def _generate_dashboard_recommendations(self, categories):
        """ダッシュボード推奨事項生成"""
        recommendations = []
        
        for category, tools in categories.items():
            if len(tools) == 0:
                recommendations.append({
                    "priority": "high",
                    "action": f"Add {category.lower()} MCP tools",
                    "reason": f"Missing essential {category.lower()} capabilities"
                })
            elif len(tools) == 1:
                recommendations.append({
                    "priority": "medium", 
                    "action": f"Expand {category.lower()} toolkit",
                    "reason": f"Limited {category.lower()} tool diversity"
                })
        
        # 高効率化のための特別推奨
        if len(categories.get("Development", [])) < 2:
            recommendations.append({
                "priority": "high",
                "action": "Install development-focused MCP tools",
                "reason": "Critical for daily development efficiency"
            })
        
        return recommendations
    
    def _create_obsidian_dashboard_report(self, dashboard):
        """Obsidianダッシュボードレポート作成"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        content = f"""# MCP Efficiency Dashboard - {timestamp}

## 📊 Overall Status
- **Total MCP Tools**: {dashboard['total_mcps']}
- **Efficiency Score**: {dashboard['efficiency_score']}/100

## 📁 Category Breakdown
"""
        
        for category, data in dashboard['categories'].items():
            coverage_emoji = {
                "excellent": "🟢",
                "good": "🟡", 
                "missing": "🔴"
            }.get(data['coverage'], "⚪")
            
            content += f"""
### {coverage_emoji} {category} ({data['count']} tools)
Coverage: {data['coverage'].title()}
{chr(10).join(f"- {tool}" for tool in data['tools']) if data['tools'] else "- No tools configured"}
"""
        
        if dashboard['recommendations']:
            content += f"""
## 🎯 Recommendations
{chr(10).join(f"- **{rec['priority'].title()}**: {rec['action']} - {rec['reason']}" for rec in dashboard['recommendations'])}
"""
        
        content += """
## 🚀 Next Steps
1. Install missing high-priority tools
2. Configure custom development efficiency server
3. Set up automated MCP monitoring

#mcp #dashboard #efficiency #development

---
*Auto-generated by MCP Integration Manager*
"""
        
        try:
            ps_command = f"""
$obsidianPath = "G:\\マイドライブ\\Obsidian Vault\\Development\\MCP_Dashboards"
New-Item -ItemType Directory -Force -Path $obsidianPath | Out-Null
$content = @'
{content}
'@
$filename = "mcp_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
$content | Out-File -FilePath "$obsidianPath\\$filename" -Encoding UTF8
"""
            
            subprocess.run([
                "powershell.exe", "-Command", ps_command
            ], capture_output=True, timeout=15)
            
            print("📝 Dashboard report saved to Obsidian")
            
        except Exception as e:
            print(f"⚠️ Obsidian report save failed: {e}")
    
    def complete_integration_setup(self):
        """完全統合セットアップ"""
        print("🚀 MCP Integration Manager - Complete Setup")
        print("=" * 50)
        
        # 1. カスタムMCPサーバー設定
        custom_server_success = self.setup_custom_mcp_server()
        
        # 2. 必須ツールインストール
        install_result = self.install_essential_tools()
        
        # 3. ダッシュボード作成
        dashboard = self.create_efficiency_dashboard()
        
        # 4. 統合結果レポート
        integration_report = {
            "timestamp": datetime.now().isoformat(),
            "custom_server": custom_server_success,
            "essential_tools": install_result,
            "dashboard": dashboard,
            "integration_success": custom_server_success and len(install_result["installed"]) > 0
        }
        
        # レポート保存
        with open("mcp_integration_report.json", "w") as f:
            json.dump(integration_report, f, indent=2)
        
        print("\n🎉 MCP Integration Setup Complete!")
        print(f"  🔧 Custom Server: {'✅' if custom_server_success else '❌'}")
        print(f"  📦 Essential Tools: {len(install_result['installed'])}/{len(install_result['installed']) + len(install_result['failed'])}")
        print(f"  📊 Efficiency Score: {dashboard['efficiency_score']}/100")
        print(f"  🎯 Overall Success: {'✅' if integration_report['integration_success'] else '❌'}")
        
        return integration_report

def main():
    """メイン実行"""
    import sys
    
    manager = MCPIntegrationManager()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "setup":
            # 完全統合セットアップ
            manager.complete_integration_setup()
            
        elif cmd == "dashboard":
            # ダッシュボードのみ作成
            manager.create_efficiency_dashboard()
            
        elif cmd == "custom-server":
            # カスタムサーバーのみ設定
            manager.setup_custom_mcp_server()
            
        elif cmd == "essential":
            # 必須ツールのみインストール
            manager.install_essential_tools()
            
        else:
            print("使用方法:")
            print("  python3 mcp_integration_manager.py setup         # 完全統合セットアップ")
            print("  python3 mcp_integration_manager.py dashboard     # ダッシュボード作成")
            print("  python3 mcp_integration_manager.py custom-server # カスタムサーバー設定")
            print("  python3 mcp_integration_manager.py essential     # 必須ツールインストール")
    else:
        # デフォルト: 完全セットアップ
        manager.complete_integration_setup()

if __name__ == "__main__":
    main()