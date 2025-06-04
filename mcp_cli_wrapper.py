#!/usr/bin/env python3
"""
MCP CLI Wrapper - Claude Code CLI環境でMCPツールを簡単利用
========================================================
JSON入力なしで MCP 機能を直接利用可能
"""

import json
import subprocess
import sys
import os

class MCPCLIWrapper:
    def __init__(self):
        self.repo_path = "/mnt/c/Claude Code/tool"
        self.mcp_servers = {
            "dev": "/mnt/c/Claude Code/tool/mcp_dev_efficiency.py"
        }
    
    def call_mcp_tool(self, server, tool_name, **args):
        """MCP ツールの呼び出し"""
        request = {
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": args
            }
        }
        
        if server not in self.mcp_servers:
            return {"error": f"Unknown server: {server}"}
        
        server_path = self.mcp_servers[server]
        
        try:
            # JSON 入力で MCP サーバーを呼び出し
            result = subprocess.run([
                "python3", server_path
            ], input=json.dumps(request), text=True, 
              capture_output=True, cwd=self.repo_path)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"error": f"MCP call failed: {result.stderr}"}
                
        except Exception as e:
            return {"error": f"Execution failed: {str(e)}"}
    
    def dev_quick_commit(self, message=None):
        """開発用クイックコミット"""
        result = self.call_mcp_tool("dev", "dev_quick_commit", message=message)
        return self._format_response(result)
    
    def dev_file_context(self, file_path):
        """ファイル開発コンテキスト分析"""
        result = self.call_mcp_tool("dev", "dev_file_context", file_path=file_path)
        return self._format_response(result)
    
    def dev_pattern_detect(self, days=7):
        """開発パターン検出"""
        result = self.call_mcp_tool("dev", "dev_pattern_detect", days=days)
        return self._format_response(result)
    
    def dev_auto_optimize(self, focus="efficiency"):
        """開発ワークフロー最適化"""
        result = self.call_mcp_tool("dev", "dev_auto_optimize", focus=focus)
        return self._format_response(result)
    
    def dev_knowledge_sync(self, sync_type="session"):
        """開発知識同期"""
        result = self.call_mcp_tool("dev", "dev_knowledge_sync", type=sync_type)
        return self._format_response(result)
    
    def _format_response(self, result):
        """レスポンスの整形"""
        if "error" in result:
            return f"❌ Error: {result['error']}"
        
        if "content" in result and result["content"]:
            return result["content"][0].get("text", str(result))
        
        return str(result)

def main():
    """メイン実行: シンプルなCLIインターフェース"""
    wrapper = MCPCLIWrapper()
    
    if len(sys.argv) < 2:
        print("🤖 MCP CLI Wrapper - Claude Code CLI 用")
        print("使用方法:")
        print("  python3 mcp_cli_wrapper.py quick [message]     # クイックコミット")
        print("  python3 mcp_cli_wrapper.py context <file>      # ファイルコンテキスト")
        print("  python3 mcp_cli_wrapper.py patterns [days]     # パターン検出")
        print("  python3 mcp_cli_wrapper.py optimize [focus]    # ワークフロー最適化")
        print("  python3 mcp_cli_wrapper.py sync [type]         # 知識同期")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "quick":
        message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
        result = wrapper.dev_quick_commit(message)
        print(result)
        
    elif cmd == "context":
        if len(sys.argv) < 3:
            print("❌ ファイルパスが必要です")
            return
        file_path = sys.argv[2]
        result = wrapper.dev_file_context(file_path)
        print(result)
        
    elif cmd == "patterns":
        days = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 7
        result = wrapper.dev_pattern_detect(days)
        print(result)
        
    elif cmd == "optimize":
        focus = sys.argv[2] if len(sys.argv) > 2 else "efficiency"
        result = wrapper.dev_auto_optimize(focus)
        print(result)
        
    elif cmd == "sync":
        sync_type = sys.argv[2] if len(sys.argv) > 2 else "session"
        result = wrapper.dev_knowledge_sync(sync_type)
        print(result)
        
    else:
        print(f"❌ 不明なコマンド: {cmd}")

if __name__ == "__main__":
    main()