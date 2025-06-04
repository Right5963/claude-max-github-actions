@echo off
echo 🚀 Claude Max + GitHub Actions Repository Creation
echo ================================================

echo.
echo 📁 Current Implementation Status:
echo ✅ All files committed to local git
echo ✅ Perplexity MCP integration complete  
echo ✅ GitHub Actions workflow ready
echo ✅ Self-hosted runner prepared
echo ✅ Claude API direct integration implemented

echo.
echo 🎯 Next Steps:
echo.
echo 1. Go to https://github.com/new
echo 2. Repository name: claude-max-github-actions
echo 3. Description: Claude Max + GitHub Actions integration with Perplexity MCP
echo 4. Click "Create repository"
echo.
echo 5. Copy the repository URL (https://github.com/YOUR_USERNAME/claude-max-github-actions.git)

echo.
echo 6. Run the following commands in WSL:
echo.
echo    cd "/mnt/c/Claude Code/tool"
echo    git remote add origin https://github.com/YOUR_USERNAME/claude-max-github-actions.git
echo    git push -u origin master

echo.
echo 📋 GitHub Secrets to Configure:
echo.
echo Go to Repository Settings ^> Secrets and variables ^> Actions
echo.
echo PERPLEXITY_API_KEY: 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
echo ANTHROPIC_API_KEY: [Your Claude Max API Key]

echo.
echo 🏃‍♂️ Self-hosted Runner Setup:
echo.
echo After pushing to GitHub:
echo 1. Go to Repository Settings ^> Actions ^> Runners
echo 2. Click "New self-hosted runner"  
echo 3. Follow the setup instructions
echo 4. Or run: ./setup_github_actions_runner.sh

echo.
echo 🧪 First Test:
echo.
echo 1. Go to repository Actions tab
echo 2. Run "Claude MCP Research Automation"
echo 3. Input: "Claude MCP integration test"
echo 4. Verify automated research execution

echo.
echo 💰 @akira_papa_IT Methodology Implemented:
echo ✅ Self-hosted runners for free GitHub Actions
echo ✅ 5-minute timeout for efficiency  
echo ✅ Claude Max ^+ Perplexity Pro integration ($25/month total)
echo ✅ Enterprise-grade automation at minimal cost

echo.
echo 🎉 Ready to launch! Press any key to open GitHub...
pause >nul
start https://github.com/new

echo.
echo Repository creation page opened in browser.
echo Follow the steps above to complete setup.
echo.
pause