# ==============================================================================
# IndexNow Batch Submit & Sitemap Generation Script (Windows PowerShell Native)
# ==============================================================================
[CmdletBinding()]
param (
    [string]$Domain = 'https://colasaiko.github.io/Home',
    [string]$Key = '75da1e777ebd2f0b784376f25d3501f9',
    [ValidateSet('Incremental', 'Full', 'SitemapOnly', 'DryRun')]
    [string]$Mode = 'Incremental',
    [switch]$DryRun,
    [int]$BatchSize = 1000
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host '==========================================================' -ForegroundColor Cyan
Write-Host '  IndexNow 搜索引擎提交与 Sitemap 维护程序' -ForegroundColor Cyan
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

if ($DryRun) {
    $Mode = 'DryRun'
}

Write-Host ('目标站点: ' + $baseUrl) -ForegroundColor Yellow
Write-Host ('Host标识: ' + $hostName) -ForegroundColor Yellow
Write-Host ('API 密钥: ' + $Key) -ForegroundColor Yellow
Write-Host ('运行模式: ' + $Mode) -ForegroundColor Yellow
Write-Host ''

$currentDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if (-not $currentDir) { $currentDir = (Get-Location).Path }

# 1. 验证 Key 文件
$keyFileName = $Key + '.txt'
$keyFilePath = Join-Path $currentDir $keyFileName

if (-not (Test-Path $keyFilePath)) {
    Write-Host ('[提示] 正在创建密钥校验文件: ' + $keyFileName) -ForegroundColor DarkYellow
    [System.IO.File]::WriteAllText($keyFilePath, $Key, [System.Text.Encoding]::ASCII)
    Write-Host '[成功] 已生成密钥校验文件！' -ForegroundColor Green
} else {
    Write-Host ('[OK] 密钥校验文件存在: ' + $keyFileName) -ForegroundColor Green
}

# 2. 读取 Git 真实提交历史，映射真实的真实修改日期 (杜绝批量伪造为当天)
Write-Host ''
Write-Host '正在读取 Git 真实版本记录获取 lastmod 日期...' -ForegroundColor Cyan
$gitDates = @{}
try {
    $gitLog = git log --name-only --format="COMMIT_DATE:%as" 2>$null
    if ($gitLog) {
        $curDate = ''
        foreach ($line in $gitLog) {
            $tLine = $line.Trim()
            if ($tLine.StartsWith('COMMIT_DATE:')) {
                $curDate = $tLine.Substring(12)
            } elseif ($tLine.Length -gt 0 -and $curDate) {
                $normPath = $tLine.Replace('\', '/')
                if (-not $gitDates.ContainsKey($normPath)) {
                    $gitDates[$normPath] = $curDate
                }
            }
        }
    }
} catch {
    Write-Host '[提示] Git 历史未读取或环境受限，将使用文件实际最后修改时间。' -ForegroundColor Yellow
}

# 3. 扫描全站 HTML 静态文件
Write-Host '正在扫描全站有效 HTML 页面...' -ForegroundColor Cyan

$htmlFiles = Get-ChildItem -Path $currentDir -Recurse -Filter *.html | Where-Object {
    $_.FullName -notmatch '[\\/]\.git[\\/]' -and
    $_.FullName -notmatch '[\\/]node_modules[\\/]' -and
    $_.FullName -notmatch '[\\/]\.gemini[\\/]' -and
    $_.FullName -notmatch '[\\/]scratch[\\/]' -and
    $_.FullName -notmatch '[\\/]scripts[\\/]' -and
    $_.Name -notmatch '^test' -and
    $_.Name -notmatch '^google'
}

$allEntries = [System.Collections.Generic.List[PSObject]]::new()
$skippedNoindex = 0

foreach ($file in $htmlFiles) {
    $relPath = $file.FullName.Substring($currentDir.Length).TrimStart('\', '/')
    $normRel = $relPath.Replace('\', '/')
    
    # 检查 noindex
    $rawContent = [System.IO.File]::ReadAllText($file.FullName)
    if ($rawContent -match 'name=["'']robots["''][^>]*content=["''][^"'']*noindex' -or $rawContent -match 'noindex,follow') {
        $skippedNoindex++
        continue
    }

    # 规范化 Canonical URL (目录页统一以 / 结尾，普通页保留 .html)
    $canonicalUrl = ''
    if ($normRel -eq 'index.html') {
        $canonicalUrl = $baseUrl + '/'
    } elseif ($normRel.EndsWith('/index.html')) {
        $dirOnly = $normRel.Substring(0, $normRel.Length - 11)
        $canonicalUrl = $baseUrl + '/' + $dirOnly + '/'
    } else {
        $canonicalUrl = $baseUrl + '/' + $normRel
    }

    # 确定真实 lastmod
    $fileLastmod = ''
    if ($gitDates.ContainsKey($normRel)) {
        $fileLastmod = $gitDates[$normRel]
    } else {
        $fileLastmod = $file.LastWriteTime.ToString('yyyy-MM-dd')
    }

    # 确定 Priority
    $priority = '0.8'
    $freq = 'weekly'
    if ($canonicalUrl -eq ($baseUrl + '/') -or $canonicalUrl -eq ($baseUrl + '/topic/tuijianjichang/')) {
        $priority = '1.0'
        $freq = 'daily'
    } elseif ($canonicalUrl -eq ($baseUrl + '/topic/tuijianjichang/comparison.html') -or
              $canonicalUrl -eq ($baseUrl + '/topic/tuijianjichang/brands/') -or
              $canonicalUrl -eq ($baseUrl + '/topic/tuijianjichang/faq/')) {
        $priority = '0.9'
        $freq = 'daily'
    } elseif ($canonicalUrl.StartsWith($baseUrl + '/topic/tuijianjichang/')) {
        $priority = '0.85'
        $freq = 'weekly'
    } else {
        $priority = '0.7'
        $freq = 'monthly'
    }

    $allEntries.Add([PSCustomObject]@{
        Url = $canonicalUrl
        Lastmod = $fileLastmod
        Priority = $priority
        ChangeFreq = $freq
        RelPath = $normRel
        FileObj = $file
    })
}

Write-Host ('扫描完成！共收集到 ' + $allEntries.Count + ' 个有效规范 URL (已排除 ' + $skippedNoindex + ' 个 noindex/重定向废弃页)。') -ForegroundColor Green

# 4. 生成规范 sitemap.xml
$sitemapPath = Join-Path $currentDir 'sitemap.xml'
Write-Host '正在同步生成全站规范 sitemap.xml...' -ForegroundColor Cyan

$xmlBuilder = [System.Text.StringBuilder]::new()
[void]$xmlBuilder.AppendLine('<?xml version="1.0" encoding="UTF-8"?>')
[void]$xmlBuilder.AppendLine('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

# 排序：首页及重点核心页在前
$sortedEntries = $allEntries | Sort-Object -Property @{Expression = {[double]$_.Priority}; Descending = $true}, @{Expression = {$_.Url}; Descending = $false}

foreach ($e in $sortedEntries) {
    [void]$xmlBuilder.AppendLine('  <url>')
    [void]$xmlBuilder.AppendLine(('    <loc>' + $e.Url + '</loc>'))
    [void]$xmlBuilder.AppendLine(('    <lastmod>' + $e.Lastmod + '</lastmod>'))
    [void]$xmlBuilder.AppendLine(('    <changefreq>' + $e.ChangeFreq + '</changefreq>'))
    [void]$xmlBuilder.AppendLine(('    <priority>' + $e.Priority + '</priority>'))
    [void]$xmlBuilder.AppendLine('  </url>')
}
[void]$xmlBuilder.AppendLine('</urlset>')

[System.IO.File]::WriteAllText($sitemapPath, $xmlBuilder.ToString(), [System.Text.Encoding]::UTF8)
Write-Host ('[成功] 已生成最新全站地图: sitemap.xml (共 ' + $sortedEntries.Count + ' 条真实 URL)') -ForegroundColor Green

# 5. 更新 robots.txt
$robotsPath = Join-Path $currentDir 'robots.txt'
$robotsContent = "User-agent: *" + [System.Environment]::NewLine + "Allow: /" + [System.Environment]::NewLine + [System.Environment]::NewLine + "# Sitemap" + [System.Environment]::NewLine + "Sitemap: " + $baseUrl + "/sitemap.xml" + [System.Environment]::NewLine
[System.IO.File]::WriteAllText($robotsPath, $robotsContent, [System.Text.Encoding]::UTF8)
Write-Host '[成功] 已同步确认 robots.txt' -ForegroundColor Green

if ($Mode -eq 'SitemapOnly') {
    Write-Host ''
    Write-Host '[完成] 仅生成 Sitemap 模式已结束，未向 IndexNow API 提交请求。' -ForegroundColor Cyan
    exit 0
}

# 6. 计算待提交的 URL 列表 (增量 vs 全量)
$targetSubmitUrls = [System.Collections.Generic.List[string]]::new()

if ($Mode -eq 'Full') {
    Write-Host ''
    Write-Host '[模式] 全量提交模式 (提交全部 ' + $sortedEntries.Count + ' 条链接)' -ForegroundColor Yellow
    foreach ($item in $sortedEntries) {
        $targetSubmitUrls.Add($item.Url)
    }
} else {
    Write-Host ''
    Write-Host '[模式] 增量提交模式 (只提取本地改动、新增或最近 3 天更新的页面)...' -ForegroundColor Cyan
    
    # 查找本地未提交改动
    $gitStatusFiles = @()
    try {
        $statusOut = git status --porcelain 2>$null
        if ($statusOut) {
            foreach ($sLine in $statusOut) {
                if ($sLine.Length -ge 4) {
                    $gitStatusFiles += ($sLine.Substring(3).Trim().Replace('\', '/'))
                }
            }
        }
    } catch {}

    # 查找最新一次 commit 的改动
    $recentCommitFiles = @()
    try {
        $diffOut = git diff --name-only HEAD~1 2>$null
        if ($diffOut) {
            foreach ($dLine in $diffOut) {
                $recentCommitFiles += ($dLine.Trim().Replace('\', '/'))
            }
        }
    } catch {}

    $cutoffDate = (Get-Date).AddDays(-3).ToString('yyyy-MM-dd')

    foreach ($item in $sortedEntries) {
        $isModified = $false
        if ($gitStatusFiles -contains $item.RelPath) {
            $isModified = $true
        } elseif ($recentCommitFiles -contains $item.RelPath) {
            $isModified = $true
        } elseif ($item.Lastmod -ge $cutoffDate) {
            $isModified = $true
        }

        if ($isModified) {
            $targetSubmitUrls.Add($item.Url)
        }
    }
}

$submitCount = $targetSubmitUrls.Count
Write-Host ('待提交有效链接数: ' + $submitCount) -ForegroundColor Green

if ($submitCount -eq 0) {
    Write-Host '[提示] 未检测到需要提交的改动页面。站点地图已保持最新，无需向 IndexNow 重复提交旧内容。' -ForegroundColor Cyan
    exit 0
}

if ($Mode -eq 'DryRun') {
    Write-Host ''
    Write-Host '==========================================================' -ForegroundColor Yellow
    Write-Host '  [DRY RUN 预览模式] 以下链接将被提交 (未向 API 发送实际请求)：' -ForegroundColor Yellow
    Write-Host '==========================================================' -ForegroundColor Yellow
    foreach ($u in $targetSubmitUrls) {
        Write-Host ('  - ' + $u)
    }
    Write-Host '==========================================================' -ForegroundColor Yellow
    exit 0
}

# 7. 向 IndexNow 官方 API 提交
$batches = [Math]::Ceiling($submitCount / $BatchSize)
Write-Host ''
Write-Host '==========================================================' -ForegroundColor Cyan
Write-Host ('  向 IndexNow API 提交 (共 ' + $batches + ' 批次)...') -ForegroundColor Cyan
Write-Host '==========================================================' -ForegroundColor Cyan

for ($i = 0; $i -lt $batches; $i++) {
    $startIndex = $i * $BatchSize
    $count = [Math]::Min($BatchSize, $submitCount - $startIndex)
    $currentBatchUrls = $targetSubmitUrls.GetRange($startIndex, $count)
    
    $payloadObj = @{
        host = $hostName
        key = $Key
        keyLocation = ($baseUrl + '/' + $Key + '.txt')
        urlList = $currentBatchUrls
    }

    $jsonBody = $payloadObj | ConvertTo-Json -Depth 5 -Compress

    $batchNum = $i + 1
    Write-Host ('[批次 ' + $batchNum + '/' + $batches + '] 提交 ' + $count + ' 条 URL...') -NoNewline

    $submitted = $false
    $primaryEndpoint = 'https://api.indexnow.org/indexnow'
    $fallbackEndpoint = 'https://www.bing.com/indexnow'

    try {
        $response = Invoke-RestMethod -Uri $primaryEndpoint -Method Post -Body $jsonBody -ContentType 'application/json; charset=utf-8' -TimeoutSec 15 -ErrorAction Stop
        Write-Host ' -> [成功] 200 OK (已提交至 api.indexnow.org)' -ForegroundColor Green
        $submitted = $true
    } catch {
        $statusCode = 0
        $statusDesc = ''
        if ($_.Exception -and $_.Exception.Response) {
            $statusCode = [int]$_.Exception.Response.StatusCode
            $statusDesc = $_.Exception.Response.StatusDescription
        }

        if ($statusCode -eq 200 -or $statusCode -eq 202) {
            Write-Host (' -> [成功] ' + $statusCode + ' ' + $statusDesc + ' (已成功接收进入索引队列)') -ForegroundColor Green
            $submitted = $true
        } else {
            Write-Host (' -> [异常 ' + $statusCode + ': ' + $statusDesc + '] 尝试备用网关...') -ForegroundColor Yellow
            try {
                $response = Invoke-RestMethod -Uri $fallbackEndpoint -Method Post -Body $jsonBody -ContentType 'application/json; charset=utf-8' -TimeoutSec 15 -ErrorAction Stop
                Write-Host ' -> [成功] 200 OK (已提交至 www.bing.com/indexnow)' -ForegroundColor Green
                $submitted = $true
            } catch {
                $subStatus = 0
                if ($_.Exception -and $_.Exception.Response) {
                    $subStatus = [int]$_.Exception.Response.StatusCode
                }
                if ($subStatus -eq 200 -or $subStatus -eq 202) {
                    Write-Host (' -> [成功] ' + $subStatus + ' (备用网关接收成功)') -ForegroundColor Green
                    $submitted = $true
                } else {
                    Write-Host (' -> [失败] 状态码: ' + $subStatus + ' / ' + $_.Exception.Message) -ForegroundColor Red
                }
            }
        }
    }
}

Write-Host ''
Write-Host '==========================================================' -ForegroundColor Cyan
Write-Host '  IndexNow 提交执行完毕！' -ForegroundColor Green
Write-Host ('  - 实际提交 URL 数: ' + $submitCount) -ForegroundColor Green
Write-Host ('  - 验证密钥文件地址: ' + $baseUrl + '/' + $Key + '.txt') -ForegroundColor Green
Write-Host ('  - 规范站点地图地址: ' + $baseUrl + '/sitemap.xml') -ForegroundColor Green
Write-Host '  - 注意事项: API 成功接收代表搜索引擎已收到更新信号，' -ForegroundColor Yellow
Write-Host '              实际抓取与展示取决于 Bing 独立算法及调度排期。' -ForegroundColor Yellow
Write-Host '==========================================================' -ForegroundColor Cyan
