# Run the AI Job Matcher application
# This script activates the virtual environment and starts the backend server

Write-Host "🤖 Starting AI Job Matcher..." -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    . ".\venv\Scripts\Activate.ps1"
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "✗ Virtual environment not found. Run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Start the application
Write-Host "Starting FastAPI server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Application will be available at:" -ForegroundColor Green
Write-Host "  → http://localhost:8000" -ForegroundColor Cyan
Write-Host "  → http://localhost:8000/docs (API Docs)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Default credentials:" -ForegroundColor Yellow
Write-Host "  Email: recruiter@jobmatcher.com" -ForegroundColor White
Write-Host "  Password: recruiter123" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python backend/main.py
