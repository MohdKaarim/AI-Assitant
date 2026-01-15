# Frontend Startup Script
$frontendPath = Join-Path $PSScriptRoot "frontend"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "
    Write-Host 'Starting AI Language Tutor Frontend...' -ForegroundColor Green;
    Set-Location -LiteralPath '$frontendPath';
    Write-Host 'Starting Angular development server...' -ForegroundColor Yellow;
    npm start;
    Read-Host 'Press Enter to exit';
"
