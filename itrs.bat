@echo off
REM ITRS - Integrated Thinking-Research System
REM Easy Windows launcher

cd /d "%~dp0"

if "%1"=="" (
    echo.
    echo ITRS - Integrated Thinking-Research System
    echo ==========================================
    echo.
    echo Usage:
    echo   itrs think "Your thought here"     - Process a thought
    echo   itrs verify "Claim to verify"      - Verify a claim  
    echo   itrs analyze "Text to analyze"     - Analyze assumptions
    echo   itrs synthesize [count]            - Synthesize recent thoughts
    echo   itrs summary                       - Show session summary
    echo   itrs evolution [thought_id]        - Show thought evolution
    echo   itrs interactive                   - Enter interactive mode
    echo.
    echo Example:
    echo   itrs think "Is AI going to replace programmers?"
    echo.
    pause
    exit /b
)

python itrs_cli.py %*