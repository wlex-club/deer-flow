@echo off
REM Start DeerFlow with Eko Event-Driven Architecture enabled
REM This script provides a convenient way to launch DeerFlow with Eko framework

echo.
echo 🦌 DeerFlow with Eko Event-Driven Architecture
echo ===============================================

REM Set Eko environment variables
set EKO_ENABLED=true
set EKO_DEBUG=true
set EKO_LANGGRAPH_COMPAT=true
set EKO_METRICS_ENABLED=true
set EKO_EVENT_STORE=memory
set EKO_EVENT_BUS=memory

echo 🔧 Eko Configuration:
echo    - Framework: ENABLED
echo    - Debug Mode: ON
echo    - LangGraph Compatibility: ON
echo    - Metrics Collection: ON
echo    - Event Store: Memory
echo    - Event Bus: Memory
echo.

echo 🎯 Eko API Endpoints will be available at:
echo    - http://localhost:8000/api/eko/status
echo    - http://localhost:8000/api/eko/events/{thread_id}
echo    - http://localhost:8000/api/eko/metrics
echo.

echo 🚀 Starting DeerFlow backend server with Eko...
echo    Press Ctrl+C to stop the server
echo.

REM Start the server using Python directly
python -m uvicorn src.server:app --host localhost --port 8000 --reload

echo.
echo 🛑 Server has stopped.
pause 