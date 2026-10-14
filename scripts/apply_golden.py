import re

path = r'c:\Users\USER\Desktop\BLOG\Github内容\Home\topic\tuijianjichang\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the inline style from Dalao
content = content.replace('style="border-color: #f39c12;"', '')

# Add a premium golden highlight CSS class for all brand cards
golden_css = """
/* --- Golden Highlight for All Main Brands --- */
.brand-grid .brand-card {
    border: 1px solid #f39c12 !important;
    box-shadow: 0 4px 15px rgba(243, 156, 18, 0.15);
    transition: all 0.3s ease;
}
.brand-grid .brand-card:hover {
    box-shadow: 0 8px 25px rgba(243, 156, 18, 0.4);
    transform: translateY(-5px);
}
"""

if 'Golden Highlight' not in content:
    content = content.replace('</style>', f'{golden_css}\n</style>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Golden highlight applied to all brands successfully.")
