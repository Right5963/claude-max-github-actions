#!/usr/bin/env python3
"""
システムヘルスチェック自動化
============================
各種システムの健全性を定期的にチェック
"""

import os
import json
import psutil
import subprocess
from datetime import datetime
from pathlib import Path

class HealthCheckAuto:
    def __init__(self):
        self.report_file = "system_health_report.json"
        self.critical_processes = [
            "claude",
            "node",
            "python3"
        ]
        self.check_items = []
        
    def check_disk_space(self):
        """ディスク容量チェック"""
        disk = psutil.disk_usage('/')
        status = "✅" if disk.percent < 80 else "⚠️" if disk.percent < 90 else "❌"
        
        return {
            "name": "ディスク容量",
            "status": status,
            "value": f"{disk.percent:.1f}% 使用中",
            "details": f"空き: {disk.free // (1024**3)}GB / 合計: {disk.total // (1024**3)}GB"
        }
    
    def check_memory(self):
        """メモリ使用状況チェック"""
        mem = psutil.virtual_memory()
        status = "✅" if mem.percent < 70 else "⚠️" if mem.percent < 85 else "❌"
        
        return {
            "name": "メモリ使用率",
            "status": status,
            "value": f"{mem.percent:.1f}%",
            "details": f"使用中: {mem.used // (1024**3)}GB / 合計: {mem.total // (1024**3)}GB"
        }
    
    def check_session_monitor(self):
        """セッション監視プロセスチェック"""
        pid_file = ".session_monitor.pid"
        
        if os.path.exists(pid_file):
            try:
                with open(pid_file, 'r') as f:
                    pid = int(f.read().strip())
                
                # プロセスが存在するかチェック
                if psutil.pid_exists(pid):
                    return {
                        "name": "セッション監視",
                        "status": "✅",
                        "value": f"稼働中 (PID: {pid})",
                        "details": "5分ごとに自動保存実行中"
                    }
            except:
                pass
        
        return {
            "name": "セッション監視",
            "status": "❌",
            "value": "停止中",
            "details": "監視プロセスが実行されていません"
        }
    
    def check_mcp_servers(self):
        """MCPサーバー状態チェック"""
        try:
            # claudeプロセスをチェック
            claude_procs = [p for p in psutil.process_iter(['pid', 'name', 'cmdline']) 
                          if 'claude' in str(p.info['cmdline']).lower()]
            
            if claude_procs:
                return {
                    "name": "MCPサーバー",
                    "status": "✅",
                    "value": f"{len(claude_procs)}個のプロセス稼働中",
                    "details": "Claude Code MCPサーバーが正常に動作中"
                }
        except:
            pass
        
        return {
            "name": "MCPサーバー",
            "status": "⚠️",
            "value": "確認できません",
            "details": "MCPサーバーの状態を確認できません"
        }
    
    def check_obsidian_access(self):
        """Obsidianアクセスチェック"""
        try:
            # MCPブリッジ経由でテスト
            result = subprocess.run(
                ["./mcp_bridge_extended.sh", "obsidian_list", ""],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {
                    "name": "Obsidianアクセス",
                    "status": "✅",
                    "value": "正常",
                    "details": "Obsidian Vaultへのアクセス可能"
                }
        except:
            pass
        
        return {
            "name": "Obsidianアクセス",
            "status": "❌",
            "value": "アクセス不可",
            "details": "Obsidian Vaultにアクセスできません"
        }
    
    def check_git_status(self):
        """Gitリポジトリ状態チェック"""
        try:
            # git status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                
                if changes == 0:
                    status = "✅"
                    value = "クリーン"
                    details = "コミットされていない変更はありません"
                else:
                    status = "⚠️"
                    value = f"{changes}個の変更"
                    details = "コミットされていない変更があります"
                
                return {
                    "name": "Gitステータス",
                    "status": status,
                    "value": value,
                    "details": details
                }
        except:
            pass
        
        return {
            "name": "Gitステータス",
            "status": "❌",
            "value": "エラー",
            "details": "Gitリポジトリではありません"
        }
    
    def check_python_packages(self):
        """重要なPythonパッケージチェック"""
        required_packages = ["psutil", "requests", "beautifulsoup4"]
        missing = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if not missing:
            return {
                "name": "Pythonパッケージ",
                "status": "✅",
                "value": "全て利用可能",
                "details": f"必須パッケージ: {', '.join(required_packages)}"
            }
        else:
            return {
                "name": "Pythonパッケージ",
                "status": "⚠️",
                "value": f"{len(missing)}個不足",
                "details": f"不足: {', '.join(missing)}"
            }
    
    def run_health_check(self, quiet=False):
        """全てのヘルスチェックを実行"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 各チェックを実行
        checks = [
            self.check_disk_space(),
            self.check_memory(),
            self.check_session_monitor(),
            # Git/MCP/Obsidianチェックは省略可能
        ]
        
        # 結果を集計
        critical_count = 0
        warning_count = 0
        critical_issues = []
        
        for check in checks:
            if "❌" in check['status']:
                critical_count += 1
                critical_issues.append(check)
            elif "⚠️" in check['status']:
                warning_count += 1
        
        # quietモード: 問題がある時のみ表示
        if quiet and critical_count == 0 and warning_count == 0:
            return  # 問題なければ何も表示しない
        
        # 通常表示
        if not quiet:
            print(f"🏥 システムヘルスチェック - {timestamp}")
            print("=" * 50)
            
            for check in checks:
                print(f"{check['status']} {check['name']}: {check['value']}")
        
        # 重大な問題がある場合は常に表示
        if critical_count > 0:
            print("\n🚨 重大な問題が検出されました:")
            for issue in critical_issues:
                print(f"  ❌ {issue['name']}: {issue['details']}")
            
            # 自動修復を試みる
            if issue['name'] == "セッション監視":
                print("  → セッション監視を再起動します...")
                subprocess.run(["./simple_monitor.sh", "start"], capture_output=True)
        
        # サマリー
        if not quiet or critical_count > 0 or warning_count > 0:
            print("\n📊 サマリー:")
            if critical_count == 0 and warning_count == 0:
                print("✅ システムは完全に健全です")
            elif critical_count == 0:
                print(f"⚠️ {warning_count}個の警告があります")
            else:
                print(f"❌ {critical_count}個の重大な問題、{warning_count}個の警告")
        
        # レポートを保存
        report = {
            "timestamp": timestamp,
            "checks": checks,
            "summary": {
                "total": len(checks),
                "healthy": len([c for c in checks if "✅" in c['status']]),
                "warning": warning_count,
                "critical": critical_count
            }
        }
        
        with open(self.report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report
    
    def auto_fix(self):
        """自動修復を試みる"""
        print("\n🔧 自動修復を実行中...")
        
        # セッション監視が停止していたら再起動
        if not os.path.exists(".session_monitor.pid"):
            print("- セッション監視を再起動...")
            subprocess.run(["./session_monitor_launcher.sh", "start"], capture_output=True)
        
        # その他の自動修復処理をここに追加
        
        print("✅ 自動修復完了")

def main():
    """メイン関数"""
    import sys
    
    checker = HealthCheckAuto()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "quiet":
            # 静かモード（問題がある時のみ表示）
            checker.run_health_check(quiet=True)
        elif sys.argv[1] == "fix":
            # ヘルスチェック後に自動修復
            checker.run_health_check()
            checker.auto_fix()
        elif sys.argv[1] == "daemon":
            # デーモンモード（1時間ごと）
            import time
            print("🤖 ヘルスチェックデーモンを開始")
            
            while True:
                try:
                    checker.run_health_check(quiet=True)  # デーモンモードは静かに
                    time.sleep(3600)  # 1時間
                except KeyboardInterrupt:
                    print("\n⏹️ 停止しました")
                    break
    else:
        # 通常実行
        checker.run_health_check()

if __name__ == "__main__":
    main()