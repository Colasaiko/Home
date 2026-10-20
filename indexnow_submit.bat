@echo off
chcp 65001 >nul
title IndexNow 提交与 Sitemap 维护工具 (Windows 原生版)
color 0B

echo ============================================================
echo      IndexNow 提交与 Sitemap 维护工具 (Windows 原生版)
echo ============================================================
echo.
echo 请选择执行模式：
echo  [1] 增量提交模式 (默认 - 仅提交新增与最近改动页面，推荐)
echo  [2] 仅更新站点地图 (同步真实 lastmod 规范 sitemap.xml，不调用 API)
echo  [3] 模拟预览模式 (Dry Run - 仅预览将提交的链接，不发送请求)
echo  [4] 全量提交模式 (提交全站所有链接，谨慎使用)
echo.

set /p CHOICE="请输入数字选项 [1-4] (直接回车默认运行 [1] 增量提交): "
if "%CHOICE%"=="" set CHOICE=1

set MODE_ARG=Incremental
if "%CHOICE%"=="1" set MODE_ARG=Incremental
if "%CHOICE%"=="2" set MODE_ARG=SitemapOnly
if "%CHOICE%"=="3" set MODE_ARG=DryRun
if "%CHOICE%"=="4" set MODE_ARG=Full

echo.
echo 已选择模式: %MODE_ARG%
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0indexnow_submit.ps1" -Mode %MODE_ARG%

echo.
echo ============================================================
echo 执行完毕，按任意键退出窗口...
echo ============================================================
pause >nul
