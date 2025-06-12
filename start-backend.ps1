# PowerShell script to start the DeerFlow backend server
# Usage: .\start-backend.ps1 [--port PORT] [--host HOST] [--reload] [--eko] [--eko-debug]

param(
    [int]$Port = 8000,
    [string]$ServerHost = "localhost", 
    [switch]$Reload,
    [switch]$Eko,
    [switch]$EkoDebug,
    [switch]$Help
)

# Show help information
if ($Help) {
    Write-Host "DeerFlow Backend Server Startup Script" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage: .\start-backend.ps1 [OPTIONS]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  -Port NUMBER       Port to bind server to (default: 8000)"
    Write-Host "  -ServerHost ADDR   Host address to bind to (default: localhost)"
    Write-Host "  -Reload            Enable auto-reload for development"
    Write-Host "  -Eko               Enable Eko Event-Driven Architecture"
    Write-Host "  -EkoDebug          Enable Eko debug mode (implies -Eko)"
    Write-Host "  -Help              Show this help message"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\start-backend.ps1                              # Start with defaults"
    Write-Host "  .\start-backend.ps1 -Port 3000 -Reload           # Dev mode on port 3000"
    Write-Host "  .\start-backend.ps1 -Eko                         # Enable Eko framework"
    Write-Host "  .\start-backend.ps1 -EkoDebug                    # Enable Eko with debug"
    Write-Host "  .\start-backend.ps1 -ServerHost 0.0.0.0         # Bind to all interfaces"
    exit 0
}

Write-Host "🦌 Starting DeerFlow Backend Server..." -ForegroundColor Green

# Set Eko environment variables if requested
if ($EkoDebug) {
    Write-Host "🔧 Enabling Eko Event-Driven Architecture with Debug Mode" -ForegroundColor Yellow
    $env:EKO_ENABLED = "true"
    $env:EKO_DEBUG = "true"
    $env:EKO_LANGGRAPH_COMPAT = "true"
    $env:EKO_METRICS_ENABLED = "true"
    $Eko = $true
} elseif ($Eko) {
    Write-Host "🔧 Enabling Eko Event-Driven Architecture" -ForegroundColor Yellow  
    $env:EKO_ENABLED = "true"
    $env:EKO_DEBUG = "false"
    $env:EKO_LANGGRAPH_COMPAT = "true"
    $env:EKO_METRICS_ENABLED = "true"
} else {
    Write-Host "🔧 Starting in Traditional Mode (Eko disabled)" -ForegroundColor Blue
    $env:EKO_ENABLED = "false"
}

# Build uvicorn command
$uvicornArgs = @(
    "src.server:app"
    "--host", $ServerHost
    "--port", $Port.ToString()
)

if ($Reload) {
    $uvicornArgs += "--reload"
    Write-Host "🔄 Auto-reload enabled for development" -ForegroundColor Blue
}

# Show startup configuration
Write-Host ""
Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  Host: $ServerHost" -ForegroundColor White
Write-Host "  Port: $Port" -ForegroundColor White
Write-Host "  Reload: $($Reload.ToString())" -ForegroundColor White
Write-Host "  Eko Framework: $($env:EKO_ENABLED)" -ForegroundColor White
if ($env:EKO_ENABLED -eq "true") {
    Write-Host "  Eko Debug: $($env:EKO_DEBUG)" -ForegroundColor White
    Write-Host ""
    Write-Host "🎯 Eko API Endpoints will be available at:" -ForegroundColor Green
    Write-Host "  - http://${ServerHost}:${Port}/api/eko/status" -ForegroundColor Gray
    Write-Host "  - http://${ServerHost}:${Port}/api/eko/events/{thread_id}" -ForegroundColor Gray
    Write-Host "  - http://${ServerHost}:${Port}/api/eko/metrics" -ForegroundColor Gray
}
Write-Host ""

# Check if Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python not found. Please install Python 3.8+ and try again." -ForegroundColor Red
    exit 1
}

# Check if uvicorn is available
try {
    python -m uvicorn --help | Out-Null
} catch {
    Write-Host "❌ uvicorn not found. Please install it with: pip install uvicorn" -ForegroundColor Red
    exit 1
}

Write-Host "🚀 Starting server..." -ForegroundColor Green
Write-Host "   URL: http://${ServerHost}:${Port}" -ForegroundColor Yellow
Write-Host "   Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

# Start the server
try {
    python -m uvicorn @uvicornArgs
} catch {
    Write-Host "❌ Failed to start server: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} 