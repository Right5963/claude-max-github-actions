#!/bin/bash
# 拡張MCPブリッジスクリプト - 全MCPツール対応版

MCP_TOOL=$1
shift
MCP_ARGS="$@"

# 共通変数
TOOL_DIR="/mnt/c/Claude Code/tool"
MCP_DIR="/mnt/c/Claude Code/MCP"
MEMORY_DB="$TOOL_DIR/mcp_memory.db"
OBSIDIAN_VAULT="G:\\マイドライブ\\Obsidian Vault"

case "$MCP_TOOL" in
    # === Obsidian MCP ===
    "obsidian_search")
        powershell.exe -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Get-ChildItem '$OBSIDIAN_VAULT' -Recurse -Filter '*.md' | Select-String -Pattern '$MCP_ARGS' -Encoding UTF8 | Select-Object -First 10"
        ;;
    
    "obsidian_read")
        powershell.exe -Command "Get-Content '$OBSIDIAN_VAULT\\$MCP_ARGS' -Encoding UTF8"
        ;;
    
    "obsidian_write")
        FILE_PATH=$1
        shift
        CONTENT="$@"
        powershell.exe -Command "Set-Content -Path '$OBSIDIAN_VAULT\\$FILE_PATH' -Value '$CONTENT' -Encoding UTF8"
        ;;
    
    "obsidian_list")
        powershell.exe -Command "Get-ChildItem '$OBSIDIAN_VAULT' -Filter '*.md' -Recurse | Select-Object -Property Name, DirectoryName, LastWriteTime | ConvertTo-Json"
        ;;
    
    # === Filesystem MCP ===
    "filesystem_list")
        ls -la "$MCP_ARGS" 2>/dev/null || echo "Directory not found"
        ;;
    
    "filesystem_read")
        cat "$MCP_ARGS" 2>/dev/null || echo "File not found"
        ;;
    
    "filesystem_write")
        FILE_PATH=$1
        shift
        CONTENT="$@"
        echo "$CONTENT" > "$FILE_PATH"
        ;;
    
    # === Desktop Commander ===
    "desktop_screenshot")
        # スクリーンショット取得
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        OUTPUT_FILE="$TOOL_DIR/screenshot_$TIMESTAMP.png"
        powershell.exe -Command "
            Add-Type -AssemblyName System.Windows.Forms,System.Drawing
            \$bitmap = [System.Drawing.Bitmap]::new([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height)
            \$graphics = [System.Drawing.Graphics]::FromImage(\$bitmap)
            \$graphics.CopyFromScreen(0, 0, 0, 0, \$bitmap.Size)
            \$bitmap.Save('$(wslpath -w "$OUTPUT_FILE")')
            \$graphics.Dispose()
            \$bitmap.Dispose()
        "
        echo "Screenshot saved: $OUTPUT_FILE"
        ;;
    
    "desktop_windows")
        # ウィンドウ一覧
        powershell.exe -Command "Get-Process | Where-Object {$_.MainWindowTitle -ne ''} | Select-Object ProcessName, MainWindowTitle | ConvertTo-Json"
        ;;
    
    "desktop_sysinfo")
        # システム情報
        powershell.exe -Command "
            \$os = Get-CimInstance Win32_OperatingSystem
            \$cpu = Get-CimInstance Win32_Processor
            \$mem = Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum
            @{
                OS = \$os.Caption
                Version = \$os.Version
                CPU = \$cpu.Name
                Cores = \$cpu.NumberOfCores
                Memory = [math]::Round(\$mem.Sum / 1GB, 2)
            } | ConvertTo-Json
        "
        ;;
    
    # === Memory MCP ===
    "memory_init")
        # メモリDBの初期化
        powershell.exe -Command "sqlite3.exe '$(wslpath -w "$MEMORY_DB")' 'CREATE TABLE IF NOT EXISTS memory (key TEXT PRIMARY KEY, value TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP);'"
        echo "Memory database initialized"
        ;;
    
    "memory_store")
        KEY=$1
        shift
        VALUE="$@"
        powershell.exe -Command "sqlite3.exe '$(wslpath -w "$MEMORY_DB")' \"INSERT OR REPLACE INTO memory (key, value, updated_at) VALUES ('$KEY', '$VALUE', CURRENT_TIMESTAMP);\""
        echo "Stored: $KEY"
        ;;
    
    "memory_get")
        powershell.exe -Command "sqlite3.exe '$(wslpath -w "$MEMORY_DB")' \"SELECT value FROM memory WHERE key = '$MCP_ARGS';\""
        ;;
    
    "memory_list")
        powershell.exe -Command "sqlite3.exe '$(wslpath -w "$MEMORY_DB")' \"SELECT key, substr(value, 1, 50) || '...' as preview, updated_at FROM memory ORDER BY updated_at DESC;\""
        ;;
    
    "memory_delete")
        powershell.exe -Command "sqlite3.exe '$(wslpath -w "$MEMORY_DB")' \"DELETE FROM memory WHERE key = '$MCP_ARGS';\""
        echo "Deleted: $MCP_ARGS"
        ;;
    
    # === SQLite MCP ===
    "sqlite_query")
        DB_PATH="$MCP_DIR/data/knowledge.db"
        sqlite3 "$DB_PATH" "$MCP_ARGS"
        ;;
    
    "sqlite_tables")
        DB_PATH="$MCP_DIR/data/knowledge.db"
        sqlite3 "$DB_PATH" ".tables"
        ;;
    
    "sqlite_schema")
        DB_PATH="$MCP_DIR/data/knowledge.db"
        TABLE=$MCP_ARGS
        sqlite3 "$DB_PATH" ".schema $TABLE"
        ;;
    
    # === Playwright MCP (簡易版) ===
    "browser_open")
        # デフォルトブラウザで開く
        powershell.exe -Command "Start-Process '$MCP_ARGS'"
        echo "Opened: $MCP_ARGS"
        ;;
    
    "browser_screenshot")
        URL=$1
        OUTPUT="$TOOL_DIR/web_$(date +%Y%m%d_%H%M%S).png"
        # Edge/Chrome のヘッドレスモードを使用
        powershell.exe -Command "
            & 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe' --headless --screenshot='$(wslpath -w "$OUTPUT")' '$URL'
        " 2>/dev/null
        echo "Web screenshot saved: $OUTPUT"
        ;;
    
    # === セッション管理 MCP ===
    "session_monitor_start")
        echo "🔄 MCPブリッジセッション監視を開始"
        # セッション監視スクリプトを作成
        cat > "$TOOL_DIR/session_mcp_monitor.sh" << 'EOF'
