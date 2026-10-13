# ==============================================================================
# IndexNow Batch Submit Script (Windows PowerShell Native)
# ==============================================================================
[CmdletBinding()]
param (
    [string]$Domain = 'https://colasaiko.github.io/Home',
    [string]$Key = '75da1e777ebd2f0b784376f25d3501f9',
    [int]$BatchSize = 1000
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host '==========================================================' -ForegroundColor Cyan
Write-Host '  IndexNow 搜索引擎批量提交程序 (PowerShell 原生引擎)' -ForegroundColor Cyan
Write-Host '==========================================================' -ForegroundColor Cyan

$cleanDomain = $Domain.Trim()
if ($cleanDomain.StartsWith('http://', [System.StringComparison]::OrdinalIgnoreCase) -or $cleanDomain.StartsWith('https://', [System.StringComparison]::OrdinalIgnoreCase)) {
    $uri = [System.Uri]$cleanDomain
    $hostName = $uri.Host
    $baseUrl = $cleanDomain.TrimEnd('/')
} else {
    $hostName = $cleanDomain.TrimEnd('/')
    $baseUrl = 'https://' + $hostName
}

Write-Host ('目标站点: ' + $baseUrl) -ForegroundColor Yellow
Write-Host ('Host标识: ' + $hostName) -ForegroundColor Yellow
Write-Host ('API 密钥: ' + $Key) -ForegroundColor Yellow
Write-Host ''

$currentDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if (-not $currentDir) { $currentDir = (Get-Location).Path }

$keyFileName = $Key + '.txt'
$keyFilePath = Join-Path $currentDir $keyFileName

if (-not (Test-Path $keyFilePath)) {
    Write-Host ('[提示] 正在创建密钥校验文件: ' + $keyFileName) -ForegroundColor DarkYellow
    [System.IO.File]::WriteAllText($keyFilePath, $Key, [System.Text.Encoding]::ASCII)
    Write-Host '[成功] 已生成密钥校验文件！' -ForegroundColor Green
} else {
    Write-Host ('[OK] 密钥校验文件存在: ' + $keyFileName) -ForegroundColor Green
}

Write-Host ''
Write-Host '正在扫描全站 HTML 静态页面...' -ForegroundColor Cyan

$htmlFiles = Get-ChildItem -Path $currentDir -Recurse -Filter *.html | Where-Object {
    $_.FullName -notmatch '[\\/]\.git[\\/]' -and
    $_.FullName -notmatch '[\\/]node_modules[\\/]' -and
    $_.FullName -notmatch '[\\/]\.gemini[\\/]' -and
    $_.FullName -notmatch '[\\/]scratch[\\/]'
}

$urlList = [System.Collections.Generic.List[string]]::new()

foreach ($file in $htmlFiles) {
    $relPath = $file.FullName.Substring($currentDir.Length).TrimStart('\', '/')
    $relUrl = $relPath.Replace('\', '/')
    if ($relUrl -eq 'index.html') {
        $urlList.Add($baseUrl + '/')
    } else {
        $urlList.Add($baseUrl + '/' + $relUrl)
    }
}

$totalCount = $urlList.Count
Write-Host ('扫描完成！共收集到 ' + $totalCount + ' 个待提交网页链接。') -ForegroundColor Green

if ($totalCount -eq 0) {
    Write-Host '[警告] 未发现任何有效的 HTML 页面，程序退出。' -ForegroundColor Red
    exit 0
}

# 生成 sitemap.xml
$sitemapPath = Join-Path $currentDir 'sitemap.xml'
Write-Host '正在同步生成本地全站 sitemap.xml...' -ForegroundColor Cyan

$xmlBuilder = [System.Text.StringBuilder]::new()
[void]$xmlBuilder.AppendLine('<?xml version="1.0" encoding="UTF-8"?>')
[void]$xmlBuilder.AppendLine('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

$nowDate = (Get-Date).ToString('yyyy-MM-dd')
foreach ($u in $urlList) {
    [void]$xmlBuilder.AppendLine('  <url>')
    [void]$xmlBuilder.AppendLine(('    <loc>' + $u + '</loc>'))
    [void]$xmlBuilder.AppendLine(('    <lastmod>' + $nowDate + '</lastmod>'))
    [void]$xmlBuilder.AppendLine('    <changefreq>weekly</changefreq>')
    if ($u -eq ($baseUrl + '/')) {
        [void]$xmlBuilder.AppendLine('    <priority>1.0</priority>')
    } elseif ($u -match 'tuijianjichang') {
        [void]$xmlBuilder.AppendLine('    <priority>0.9</priority>')
    } else {
        [void]$xmlBuilder.AppendLine('    <priority>0.8</priority>')
    }
    [void]$xmlBuilder.AppendLine('  </url>')
}
[void]$xmlBuilder.AppendLine('</urlset>')

[System.IO.File]::WriteAllText($sitemapPath, $xmlBuilder.ToString(), [System.Text.Encoding]::UTF8)
Write-Host ('[成功] 已生成最新全站地图: sitemap.xml (包含 ' + $totalCount + ' 条链接)') -ForegroundColor Green

# 更新 robots.txt
$robotsPath = Join-Path $currentDir 'robots.txt'
$robotsContent = 'User-agent: *' + [System.Environment]::NewLine + 'Allow: /' + [System.Environment]::NewLine + [System.Environment]::NewLine + '# Sitemap' + [System.Environment]::NewLine + 'Sitemap: ' + $baseUrl + '/sitemap.xml' + [System.Environment]::NewLine
[System.IO.File]::WriteAllText($robotsPath, $robotsContent, [System.Text.Encoding]::UTF8)
Write-Host '[成功] 已同步更新 robots.txt' -ForegroundColor Green

# 提交至 IndexNow
$endpoints = @(
    'https://api.indexnow.org/indexnow',
    'https://www.bing.com/indexnow'
)

$batches = [Math]::Ceiling($totalCount / $BatchSize)
Write-Host ''
Write-Host '==========================================================' -ForegroundColor Cyan
Write-Host ('  开始向 IndexNow 官方 API 批量提交 (共 ' + $batches + ' 批次)') -ForegroundColor Cyan
Write-Host '==========================================================' -ForegroundColor Cyan

for ($i = 0; $i -lt $batches; $i++) {
    $startIndex = $i * $BatchSize
    $count = [Math]::Min($BatchSize, $totalCount - $startIndex)
    $currentBatchUrls = $urlList.GetRange($startIndex, $count)
    
    $payloadObj = @{
        host = $hostName
        key = $Key
        keyLocation = ($baseUrl + '/' + $Key + '.txt')
        urlList = $currentBatchUrls
    }

    $jsonBody = $payloadObj | ConvertTo-Json -Depth 5 -Compress

    $batchNum = $i + 1
    Write-Host ('[批次 ' + $batchNum + '/' + $batches + '] 正在提交 ' + $count + ' 条 URL...') -NoNewline

    $submitted = $false
    foreach ($apiEndpoint in $endpoints) {
        try {
            $response = Invoke-RestMethod -Uri $apiEndpoint -Method Post -Body $jsonBody -ContentType 'application/json; charset=utf-8' -TimeoutSec 15 -ErrorAction Stop
            Write-Host ' -> 提交成功!' -ForegroundColor Green
            $submitted = $true
            break
        } catch {
            $statusCode = 0
            if ($_.Exception -and $_.Exception.Response) {
                $statusCode = $_.Exception.Response.StatusCode.value__
            }
            if ($statusCode -eq 200 -or $statusCode -eq 202) {
                Write-Host (' -> 提交成功 (' + $statusCode + ')') -ForegroundColor Green
                $submitted = $true
                break
            }
        }
    }

    if (-not $submitted) {
        Write-Host ' -> [提示] 远程 API 响应或尚未配置真实域名 (本地测试属正常现象)' -ForegroundColor Yellow
    }
}

Write-Host ''
Write-Host '==========================================================' -ForegroundColor Cyan
Write-Host '  IndexNow 提交执行完毕！' -ForegroundColor Green
Write-Host ('  - 提交 URL 总数: ' + $totalCount) -ForegroundColor Green
Write-Host ('  - 密钥校验地址: ' + $baseUrl + '/' + $Key + '.txt') -ForegroundColor Green
Write-Host ('  - 站点地图地址: ' + $baseUrl + '/sitemap.xml') -ForegroundColor Green
Write-Host '==========================================================' -ForegroundColor Cyan