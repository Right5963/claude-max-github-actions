#!/usr/bin/env python3
"""
自動セッション監視システム
=========================
session_manager_simple.pyをベースに自動監視機能を追加
5分ごとに自動保存し、変更を検出して記録
"""

import json
import os
import sys
import time
import signal
from datetime import datetime
import subprocess

class SessionAutoMonitor:
    def __init__(self):
        self.session_file = "current_session.json"
        self.monitor_log = "session_monitor.log"
        self.pid_file = ".session_monitor.pid"
        self.interval = 300  # 5分 = 300秒
        self.running = True
        
    def write_log(self, message):
        """ログ出力"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        with open(self.monitor_log, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def save_pid(self):
        """PIDファイル保存"""
        with open(self.pid_file, 'w') as f:
            f.write(str(os.getpid()))
        self.write_log(f"監視開始: PID {os.getpid()}")
    
    def cleanup(self):
        """終了処理"""
        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)
        self.write_log("監視終了")
    
    def signal_handler(self, signum, frame):
        """シグナルハンドラ"""
        self.write_log(f"シグナル受信: {signum}")
        self.running = False
    
    def execute_session_command(self, command, message=""):
        """session_manager_simple.pyのコマンド実行"""
        try:
            cmd = ["python3", "session_manager_simple.py", command]
            if message:
                cmd.append(message)
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                self.write_log(f"コマンド成功: {command} {message}")
            else:
                self.write_log(f"コマンド失敗: {result.stderr}")
        except Exception as e:
            self.write_log(f"エラー: {str(e)}")
    
    def check_session_changes(self):
        """セッションの変更を検出"""
        try:
            # 現在のセッションファイルの更新時刻
            if os.path.exists(self.session_file):
                mtime = os.path.getmtime(self.session_file)
                mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                self.write_log(f"セッション更新時刻: {mtime_str}")
                return True
            return False
        except Exception as e:
            self.write_log(f"チェックエラー: {str(e)}")
            return False
    
    def auto_save(self):
        """自動保存実行"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.execute_session_command("activity", f"自動保存実行 - {timestamp}")
        
        # セッションをバックアップ
        try:
            if os.path.exists(self.session_file):
                backup_dir = "sessions"
                os.makedirs(backup_dir, exist_ok=True)
                
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                # セッションIDを取得または生成
                session_id = session_data.get('session_id', datetime.now().strftime("%Y%m%d_%H%M%S"))
                backup_file = os.path.join(backup_dir, f"session_{session_id}.json")
                
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(session_data, f, ensure_ascii=False, indent=2)
                
                self.write_log(f"バックアップ保存: {backup_file}")
        except Exception as e:
            self.write_log(f"バックアップエラー: {str(e)}")
    
    def monitor_loop(self):
        """メイン監視ループ"""
        self.save_pid()
        
        # シグナル設定
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        
        self.write_log(f"監視開始: {self.interval}秒ごとに自動保存")
        
        try:
            while self.running:
                # 自動保存実行
                self.auto_save()
                
                # 次の実行まで待機
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)
                    
        except Exception as e:
            self.write_log(f"監視エラー: {str(e)}")
        finally:
            self.cleanup()
    
    def start(self):
        """監視開始"""
        # 既存のプロセスをチェック
        if os.path.exists(self.pid_file):
            with open(self.pid_file, 'r') as f:
                old_pid = int(f.read().strip())
            
            # プロセスが生きているかチェック
            try:
                os.kill(old_pid, 0)
                print(f"監視プロセスは既に実行中です (PID: {old_pid})")
                return
            except ProcessLookupError:
                self.write_log(f"古いPIDファイルを削除: {old_pid}")
                os.remove(self.pid_file)
        
        # デーモンとして起動
        self.monitor_loop()
    
    def stop(self):
        """監視停止"""
        if os.path.exists(self.pid_file):
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            try:
                os.kill(pid, signal.SIGTERM)
                print(f"監視プロセスを停止しました (PID: {pid})")
            except ProcessLookupError:
                print("監視プロセスは既に停止しています")
                os.remove(self.pid_file)
        else:
            print("監視プロセスは実行されていません")
    
    def status(self):
        """状態確認"""
        if os.path.exists(self.pid_file):
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            try:
                os.kill(pid, 0)
                print(f"✅ 監視プロセス実行中 (PID: {pid})")
                
                # 最新のログを表示
                if os.path.exists(self.monitor_log):
                    print("\n📋 最新のログ:")
                    with open(self.monitor_log, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for line in lines[-5:]:
                            print(f"  {line.rstrip()}")
            except ProcessLookupError:
                print("❌ 監視プロセスは停止しています")
                os.remove(self.pid_file)
        else:
            print("❌ 監視プロセスは実行されていません")

def main():
    """メイン関数"""
    monitor = SessionAutoMonitor()
    
    if len(sys.argv) < 2:
        print("🤖 自動セッション監視システム")
        print("\n使用方法:")
        print("  python3 session_auto_monitor.py start   # 監視開始")
        print("  python3 session_auto_monitor.py stop    # 監視停止")
        print("  python3 session_auto_monitor.py status  # 状態確認")
        print("\n現在の状態:")
        monitor.status()
        return
    
    command = sys.argv[1]
    
    if command == "start":
        monitor.start()
    elif command == "stop":
        monitor.stop()
    elif command == "status":
        monitor.status()
    else:
        print(f"❌ 不明なコマンド: {command}")

if __name__ == "__main__":
    main()