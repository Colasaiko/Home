@echo off
chcp 65001 >nul
title IndexNow 全站自动化提交工具 (无需 Python 环境)
color 0B

echo ============================================================
echo           IndexNow 批量提交工具 (Windows 原生极速版)
echo ============================================================
echo.
echo 提示：
echo 1. 本工具不需要电脑安装 Python，使用 Windows 自带的 PowerShell 运行。
echo 2. 如果您的站点有自定义域名（如 https://xxx.com），可在下方输入。
echo    如果直接回车，将使用默认配置或当前预设。
echo.

set /p USER_DOMAIN="请输入您的网站完整域名 (默认: https://colasaiko.github.io/Home，直接回车使用默认值): "

if "%USER_DOMAIN%"=="" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0indexnow_submit.ps1"
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0indexnow_submit.ps1" -Domain "%USER_DOMAIN%"
)

echo.
echo ============================================================
echo 执行完毕，按任意键退出窗口...
echo ============================================================
pause >nul
