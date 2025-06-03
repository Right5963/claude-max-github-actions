@echo off
chcp 65001 > nul
echo 🔄 Obsidian Vault同期中...
python "/mnt/c/Claude Code/tool/sync_obsidian_from_gdrive.py"
pause
