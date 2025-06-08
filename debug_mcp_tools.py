#!/usr/bin/env python3
"""
MCPツールが利用できない原因を調査
"""

import subprocess
import json
import os

def main():
    print("=== MCP Tools Debug Investigation ===\n")
    
    # 1. 利用可能なツール一覧を取得
    print("1. Available Tools in Claude Code CLI:")
    try:
        # この方法ではツール一覧を取得できないため、手動でテスト
        available_tools = []
        
        # 既知の動作するツールをテスト
        test_tools = [
            "mcp__memory__read_graph",
            "mcp__filesystem__list_directory", 
            "mcp__obsidian__search_notes",
            "mcp__filesystem-gdrive__list_directory",
            "mcp__playwright__browser_navigate",
            "mcp__desktop-commander__take_screenshot"
        ]
        
        print("Testing known MCP tools:")
        for tool in test_tools:
            print(f"  - {tool}: Unknown (Cannot test directly)")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # 2. MCPサーバープロセス確認
    print("\n2. Running MCP Server Processes:")
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        mcp_lines = [line for line in result.stdout.split('\n') 
                    if any(keyword in line.lower() for keyword in 
                          ['mcp-server', 'obsidian-mcp', 'server-filesystem', 'server-memory'])]
        
        for line in mcp_lines:
            if line.strip():
                print(f"  ✓ {line.strip()}")
                
    except Exception as e:
        print(f"Error: {e}")
    
    # 3. MCP設定確認
    print("\n3. MCP Configuration:")
    try:
        result = subprocess.run(['claude', 'mcp', 'list'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if ':' in line:
                name, command = line.split(':', 1)
                print(f"  📋 {name.strip()}: {command.strip()}")
                
    except Exception as e:
        print(f"Error: {e}")
    
    # 4. Claude設定ファイル確認
    print("\n4. Claude Configuration Files:")
    
    # プロジェクト設定
    project_config = "/mnt/c/Claude Code/tool/.claude/settings.local.json"
    if os.path.exists(project_config):
        try:
            with open(project_config, 'r') as f:
                config = json.load(f)
            print(f"  📁 Project Config: {project_config}")
            print(f"     enableAllProjectMcpServers: {config.get('enableAllProjectMcpServers', 'not set')}")
        except Exception as e:
            print(f"  ❌ Error reading project config: {e}")
    
    # ユーザー設定
    user_config = "/home/user/.claude/settings.local.json"
    if os.path.exists(user_config):
        try:
            with open(user_config, 'r') as f:
                config = json.load(f)
            print(f"  🏠 User Config: {user_config}")
            print(f"     enableAllProjectMcpServers: {config.get('enableAllProjectMcpServers', 'not set')}")
        except Exception as e:
            print(f"  ❌ Error reading user config: {e}")
    
    # 5. 環境変数確認
    print("\n5. Environment Variables:")
    env_vars = ['CLAUDE_MCP_SERVERS', 'MCP_SERVER_PATH', 'NODE_PATH']
    for var in env_vars:
        value = os.environ.get(var, 'not set')
        print(f"  🔧 {var}: {value}")
    
    # 6. 推奨解決策
    print("\n6. Potential Solutions:")
    print("  💡 1. Check if MCPサーバーが正常に起動しているが、ツール名が違う可能性")
    print("  💡 2. Claude Code CLIとClaude Desktopの環境の違い")
    print("  💡 3. MCP Protocol version mismatch")
    print("  💡 4. パス・権限の問題")
    print("  💡 5. プロセス間通信の問題")

if __name__ == "__main__":
    main()