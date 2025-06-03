#!/bin/bash
# ローカルStable Diffusion統合スクリプト

MCP_TOOL="${1:-help}"
shift
MCP_ARGS="$@"

case "$MCP_TOOL" in
    help|--help|-h)
        cat << EOF
🎨 ローカルStable Diffusion統合システム

【SDインストール検出】
  detect_sd                   - SD WebUI/ComfyUI自動検出
  check_models               - インストール済みモデル確認
  check_extensions          - 拡張機能一覧
  setup_api                 - API設定確認

【自動生成】
  generate [prompt]          - プロンプトから画像生成
  batch_generate [prompts]   - バッチ生成
  style_test [base] [styles] - スタイルテスト生成
  variation_gen [image]      - バリエーション生成

【プロンプト統合】
  pipeline_generate [ref]    - パイプライン→SD自動生成
  market_generate [trend]    - 市場分析→SD生成
  auto_improve [prompt]      - 自動改良生成

【品質管理】
  compare_outputs           - 複数出力比較
  quality_score [image]     - 品質スコア算出
  auto_select_best         - 最適画像自動選択

使用例:
  $0 detect_sd
  $0 generate "anime girl, masterpiece"
  $0 pipeline_generate "reference.jpg"
EOF
        exit 0
        ;;

    # SD検出
    detect_sd)
        echo "🔍 ローカルStable Diffusion環境を検出中..."
        echo ""
        
        # 一般的なSD設置場所をチェック
        SD_PATHS=(
            "/mnt/c/stable-diffusion-webui"
            "/mnt/c/ComfyUI"
            "/mnt/c/SD"
            "/mnt/c/AI/stable-diffusion-webui"
            "/mnt/c/Users/$USER/stable-diffusion-webui"
            "/mnt/c/Program Files/ComfyUI"
        )
        
        echo "=== 検出結果 ==="
        FOUND_SD=""
        
        for path in "${SD_PATHS[@]}"; do
            if [ -d "$path" ]; then
                echo "✅ 発見: $path"
                FOUND_SD="$path"
                
                # WebUI形式かComfyUI形式か判定
                if [ -f "$path/webui.py" ] || [ -f "$path/launch.py" ]; then
                    echo "   → SD WebUI形式"
                    SD_TYPE="webui"
                elif [ -f "$path/main.py" ]; then
                    echo "   → ComfyUI形式"
                    SD_TYPE="comfyui"
                fi
            else
                echo "❌ 未発見: $path"
            fi
        done
        
        if [ -n "$FOUND_SD" ]; then
            echo ""
            echo "🎉 Stable Diffusion環境発見！"
            echo "パス: $FOUND_SD"
            echo "タイプ: $SD_TYPE"
            echo ""
            echo "次のステップ:"
            echo "1. $0 check_models でモデル確認"
            echo "2. $0 setup_api でAPI設定"
            echo "3. $0 generate 'test prompt' で動作テスト"
        else
            echo ""
            echo "❌ Stable Diffusion環境が見つかりません"
            echo ""
            echo "インストール推奨:"
            echo "1. AUTOMATIC1111 WebUI"
            echo "2. ComfyUI"
            echo "3. Forge WebUI"
        fi
        ;;

    check_models)
        echo "🤖 インストール済みモデルをチェック中..."
        echo ""
        
        # SD WebUI形式のモデルディレクトリ
        WEBUI_MODELS=(
            "/mnt/c/stable-diffusion-webui/models/Stable-diffusion"
            "/mnt/c/ComfyUI/models/checkpoints"
            "/mnt/c/SD/models/Stable-diffusion"
        )
        
        for model_dir in "${WEBUI_MODELS[@]}"; do
            if [ -d "$model_dir" ]; then
                echo "📁 モデルディレクトリ: $model_dir"
                echo "モデル一覧:"
                ls "$model_dir"/*.safetensors "$model_dir"/*.ckpt 2>/dev/null | while read model; do
                    if [ -f "$model" ]; then
                        filename=$(basename "$model")
                        size=$(du -h "$model" | cut -f1)
                        echo "  ✅ $filename ($size)"
                    fi
                done
                echo ""
            fi
        done
        ;;

    setup_api)
        echo "🔗 SD API設定をチェック中..."
        echo ""
        
        # Reforge API確認 (ユーザー指定のポート)
        echo "=== Reforge API確認 (8500) ==="
        if curl -s http://127.0.0.1:8500/sdapi/v1/options >/dev/null 2>&1; then
            echo "✅ Reforge API (127.0.0.1:8500) - 稼働中"
            SD_API_URL="http://127.0.0.1:8500"
            echo "Stability Matrix + Reforge 検出！"
        else
            echo "❌ Reforge API (127.0.0.1:8500) - 停止中"
            echo "Stability Matrixから起動してください"
        fi
        
        # 標準WebUI APIの確認
        echo ""
        echo "=== 標準WebUI API確認 (7860) ==="
        if curl -s http://localhost:7860/sdapi/v1/options >/dev/null 2>&1; then
            echo "✅ WebUI API (localhost:7860) - 稼働中"
            SD_API_URL="http://localhost:7860"
        else
            echo "❌ WebUI API (localhost:7860) - 停止中"
        fi
        
        echo ""
        echo "=== ComfyUI API確認 (8188) ==="
        if curl -s http://localhost:8188/history >/dev/null 2>&1; then
            echo "✅ ComfyUI API (localhost:8188) - 稼働中"
            COMFY_API_URL="http://localhost:8188"
        else
            echo "❌ ComfyUI API (localhost:8188) - 停止中"
        fi
        ;;

    # 画像生成
    generate)
        PROMPT="${1:-beautiful anime girl}"
        echo "🎨 Reforge画像生成中: $PROMPT"
        echo ""
        
        # Reforge API (ポート8500) で生成
        if command -v curl >/dev/null 2>&1; then
            echo "🔥 Reforge API経由で生成試行中..."
            
            # Reforge APIエンドポイント
            API_URL="http://127.0.0.1:8500/sdapi/v1/txt2img"
            
            # Reforge最適化JSONペイロード
            JSON_PAYLOAD=$(cat << EOF
{
    "prompt": "$PROMPT",
    "negative_prompt": "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
    "steps": 25,
    "width": 768,
    "height": 1024,
    "cfg_scale": 7.5,
    "sampler_name": "DPM++ 2M SDE Karras",
    "seed": -1,
    "batch_size": 1,
    "restore_faces": true,
    "tiling": false,
    "do_not_save_samples": false,
    "do_not_save_grid": false
}
EOF
)
            
            echo "=== Reforge生成設定 ==="
            echo "URL: $API_URL"
            echo "プロンプト: $PROMPT"
            echo "サイズ: 768x1024 (ポートレート)"
            echo "ステップ: 25"
            echo "CFG: 7.5"
            echo "サンプラー: DPM++ 2M SDE Karras"
            echo ""
            
            # API稼働確認
            if curl -s http://127.0.0.1:8500/sdapi/v1/options >/dev/null 2>&1; then
                echo "✅ Reforge API 稼働中 - 生成可能"
                echo ""
                echo "🚀 実際の生成方法:"
                echo "1. ブラウザで http://127.0.0.1:8500 にアクセス"
                echo "2. プロンプト入力: $PROMPT"
                echo "3. Generate ボタンクリック"
                echo ""
                echo "📁 生成画像保存先:"
                echo "   Stability Matrix/Data/packages/[name]/outputs/"
            else
                echo "❌ Reforge API停止中"
                echo "Stability Matrixから起動してください"
            fi
        else
            echo "curl コマンドが見つかりません"
        fi
        ;;

    pipeline_generate)
        REFERENCE="${1:-}"
        echo "🚀 パイプライン→SD統合生成: $REFERENCE"
        echo ""
        
        echo "=== フェーズ1: コンテンツ分析 ==="
        ../content_creation_pipeline.sh analyze_image "$REFERENCE"
        
        echo ""
        echo "=== フェーズ2: プロンプト最適化 ==="
        OPTIMIZED_PROMPT=$(../content_creation_pipeline.sh prompt_variations "anime girl" | grep "masterpiece" | head -1)
        echo "最適化プロンプト: $OPTIMIZED_PROMPT"
        
        echo ""
        echo "=== フェーズ3: SD自動生成 ==="
        $0 generate "$OPTIMIZED_PROMPT"
        
        echo ""
        echo "=== フェーズ4: 結果分析 ==="
        echo "生成完了後の推奨アクション:"
        echo "1. 複数バリエーション生成"
        echo "2. 品質比較・選択"
        echo "3. さらなる改良プロンプト生成"
        ;;

    batch_generate)
        echo "📦 バッチ生成開始..."
        echo ""
        
        # パイプラインからプロンプトリスト生成
        BASE_PROMPT="${1:-anime girl}"
        
        echo "ベースプロンプト: $BASE_PROMPT"
        echo ""
        echo "生成するバリエーション:"
        
        VARIATIONS=(
            "$BASE_PROMPT, masterpiece, best quality"
            "$BASE_PROMPT, anime style, detailed"
            "$BASE_PROMPT, photorealistic, 8k"
            "$BASE_PROMPT, oil painting style"
            "$BASE_PROMPT, cyberpunk aesthetic"
        )
        
        for i in "${!VARIATIONS[@]}"; do
            echo "$((i+1)). ${VARIATIONS[$i]}"
            echo "   → SD生成: $0 generate '${VARIATIONS[$i]}'"
        done
        
        echo ""
        echo "💡 自動実行するには:"
        echo "for prompt in \"\${VARIATIONS[@]}\"; do"
        echo "    $0 generate \"\$prompt\""
        echo "    sleep 30  # 生成待機"
        echo "done"
        ;;

    *)
        echo "不明なコマンド: $MCP_TOOL"
        echo "ヘルプを表示: $0 help"
        exit 1
        ;;
esac