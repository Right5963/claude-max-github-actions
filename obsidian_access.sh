#!/bin/bash
# Obsidian Vaultへの自動アクセススクリプト

OBSIDIAN_PATH="/mnt/c/ObsidianVault"
OBSIDIAN_PATH_ALT="/mnt/c/ObsidianVaultLink"
G_DRIVE_PATH="/mnt/g/マイドライブ/Obsidian Vault"

# アクセス方法を試行
if [ -d "$OBSIDIAN_PATH" ]; then
    echo "✅ Obsidian Vault (Junction経由) にアクセス可能"
    export OBSIDIAN_VAULT="$OBSIDIAN_PATH"
elif [ -d "$OBSIDIAN_PATH_ALT" ]; then
    echo "✅ Obsidian Vault (Junction Link経由) にアクセス可能"
    export OBSIDIAN_VAULT="$OBSIDIAN_PATH_ALT"
elif [ -d "$G_DRIVE_PATH" ]; then
    echo "✅ Obsidian Vault (Gドライブ) にアクセス可能"
    export OBSIDIAN_VAULT="$G_DRIVE_PATH"
else
    echo "❌ Obsidian Vaultにアクセスできません"
    echo "setup_g_drive.sh または create_junction.bat を実行してください"
    exit 1
fi

# シンボリックリンクを更新
ln -sfn "$OBSIDIAN_VAULT" ./obsidian-vault
echo "📁 ./obsidian-vault からアクセスできます"