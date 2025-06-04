#!/usr/bin/env python3
"""
MCP Development Efficiency Tool
==============================
開発効率化特化のカスタムMCPサーバー
"""

import json
import subprocess
import os
import sys
from datetime import datetime
from pathlib import Path

class MCPDevEfficiencyServer:
    def __init__(self):
        self.repo_path = "/mnt/c/Claude Code/tool"
        self.tools = {
            "dev_quick_commit": {
                "description": "Smart quick commit with context analysis",
                "parameters": {
                    "message": {"type": "string", "description": "Optional commit message"}
                }
            },
            "dev_file_context": {
                "description": "Get development context for files",
                "parameters": {
                    "file_path": {"type": "string", "description": "Path to analyze"}
                }
            },
            "dev_pattern_detect": {
                "description": "Detect development patterns in recent changes",
                "parameters": {
                    "days": {"type": "number", "description": "Days to analyze", "default": 7}
                }
            },
            "dev_auto_optimize": {
                "description": "Auto-optimize development workflow",
                "parameters": {
                    "focus": {"type": "string", "description": "Focus area: speed|quality|efficiency"}
                }
            },
            "dev_knowledge_sync": {
                "description": "Sync development knowledge to Obsidian",
                "parameters": {
                    "type": {"type": "string", "description": "Type: session|learning|pattern"}
                }
            }
        }
    
    def handle_request(self, request):
        """MCP request handling"""
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "tools/list":
            return self._list_tools()
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            return self._call_tool(tool_name, tool_args)
        else:
            return {"error": f"Unknown method: {method}"}
    
    def _list_tools(self):
        """Available tools list"""
        return {
            "tools": [
                {
                    "name": name,
                    "description": info["description"],
                    "inputSchema": {
                        "type": "object",
                        "properties": info["parameters"]
                    }
                }
                for name, info in self.tools.items()
            ]
        }
    
    def _call_tool(self, tool_name, args):
        """Tool execution dispatcher"""
        try:
            if tool_name == "dev_quick_commit":
                return self._dev_quick_commit(args)
            elif tool_name == "dev_file_context":
                return self._dev_file_context(args)
            elif tool_name == "dev_pattern_detect":
                return self._dev_pattern_detect(args)
            elif tool_name == "dev_auto_optimize":
                return self._dev_auto_optimize(args)
            elif tool_name == "dev_knowledge_sync":
                return self._dev_knowledge_sync(args)
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}
    
    def _dev_quick_commit(self, args):
        """Smart quick commit with analysis"""
        message = args.get("message")
        
        # Git status analysis
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=self.repo_path
        )
        
        if not status_result.stdout.strip():
            return {"content": [{"type": "text", "text": "No changes to commit"}]}
        
        # Smart message generation if not provided
        if not message:
            changes = status_result.stdout.strip().split('\n')
            file_count = len(changes)
            
            # Pattern detection
            patterns = []
            if any('.py' in change for change in changes):
                patterns.append("Python")
            if any('.md' in change for change in changes):
                patterns.append("Docs")
            if any('.json' in change for change in changes):
                patterns.append("Config")
            
            pattern_str = "+".join(patterns) if patterns else "Mixed"
            message = f"Auto: {pattern_str} changes ({file_count} files)"
        
        # Execute commit
        try:
            subprocess.run(["git", "add", "."], cwd=self.repo_path, check=True)
            result = subprocess.run(
                ["git", "commit", "-m", message],
                capture_output=True, text=True, cwd=self.repo_path, check=True
            )
            
            return {
                "content": [{
                    "type": "text", 
                    "text": f"✅ Committed: {message}\n{result.stdout}"
                }]
            }
        except subprocess.CalledProcessError as e:
            return {"error": f"Commit failed: {e.stderr}"}
    
    def _dev_file_context(self, args):
        """Get development context for files"""
        file_path = args.get("file_path")
        
        if not file_path:
            return {"error": "file_path is required"}
        
        full_path = os.path.join(self.repo_path, file_path)
        
        if not os.path.exists(full_path):
            return {"error": f"File not found: {file_path}"}
        
        context = {
            "file_info": {
                "path": file_path,
                "size": os.path.getsize(full_path),
                "modified": datetime.fromtimestamp(os.path.getmtime(full_path)).isoformat()
            }
        }
        
        # Git history
        try:
            git_log = subprocess.run([
                "git", "log", "--oneline", "-5", "--", file_path
            ], capture_output=True, text=True, cwd=self.repo_path)
            
            context["recent_changes"] = git_log.stdout.strip().split('\n') if git_log.stdout else []
        except:
            context["recent_changes"] = []
        
        # File analysis
        if file_path.endswith('.py'):
            context["language"] = "Python"
            context["analysis"] = self._analyze_python_file(full_path)
        elif file_path.endswith('.md'):
            context["language"] = "Markdown"
            context["analysis"] = self._analyze_markdown_file(full_path)
        
        return {
            "content": [{
                "type": "text",
                "text": json.dumps(context, indent=2)
            }]
        }
    
    def _analyze_python_file(self, file_path):
        """Python file analysis"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = {
                "lines": len(content.split('\n')),
                "functions": len([line for line in content.split('\n') if line.strip().startswith('def ')]),
                "classes": len([line for line in content.split('\n') if line.strip().startswith('class ')]),
                "imports": len([line for line in content.split('\n') if line.strip().startswith('import ') or line.strip().startswith('from ')])
            }
            
            return analysis
        except:
            return {"error": "Analysis failed"}
    
    def _analyze_markdown_file(self, file_path):
        """Markdown file analysis"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = {
                "lines": len(content.split('\n')),
                "headings": len([line for line in content.split('\n') if line.strip().startswith('#')]),
                "code_blocks": content.count('```'),
                "links": content.count('[')
            }
            
            return analysis
        except:
            return {"error": "Analysis failed"}
    
    def _dev_pattern_detect(self, args):
        """Development pattern detection"""
        days = args.get("days", 7)
        
        try:
            # Recent commits analysis
            git_log = subprocess.run([
                "git", "log", f"--since={days} days ago", "--pretty=format:%s", "--no-merges"
            ], capture_output=True, text=True, cwd=self.repo_path)
            
            commits = git_log.stdout.strip().split('\n') if git_log.stdout else []
            
            patterns = {
                "commit_count": len(commits),
                "patterns": {},
                "recommendations": []
            }
            
            # Pattern analysis
            pattern_keywords = {
                "features": ["add", "implement", "create", "new"],
                "fixes": ["fix", "bug", "error", "issue"],
                "refactor": ["refactor", "cleanup", "improve", "optimize"],
                "docs": ["doc", "readme", "comment", "explain"],
                "auto": ["auto", "automatic", "batch"]
            }
            
            for pattern_name, keywords in pattern_keywords.items():
                count = sum(1 for commit in commits if any(kw in commit.lower() for kw in keywords))
                patterns["patterns"][pattern_name] = count
            
            # Recommendations based on patterns
            if patterns["patterns"].get("features", 0) > patterns["patterns"].get("fixes", 0) * 2:
                patterns["recommendations"].append("Consider adding more testing - feature development is outpacing fixes")
            
            if patterns["patterns"].get("auto", 0) > 5:
                patterns["recommendations"].append("Good automation habits detected - consider expanding automation")
            
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps(patterns, indent=2)
                }]
            }
        except Exception as e:
            return {"error": f"Pattern detection failed: {str(e)}"}
    
    def _dev_auto_optimize(self, args):
        """Auto-optimize development workflow"""
        focus = args.get("focus", "efficiency")
        
        optimizations = []
        
        if focus == "speed":
            optimizations = [
                "Enable git-daily quick commands for faster commits",
                "Set up file watchers for auto-reload",
                "Configure IDE shortcuts for common operations",
                "Use MCP tools for automated file operations"
            ]
        elif focus == "quality":
            optimizations = [
                "Enable pre-commit hooks for code quality",
                "Set up automated testing on commit",
                "Configure linters and formatters",
                "Add code review automation"
            ]
        elif focus == "efficiency":
            optimizations = [
                "Implement smart commit message generation",
                "Set up automated knowledge extraction",
                "Configure Obsidian auto-sync",
                "Enable pattern-based workflow automation"
            ]
        
        return {
            "content": [{
                "type": "text",
                "text": f"🎯 Optimization recommendations for {focus}:\n\n" + 
                       "\n".join(f"• {opt}" for opt in optimizations)
            }]
        }
    
    def _dev_knowledge_sync(self, args):
        """Sync development knowledge to Obsidian"""
        sync_type = args.get("type", "session")
        
        try:
            if sync_type == "session":
                # Current session info
                session_data = {
                    "timestamp": datetime.now().isoformat(),
                    "branch": self._get_current_branch(),
                    "uncommitted_files": self._get_uncommitted_count(),
                    "recent_commits": self._get_recent_commits(3)
                }
                
                # Save to Obsidian
                content = f"""# Dev Session - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Current State
- Branch: {session_data['branch']}
- Uncommitted files: {session_data['uncommitted_files']}

## Recent Work
{chr(10).join(f"- {commit}" for commit in session_data['recent_commits'])}

#development #session #auto-generated
"""
                
                self._save_to_obsidian("Dev_Sessions", f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md", content)
                
                return {
                    "content": [{
                        "type": "text",
                        "text": "✅ Development session synced to Obsidian"
                    }]
                }
            
            return {"error": f"Unknown sync type: {sync_type}"}
            
        except Exception as e:
            return {"error": f"Knowledge sync failed: {str(e)}"}
    
    def _get_current_branch(self):
        """Get current git branch"""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True, text=True, cwd=self.repo_path
            )
            return result.stdout.strip()
        except:
            return "unknown"
    
    def _get_uncommitted_count(self):
        """Get number of uncommitted files"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, cwd=self.repo_path
            )
            return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        except:
            return 0
    
    def _get_recent_commits(self, count):
        """Get recent commits"""
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", f"-{count}"],
                capture_output=True, text=True, cwd=self.repo_path
            )
            return result.stdout.strip().split('\n') if result.stdout else []
        except:
            return []
    
    def _save_to_obsidian(self, folder, filename, content):
        """Save content to Obsidian"""
        try:
            ps_command = f"""
$obsidianPath = "G:\\マイドライブ\\Obsidian Vault\\{folder}"
New-Item -ItemType Directory -Force -Path $obsidianPath | Out-Null
$content = @'
{content}
'@
$content | Out-File -FilePath "$obsidianPath\\{filename}" -Encoding UTF8
"""
            
            subprocess.run([
                "powershell.exe", "-Command", ps_command
            ], capture_output=True, timeout=10)
            
        except Exception:
            # Fallback to local storage
            os.makedirs(f"obsidian_sync/{folder}", exist_ok=True)
            with open(f"obsidian_sync/{folder}/{filename}", 'w', encoding='utf-8') as f:
                f.write(content)

def main():
    """MCP Server main execution"""
    server = MCPDevEfficiencyServer()
    
    # Stdin/Stdout communication for MCP protocol
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            response = server.handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON"}))
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()