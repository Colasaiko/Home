$files = @(
    "jichang-disney.html",
    "jichang-gemini.html",
    "jichang-ipipshenme-qubie.html"
)

$contents = @(
    (Get-Content -Path "disney_content.html" -Raw -Encoding UTF8),
    (Get-Content -Path "gemini_content.html" -Raw -Encoding UTF8),
    (Get-Content -Path "ip_content.html" -Raw -Encoding UTF8)
)

for ($i = 0; $i -lt 3; $i++) {
    $file = $files[$i]
    $content = Get-Content -Path $file -Raw -Encoding UTF8
    
    # regex replace with actual content
    $content = $content -replace '<p>内容深度撰写中，稍后由 AI 接入更新\.\.\.</p>', $contents[$i]
    
    Set-Content -Path $file -Value $content -Encoding UTF8
}