#!/bin/bash
while true; do
    sleep 300  # 5分待機
    SESSION_ID=$(cat "/mnt/c/Claude Code/tool/.current_session" 2>/dev/null)
    if [ -n "$SESSION_ID" ]; then
        echo "[$(date)] セッション監視: $SESSION_ID"
        /mnt/c/Claude\ Code/tool/mcp_bridge_extended.sh session_save_obsidian "$SESSION_ID"
    fi
done
EOF
        chmod +x "$TOOL_DIR/session_mcp_monitor.sh"
        nohup "$TOOL_DIR/session_mcp_monitor.sh" > "$TOOL_DIR/session_mcp_monitor.log" 2>&1 &
        echo "PID: $!" > "$TOOL_DIR/.session_monitor_pid"
        echo "✅ セッション監視開始（PID: $!）"
        ;;
    
    "session_monitor_stop")
        if [ -f "$TOOL_DIR/.session_monitor_pid" ]; then
            PID=$(cat "$TOOL_DIR/.session_monitor_pid")
            kill $PID 2>/dev/null
            rm -f "$TOOL_DIR/.session_monitor_pid"
            echo "⏹️ セッション監視停止（PID: $PID）"
        else
            echo "⚠️ 監視プロセスが見つかりません"
        fi
        ;;
    
    "session_save_obsidian")
        SESSION_ID="$MCP_ARGS"
        SESSION_FILE="/mnt/c/Claude Code/tool/sessions/session_${SESSION_ID}.json"
        
        if [ -f "$SESSION_FILE" ]; then
            TIMESTAMP=$(date +%Y-%m-%d)
            OBSIDIAN_FILE="Sessions/Claude Session ${TIMESTAMP} - ${SESSION_ID}.md"
            
            # JSONからマークダウン作成
            SUMMARY=$(python3 -c "
import json
import sys
try:
    with open('$SESSION_FILE', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print('# セッション記録 - $TIMESTAMP')
    print()
    print('## 完了タスク')
    for task in data.get('completed_tasks', []):
        print(f'- ✅ {task}')
    print()
    print('## コンテキスト')
    print(f'- 最終更新: {data.get(\"last_updated\", \"N/A\")}')
    context = data.get('context', {})
    if context.get('working_dir'):
        print(f'- 作業ディレクトリ: {context[\"working_dir\"]}')
    if context.get('key_files'):
        print(f'- 主要ファイル: {context[\"key_files\"]}')
except Exception as e:
    print(f'エラー: {e}')
")
            
            # Obsidianに保存（直接PowerShell実行）
            ESCAPED_SUMMARY=$(echo "$SUMMARY" | sed 's/"/\\"/g')
            powershell.exe -Command "Set-Content -Path 'G:\\マイドライブ\\Obsidian Vault\\$OBSIDIAN_FILE' -Value \"$ESCAPED_SUMMARY\" -Encoding UTF8"
            echo "💾 セッション $SESSION_ID をObsidianに保存完了"
        else
            echo "⚠️ セッションファイルが見つかりません: $SESSION_FILE"
        fi
        ;;
    
    "session_status")
        if [ -f "$TOOL_DIR/.session_monitor_pid" ]; then
            PID=$(cat "$TOOL_DIR/.session_monitor_pid")
            if ps -p "$PID" > /dev/null 2>&1; then
                echo "✅ セッション監視実行中（PID: $PID）"
            else
                echo "❌ セッション監視プロセス停止済み"
                rm -f "$TOOL_DIR/.session_monitor_pid"
            fi
        else
            echo "❌ セッション監視未実行"
        fi
        ;;
    
    # === Git操作 ===
    "git_auto_commit")
        VAULT_PATH="/mnt/c/Users/user/Documents/Obsidian Vault"
        cd "$VAULT_PATH"
        
        # 変更ファイルの確認
        CHANGES=$(git status --porcelain)
        if [ -z "$CHANGES" ]; then
            echo "コミットする変更がありません"
            exit 0
        fi
        
        # 自動コミット
        git add -A
        COMMIT_MSG="Auto-backup: $(date '+%Y-%m-%d %H:%M:%S')"
        git commit -m "$COMMIT_MSG"
        
        # プッシュ（エラーがあっても継続）
        git push origin main 2>/dev/null || echo "プッシュに失敗しました（ネットワーク確認）"
        
        echo "✅ 自動バックアップ完了: $COMMIT_MSG"
        ;;
    
    "git_status")
        git -C "/mnt/c/Users/user/Documents/Obsidian Vault" status --short
        ;;
    
    "git_log")
        git -C "/mnt/c/Users/user/Documents/Obsidian Vault" log --oneline -10
        ;;
    
    "git_sync")
        VAULT_PATH="/mnt/c/Users/user/Documents/Obsidian Vault"
        cd "$VAULT_PATH"
        
        echo "📥 リモートから最新を取得中..."
        git pull origin main
        
        # ローカル変更があれば自動コミット
        CHANGES=$(git status --porcelain)
        if [ ! -z "$CHANGES" ]; then
            echo "📝 ローカル変更を自動コミット中..."
            git add -A
            git commit -m "Auto-sync: $(date '+%Y-%m-%d %H:%M:%S')"
        fi
        
        echo "📤 リモートにプッシュ中..."
        git push origin main
        
        echo "✅ 同期完了"
        ;;
    
    # === Ollama MCP ===
    "ollama_quick")
        PROMPT="$MCP_ARGS"
        # 軽量なLlama 3.2 3Bを使用
        powershell.exe -Command "ollama run llama3.2:3b '$PROMPT'" 2>/dev/null || echo "Ollama not available (updating or model not installed)"
        ;;
    
    "ollama_code")
        CODE_REQUEST="$MCP_ARGS"
        # CodeLlama 7B専用コード生成
        PROMPT="Generate code for the following request:\n\n$CODE_REQUEST"
        powershell.exe -Command "ollama run codellama:7b '$PROMPT'" 2>/dev/null || echo "CodeLlama not available"
        ;;
    
    "ollama_code_review")
        CODE="$MCP_ARGS"
        # CodeLlama 7Bでコードレビュー
        PROMPT="Review this code and suggest improvements:\n\n$CODE"
        powershell.exe -Command "ollama run codellama:7b '$PROMPT'" 2>/dev/null || echo "CodeLlama not available"
        ;;
    
    "ollama_code_explain")
        CODE="$MCP_ARGS"
        PROMPT="Please explain what this code does in simple terms:\n\n$CODE"
        powershell.exe -Command "ollama run codellama:7b '$PROMPT'" 2>/dev/null || echo "CodeLlama not available"
        ;;
    
    "ollama_summarize")
        TEXT="$MCP_ARGS"
        PROMPT="Please summarize the following text in 2-3 sentences:\n\n$TEXT"
        powershell.exe -Command "ollama run llama3.2:3b '$PROMPT'" 2>/dev/null || echo "Ollama not available"
        ;;
    
    "ollama_translate")
        TEXT="$MCP_ARGS"
        PROMPT="Please translate the following text to Japanese:\n\n$TEXT"
        powershell.exe -Command "ollama run llama3.2:3b '$PROMPT'" 2>/dev/null || echo "Ollama not available"
        ;;
    
    "claude_smart")
        TASK="$MCP_ARGS"
        # タスク複雑度判定（簡易版）
        if echo "$TASK" | grep -q -i -E "(complex|strategy|design|architecture|analysis)"; then
            echo "🎯 Complex task detected - Recommend Claude Max for optimal results"
            echo "Task: $TASK"
        elif echo "$TASK" | grep -q -i -E "(code|program|script|function)"; then
            echo "💻 Code task - Using CodeLlama..."
            powershell.exe -Command "ollama run codellama:7b '$TASK'" 2>/dev/null || echo "CodeLlama not available"
        else
            echo "⚡ Simple task - Using Ollama..."
            powershell.exe -Command "ollama run llama3.2:3b '$TASK'" 2>/dev/null || echo "Ollama not available"
        fi
        ;;
    
    "ollama_status")
        powershell.exe -Command "ollama list" 2>/dev/null || echo "Ollama not running"
        ;;
    
    # === Claude Code Action 無料代替システム ===
    "action_smart_edit")
        FILE_PATH=$1
        shift
        INSTRUCTION="$@"
        
        if [ ! -f "$FILE_PATH" ]; then
            echo "❌ File not found: $FILE_PATH"
            exit 1
        fi
        
        echo "🔧 Analyzing file for intelligent editing..."
        
        # プロジェクトコンテキスト取得
        PROJECT_DIR=$(dirname "$FILE_PATH")
        FILE_EXTENSION="${FILE_PATH##*.}"
        
        # ファイル内容読み込み
        CURRENT_CONTENT=$(cat "$FILE_PATH")
        
        # CodeLlamaまたはLlama3.2による編集
        if echo "$FILE_EXTENSION" | grep -q -E "(py|js|ts|sh|json|md|c|cpp|java)"; then
            echo "💻 Code file detected - Using CodeLlama..."
            EDIT_PROMPT="Project: $(basename $(pwd))
