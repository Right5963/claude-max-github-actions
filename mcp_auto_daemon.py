#!/usr/bin/env python3
"""
MCP Auto Daemon - MCPツール自動管理デーモン
==========================================
定期的なMCPエコシステム監視と自動導入
"""

import subprocess
import json
import time
import schedule
import os
from datetime import datetime
from pathlib import Path
import threading

class MCPAutoDaemon:
    def __init__(self):
        self.repo_path = "/mnt/c/Claude Code/tool"
        self.config_file = "mcp_auto_config.json"
        self.log_file = "mcp_auto_daemon.log"
        self.running = False
        
        self.default_config = {
            "check_interval_hours": 24,
            "auto_install": True,
            "max_installs_per_day": 3,
            "efficiency_threshold": 7,
            "categories_priority": {
                "code_analysis": 9,
                "file_operations": 8,
                "ai_integration": 9,
                "productivity": 8,
                "testing": 7
            },
            "blacklist": [],
            "whitelist": []
        }
        
        self.load_config()
    
    def load_config(self):
        """設定ファイルの読み込み"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = self.default_config
                self.save_config()
        except Exception as e:
            self.log(f"Config load failed: {e}")
            self.config = self.default_config
    
    def save_config(self):
        """設定ファイルの保存"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.log(f"Config save failed: {e}")
    
    def log(self, message):
        """ログ記録"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        print(log_entry)
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except Exception:
            pass
    
    def start_daemon(self):
        """デーモン開始"""
        self.log("🚀 MCP Auto Daemon Starting")
        self.running = True
        
        # スケジュール設定
        schedule.every(self.config["check_interval_hours"]).hours.do(self.scheduled_check)
        
        # 即座に初回チェック実行
        self.log("🔍 Initial MCP ecosystem check")
        self.scheduled_check()
        
        # メインループ
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # 1分間隔でスケジュールチェック
            except KeyboardInterrupt:
                self.log("⏹️ Daemon stopping by user request")
                break
            except Exception as e:
                self.log(f"❌ Daemon error: {e}")
                time.sleep(300)  # エラー時は5分待機
    
    def scheduled_check(self):
        """定期チェック実行"""
        self.log("🔍 Scheduled MCP ecosystem check starting")
        
        try:
            # MCPマネージャーを使用して最新ツール発見
            from mcp_auto_manager import MCPAutoManager
            
            manager = MCPAutoManager()
            
            # エコシステム発見
            categorized = manager.discover_mcp_ecosystem()
            analysis = manager.analyze_efficiency_impact(categorized)
            
            # 高品質ツールのフィルタリング
            high_quality_recommendations = self._filter_high_quality(analysis["recommendation"])
            
            if self.config["auto_install"] and high_quality_recommendations:
                # 自動インストール実行
                install_count = min(
                    len(high_quality_recommendations),
                    self.config["max_installs_per_day"]
                )
                
                install_list = high_quality_recommendations[:install_count]
                result = manager.auto_install_system(install_list)
                
                self.log(f"📦 Auto-installed {len(result['installed'])} tools")
                
                # Obsidianに記録
                self._log_installation_to_obsidian(result)
            else:
                self.log("🔍 Check completed, no auto-installation needed")
            
            # 統計更新
            self._update_statistics(categorized, analysis)
            
        except Exception as e:
            self.log(f"❌ Scheduled check failed: {e}")
    
    def _filter_high_quality(self, recommendations):
        """高品質ツールのフィルタリング"""
        filtered = []
        
        for rec in recommendations:
            if rec["action"] != "install":
                continue
            
            tool_name = rec.get("tool", "")
            
            # ブラックリストチェック
            if any(blocked in tool_name.lower() for blocked in self.config["blacklist"]):
                continue
            
            # ホワイトリストがある場合の優先
            if self.config["whitelist"]:
                if not any(allowed in tool_name.lower() for allowed in self.config["whitelist"]):
                    continue
            
            # 効率性スコアチェック（今後実装）
            # if rec.get("efficiency_score", 0) < self.config["efficiency_threshold"]:
            #     continue
            
            filtered.append(rec)
        
        return filtered
    
    def _log_installation_to_obsidian(self, result):
        """インストール結果をObsidianに記録"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        content = f"""# MCP Auto Installation - {timestamp}

