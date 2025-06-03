#!/bin/bash
# Obsidianリンクの状態を確認して自動修復

echo "🔍 Obsidianリンクチェッカー v2.0"
echo "================================"
echo

# 色の定義
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# チェック結果
CHECKS_PASSED=0
TOTAL_CHECKS=0

# チェック関数
check_path() {
    local path="$1"
    local desc="$2"
    ((TOTAL_CHECKS++))
    
    if [ -d "$path" ]; then
        echo -e "${GREEN}✅ $desc${NC}"
        echo "   パス: $path"
        ((CHECKS_PASSED++))
        return 0
    else
        echo -e "${RED}❌ $desc${NC}"
        return 1
    fi
}

# リンク作成関数
create_link() {
    local target="$1"
    local link="./obsidian-vault"
    
    if [ -L "$link" ]; then
        rm "$link"
    fi
    
    ln -sfn "$target" "$link"
    echo -e "${GREEN}✅ シンボリックリンクを作成しました${NC}"
    echo "   $link -> $target"
}

echo "1. Windows側のジャンクションを確認..."
if check_path "/mnt/c/ObsidianVault" "C:\\ObsidianVault (ジャンクション)"; then
    # TAL_INFO.mdを確認
    if [ -f "/mnt/c/ObsidianVault/TAL_INFO.md" ]; then
        echo -e "${GREEN}   📝 TAL_INFO.mdが存在します${NC}"
    fi
    
    # 自動的にシンボリックリンクを作成
    create_link "/mnt/c/ObsidianVault"
    
    # Vault内のファイルを表示
    echo
    echo "📁 Vault内のファイル（最初の10個）:"
    find /mnt/c/ObsidianVault -name "*.md" -type f 2>/dev/null | head -10 | while read -r file; do
        echo "   - $(basename "$file")"
    done
else
    echo
    echo "2. 代替パスを検索中..."
    
    # 可能なパスのリスト
    POSSIBLE_PATHS=(
        "/mnt/g/マイドライブ/Obsidian Vault"
        "/mnt/c/Users/*/Google Drive/Obsidian Vault"
        "/mnt/c/Users/*/GoogleDrive/Obsidian Vault"
        "/mnt/c/Users/*/OneDrive/Obsidian Vault"
        "/mnt/c/Users/*/Documents/Obsidian Vault"
    )
    
    FOUND=0
    for pattern in "${POSSIBLE_PATHS[@]}"; do
        # ワイルドカードを展開
        for path in $pattern; do
            if [ -d "$path" ]; then
                echo -e "${GREEN}✅ Vaultを発見: $path${NC}"
                create_link "$path"
                FOUND=1
                ((CHECKS_PASSED++))
                break 2
            fi
        done
    done
    
    if [ $FOUND -eq 0 ]; then
        echo -e "${YELLOW}⚠️  Obsidian Vaultが見つかりません${NC}"
        echo
        echo "💡 解決方法:"
        echo "1. Windowsで ULTIMATE_OBSIDIAN_LINK.bat を管理者として実行"
        echo "2. 手動でパスを指定してリンクを作成:"
        echo "   ln -sfn \"実際のパス\" ./obsidian-vault"
    fi
fi

echo
echo "================================"
echo "チェック結果: $CHECKS_PASSED/$TOTAL_CHECKS"

# リンクの最終確認
if [ -L "./obsidian-vault" ]; then
    echo
    echo -e "${GREEN}📁 ./obsidian-vault からアクセス可能です${NC}"
    echo "   実際のパス: $(readlink -f ./obsidian-vault)"
fi