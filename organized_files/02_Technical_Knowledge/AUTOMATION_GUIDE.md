# 自動化システム使用ガイド

## 概要
バランスの取れた自動化システムです。Simple Firstを基本としながら、必要に応じて高度な自動化も利用できます。

## 自動化レベル

### 🔹 Minimal（ミニマル）- デフォルト
- **セッション監視のみ**
- リソース使用: 最小限
- 推奨: 短時間の作業、リソースが限られる環境

### 🔸 Balanced（バランス）
- **セッション監視**（5分ごと）
- **ヘルスチェック**（1時間ごと、静かモード）
- **日次レポート**（18:00に自動生成）
- リソース使用: 中程度
- 推奨: 通常の開発作業、1日中作業する場合

### 🔶 Full（フル）
- **全機能稼働**
- Obsidian同期も含む（15分ごと）
- リソース使用: 高め
- 推奨: 長期プロジェクト、完全なバックアップが必要な場合

## 使い方

### レベルの設定
```bash
# 現在のレベル確認
./auto_level_manager.sh level

# レベル変更
./auto_level_manager.sh level minimal    # 最小限
./auto_level_manager.sh level balanced   # バランス
./auto_level_manager.sh level full       # フル機能
```

### 起動と停止
```bash
# 通常の使用（自動）
claude  # 設定されたレベルで自動起動

# 手動管理
./auto_level_manager.sh start   # 起動
./auto_level_manager.sh stop    # 停止
./auto_level_manager.sh status  # 状態確認
```

### 個別ツールの手動実行
```bash
# いつでも手動実行可能
./simple_health_check.sh         # シンプルヘルスチェック
python3 simple_daily_report.py   # シンプル日次レポート
python3 health_check_auto.py     # 詳細ヘルスチェック
python3 daily_report_auto.py     # 詳細日次レポート
```

## 選び方の指針

### Minimalを選ぶべき場合
- 初めて使う
- 短時間の作業
- システムリソースが限られている
- シンプルさを重視

### Balancedを選ぶべき場合
- 1日中作業する
- システムの健全性を定期的に確認したい
- 日次の振り返りを忘れたくない
- 適度な自動化が欲しい

### Fullを選ぶべき場合
- 重要なプロジェクトで作業
- 完全なバックアップが必要
- Obsidianと連携したい
- リソースに余裕がある

## トラブルシューティング

### レベル変更が反映されない
```bash
# 一度停止してから再起動
./auto_level_manager.sh stop
./auto_level_manager.sh start
```

### 特定の自動化だけ停止したい
```bash
# 例：ヘルスチェックのみ停止
kill $(cat .health_check.pid)
rm -f .health_check.pid
```

### ログを確認したい
```bash
# 各システムのログ
tail -f auto_systems_logs/health_check.log
tail -f auto_systems_logs/daily_report.log
tail -f auto_systems_logs/obsidian_sync.log
tail -f session_monitor.log
```

## 設計思想

### Simple First, But Not Simple Only
- デフォルトは最小限（Simple First）
- 必要に応じて機能を追加可能
- ユーザーが選択権を持つ

### 段階的導入
1. Minimalから始める
2. 必要を感じたらBalancedへ
3. 完全な自動化が必要ならFullへ

### 透明性
- 何が動いているか常に確認可能
- ログで動作を追跡可能
- 手動実行も常に可能

## まとめ

**「適切な自動化は、適切なタイミングで」**

過度な自動化も、不足する自動化も、どちらも問題です。
このシステムは、あなたのニーズに合わせて調整できる柔軟性を提供します。