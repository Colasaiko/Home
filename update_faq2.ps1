$target_bytes = [System.Convert]::FromBase64String('PHA+5YaF5a655rex5bqm5pKS5YaZ5Lit77yM56iN5ZCO55SxIEFJIOaOpeWFpeabtOaWsC4uLjwvcD4=')
$target_text_raw = [System.Text.Encoding]::UTF8.GetString($target_bytes)
$target_text = [regex]::Escape($target_text_raw)

$qx_html = Get-Content 'C:\Users\USER\Desktop\BLOG\Github内容\Home\qx.txt' -Raw -Encoding UTF8
$sr_html = Get-Content 'C:\Users\USER\Desktop\BLOG\Github内容\Home\sr.txt' -Raw -Encoding UTF8
$sb_html = Get-Content 'C:\Users\USER\Desktop\BLOG\Github内容\Home\sb.txt' -Raw -Encoding UTF8

$path_qx = 'C:\Users\USER\Desktop\BLOG\Github内容\Home\topic\tuijianjichang\faq\jichang-dingyue-lianjie-zenme-daoru-quantumultx.html'
$path_sr = 'C:\Users\USER\Desktop\BLOG\Github内容\Home\topic\tuijianjichang\faq\jichang-dingyue-lianjie-zenme-daoru-shadowrocket.html'
$path_sb = 'C:\Users\USER\Desktop\BLOG\Github内容\Home\topic\tuijianjichang\faq\jichang-dingyue-lianjie-zenme-daoru-sing-box.html'

(Get-Content $path_qx -Raw -Encoding UTF8) -replace $target_text, $qx_html | Set-Content $path_qx -Encoding UTF8
(Get-Content $path_sr -Raw -Encoding UTF8) -replace $target_text, $sr_html | Set-Content $path_sr -Encoding UTF8
(Get-Content $path_sb -Raw -Encoding UTF8) -replace $target_text, $sb_html | Set-Content $path_sb -Encoding UTF8
