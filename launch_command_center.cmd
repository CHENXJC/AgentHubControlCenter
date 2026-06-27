@echo off
setlocal

title AgentHubControlCenter V2

set "PROJECT_DIR=F:\AIProjects\AgentHubControlCenter"
set "PORT=8525"
set "URL=http://localhost:%PORT%"
set "VENV_PYTHON=%PROJECT_DIR%\.venv\Scripts\python.exe"
set "VENV_STREAMLIT=%PROJECT_DIR%\.venv\Scripts\streamlit.exe"

cd /d "%PROJECT_DIR%"
if errorlevel 1 (
    echo [ERROR] Could not switch to "%PROJECT_DIR%".
    echo Confirm the AgentHubControlCenter project folder exists.
    pause
    exit /b 1
)

if exist "%VENV_PYTHON%" (
    echo Starting AgentHubControlCenter V2 on %URL%
    echo Using virtual environment Python: %VENV_PYTHON%
    if /I not "%AGENTHUB_NO_BROWSER%"=="1" start "" "%URL%"
    "%VENV_PYTHON%" -m streamlit run app.py --server.port %PORT% --server.address localhost --server.headless true
    exit /b %ERRORLEVEL%
)

if exist "%VENV_STREAMLIT%" (
    echo Starting AgentHubControlCenter V2 on %URL%
    echo Using virtual environment Streamlit: %VENV_STREAMLIT%
    if /I not "%AGENTHUB_NO_BROWSER%"=="1" start "" "%URL%"
    "%VENV_STREAMLIT%" run app.py --server.port %PORT% --server.address localhost --server.headless true
    exit /b %ERRORLEVEL%
)

echo [ERROR] No local virtual environment runner was found.
echo Expected one of:
echo   %VENV_PYTHON%
echo   %VENV_STREAMLIT%
echo.
echo Create or repair the project .venv, then run this launcher again.
echo This launcher does not read .env, tokens, credentials, or secrets.
pause
exit /b 1
