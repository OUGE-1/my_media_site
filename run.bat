@echo off
title Django 服务启动器

:menu
cls
echo =========================================
echo          Django 服务启动器
echo =========================================
echo   [1] 启动 生存建造游戏 (端口 8000)
echo   [2] 启动 网易云音乐API (端口 8001)
echo   [3] 启动 本地影音网站 (端口 8002)   [新增]
echo   [4] 启动 全部服务
echo   [5] 关闭 全部服务
echo   [6] 退出
echo =========================================
set /p choice="请选择 [1-6]: "

if "%choice%"=="1" goto start_game
if "%choice%"=="2" goto start_music
if "%choice%"=="3" goto start_media
if "%choice%"=="4" goto start_all
if "%choice%"=="5" goto stop_all
if "%choice%"=="6" goto exit
echo 无效选项，请重新选择！
timeout /t 2 >nul
goto menu

:start_game
echo.
echo 正在启动 生存建造游戏 (端口 8000)...
start "生存建造游戏" cmd /k "cd /d D:\python_file\联机\survival_game && call D:\python_file\联机\venv\Scripts\activate.bat && python manage.py runserver 0.0.0.0:8000"
echo 服务已启动！
pause
goto menu

:start_music
echo.
echo 正在启动 网易云音乐API (端口 8001)...
start "网易云音乐API" cmd /k "cd /d D:\python\django\163api && call D:\python\django\my_media_site\.venv\Scripts\activate.bat && python manage.py runserver 0.0.0.0:8001"
echo 服务已启动！
pause
goto menu

:start_media
echo.
echo 正在启动 本地影音网站 (端口 8002)...
start "本地影音网站" cmd /k "cd /d D:\python\django\my_media_site && call D:\python\django\my_media_site\.venv\Scripts\activate.bat && python manage.py runserver 0.0.0.0:8002"
echo 服务已启动！
pause
goto menu

:start_all
echo.
echo 正在启动全部服务...
start "生存建造游戏" cmd /k "cd /d D:\python_file\联机\survival_game && call D:\python_file\联机\venv\Scripts\activate.bat && python manage.py runserver 0.0.0.0:8000"
start "网易云音乐API" cmd /k "cd /d D:\python_file\新建文件夹\Python_NetEaseMusicAPI && call D:\python_file\新建文件夹\Python_NetEaseMusicAPI\.venv\Scripts\activate.bat && python manage.py runserver 0.0.0.0:8001"
start "本地影音网站" cmd /k "cd /d D:\python\django\my_media_site && call D:\python\django\my_media_site\.venv\Scripts\activate.bat && python manage.py runserver 0.0.0.0:8002"
echo 全部服务已启动！
pause
goto menu

:stop_all
echo.
echo 正在关闭所有 Django 服务...
taskkill /F /IM python.exe 2>nul
echo 已关闭所有服务！
pause
goto menu

:exit
echo.
echo 再见！
timeout /t 1 >nul
exit