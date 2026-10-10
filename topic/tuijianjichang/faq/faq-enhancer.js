document.addEventListener("DOMContentLoaded", () => {
    const article = document.querySelector('.article-content');
    if (!article) return;

    // --- 0.5 Auto-Link Brand Keywords (Internal SEO Linking) ---
    const brandMap = [
        { regex: /微风(网络)?/g, url: '../../weifeng/index.html', name: '微风' },
        { regex: /飞猫(云)?/g, url: '../../feimao/index.html', name: '飞猫' },
        { regex: /暮光云/g, url: '../../muguang/index.html', name: '暮光云' },
        { regex: /大佬(云)?/g, url: '../../dalao/index.html', name: '大佬' },
        { regex: /Firefly/gi, url: '../../firefly/index.html', name: 'Firefly' },
        { regex: /灵猫/g, url: '../../lingmao/index.html', name: '灵猫' },
        { regex: /闪跃/g, url: '../../shanyue/index.html', name: '闪跃' },
        { regex: /无忧/g, url: '../../wuyou/index.html', name: '无忧' },
        { regex: /跨界/g, url: '../../kuajie/index.html', name: '跨界' }
    ];

    function replaceTextWithLinks(node) {
        if (node.nodeType === 3) {
            let text = node.nodeValue;
            let replaced = false;
            
            for (let b of brandMap) {
                if (text.match(b.regex)) {
                    replaced = true;
                }
            }
            
            if (replaced) {
                let htmlStr = text;
                // Escape < and > to prevent raw text from breaking HTML if it contained brackets
                htmlStr = htmlStr.replace(/</g, "&lt;").replace(/>/g, "&gt;");
                
                for (let b of brandMap) {
                    htmlStr = htmlStr.replace(b.regex, `<a href="${b.url}" class="brand-inline-btn" title="前往 ${b.name} 专区">$& <i class="fa-solid fa-arrow-up-right-from-square" style="font-size:0.8em"></i></a>`);
                }
                const span = document.createElement('span');
                span.innerHTML = htmlStr;
                node.parentNode.replaceChild(span, node);
            }
        } else if (node.nodeType === 1 && node.nodeName !== 'A' && node.nodeName !== 'SCRIPT' && node.nodeName !== 'STYLE' && !node.classList.contains('brand-inline-btn')) {
            // Convert childNodes to array to avoid live NodeList iteration issues
            const children = Array.from(node.childNodes);
            for (let i = 0; i < children.length; i++) {
                replaceTextWithLinks(children[i]);
            }
        }
    }
    
    replaceTextWithLinks(article);

    // --- 0.8 Auto-Fix AI Formatting ---
    let headings = article.querySelectorAll('h2, h3, h4');
    if (headings.length <= 1) {
        const pTags = article.querySelectorAll('p');
        pTags.forEach(p => {
            const strong = p.querySelector('strong');
            if (strong && p.textContent.trim().startsWith(strong.textContent.trim())) {
                const text = strong.textContent.trim();
                // Match standard step numbering like "1. ", "一、", "Q:", etc.
                if (/^(\d+|一|二|三|四|首先|其次|最后|Q:|原因|步骤|总结)/.test(text) || (text.length > 2 && text.length < 20 && text.includes('：'))) {
                    const h3 = document.createElement('h3');
                    h3.innerHTML = p.innerHTML; 
                    h3.style.color = '#fff';
                    h3.style.marginTop = '30px';
                    h3.style.marginBottom = '15px';
                    p.parentNode.replaceChild(h3, p);
                }
            }
        });
        headings = article.querySelectorAll('h2, h3, h4');
    }

    // --- 1 & 2. Number headings and Build TOC ---
    let tocHTML = '<div class="faq-toc" id="faqToc"><div class="toc-header" id="tocToggle"><h4><i class="fa-solid fa-list-ul"></i> 文章目录</h4><i class="fa-solid fa-chevron-up toc-toggle"></i></div><ul class="toc-list">';
    let hCounter = 1;
    
    headings.forEach((h, index) => {
        if ((h.tagName === 'H2' || h.tagName === 'H3' || h.tagName === 'H4') && index === 0 && h.textContent.includes('指南')) {
            // Optional skip logic
        } else {
            const cleanText = h.textContent.replace(/^[\s\d\.、]+/g, '');
            
            let iconHtml = '';
            const icon = h.querySelector('i');
            if (icon && !icon.classList.contains('fa-arrow-up-right-from-square')) {
                iconHtml = icon.outerHTML + ' ';
                h.removeChild(icon);
            }
            
            h.innerHTML = iconHtml + hCounter + '. ' + cleanText;
            const anchorId = 'section-' + hCounter;
            h.id = anchorId;
            
            tocHTML += `<li><a href="#${anchorId}">${hCounter}. ${cleanText}</a></li>`;
            hCounter++;
        }
    });
    tocHTML += '</ul></div>';
    
    if (headings.length > 0) {
        const tocDiv = document.createElement('div');
        tocDiv.innerHTML = tocHTML;
        article.insertBefore(tocDiv.firstChild, article.firstChild);

        const tocContainer = document.getElementById('faqToc');
        const tocToggleBtn = document.getElementById('tocToggle');
        if (tocToggleBtn && tocContainer) {
            tocToggleBtn.addEventListener('click', () => {
                tocContainer.classList.toggle('collapsed');
            });
        }
    }

    // --- 3 & 4. Prev/Next and Related Articles ---
    if (typeof faqList !== 'undefined' && faqList.length > 0) {
        const currentPath = window.location.pathname;
        const currentUrl = currentPath.substring(currentPath.lastIndexOf('/') + 1);
        
        let currentIndex = faqList.findIndex(f => f.url === currentUrl);
        if (currentIndex === -1) currentIndex = 0;
        
        const prevItem = currentIndex > 0 ? faqList[currentIndex - 1] : null;
        const nextItem = currentIndex < faqList.length - 1 ? faqList[currentIndex + 1] : null;
        
        let navHTML = '<div class="faq-nav">';
        if (prevItem) navHTML += `<a href="${prevItem.url}" class="nav-prev"><i class="fa-solid fa-arrow-left"></i> 上一篇<br><span>${prevItem.title}</span></a>`;
        else navHTML += `<span class="nav-prev empty">已经是第一篇了</span>`;
        
        if (nextItem) navHTML += `<a href="${nextItem.url}" class="nav-next">下一篇 <i class="fa-solid fa-arrow-right"></i><br><span>${nextItem.title}</span></a>`;
        else navHTML += `<span class="nav-next empty">已经是最后一篇了</span>`;
        navHTML += '</div>';
        
        let relatedHTML = '<div class="faq-related"><h4><i class="fa-solid fa-fire"></i> 相关推荐文章</h4><div class="related-grid">';
        const others = faqList.filter(f => f.url !== currentUrl);
        const shuffled = others.sort(() => 0.5 - Math.random());
        const selected = shuffled.slice(0, 3);
        
        selected.forEach(s => {
            relatedHTML += `<a href="${s.url}" class="related-card"><i class="fa-solid fa-angle-right"></i> ${s.title}</a>`;
        });
        relatedHTML += '</div></div>';
        
        const footerDiv = document.createElement('div');
        footerDiv.innerHTML = navHTML + relatedHTML;
        article.appendChild(footerDiv);
    }
});
