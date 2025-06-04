#!/usr/bin/env python3
"""
Perplexity MCP Server - True MCP Protocol Implementation
========================================================
Claude Code でネイティブにMCPとして認識される形の実装
"""

import asyncio
import json
import sys
import os
from typing import Any, Dict, List
from instant_research_ai import InstantResearchAI

class PerplexityMCPServer:
    """Perplexity MCP Server - MCPプロトコル準拠"""
    
    def __init__(self):
        self.research_ai = InstantResearchAI()
        self.capabilities = {
            "tools": [
                {
                    "name": "perplexity_instant_search",
                    "description": "瞬間検索 - 最速回答",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "検索クエリ"}
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "perplexity_deep_research", 
                    "description": "深層リサーチ - 構造化された詳細分析",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "topic": {"type": "string", "description": "リサーチテーマ"}
                        },
                        "required": ["topic"]
                    }
                },
                {
                    "name": "perplexity_research_session",
                    "description": "包括的リサーチセッション - 5つの観点で並列調査", 
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "theme": {"type": "string", "description": "包括的テーマ"}
                        },
                        "required": ["theme"]
                    }
                },
                {
                    "name": "perplexity_usage_stats",
                    "description": "使用量統計表示",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            ]
        }
    
    async def handle_initialize(self) -> Dict[str, Any]:
        """MCP初期化"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": self.capabilities,
            "serverInfo": {
                "name": "perplexity-research",
                "version": "1.0.0"
            }
        }
    
    async def handle_call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """MCPツール呼び出し処理"""
        try:
            if name == "perplexity_instant_search":
                result = self.research_ai.instant_search(arguments["query"])
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"🔍 瞬間検索結果:\n\n{result['content'] if result else '検索に失敗しました'}"
                        }
                    ]
                }
            
            elif name == "perplexity_deep_research":
                result = self.research_ai.deep_research(arguments["topic"])
                return {
                    "content": [
                        {
                            "type": "text", 
                            "text": f"🔬 深層リサーチ結果:\n\n{result['content'] if result else 'リサーチに失敗しました'}"
                        }
                    ]
                }
            
            elif name == "perplexity_research_session":
                results = self.research_ai.research_session(arguments["theme"])
                summary = f"📊 包括的リサーチ完了: {len(results) if results else 0}個の観点で調査"
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": summary
                        }
                    ]
                }
            
            elif name == "perplexity_usage_stats":
                # 使用量統計を文字列として取得
                import io
                import contextlib
                
                f = io.StringIO()
                with contextlib.redirect_stdout(f):
                    self.research_ai.show_usage_stats()
                stats_output = f.getvalue()
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": stats_output
                        }
                    ]
                }
            
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"❌ 未知のツール: {name}"
                        }
                    ],
                    "isError": True
                }
                
        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text", 
                        "text": f"❌ エラー: {str(e)}"
                    }
                ],
                "isError": True
            }
    
    async def handle_list_tools(self) -> Dict[str, Any]:
        """利用可能ツール一覧"""
        return {"tools": self.capabilities["tools"]}
    
    async def run_server(self):
        """MCPサーバー実行"""
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                request = json.loads(line.strip())
                
                if request["method"] == "initialize":
                    response = await self.handle_initialize()
                elif request["method"] == "tools/list":
                    response = await self.handle_list_tools()
                elif request["method"] == "tools/call":
                    response = await self.handle_call_tool(
                        request["params"]["name"],
                        request["params"].get("arguments", {})
                    )
                else:
                    response = {"error": f"Unknown method: {request['method']}"}
                
                # MCPプロトコル準拠のレスポンス
                mcp_response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": response
                }
                
                print(json.dumps(mcp_response))
                sys.stdout.flush()
                
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id") if 'request' in locals() else None,
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()

async def main():
    """MCPサーバー起動"""
    if len(sys.argv) > 1 and sys.argv[1] == "mcp-server":
        # MCPサーバーモード
        server = PerplexityMCPServer()
        await server.run_server()
    else:
        # 通常モード（既存の動作）
        print("Perplexity MCP Server")
        print("MCPサーバーとして起動: python3 perplexity_mcp_server.py mcp-server")

if __name__ == "__main__":
    asyncio.run(main())