## Installation Results
- **Successful**: {len(result['installed'])}
- **Failed**: {len(result['failed'])}
- **Success Rate**: {result['success_rate']:.1%}

## Installed Tools
{chr(10).join(f"- ✅ {tool}" for tool in result['installed'])}

## Failed Installations
{chr(10).join(f"- ❌ {tool}" for tool in result['failed'])}

#mcp #automation #installation #daemon

---
*Auto-generated by MCP Auto Daemon*
"""
        
        try:
            ps_command = f"""
$obsidianPath = "G:\\マイドライブ\\Obsidian Vault\\Development\\MCP_Auto_Installs"
New-Item -ItemType Directory -Force -Path $obsidianPath | Out-Null
$content = @'
{content}
'@
$filename = "mcp_install_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
$content | Out-File -FilePath "$obsidianPath\\$filename" -Encoding UTF8
"""
            
            subprocess.run([
                "powershell.exe", "-Command", ps_command
            ], capture_output=True, timeout=15)
            
            self.log("📝 Installation results logged to Obsidian")
            
        except Exception as e:
            self.log(f"⚠️ Obsidian logging failed: {e}")
    
    def _update_statistics(self, categorized, analysis):
        """統計情報の更新"""
        stats = {
            "last_check": datetime.now().isoformat(),
            "discovered_tools": sum(len(tools) for tools in categorized.values()),
            "high_impact_tools": len(analysis["high_impact_tools"]),
            "current_gaps": len(analysis["current_gaps"]),
            "categories": {
                category: len(tools) 
                for category, tools in categorized.items()
            }
        }
        
        try:
            with open("mcp_daemon_stats.json", "w") as f:
                json.dump(stats, f, indent=2)
            
            self.log(f"📊 Stats updated: {stats['discovered_tools']} tools discovered")
            
        except Exception as e:
            self.log(f"⚠️ Stats update failed: {e}")
    
    def stop_daemon(self):
        """デーモン停止"""
        self.log("⏹️ MCP Auto Daemon Stopping")
        self.running = False
    
    def status(self):
        """デーモン状態確認"""
        try:
            with open("mcp_daemon_stats.json", "r") as f:
                stats = json.load(f)
            
            status_info = {
                "running": self.running,
                "config": self.config,
                "last_stats": stats
            }
            
            return status_info
            
        except Exception as e:
            return {
                "running": self.running,
                "config": self.config,
                "error": str(e)
            }
    
    def configure(self, key, value):
        """設定変更"""
        if key in self.config:
            old_value = self.config[key]
            self.config[key] = value
            self.save_config()
            
            self.log(f"⚙️ Config updated: {key} = {value} (was: {old_value})")
            return True
        else:
            self.log(f"❌ Unknown config key: {key}")
            return False

def main():
    """メイン実行"""
    import sys
    
    daemon = MCPAutoDaemon()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "start":
            # デーモン開始
            daemon.start_daemon()
            
        elif cmd == "status":
            # 状態確認
            status = daemon.status()
            print(json.dumps(status, indent=2))
            
        elif cmd == "configure":
            # 設定変更
            if len(sys.argv) >= 4:
                key, value = sys.argv[2], sys.argv[3]
                try:
                    # 数値変換の試行
                    if value.isdigit():
                        value = int(value)
                    elif value.lower() in ['true', 'false']:
                        value = value.lower() == 'true'
                except:
                    pass
                
                if daemon.configure(key, value):
                    print(f"✅ Configuration updated: {key} = {value}")
                else:
                    print(f"❌ Failed to update configuration")
            else:
                print("Usage: python3 mcp_auto_daemon.py configure <key> <value>")
                
        elif cmd == "check":
            # 手動チェック実行
            daemon.scheduled_check()
            
        else:
            print("使用方法:")
            print("  python3 mcp_auto_daemon.py start      # デーモン開始")
            print("  python3 mcp_auto_daemon.py status     # 状態確認")
            print("  python3 mcp_auto_daemon.py check      # 手動チェック")
            print("  python3 mcp_auto_daemon.py configure <key> <value>  # 設定変更")
    else:
        # デフォルト: 状態確認
        status = daemon.status()
        print("🤖 MCP Auto Daemon Status:")
        print(json.dumps(status, indent=2))

if __name__ == "__main__":
    main()