#!/usr/bin/env python3
"""
Auto Research System - 自動リサーチ・発見システム
===============================================
Claude Code コマンド、MCP、効率化ツールの自動発見
"""

import subprocess
import requests
import json
import re
import os
from datetime import datetime
from pathlib import Path

class AutoResearchSystem:
    def __init__(self):
        self.repo_path = "/mnt/c/Claude Code/tool"
        self.research_db = "auto_research_discoveries.json"
        
    def research_claude_code_commands(self):
        """Claude Code コマンドの自動発見"""
        print("🔍 Claude Code コマンド自動リサーチ開始")
        
        discoveries = []
        
        # Help コマンドからの発見
        try:
            result = subprocess.run(
                ["claude", "--help"],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                help_text = result.stdout
                
                # MCP関連コマンドの抽出
                mcp_commands = re.findall(r'claude mcp [a-zA-Z-]+', help_text)
                for cmd in mcp_commands:
                    discoveries.append({
                        "type": "claude_command",
                        "command": cmd,
                        "source": "claude --help",
                        "discovered_at": datetime.now().isoformat()
                    })
                
                print(f"  ✅ {len(mcp_commands)} MCP関連コマンド発見")
                
        except Exception as e:
            print(f"  ⚠️ Claude help 取得エラー: {e}")
        
        # MCP specific help
        try:
            result = subprocess.run(
                ["claude", "mcp", "--help"],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                mcp_help = result.stdout
                
                # 隠れたMCPコマンドの発見
                hidden_commands = re.findall(r'(add-from-[a-zA-Z-]+|sync-[a-zA-Z-]+|export-[a-zA-Z-]+)', mcp_help)
                for cmd in hidden_commands:
                    discoveries.append({
                        "type": "hidden_mcp_command",
                        "command": f"claude mcp {cmd}",
                        "source": "claude mcp --help",
                        "discovered_at": datetime.now().isoformat()
                    })
                
                print(f"  ✅ {len(hidden_commands)} 隠れたMCPコマンド発見")
                
        except Exception as e:
            print(f"  ⚠️ MCP help 取得エラー: {e}")
        
        return discoveries
    
    def research_claude_desktop_config(self):
        """Claude Desktop 設定の自動発見"""
        print("🔍 Claude Desktop設定自動リサーチ開始")
        
        discoveries = []
        config_paths = [
            os.path.expanduser("~/.config/claude/claude_desktop_config.json"),
            os.path.expanduser("~/AppData/Roaming/Claude/claude_desktop_config.json"),
            "/mnt/c/Users/*/AppData/Roaming/Claude/claude_desktop_config.json"
        ]
        
        for config_path in config_paths:
            try:
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                    
                    if "mcpServers" in config:
                        for server_name, server_config in config["mcpServers"].items():
                            discoveries.append({
                                "type": "claude_desktop_mcp",
                                "server_name": server_name,
                                "command": server_config.get("command", ""),
                                "args": server_config.get("args", []),
                                "source": config_path,
                                "discovered_at": datetime.now().isoformat()
                            })
                    
                    print(f"  ✅ {len(config.get('mcpServers', {}))} Claude Desktop MCPサーバー発見")
                    break
                    
            except Exception as e:
                print(f"  ⚠️ 設定ファイル読み込みエラー {config_path}: {e}")
        
        return discoveries
    
    def research_github_awesome_lists(self):
        """GitHub Awesome リストからの自動発見"""
        print("🔍 GitHub Awesome リスト自動リサーチ開始")
        
        discoveries = []
        awesome_repos = [
            "awesome-mcp",
            "awesome-claude",
            "awesome-claude-code",
            "awesome-ai-tools"
        ]
        
        for repo in awesome_repos:
            try:
                # GitHub search API
                url = f"https://api.github.com/search/repositories?q={repo}&sort=updated&per_page=5"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for item in data.get("items", []):
                        discoveries.append({
                            "type": "awesome_github_repo",
                            "name": item.get("name", ""),
                            "url": item.get("html_url", ""),
                            "description": item.get("description", ""),
                            "stars": item.get("stargazers_count", 0),
                            "source": f"GitHub search: {repo}",
                            "discovered_at": datetime.now().isoformat()
                        })
                
                print(f"  ✅ {repo} 関連リポジトリ発見")
                
            except Exception as e:
                print(f"  ⚠️ GitHub検索エラー {repo}: {e}")
        
        return discoveries
    
    def research_npm_mcp_packages(self):
        """NPM MCP パッケージの自動発見"""
        print("🔍 NPM MCP パッケージ自動リサーチ開始")
        
        discoveries = []
        search_terms = [
            "mcp-",
            "@mcp-",
            "claude-mcp",
            "model-context-protocol"
        ]
        
        for term in search_terms:
            try:
                url = f"https://registry.npmjs.org/-/v1/search?text={term}&size=10"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for obj in data.get("objects", []):
                        package = obj.get("package", {})
                        
                        discoveries.append({
                            "type": "npm_mcp_package",
                            "name": package.get("name", ""),
                            "version": package.get("version", ""),
                            "description": package.get("description", ""),
                            "keywords": package.get("keywords", []),
                            "install_cmd": f"npx -y {package.get('name', '')}",
                            "source": f"NPM search: {term}",
                            "discovered_at": datetime.now().isoformat()
                        })
                
                print(f"  ✅ {term} 関連NPMパッケージ発見")
                
            except Exception as e:
                print(f"  ⚠️ NPM検索エラー {term}: {e}")
        
        return discoveries
    
    def research_claude_docs(self):
        """Claude 公式ドキュメントの自動リサーチ"""
        print("🔍 Claude公式ドキュメント自動リサーチ開始")
        
        discoveries = []
        doc_urls = [
            "https://docs.anthropic.com/en/docs/claude-code",
            "https://docs.anthropic.com/en/docs/claude-code/cli-usage",
            "https://modelcontextprotocol.io/docs"
        ]
        
        for url in doc_urls:
            try:
                response = requests.get(url, timeout=15)
                
                if response.status_code == 200:
                    content = response.text
                    
                    # コマンドパターンの抽出
                    commands = re.findall(r'claude [a-zA-Z-]+ [a-zA-Z-]+', content)
                    for cmd in commands:
                        discoveries.append({
                            "type": "official_command",
                            "command": cmd,
                            "source": url,
                            "discovered_at": datetime.now().isoformat()
                        })
                    
                    # MCP関連情報の抽出
                    mcp_mentions = re.findall(r'(mcp-[a-zA-Z0-9-]+|@[a-zA-Z0-9-]+/mcp-[a-zA-Z0-9-]+)', content)
                    for mention in mcp_mentions:
                        discoveries.append({
                            "type": "official_mcp_tool",
                            "tool_name": mention,
                            "source": url,
                            "discovered_at": datetime.now().isoformat()
                        })
                
                print(f"  ✅ {url} から情報発見")
                
            except Exception as e:
                print(f"  ⚠️ ドキュメント取得エラー {url}: {e}")
        
        return discoveries
    
    def save_discoveries(self, all_discoveries):
        """発見した情報の保存"""
        try:
            # 既存の発見情報を読み込み
            existing_discoveries = []
            if os.path.exists(self.research_db):
                with open(self.research_db, 'r') as f:
                    existing_discoveries = json.load(f)
            
            # 新しい発見を追加
            combined_discoveries = existing_discoveries + all_discoveries
            
            # 重複除去（簡易版）
            unique_discoveries = []
            seen = set()
            
            for discovery in combined_discoveries:
                key = f"{discovery.get('type', '')}_{discovery.get('command', '')}_{discovery.get('name', '')}"
                if key not in seen:
                    seen.add(key)
                    unique_discoveries.append(discovery)
            
            # 保存
            with open(self.research_db, 'w') as f:
                json.dump(unique_discoveries, f, indent=2)
            
            print(f"📊 総発見数: {len(unique_discoveries)} (新規: {len(all_discoveries)})")
            
            return unique_discoveries
            
        except Exception as e:
            print(f"❌ 発見情報保存エラー: {e}")
            return all_discoveries
    
    def generate_research_report(self, discoveries):
        """リサーチレポートの生成"""
        report = f"""# 自動リサーチレポート - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📊 発見サマリー
- **総発見数**: {len(discoveries)}

"""
        
        # カテゴリ別集計
        categories = {}
        for discovery in discoveries:
            category = discovery.get('type', 'unknown')
            if category not in categories:
                categories[category] = []
            categories[category].append(discovery)
        
        for category, items in categories.items():
            report += f"### {category.replace('_', ' ').title()} ({len(items)}個)\n"
            
            for item in items[:5]:  # 最大5個まで表示
                if 'command' in item:
                    report += f"- `{item['command']}`\n"
                elif 'name' in item:
                    report += f"- **{item['name']}**: {item.get('description', '')}\n"
                else:
                    report += f"- {item.get('tool_name', 'Unknown')}\n"
            
            if len(items) > 5:
                report += f"- ... 他 {len(items) - 5} 個\n"
            
            report += "\n"
        
        # Obsidianに保存
        try:
            ps_command = f"""
$obsidianPath = "G:\\マイドライブ\\Obsidian Vault\\Research\\Auto_Research"
New-Item -ItemType Directory -Force -Path $obsidianPath | Out-Null
$content = @'
{report}
'@
$filename = "auto_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
$content | Out-File -FilePath "$obsidianPath\\$filename" -Encoding UTF8
"""
            
            subprocess.run([
                "powershell.exe", "-Command", ps_command
            ], capture_output=True, timeout=15)
            
            print("📝 リサーチレポートをObsidianに保存")
            
        except Exception as e:
            print(f"⚠️ Obsidian保存エラー: {e}")
        
        return report
    
    def full_auto_research(self):
        """完全自動リサーチ実行"""
        print("🚀 完全自動リサーチシステム開始")
        print("=" * 50)
        
        all_discoveries = []
        
        # 各リサーチモジュールを実行
        research_modules = [
            self.research_claude_code_commands,
            self.research_claude_desktop_config, 
            self.research_github_awesome_lists,
            self.research_npm_mcp_packages,
            self.research_claude_docs
        ]
        
        for module in research_modules:
            try:
                discoveries = module()
                all_discoveries.extend(discoveries)
            except Exception as e:
                print(f"⚠️ リサーチモジュールエラー: {e}")
        
        # 発見情報の保存
        unique_discoveries = self.save_discoveries(all_discoveries)
        
        # レポート生成
        report = self.generate_research_report(unique_discoveries)
        
        print("\n🎉 自動リサーチ完了！")
        print(f"📊 総発見数: {len(unique_discoveries)}")
        
        return unique_discoveries

def main():
    """メイン実行"""
    import sys
    
    researcher = AutoResearchSystem()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "claude-commands":
            researcher.research_claude_code_commands()
        elif cmd == "desktop-config":
            researcher.research_claude_desktop_config()
        elif cmd == "github":
            researcher.research_github_awesome_lists()
        elif cmd == "npm":
            researcher.research_npm_mcp_packages()
        elif cmd == "docs":
            researcher.research_claude_docs()
        else:
            print("使用方法:")
            print("  python3 auto_research_system.py              # 完全自動リサーチ")
            print("  python3 auto_research_system.py claude-commands  # Claudeコマンド発見")
            print("  python3 auto_research_system.py desktop-config   # Desktop設定発見")
            print("  python3 auto_research_system.py github           # GitHub発見")
            print("  python3 auto_research_system.py npm              # NPM発見")
            print("  python3 auto_research_system.py docs             # 公式ドキュメント発見")
    else:
        # デフォルト: 完全自動リサーチ
        researcher.full_auto_research()

if __name__ == "__main__":
    main()