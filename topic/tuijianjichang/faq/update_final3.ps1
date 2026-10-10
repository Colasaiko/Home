$files = @(
    "jichang-disney.html",
    "jichang-gemini.html",
    "jichang-ipipshenme-qubie.html"
)

$contents = @(
    ([System.IO.File]::ReadAllText("$PSScriptRoot\disney_content.html")),
    ([System.IO.File]::ReadAllText("$PSScriptRoot\gemini_content.html")),
    ([System.IO.File]::ReadAllText("$PSScriptRoot\ip_content.html"))
)

$utf8NoBom = New-Object System.Text.UTF8Encoding $false

for ($i = 0; $i -lt 3; $i++) {
    $file = "$PSScriptRoot\" + $files[$i]
    $content = [System.IO.File]::ReadAllText($file)
    
    # regex replace everything inside <div class="article-content" ...>...</div>
    $content = $content -replace '(?s)(<div class="article-content"[^>]*>).*?(</div>)', "`$1$($contents[$i])`$2"
    
    [System.IO.File]::WriteAllText($file, $content, $utf8NoBom)
}
