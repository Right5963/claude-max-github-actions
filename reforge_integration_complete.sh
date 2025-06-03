#!/bin/bash
# Stability Matrix + Reforge 完全統合スクリプト

MCP_TOOL="${1:-help}"
shift
MCP_ARGS="$@"

# Reforge設定
REFORGE_URL="http://127.0.0.1:8500"
REFORGE_API="$REFORGE_URL/sdapi/v1"

case "$MCP_TOOL" in
    help|--help|-h)
        cat << EOF
🔥 Stability Matrix + Reforge 完全統合

【環境確認】
  check_reforge              - Reforge稼働状況確認
  get_models                - 利用可能モデル一覧
  get_samplers              - サンプラー一覧
  system_info               - システム情報

【即座に生成】
  quick_gen [prompt]        - クイック生成 (768x1024)
  poster_gen [prompt]       - ポスター向け (1024x768)
  square_gen [prompt]       - 正方形 (1024x1024)
  portrait_gen [prompt]     - ポートレート (768x1344)

【高品質生成】
  hq_anime [prompt]         - 高品質アニメ
  hq_realistic [prompt]     - 高品質リアル
  hq_artwork [prompt]       - 高品質アートワーク

【バッチ生成】
  market_batch [base_prompt] - 市場向けバッチ生成
  style_batch [prompt]      - スタイルバリエーション
  size_batch [prompt]       - サイズバリエーション

【パイプライン統合】
  full_workflow [reference] - 分析→プロンプト→生成
  market_workflow [trend]   - 市場分析→生成

使用例:
  $0 check_reforge
  $0 quick_gen "anime girl, cyberpunk"
  $0 full_workflow "bestseller.jpg"