File: $FILE_PATH
Current content:
$CURRENT_CONTENT

Instruction: $INSTRUCTION

Please provide the complete edited file content:"
            
            EDITED_CONTENT=$(powershell.exe -Command "ollama run codellama:7b '$EDIT_PROMPT'" 2>/dev/null)
        else
            echo "📄 Text file detected - Using Llama3.2..."
            EDIT_PROMPT="File: $FILE_PATH
Current content:
$CURRENT_CONTENT

Edit instruction: $INSTRUCTION

Provide the complete edited file:"
            
            EDITED_CONTENT=$(powershell.exe -Command "ollama run llama3.2:3b '$EDIT_PROMPT'" 2>/dev/null)
        fi
        
        if [ $? -eq 0 ] && [ ! -z "$EDITED_CONTENT" ]; then
            # バックアップ作成
            BACKUP_FILE="${FILE_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
            cp "$FILE_PATH" "$BACKUP_FILE"
            echo "📦 Backup created: $BACKUP_FILE"
            
            # 編集内容を適用
            echo "$EDITED_CONTENT" > "$FILE_PATH"
            echo "✅ File edited successfully: $FILE_PATH"
            echo "📝 Instruction: $INSTRUCTION"
            
            # 差分表示
            echo "📊 Changes preview:"
            diff -u "$BACKUP_FILE" "$FILE_PATH" | head -20 || echo "Files differ significantly"
        else
            echo "❌ Edit failed - Ollama not available or error occurred"
        fi
        ;;
    
    "action_project_analyze")
        TARGET_DIR=${1:-$(pwd)}
        echo "🔍 Analyzing project structure..."
        
        # プロジェクト基本情報
        echo "📁 Project: $(basename $TARGET_DIR)"
        echo "📍 Path: $TARGET_DIR"
        
        # ファイル統計
        TOTAL_FILES=$(find "$TARGET_DIR" -type f | wc -l)
        CODE_FILES=$(find "$TARGET_DIR" -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.sh" | wc -l)
        echo "📈 Total files: $TOTAL_FILES (Code files: $CODE_FILES)"
        
        # 主要ファイル
        echo "🎯 Key files:"
        find "$TARGET_DIR" -maxdepth 2 -name "*.md" -o -name "package.json" -o -name "requirements.txt" -o -name "*.py" | head -10
        
        # Git情報
        if [ -d "$TARGET_DIR/.git" ]; then
            echo "📊 Git status:"
            git -C "$TARGET_DIR" status --short | head -5
        fi
        
        # プロジェクト分析をOllamaに依頼
        PROJECT_SUMMARY=$(find "$TARGET_DIR" -maxdepth 2 -type f -name "*.md" -o -name "*.txt" | head -3 | xargs cat 2>/dev/null)
        ANALYSIS_PROMPT="Analyze this project structure and provide insights:
Project: $(basename $TARGET_DIR)
Files: $TOTAL_FILES total, $CODE_FILES code files
Summary content: $PROJECT_SUMMARY

Provide a brief analysis of the project purpose and structure:"
        
        echo "🤖 AI Analysis:"
        powershell.exe -Command "ollama run llama3.2:3b '$ANALYSIS_PROMPT'" 2>/dev/null || echo "Ollama analysis not available"
        ;;
    
    # === Note API (スタブ) ===
    "note_test")
        echo "Note API connection test - This would connect to note.com API"
        ;;
    
    # === ヘルプ ===
    *)
        cat << EOF
