# 🚀 Tmux基本設定完了

## 基本的な使用方法

### 起動方法

```bash
# WSL環境でTmuxセッション開始
wsl -e tmux

# 名前付きセッション作成
wsl -e tmux new -s mywork

# セッション一覧表示
wsl -e tmux ls

# セッションに再接続
wsl -e tmux attach -t mywork
```

### 基本操作（プレフィックス: Ctrl+a）

#### ペイン分割

- `Ctrl+a` + `|` : 水平分割（左右）
- `Ctrl+a` + `-` : 垂直分割（上下）

#### ペイン移動

- `Ctrl+a` + `h` : 左のペインに移動
- `Ctrl+a` + `j` : 下のペインに移動
- `Ctrl+a` + `k` : 上のペインに移動
- `Ctrl+a` + `l` : 右のペインに移動

#### セッション操作

- `Ctrl+a` + `d` : セッションから切断（デタッチ）
- `Ctrl+a` + `r` : 設定ファイルをリロード

#### ウィンドウ操作

- `Ctrl+a` + `c` : 新しいウィンドウ作成
- `Ctrl+Left/Right` : ウィンドウ切り替え

### 便利機能

- **マウス操作対応**: ペインのクリック、リサイズが可能
- **viキーバインド**: コピーモードでvi操作
- **カラフルUI**: 見やすいステータスバー

### 実際の使用例

#### 開発作業の例

```bash
# 1. 開発用セッション開始
wsl -e tmux new -s dev

# 2. ペインを分割
# Ctrl+a + | (エディター用とターミナル用)
# Ctrl+a + - (ログ監視用)

# 3. 各ペインで作業
# - エディター（vim, nano等）
# - コマンド実行
# - ログ監視（tail -f）

# 4. 必要に応じてデタッチ
# Ctrl+a + d

# 5. 後で再接続
wsl -e tmux attach -t dev
```

## 設定ファイル情報

**設定ファイル**: `~/.tmux.conf` （WSL環境内）

主な設定内容:

- プレフィックスキー: `Ctrl+a`（デフォルトのCtrl+bから変更）
- マウス操作有効化
- ペイン分割とナビゲーションの改善
- 見やすいステータスバー

---

これで基本的なTmux環境の設定が完了です！
開発効率が大幅に向上します 🎉
