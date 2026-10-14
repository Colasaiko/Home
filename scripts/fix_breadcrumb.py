import os

path = r'c:\Users\USER\Desktop\BLOG\Github内容\Home\topic\tuijianjichang\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_link = '<a href="../../index.html" class="back-pill"><i class="fa-solid fa-arrow-left"></i> 返回首页</a>'
new_link = '<a href="../index.html" class="back-pill"><i class="fa-solid fa-arrow-left"></i> 返回专题库</a>'

if old_link in content:
    content = content.replace(old_link, new_link)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Breadcrumb link successfully corrected!")
else:
    print("Could not find the exact old link to replace.")
