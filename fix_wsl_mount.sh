#!/bin/bash
echo "WSLのマウント問題を解決します"
echo "================================"

# 現在のマウント状態
echo "現在マウントされているドライブ:"
mount | grep drvfs

echo -e "\n修正方法:"
echo "1. /etc/wsl.confに以下を追加:"
cat << 'EOF'

[automount]
enabled = true
root = /mnt/
options = "metadata"
mountFsTab = true
EOF

echo -e "\n2. /etc/fstabに以下を追加:"
echo "G: /mnt/g drvfs defaults 0 0"

echo -e "\n3. PowerShellで実行:"
echo "wsl --shutdown"
echo "その後WSLを再起動"

# 今すぐ試すコマンド
echo -e "\n即座に試す場合（要sudo）:"
echo "sudo mkdir -p /mnt/g"
echo "sudo mount -t drvfs G: /mnt/g"