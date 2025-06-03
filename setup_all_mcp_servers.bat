@echo off
chcp 65001 > nul
color 0A

echo ================================================
echo   完全版 MCP サーバー セットアップ
echo   Claude Desktopの全MCPをClaude Codeで使用可能に！
echo ================================================
echo.

:: npm/nodeの確認
echo 📦 Node.jsの確認...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.jsがインストールされていません
    echo 📥 https://nodejs.org/ からインストールしてください
    pause
    exit /b 1
)
echo ✅ Node.js: OK

:: Python/uvの確認
echo 🐍 Python環境の確認...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Pythonがインストールされていません（一部MCPで必要）
)

:: Claude Desktop設定ファイルのパス
set CLAUDE_CONFIG=%APPDATA%\Claude\claude_desktop_config.json

:: 既存設定のバックアップ
if exist "%CLAUDE_CONFIG%" (
    echo.
    echo 📋 既存設定をバックアップ...
    copy "%CLAUDE_CONFIG%" "%CLAUDE_CONFIG%.backup_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%" >nul
)

:: 必要なMCPサーバーをインストール
echo.
echo 🔧 必要なMCPサーバーをインストール中...
echo.

echo 1️⃣ Obsidian MCP...
npm install -g @cedricchee/mcp-obsidian

echo 2️⃣ Filesystem MCP...
npm install -g @modelcontextprotocol/server-filesystem

echo 3️⃣ Memory MCP...
npm install -g @modelcontextprotocol/server-memory

echo 4️⃣ Desktop Commander（インストール不要 - npxで実行）
echo 5️⃣ Playwright（インストール不要 - npxで実行）

:: Obsidian Vaultパスの設定
set OBSIDIAN_PATH=G:\マイドライブ\Obsidian Vault
if not exist "%OBSIDIAN_PATH%" (
    echo ⚠️  Gドライブが見つからない場合、C:\Users\user\Documents\Obsidian Vaultを使用
    set OBSIDIAN_PATH=C:\Users\user\Documents\Obsidian Vault
)

:: パスのエスケープ
set OBSIDIAN_PATH_ESCAPED=%OBSIDIAN_PATH:\=\\%
set MCP_PATH_ESCAPED=C:\\Claude Code\\MCP
set TOOL_PATH_ESCAPED=C:\\Claude Code\\tool

:: MCP設定ファイルを作成
echo.
echo 📝 Claude Desktop設定を更新中...
(
echo {
echo   "mcpServers": {
echo     "obsidian": {
echo       "command": "npx",
echo       "args": [
echo         "-y",
echo         "@cedricchee/mcp-obsidian",
echo         "%OBSIDIAN_PATH_ESCAPED%"
echo       ]
echo     },
echo     "filesystem": {
echo       "command": "npx",
echo       "args": [
echo         "-y",
echo         "@modelcontextprotocol/server-filesystem",
echo         "%MCP_PATH_ESCAPED%"
echo       ]
echo     },
echo     "filesystem-tool": {
echo       "command": "npx",
echo       "args": [
echo         "-y",
echo         "@modelcontextprotocol/server-filesystem",
echo         "%TOOL_PATH_ESCAPED%"
echo       ]
echo     },
echo     "filesystem-obsidian": {
echo       "command": "npx",
echo       "args": [
echo         "-y",
echo         "@modelcontextprotocol/server-filesystem",
echo         "%OBSIDIAN_PATH_ESCAPED%"
echo       ]
echo     },
echo     "desktop-commander": {
echo       "command": "npx",
echo       "args": [
echo         "-y",
echo         "@wonderwhy-er/desktop-commander@latest"
echo       ]
echo     },
echo     "memory": {
echo       "command": "npx",
echo       "args": [
echo         "-y",
echo         "@modelcontextprotocol/server-memory"
echo       ]
echo     },
echo     "playwright": {
echo       "command": "npx",
echo       "args": [
echo         "-y",
echo         "@playwright/mcp@latest"
echo       ]
echo     }
echo   }
echo }
) > "%CLAUDE_CONFIG%"

echo.
echo ✨ セットアップ完了！
echo.
echo 📋 利用可能なMCPサーバー:
echo.
echo 🗂️ ファイル操作系:
echo    - mcp_filesystem__* - C:\Claude Code\MCP内のファイル操作
echo    - mcp_filesystem-tool__* - C:\Claude Code\tool内のファイル操作
echo    - mcp_filesystem-obsidian__* - Obsidian Vault内のファイル操作
echo.
echo 📝 Obsidian専用:
echo    - mcp_obsidian__search_notes - ノート検索
echo    - mcp_obsidian__read_note - ノート読み込み
echo    - mcp_obsidian__create_note - ノート作成
echo.
echo 🖥️ デスクトップ操作:
echo    - mcp_desktop-commander__* - スクリーンショット、アプリ操作など
echo.
echo 🧠 メモリ管理:
echo    - mcp_memory__* - セッション間での情報保持
echo.
echo 🌐 ブラウザ自動化:
echo    - mcp_playwright__* - Webページの自動操作
echo.
echo 🚀 次のステップ:
echo    1. Claude Desktopを完全に終了
echo    2. Claude Desktopを再起動
echo    3. MCPツールが使用可能に！
echo.
pause