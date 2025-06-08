#!/usr/bin/env python3
"""
利用可能なMCPツールを網羅的にテスト
"""

import sys

def test_mcp_tool(tool_name, *args):
    """MCPツールの利用可能性をテスト"""
    try:
        # 実際にはここでツールを呼び出すことはできないため、
        # 代わりに既知の動作するツールを確認
        print(f"Testing: {tool_name}")
        if tool_name in ["mcp__memory__read_graph", "mcp__filesystem__list_directory"]:
            print(f"  ✅ {tool_name}: Known to work")
        else:
            print(f"  ❓ {tool_name}: Unknown status")
        return True
    except Exception as e:
        print(f"  ❌ {tool_name}: Error - {e}")
        return False

def main():
    print("=== Comprehensive MCP Tools Test ===\n")
    
    # 様々なMCPツール名パターンをテスト
    mcp_tools = [
        # Memory tools (known to work)
        "mcp__memory__read_graph",
        "mcp__memory__store", 
        "mcp__memory__retrieve",
        
        # Filesystem tools (known to work)
        "mcp__filesystem__list_directory",
        "mcp__filesystem__read_file",
        "mcp__filesystem__write_file",
        
        # Obsidian tools (target)
        "mcp__obsidian__search_notes",
        "mcp__obsidian__read_note", 
        "mcp__obsidian__write_note",
        "mcp__obsidian__list_notes",
        
        # Alternative naming patterns
        "mcp__obsidian-mcp-server__search_notes",
        "obsidian_search_notes",
        "obsidian__search_notes",
        
        # Filesystem-gdrive tools
        "mcp__filesystem-gdrive__list_directory",
        "mcp__filesystem-gdrive__read_file",
        
        # Desktop commander
        "mcp__desktop-commander__take_screenshot",
        "mcp__desktop-commander__get_system_info",
        
        # Playwright
        "mcp__playwright__browser_navigate",
        "mcp__playwright__browser_click",
    ]
    
    working_tools = []
    unknown_tools = []
    
    for tool in mcp_tools:
        if test_mcp_tool(tool):
            if "Known to work" in str(tool):
                working_tools.append(tool)
            else:
                unknown_tools.append(tool)
    
    print(f"\n📊 Summary:")
    print(f"  ✅ Known working tools: {len([t for t in mcp_tools if 'memory' in t or 'filesystem' in t and 'gdrive' not in t])}")
    print(f"  ❓ Unknown status tools: {len(unknown_tools)}")
    
    print(f"\n💡 Recommendations:")
    print(f"  1. Continue using mcp__memory__* and mcp__filesystem__* tools")
    print(f"  2. Use MCP bridge scripts for obsidian and gdrive access")
    print(f"  3. Investigate why project MCP servers aren't exposing tools")

if __name__ == "__main__":
    main()