# Claude Usage Stats Extension Troubleshooting Guide

## Current Status ✅

The extension is properly installed and configured:

- **Extension Location**: `~/.cursor-server/extensions/claude-usage-stats/`
- **Status File**: `/mnt/c/Claude Code/tool/.claude_status` ✅ EXISTS
- **Usage Tracker**: Working correctly ✅
- **Package Configuration**: Valid ✅

## Debugging Steps

### 1. Check Extension in Cursor

1. **Open Cursor**
2. **Check Extensions Panel**:
   - Press `Ctrl+Shift+X` (or `Cmd+Shift+X` on Mac)
   - Search for "claude usage"
   - Verify the extension appears and is **enabled**
   - If disabled, click the "Enable" button

3. **Check Developer Console**:
   - Press `F12` or `Ctrl+Shift+I`
   - Go to **Console** tab
   - Look for activation message: `"Claude Usage Stats extension is now active!"`
   - Look for any error messages

### 2. Manual Extension Reload

If the extension isn't working:

1. **Reload Window**:
   - Press `Ctrl+Shift+P` (Command Palette)
   - Type: `Developer: Reload Window`
   - Press Enter

2. **Disable/Enable Extension**:
   - Go to Extensions panel (`Ctrl+Shift+X`)
   - Find "Claude Usage Stats"
   - Click "Disable" then "Enable"

### 3. Check Status Bar

The extension should show **two items** in the status bar (bottom right):

1. **Usage Stats**: `$(icon) Claude: O0/200 S0/300 ⏱️4:59:59`
2. **Launch Button**: `$(terminal) Claude`

### 4. Test Extension Commands

Open Command Palette (`Ctrl+Shift+P`) and test these commands:

- `Claude Usage Stats: Show Details`
- `Claude Usage Stats: Launch Claude Code`
- `Claude Usage Stats: Switch Model`
- `Claude Usage Stats: Reset Session`

### 5. Check Configuration

1. **Open Settings**: `Ctrl+,`
2. **Search**: "Claude Usage Stats"
3. **Verify Settings**:
   - Update Interval: 30 seconds
   - Status File: `/mnt/c/Claude Code/tool/.claude_status`
   - Show Tokens: true
   - Warning Threshold: 70%
   - Critical Threshold: 90%

## Common Issues & Solutions

### Issue 1: Status Bar Items Not Appearing

**Symptoms**: No Claude usage info in status bar

**Solutions**:
1. Check if extension is enabled in Extensions panel
2. Reload Cursor window (`Developer: Reload Window`)
3. Check Developer Console for error messages
4. Verify status file exists and is readable

### Issue 2: "No Data" Message

**Symptoms**: Status bar shows "Claude: No Data"

**Solutions**:
1. Run usage tracker to generate status file:
   ```bash
   timeout 5 python3 "/mnt/c/Claude Code/tool/claude_usage_tracker.py"
   ```
2. Verify status file exists: `/mnt/c/Claude Code/tool/.claude_status`
3. Check file permissions and content

### Issue 3: Extension Not Loading

**Symptoms**: Extension doesn't appear in Extensions panel

**Solutions**:
1. Reinstall extension:
   ```bash
   cd "/mnt/c/Claude Code/tool/claude-usage-extension"
   ./install.sh
   ```
2. Restart Cursor completely (close all windows)
3. Check VS Code version compatibility (requires ^1.74.0)

### Issue 4: Status File Errors

**Symptoms**: Extension shows error status

**Solutions**:
1. Regenerate status file:
   ```bash
   python3 "/mnt/c/Claude Code/tool/claude_usage_tracker.py" show
   ```
2. Check file format:
   ```bash
   cat "/mnt/c/Claude Code/tool/.claude_status" | python3 -m json.tool
   ```
3. Verify path in extension settings

## Debug Commands

### Test Extension Installation
```bash
node "/mnt/c/Claude Code/tool/extension_debug.js"
```

### Test Usage Tracker
```bash
python3 "/mnt/c/Claude Code/tool/claude_usage_tracker.py" show
```

### Check Status File
```bash
cat "/mnt/c/Claude Code/tool/.claude_status"
```

### Reinstall Extension
```bash
cd "/mnt/c/Claude Code/tool/claude-usage-extension"
./install.sh
```

## Expected Behavior

When working correctly, you should see:

1. **Status Bar** (right side):
   - Green/Yellow/Orange/Red icon with usage stats
   - Claude launch button
   
2. **Tooltip** (hover over status):
   ```
   Claude Code Usage Statistics
   Session: 20250601_11
   Time Remaining: 4:59:59
   
   🔥 Opus 4: 0/200 (0.0%)
   ⚡ Sonnet 4: 0/300 (0.0%)
   
   Tokens: Opus 0 | Sonnet 0
   
   Click for detailed view
   ```

3. **Commands** available in Command Palette

4. **Detailed View** when clicking status bar item

## Still Not Working?

If the extension still doesn't appear after following all steps:

1. **Check Cursor Logs**:
   - Look in Cursor settings/logs for extension loading errors
   - Check if there are any conflicting extensions

2. **Manual Debug**:
   - Open Developer Tools in Cursor
   - Check Console and Sources tabs for errors
   - Look for the extension in the Sources tab

3. **Alternative Installation**:
   - Try installing as a VSIX package
   - Use VS Code directly instead of Cursor to test

4. **Contact Support**:
   - Provide the output of `extension_debug.js`
   - Include any error messages from Developer Console
   - Specify Cursor version and OS

## Extension Features

When working, the extension provides:

- **Real-time usage monitoring** (updates every 30 seconds)
- **Visual status indicators** (color-coded warnings)
- **One-click Claude Code launch** with multiple options
- **Detailed statistics view** with charts and graphs
- **Session management** (continue, save, restore)
- **Model switching** (Opus ↔ Sonnet ↔ Free alternatives)
- **Smart warnings** and usage optimization suggestions