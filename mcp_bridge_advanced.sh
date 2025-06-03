#!/bin/bash
# 高度なMCPブリッジスクリプト - 追加MCP機能

# 追加のMCPツール
MCP_TOOL=$1
shift
MCP_ARGS="$@"

# 共通変数
TOOL_DIR="/mnt/c/Claude Code/tool"
MCP_DIR="/mnt/c/Claude Code/MCP"

case "$MCP_TOOL" in
    # === Git MCP ===
    "git_status")
        git status
        ;;
    
    "git_log")
        git log --oneline -10
        ;;
    
    "git_diff")
        git diff
        ;;
    
    "git_branch")
        git branch -a
        ;;
    
    # === Web Search MCP ===
    "web_search")
        QUERY=$(echo "$MCP_ARGS" | sed 's/ /+/g')
        # DuckDuckGo APIを使用（プライバシー重視）
        curl -s "https://api.duckduckgo.com/?q=$QUERY&format=json&no_html=1" | python3 -m json.tool
        ;;
    
    "web_fetch")
        URL=$1
        # ウェブページの内容を取得
        curl -s "$URL" | python3 -c "
import sys
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
    
    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style']:
            self.skip = True
    
    def handle_endtag(self, tag):
        if tag in ['script', 'style']:
            self.skip = False
    
    def handle_data(self, data):
        if not self.skip:
            self.text.append(data.strip())

parser = TextExtractor()
parser.feed(sys.stdin.read())
print(' '.join(filter(None, parser.text))[:1000])
"
        ;;
    
    # === Financial Data MCP (簡易版) ===
    "finance_ticker")
        SYMBOL=$MCP_ARGS
        # Yahoo Finance の公開APIを使用（無料）
        # 注意: レート制限があるため頻繁な使用は避ける
        curl -s "https://query1.finance.yahoo.com/v8/finance/chart/$SYMBOL" | python3 -c "
import json, sys
data = json.load(sys.stdin)
try:
    result = data['chart']['result'][0]
    meta = result['meta']
    print(f\"Symbol: {meta['symbol']}\\nPrice: {meta['regularMarketPrice']}\\nCurrency: {meta['currency']}\")
except:
    print('Error fetching data')
"
        ;;
    
    # === Weather MCP ===
    "weather_current")
        LOCATION=$MCP_ARGS
        # OpenWeatherMap風の簡易実装（実際にはAPIキーが必要）
        echo "Weather for $LOCATION:"
        curl -s "https://wttr.in/$LOCATION?format=3"
        ;;
    
    # === E2B Code Sandbox (ローカル版) ===
    "sandbox_python")
        CODE=$MCP_ARGS
        # Pythonコードを安全に実行
        echo "$CODE" | python3 -c "
import sys
import subprocess
import tempfile

code = sys.stdin.read()
with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
    f.write(code)
    f.flush()
    
    # タイムアウト付きで実行
    try:
        result = subprocess.run(['python3', f.name], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        print(result.stdout)
        if result.stderr:
            print('STDERR:', result.stderr)
    except subprocess.TimeoutExpired:
        print('Code execution timed out')
"
        ;;
    
    # === Slack Integration (簡易版) ===
    "slack_webhook")
        MESSAGE=$1
        WEBHOOK_URL=$2
        if [ -n "$WEBHOOK_URL" ]; then
            curl -X POST -H 'Content-type: application/json' \
                --data "{\"text\":\"$MESSAGE\"}" \
                "$WEBHOOK_URL"
        else
            echo "Webhook URL required"
        fi
        ;;
    
    # === PDF処理 ===
    "pdf_extract")
        PDF_PATH=$1
        # pdftotext が利用可能な場合
        if command -v pdftotext &> /dev/null; then
            pdftotext "$PDF_PATH" -
        else
            echo "pdftotext not installed. Install with: sudo apt-get install poppler-utils"
        fi
        ;;
    
    # === CSV/データ分析 ===
    "data_analyze")
        CSV_PATH=$1
        # 簡易的なCSV分析
        python3 -c "
import csv
import sys

with open('$CSV_PATH', 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)
    print(f'Headers: {headers}')
    
    row_count = 1
    for row in reader:
        row_count += 1
    
    print(f'Total rows: {row_count}')
    print(f'Columns: {len(headers)}')
"
        ;;
    
    # === Email (Thunderbird経由) ===
    "email_compose")
        TO=$1
        SUBJECT=$2
        BODY=$3
        # Thunderbirdで新規メール作成
        powershell.exe -Command "Start-Process 'mailto:$TO?subject=$SUBJECT&body=$BODY'"
        ;;
    
    # === Calendar (簡易版) ===
    "calendar_today")
        cal
        echo ""
        echo "Today's events:"
        date +"%Y-%m-%d %A"
        ;;
    
    # === Voice/TTS (Windows SAPI) ===
    "voice_speak")
        TEXT=$MCP_ARGS
        powershell.exe -Command "
            Add-Type -AssemblyName System.Speech
            \$synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer
            \$synthesizer.Speak('$TEXT')
        "
        ;;
    
    # === ヘルプ ===
    "help_advanced")
        cat << EOF
高度なMCPブリッジ - 追加コマンド:

【Git操作】
  git_status              - Gitステータス
  git_log                 - コミット履歴
  git_diff                - 差分表示
  git_branch              - ブランチ一覧

【Web/API】
  web_search [query]      - Web検索
  web_fetch [URL]         - Webページ取得
  finance_ticker [symbol] - 株価取得
  weather_current [city]  - 天気情報

【コード実行】
  sandbox_python [code]   - Pythonコード実行

【データ処理】
  pdf_extract [path]      - PDF文字抽出
  data_analyze [csv]      - CSV分析

【コミュニケーション】
  slack_webhook [msg] [url] - Slack送信
  email_compose [to] [subj] [body] - メール作成
  voice_speak [text]      - 音声読み上げ

【その他】
  calendar_today          - カレンダー表示

使用例:
  $0 web_search "Claude AI MCP"
  $0 finance_ticker "AAPL"
  $0 sandbox_python "print('Hello, World!')"
EOF
        ;;
    
    *)
        # 元のスクリプトにフォールバック
        "/mnt/c/Claude Code/tool/mcp_bridge_extended.sh" "$MCP_TOOL" $MCP_ARGS
        ;;
esac