前提: Stability MatrixでReforgeを起動 (ポート8500)
EOF
        exit 0
        ;;

    # 環境確認
    check_reforge)
        echo "🔥 Reforge環境確認中..."
        echo ""
        
        echo "=== 接続テスト ==="
        if curl -s "$REFORGE_URL" >/dev/null 2>&1; then
            echo "✅ Reforge Web UI: $REFORGE_URL - 稼働中"
        else
            echo "❌ Reforge Web UI: $REFORGE_URL - 停止中"
            echo "Stability Matrixから起動してください"
            exit 1
        fi
        
        if curl -s "$REFORGE_API/options" >/dev/null 2>&1; then
            echo "✅ Reforge API: $REFORGE_API - 稼働中"
        else
            echo "❌ Reforge API: $REFORGE_API - 停止中"
            echo "Reforge起動時にAPIを有効にしてください"
            exit 1
        fi
        
        echo ""
        echo "=== システム情報 ==="
        curl -s "$REFORGE_API/memory" 2>/dev/null | head -3 || echo "メモリ情報取得失敗"
        
        echo ""
        echo "✅ Reforge環境 - 正常稼働中"
        ;;

    get_models)
        echo "🤖 利用可能モデル一覧:"
        echo ""
        curl -s "$REFORGE_API/sd-models" 2>/dev/null | grep -o '"model_name":"[^"]*"' | sed 's/"model_name":"//g' | sed 's/"//g' | nl
        ;;

    # クイック生成
    quick_gen)
        PROMPT="${1:-anime girl, masterpiece}"
        echo "⚡ クイック生成: $PROMPT"
        echo ""
        
        cat > /tmp/reforge_payload.json << EOF
{
    "prompt": "$PROMPT",
    "negative_prompt": "lowres, bad anatomy, bad hands, text, error, worst quality, low quality, jpeg artifacts, blurry",
    "steps": 20,
    "width": 768,
    "height": 1024,
    "cfg_scale": 7,
    "sampler_name": "DPM++ 2M Karras",
    "seed": -1
}
EOF
        
        echo "🚀 生成設定:"
        echo "プロンプト: $PROMPT"
        echo "サイズ: 768x1024"
        echo "ステップ: 20"
        echo ""
        echo "💻 ブラウザ実行:"
        echo "1. $REFORGE_URL を開く"
        echo "2. プロンプト貼り付け: $PROMPT"
        echo "3. Generate実行"
        ;;

    poster_gen)
        PROMPT="${1:-beautiful poster design}"
        echo "🖼️ ポスター生成: $PROMPT"
        echo ""
        
        cat > /tmp/reforge_poster.json << EOF
{
    "prompt": "$PROMPT, poster style, high resolution, detailed",
    "negative_prompt": "lowres, text, watermark, signature, blurry, worst quality",
    "steps": 28,
    "width": 1024,
    "height": 768,
    "cfg_scale": 8,
    "sampler_name": "DPM++ 2M SDE Karras",
    "seed": -1
}
EOF
        
        echo "🎨 ポスター設定:"
        echo "プロンプト: $PROMPT, poster style, high resolution, detailed"
        echo "サイズ: 1024x768 (横長)"
        echo "ステップ: 28"
        echo "CFG: 8.0"
        ;;

    # 高品質生成
    hq_anime)
        PROMPT="${1:-anime girl}"
        echo "✨ 高品質アニメ生成: $PROMPT"
        echo ""
        
        ENHANCED_PROMPT="$PROMPT, masterpiece, best quality, ultra detailed, 8k, extremely detailed CG, perfect lighting, colorful, highly detailed"
        NEG_PROMPT="lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name, monochrome"
        
        echo "🎨 高品質設定:"
        echo "プロンプト: $ENHANCED_PROMPT"
        echo "ネガティブ: $NEG_PROMPT"
        echo "ステップ: 35"
        echo "CFG: 7.5"
        echo "サイズ: 768x1024"
        echo ""
        echo "💻 実行推奨:"
        echo "$REFORGE_URL"
        ;;

    # バッチ生成
    market_batch)
        BASE_PROMPT="${1:-anime girl}"
        echo "📦 市場向けバッチ生成: $BASE_PROMPT"
        echo ""
        
        echo "=== 生成キュー (5パターン) ==="
        echo "1. $BASE_PROMPT, masterpiece, best quality"
        echo "2. $BASE_PROMPT, anime style, colorful"
        echo "3. $BASE_PROMPT, detailed illustration"
        echo "4. $BASE_PROMPT, cyberpunk aesthetic"
        echo "5. $BASE_PROMPT, fantasy art style"
        echo ""
        echo "推奨実行:"
        echo "各プロンプトでReforge生成→品質比較→ベスト選択"
        ;;

    # 完全ワークフロー
    full_workflow)
        REFERENCE="${1:-}"
        echo "🔥 完全ワークフロー実行: $REFERENCE"
        echo ""
        
        echo "=== フェーズ1: 環境確認 ==="
        $0 check_reforge
        
        echo ""
        echo "=== フェーズ2: 市場分析 ==="
        ../specialized_research_bridge.sh civitai_models checkpoint
        
        echo ""
        echo "=== フェーズ3: プロンプト生成 ==="
        OPTIMIZED_PROMPT=$(../content_creation_pipeline.sh prompt_variations "$REFERENCE" | grep "masterpiece" | head -1 | sed 's/^- //')
        echo "最適化プロンプト: $OPTIMIZED_PROMPT"
        
        echo ""
        echo "=== フェーズ4: Reforge生成 ==="
        $0 hq_anime "$OPTIMIZED_PROMPT"
        
        echo ""
        echo "=== フェーズ5: 品質確認 ==="
        echo "生成後のアクション:"
        echo "1. 複数バリエーション確認"
        echo "2. 最高品質を選択"
        echo "3. 必要に応じて再生成"
        echo "4. 最終調整・アップスケール"
        ;;

    market_workflow)
        TREND="${1:-cyberpunk anime}"
        echo "📈 市場ワークフロー: $TREND"
        echo ""
        
        echo "=== 市場分析 ==="
        ../specialized_research_bridge.sh yahoo_auction_ai "$TREND"
        
        echo ""
        echo "=== トレンド融合 ==="
        ../content_creation_pipeline.sh trend_fusion "anime" "$TREND"
        
        echo ""
        echo "=== Reforge生成 ==="
        $0 market_batch "$TREND girl"
        ;;

    *)
        echo "不明なコマンド: $MCP_TOOL"
        echo "ヘルプを表示: $0 help"
        exit 1
        ;;
esac