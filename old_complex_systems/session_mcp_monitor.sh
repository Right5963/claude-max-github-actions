#!/bin/bash
while true; do
    sleep 300  # 5分待機
    SESSION_ID=$(cat "/mnt/c/Claude Code/tool/.current_session" 2>/dev/null)
    if [ -n "$SESSION_ID" ]; then
        echo "[$(date)] セッション監視: $SESSION_ID"
        /mnt/c/Claude\ Code/tool/mcp_bridge_extended.sh session_save_obsidian "$SESSION_ID"
    fi
done