拡張MCPブリッジ - 利用可能なコマンド:

【Obsidian】
  obsidian_search [検索語]     - ノート検索
  obsidian_read [パス]         - ノート読み込み
  obsidian_write [パス] [内容] - ノート作成/更新
  obsidian_list               - ノート一覧

【ファイルシステム】
  filesystem_list [パス]       - ディレクトリ一覧
  filesystem_read [パス]       - ファイル読み込み
  filesystem_write [パス] [内容] - ファイル書き込み

【デスクトップ操作】
  desktop_screenshot          - スクリーンショット取得
  desktop_windows            - ウィンドウ一覧
  desktop_sysinfo            - システム情報

【メモリ管理】
  memory_init                - DB初期化
  memory_store [key] [value] - データ保存
  memory_get [key]           - データ取得
  memory_list                - 一覧表示
  memory_delete [key]        - データ削除

【SQLite】
  sqlite_query [SQL]         - SQLクエリ実行
  sqlite_tables              - テーブル一覧
  sqlite_schema [table]      - スキーマ表示

【Git操作】
  git_auto_commit            - Obsidian自動バックアップ
  git_status                 - Gitステータス確認
  git_log                    - コミット履歴表示
  git_sync                   - 完全同期（pull + commit + push）

【Ollama（ローカルLLM）】
  ollama_quick [prompt]      - クイック質問応答
  ollama_code [request]      - CodeLlama専用コード生成
  ollama_code_review [code]  - CodeLlamaコードレビュー
  ollama_code_explain [code] - CodeLlamaコード解説
  ollama_summarize [text]    - テキスト要約
  ollama_translate [text]    - 日本語翻訳
  claude_smart [task]        - 最適AI自動選択
  ollama_status              - 利用可能モデル一覧

