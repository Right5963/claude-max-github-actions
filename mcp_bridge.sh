#!/bin/bash
# MCPツールブリッジスクリプト
# 標準ツールからMCPツールを呼び出すためのブリッジ

MCP_TOOL=$1
shift
MCP_ARGS="$@"

case "$MCP_TOOL" in
    "obsidian_search")
        # Obsidian検索をPowerShell経由で実行
        powershell.exe -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Get-ChildItem 'G:\\マイドライブ\\Obsidian Vault' -Recurse -Filter '*.md' | Select-String -Pattern '$MCP_ARGS' -Encoding UTF8 | Select-Object -First 10"
        ;;
    
    "obsidian_read")
        # ファイル読み込み
        powershell.exe -Command "Get-Content 'G:\\マイドライブ\\Obsidian Vault\\$MCP_ARGS' -Encoding UTF8"
        ;;
    
    "obsidian_write")
        # ファイル書き込み（引数: ファイルパス 内容）
        FILE_PATH=$1
        shift
        CONTENT="$@"
        powershell.exe -Command "Set-Content -Path 'G:\\マイドライブ\\Obsidian Vault\\$FILE_PATH' -Value '$CONTENT' -Encoding UTF8"
        ;;
    
    "filesystem_list")
        # ディレクトリ一覧
        ls -la "$MCP_ARGS"
        ;;
    
    *)
        echo "Unknown MCP tool: $MCP_TOOL"
        echo "Available tools: obsidian_search, obsidian_read, obsidian_write, filesystem_list"
        exit 1
        ;;
esac