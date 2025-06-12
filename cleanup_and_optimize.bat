@echo off
chcp 65001 >nul
echo.
echo ========================================
echo     DeerFlow 文件清理和优化工具
echo ========================================
echo.

REM 检查Python是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请确保Python已安装并添加到PATH
    pause
    exit /b 1
)

:menu
echo 请选择操作:
echo.
echo 1. 📁 整理现有文件到新目录结构
echo 2. 🧹 清理临时文件 (24小时前)
echo 3. 🧹 清理临时文件 (12小时前)
echo 4. 📊 显示存储统计信息
echo 5. 📋 列出最近的输出文件
echo 6. 💾 创建备份
echo 7. 🚀 执行完整优化 (整理+统计+备份)
echo 8. 🔍 预览清理操作 (不实际删除)
echo 9. ❌ 退出
echo.
set /p choice="输入选择 (1-9): "

if "%choice%"=="1" goto organize
if "%choice%"=="2" goto cleanup24
if "%choice%"=="3" goto cleanup12
if "%choice%"=="4" goto stats
if "%choice%"=="5" goto list
if "%choice%"=="6" goto backup
if "%choice%"=="7" goto optimize
if "%choice%"=="8" goto preview
if "%choice%"=="9" goto exit

echo ❌ 无效选择，请重新输入
echo.
goto menu

:organize
echo.
echo 📁 开始整理现有文件...
python scripts/cleanup.py --organize
echo.
pause
goto menu

:cleanup24
echo.
echo 🧹 清理24小时前的临时文件...
python scripts/cleanup.py --cleanup --hours 24
echo.
pause
goto menu

:cleanup12
echo.
echo 🧹 清理12小时前的临时文件...
python scripts/cleanup.py --cleanup --hours 12
echo.
pause
goto menu

:stats
echo.
echo 📊 显示存储统计信息...
python scripts/cleanup.py --stats
echo.
pause
goto menu

:list
echo.
echo 📋 列出最近的输出文件...
python scripts/cleanup.py --list 15
echo.
pause
goto menu

:backup
echo.
echo 💾 创建备份...
python scripts/cleanup.py --backup
echo.
pause
goto menu

:optimize
echo.
echo 🚀 执行完整优化...
echo.
echo 步骤 1/3: 整理文件...
python scripts/cleanup.py --organize
echo.
echo 步骤 2/3: 显示统计...
python scripts/cleanup.py --stats
echo.
echo 步骤 3/3: 创建备份...
python scripts/cleanup.py --backup
echo.
echo ✅ 优化完成！
pause
goto menu

:preview
echo.
echo 🔍 预览清理操作 (不实际删除)...
python scripts/cleanup.py --cleanup --dry-run
echo.
pause
goto menu

:exit
echo.
echo 👋 感谢使用 DeerFlow 文件管理工具！
echo.
pause
exit /b 0 
 