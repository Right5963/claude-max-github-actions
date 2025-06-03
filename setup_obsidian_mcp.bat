@echo off
chcp 65001 > nul
color 0D

echo ================================================
echo   Obsidian MCP Server セットアップ
echo   Obsidianと直接統合する最強の方法！
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

:: Obsidian MCPサーバーのインストール
echo.
echo 🔧 Obsidian MCPサーバーをインストール中...
npm install -g @cedricchee/mcp-obsidian

:: Claude Desktop設定ファイルのパス
set CLAUDE_CONFIG=%APPDATA%\Claude\claude_desktop_config.json

:: 既存設定のバックアップ
if exist "%CLAUDE_CONFIG%" (
    echo.
    echo 📋 既存設定をバックアップ...
    copy "%CLAUDE_CONFIG%" "%CLAUDE_CONFIG%.backup_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%" >nul
)

:: Obsidian Vaultのパスを検出
echo.
echo 🔍 Obsidian Vaultを検索中...
set VAULT_PATH=

:: パターン1: Gドライブ
if exist "G:\マイドライブ\Obsidian Vault" (
    set VAULT_PATH=G:\マイドライブ\Obsidian Vault
    echo ✅ 発見: G:\マイドライブ\Obsidian Vault
    goto :found
)

:: パターン2: ユーザーのGoogle Drive
for /d %%U in (C:\Users\*) do (
    if exist "%%U\Google Drive\Obsidian Vault" (
        set VAULT_PATH=%%U\Google Drive\Obsidian Vault
        echo ✅ 発見: %%U\Google Drive\Obsidian Vault
        goto :found
    )
)

:: パターン3: Documents
for /d %%U in (C:\Users\*) do (
    if exist "%%U\Documents\Obsidian Vault" (
        set VAULT_PATH=%%U\Documents\Obsidian Vault
        echo ✅ 発見: %%U\Documents\Obsidian Vault
        goto :found
    )
)

:: 見つからない場合
echo ❌ Obsidian Vaultが見つかりません
set /p VAULT_PATH="Obsidian Vaultのフルパスを入力してください: "

:found
:: パスのバックスラッシュをエスケープ
set VAULT_PATH_ESCAPED=%VAULT_PATH:\=\\%

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
echo         "%VAULT_PATH_ESCAPED%"
echo       ]
echo     },
echo     "filesystem-obsidian": {
echo       "command": "npx",
echo       "args": [
echo         "-y", 
echo         "@modelcontextprotocol/server-filesystem",
echo         "%VAULT_PATH_ESCAPED%"
echo       ]
echo     }
echo   }
echo }
) > "%CLAUDE_CONFIG%"

echo.
echo ✨ セットアップ完了！
echo.
echo 📋 設定内容:
echo    Vault: %VAULT_PATH%
echo    設定ファイル: %CLAUDE_CONFIG%
echo.
echo 🚀 次のステップ:
echo.
echo 1. Claude Desktopを完全に終了
echo 2. Claude Desktopを再起動
echo 3. 以下のMCPツールが利用可能になります:
echo.
echo    📚 Obsidian専用ツール:
echo    - mcp_obsidian__search_notes - ノート検索
echo    - mcp_obsidian__read_note - ノート読み込み
echo    - mcp_obsidian__create_note - ノート作成
echo    - mcp_obsidian__update_note - ノート更新
echo    - mcp_obsidian__list_notes - ノート一覧
echo    - mcp_obsidian__get_tags - タグ取得
echo.
echo    📁 ファイルシステムツール:
echo    - mcp_filesystem-obsidian__list_directory
echo    - mcp_filesystem-obsidian__read_file
echo    - mcp_filesystem-obsidian__write_file
echo.
echo 💡 使用例:
echo    "TALについて検索して" → mcp_obsidian__search_notes
echo    "Projects/AI開発.mdを読んで" → mcp_obsidian__read_note
echo.
pause