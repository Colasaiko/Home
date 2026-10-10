$html = [System.IO.File]::ReadAllText('9.html', [System.Text.Encoding]::UTF8)
$newContent = [System.IO.File]::ReadAllText('new_content.txt', [System.Text.Encoding]::UTF8)
$pattern = '(?is)(<div class="article-content">).*?(</div>\s*</article>)'
$replacement = "`$1`n" + $newContent + "`n        `$2"
$replaced = [System.Text.RegularExpressions.Regex]::Replace($html, $pattern, $replacement)
[System.IO.File]::WriteAllText('9.html', $replaced, [System.Text.Encoding]::UTF8)
