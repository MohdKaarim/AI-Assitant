# Backend Startup Script
$backendPath = Join-Path $PSScriptRoot "backend"
$activatePath = Join-Path $backendPath "venv\Scripts\Activate.ps1"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "
    Write-Host 'Starting AI Language Tutor Backend...' -ForegroundColor Green;
    Set-Location -LiteralPath '$backendPath';
    if (Test-Path '$activatePath') {
        Write-Host 'Activating virtual environment...' -ForegroundColor Yellow;
        & '$activatePath';
    } else {
        Write-Host 'Error: Virtual environment not found!' -ForegroundColor Red;
        Read-Host 'Press Enter to exit';
        exit;
    }
    Write-Host 'Starting Uvicorn server...' -ForegroundColor Yellow;
    python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000;
    Read-Host 'Press Enter to exit';
"
