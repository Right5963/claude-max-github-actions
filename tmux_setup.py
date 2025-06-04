#!/usr/bin/env python
"""
Tmux基本設定ツール
==================
WSL環境でのシンプルTmux設定
"""

import subprocess

class TmuxSetup:
    def __init__(self):
        self.tmux_config = """
# Tmux基本設定 (.tmux.conf)
# ========================

# プレフィックスキーをCtrl+aに変更
set -g prefix C-a
unbind C-b

# ペイン分割のキーバインド
bind | split-window -h
bind - split-window -v

# ペイン移動のキーバインド
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# ウィンドウ移動のキーバインド
bind -n C-Left previous-window
bind -n C-Right next-window

# マウス操作を有効化
set -g mouse on

# ステータスバーの設定
set -g status-bg black
set -g status-fg white
set -g status-left '#[fg=green]#S '
set -g status-right '#[fg=yellow]%Y-%m-%d %H:%M'

# コピーモードでviキーバインドを使用
setw -g mode-keys vi

# ペインの境界線の色
set -g pane-border-style fg=magenta
set -g pane-active-border-style fg=yellow

# ウィンドウのインデックスを1から開始
set -g base-index 1
setw -g pane-base-index 1

# 設定ファイルのリロード
bind r source-file ~/.tmux.conf \\; display-message "Config reloaded!"

# セッション保存・復元（tmux-resurrect用）
# set -g @plugin 'tmux-plugins/tmux-resurrect'
"""

    def check_wsl_environment(self):
        """WSL環境の確認"""
                try:
            result = subprocess.run(['wsl', '--list', '--verbose'],
                                  capture_output=True, text=True, encoding='utf-8')
            if 'Ubuntu' in result.stdout:
                print("✅ WSL Ubuntu環境確認済み")
                return True
            else:
                print("❌ WSL Ubuntu環境が見つかりません")
                print(f"WSL出力: {result.stdout}")
                return False
        except Exception as e:
            print(f"❌ WSL確認エラー: {str(e)}")
            return False

    def install_tmux(self):
        """WSL環境にTmuxをインストール"""
        print("📦 Tmuxインストール中...")

        commands = [
            "sudo apt update",
            "sudo apt install -y tmux"
        ]

        for cmd in commands:
            try:
                print(f"実行中: {cmd}")
                result = subprocess.run(['wsl', '-e', 'bash', '-c', cmd],
                                      capture_output=True, text=True, timeout=120)
                if result.returncode != 0:
                    print(f"⚠️ コマンド実行で問題発生: {cmd}")
                    print(f"   stderr: {result.stderr}")
            except subprocess.TimeoutExpired:
                print(f"⏰ タイムアウト: {cmd}")
            except Exception as e:
                print(f"❌ エラー: {str(e)}")

    def create_tmux_config(self):
        """Tmux設定ファイルを作成"""
        try:
            # WSL環境のホームディレクトリに.tmux.confを作成
            config_cmd = f'echo "{self.tmux_config}" > ~/.tmux.conf'

            result = subprocess.run(['wsl', '-e', 'bash', '-c', config_cmd],
                                  capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ Tmux設定ファイル作成完了 (~/.tmux.conf)")
                return True
            else:
                print("❌ 設定ファイル作成失敗")
                return False

        except Exception as e:
            print(f"❌ 設定ファイル作成エラー: {str(e)}")
            return False

    def test_tmux(self):
        """Tmux動作テスト"""
        try:
            result = subprocess.run(['wsl', '-e', 'tmux', '--version'],
                                  capture_output=True, text=True)

            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ Tmux動作確認: {version}")
                return True
            else:
                print("❌ Tmux動作確認失敗")
                return False

        except Exception as e:
            print(f"❌ Tmux動作テストエラー: {str(e)}")
            return False

    def show_basic_usage(self):
        """基本的な使用方法を表示"""
        usage = """
🚀 Tmux基本的な使用方法
=======================

【起動方法】
wsl -e tmux                    # 新しいセッション開始
wsl -e tmux new -s mysession   # 名前付きセッション開始

【基本操作（プレフィックス: Ctrl+a）】
Ctrl+a + |     # 水平分割
Ctrl+a + -     # 垂直分割
Ctrl+a + h/j/k/l  # ペイン移動
Ctrl+a + d     # セッションから離脱
Ctrl+a + r     # 設定リロード

【セッション管理】
wsl -e tmux ls              # セッション一覧
wsl -e tmux attach -t 0     # セッション0に再接続
wsl -e tmux kill-session -t mysession  # セッション削除

【ウィンドウ管理】
Ctrl+Left/Right  # ウィンドウ移動
Ctrl+a + c       # 新しいウィンドウ作成
Ctrl+a + &       # ウィンドウ削除

【便利機能】
- マウス操作対応（ペイン選択・リサイズ）
- viキーバインド（コピーモード）
- カラフルなステータスバー
"""
        print(usage)

def main():
    """メイン実行"""
    setup = TmuxSetup()

    print("🛠️ Tmux基本設定ツール")
    print("=" * 30)

    # WSL環境確認
    if not setup.check_wsl_environment():
        print("WSL Ubuntu環境を先に設定してください")
        return

    print("\n📦 Tmuxインストール...")
    setup.install_tmux()

    print("\n⚙️ Tmux設定ファイル作成...")
    setup.create_tmux_config()

    print("\n🧪 Tmux動作テスト...")
    if setup.test_tmux():
        print("\n🎉 Tmux設定完了！")
        setup.show_basic_usage()
    else:
        print("\n❌ Tmux設定に問題があります")
        print("手動でインストールを確認してください:")
        print("wsl -e bash -c 'sudo apt update && sudo apt install -y tmux'")

if __name__ == "__main__":
    main()