【Claude Code Action 無料代替】
  action_smart_edit [file] [instruction] - Claude Action風ファイル編集
  action_project_analyze [dir]           - プロジェクト構造分析

【ブラウザ】
  browser_open [URL]         - URLを開く
  browser_screenshot [URL]   - Webページのスクショ

【note.com API】
  note_search [query]        - note記事検索
  note_trending              - トレンド記事取得
  note_user [username]       - ユーザー情報取得

使用例:
  $0 obsidian_search "TAL"
  $0 git_auto_commit
  $0 ollama_quick "What is AI?"
  $0 action_smart_edit "test.py" "Add error handling"
  $0 action_project_analyze "/path/to/project"
  $0 memory_store "project_name" "AI Development"
  $0 desktop_screenshot
EOF
        exit 1
        ;;
        
    note_search)
        # note.com記事検索
        QUERY="${2:-AI}"
        echo "🔍 note.comで「${QUERY}」を検索中..."
        
        # note.com検索URLを開く
        URL="https://note.com/search?q=$(echo "$QUERY" | sed 's/ /+/g')"
        powershell.exe -Command "Start-Process '$URL'"
        echo "✅ ブラウザで検索結果を開きました"
        ;;
    
    note_trending)
        # note.comトレンド記事
        echo "📈 note.comのトレンド記事を取得中..."
        
        # トレンドページを開く
        powershell.exe -Command "Start-Process 'https://note.com/explore'"
        echo "✅ ブラウザでトレンドページを開きました"
        ;;
    
    note_user)
        # note.comユーザー情報
        USERNAME="${2:-}"
        if [ -z "$USERNAME" ]; then
            echo "エラー: ユーザー名を指定してください"
            exit 1
        fi
        
        echo "👤 ユーザー「${USERNAME}」の情報を取得中..."
        URL="https://note.com/${USERNAME}"
        powershell.exe -Command "Start-Process '$URL'"
        echo "✅ ブラウザでユーザーページを開きました"
        ;;
        
    *)
        echo "不明なコマンド: $MCP_TOOL"
        exit 1
        ;;
esac