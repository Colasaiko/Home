// 等待 DOM 加载完成
document.addEventListener('DOMContentLoaded', () => {
    renderData();
    const avatar = document.getElementById('avatarImg');
    if(avatar) {
        avatar.addEventListener('click', () => {
            changeBackground(true);
        });
    }

    const newsCards = document.querySelectorAll('.hot-card');
    newsCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'scale(1.02)';
            card.style.transition = 'transform 0.3s ease';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'scale(1)';
        });
    });

    changeBackground(true);
    setInterval(() => {
        changeBackground(true);
    }, 10000);
});

const desktopImages = [
    'url("./assets/bg.jpg")', 'url("./assets/bg2.jpg")', 'url("./assets/bg3.png")', 'url("./assets/bg4.jpg")', 'url("./assets/bg7.jpg")', 'url("./assets/bg8.jpg")', 'url("./assets/bg_20.png")'
];

const mobileImages = [
    'url("./assets/bg5.jpg")', 'url("./assets/bg6.jpg")', 'url("./assets/bg_10.jpg")', 'url("./assets/bg_11.jpg")', 'url("./assets/bg_12.jpg")', 'url("./assets/bg_13.jpg")', 'url("./assets/bg_14.jpg")', 'url("./assets/bg_15.jpg")', 'url("./assets/bg_16.jpg")', 'url("./assets/bg_17.jpg")', 'url("./assets/bg_18.jpg")', 'url("./assets/bg_19.png")'
];

let desktopIndex = -1;
let mobileIndex = -1;

function changeBackground(forceNext = false) {
    const bgElement = document.getElementById('background');
    if(!bgElement) return;

    const isMobile = window.innerWidth <= 768;
    let targetUrl = '';

    if (isMobile) {
        if (forceNext) mobileIndex = (mobileIndex + 1) % mobileImages.length;
        if (mobileIndex === -1) mobileIndex = 0; 
        targetUrl = mobileImages[mobileIndex];
    } else {
        if (forceNext) desktopIndex = (desktopIndex + 1) % desktopImages.length;
        if (desktopIndex === -1) desktopIndex = 0;
        targetUrl = desktopImages[desktopIndex];
    }

    bgElement.style.transition = 'background 0.8s ease';
    bgElement.style.background = targetUrl + ' no-repeat center center';
    bgElement.style.backgroundSize = 'cover'; 
}

window.addEventListener('resize', () => {
    changeBackground(false); 
});

function renderData() {
    if (typeof profileData !== 'undefined') {
        const welcomeTitle = document.querySelector('.welcome-title');
        if (welcomeTitle) {
            welcomeTitle.innerHTML = profileData.titlePrefix + "<span>" + profileData.titleHighlight + "</span>" + profileData.titleSuffix;
        }
        
        const avatarImg = document.getElementById('avatarImg');
        if (avatarImg) {
            avatarImg.src = profileData.avatarUrl;
        }

        const tagsContainer = document.querySelector('.tags-container');
        if (tagsContainer) {
            tagsContainer.innerHTML = profileData.tags.map(tag => '<div class="tag-line">' + tag + '</div>').join('');
        }
    }

    if (typeof communitiesData !== 'undefined') {
        const socialLinks = document.querySelector('.social-links');
        if (socialLinks) {
            socialLinks.innerHTML = communitiesData.map(c => 
                '<a href="' + c.url + '" target="_blank" class="social-card" style="--hover-color: ' + c.color + ';">' +
                    '<div class="social-bg"></div>' +
                    '<div class="social-inner"><i class="' + c.icon + '"></i> <span>' + c.name + '</span></div>' +
                '</a>'
            ).join('');
        }
    }

    if (typeof projectsData !== 'undefined' && typeof blogsData !== 'undefined') {
        const projectsGrid = document.querySelector('.projects-grid');
        if (projectsGrid) {
            const blogLinksHtml = blogsData.map(b => '<a href="' + b.url + '" target="_blank" class="blog-link">' + b.name + '</a>').join('');
            
            let html = 
                '<div class="project-card" style="grid-column: 1 / -1;">' +
                    '<i class="fa-solid fa-blog star-icon"></i>' +
                    '<h3>我的博客矩阵</h3>' +
                    '<p>点击直达各个垂直站点：</p>' +
                    '<div class="blog-list">' +
                        blogLinksHtml +
                    '</div>' +
                '</div>';
            
            projectsData.forEach(p => {
                let fullWidthStyle = p.fullWidth ? 'style="grid-column: 1 / -1;"' : '';

                if (p.isWidget) {
                    html += `
                        <div class="project-card" ${fullWidthStyle}>
                            <i class="${p.icon || 'fa-solid fa-star'} star-icon" style="color: ${p.tagColor};"></i>
                            <h3>${p.title}</h3>
                            <p>${p.desc}</p>
                            <div style="margin-top: 20px;">
                                ${p.widgetHtml}
                            </div>
                            ${p.tagText ? `<div class="project-tag" style="margin-top:15px;"><span style="background: ${p.tagColor};">${p.tagText}</span></div>` : ''}
                        </div>
                    `;
                } else {
                    let cardContent = '';
                    if (p.links && p.links.length > 0) {
                        const nestedLinks = p.links.map(l => `<a href="${l.url}" class="blog-link">${l.name}</a>`).join('');
                        cardContent = `
                            <h3>${p.title}</h3>
                            <p>${p.desc}</p>
                            <div class="blog-list">${nestedLinks}</div>
                        `;
                    } else {
                        cardContent = `
                            <a href="${p.url || '#'}"><h3>${p.title}</h3></a>
                            <p>${p.desc}</p>
                        `;
                    }

                    let tagHtml = p.tagText ? `<div class="project-tag"><span style="background: ${p.tagColor};">${p.tagText}</span></div>` : '';
                    let iconHtml = `<i class="${p.icon || 'fa-solid fa-star'} star-icon" style="color: ${p.tagColor || '#ffd700'};"></i>`;

                    html += `
                        <div class="project-card" ${fullWidthStyle}>
                            ${iconHtml}
                            ${cardContent}
                            ${tagHtml}
                        </div>
                    `;
                }
            });

            projectsGrid.innerHTML = html;
            
            // 初始化音乐播放器
            initMusicPlayer();
        }
    }
}

// =======================
// 音乐播放器全局核心逻辑
// =======================
const playlist = [
    { title: "【华语】起风了", artist: "买辣椒也用券", url: "https://api.injahow.cn/meting/?server=netease&type=url&id=1330348068" }, // 0
    { title: "【欧美】Faded", artist: "Alan Walker", url: "https://api.injahow.cn/meting/?server=netease&type=url&id=36990266" }, // 1
    { title: "【日语】Lemon", artist: "米津玄师", url: "https://api.injahow.cn/meting/?server=netease&type=url&id=536622304" }, // 2
    { title: "【韩语】LOSER (占位)", artist: "BIGBANG", url: "https://api.injahow.cn/meting/?server=netease&type=url&id=29829683" }, // 3
    { title: "【华语】平凡之路", artist: "朴树", url: "https://api.injahow.cn/meting/?server=netease&type=url&id=28815250" }, // 4
    { title: "【欧美】Shape of You", artist: "Ed Sheeran", url: "https://api.injahow.cn/meting/?server=netease&type=url&id=29829683" }, // 5 占位
    { title: "【日语】打上花火", artist: "DAOKO / 米津玄师", url: "https://api.injahow.cn/meting/?server=netease&type=url&id=496869422" }, // 6
    { title: "【韩语】STAY (占位)", artist: "BLACKPINK", url: "https://api.injahow.cn/meting/?server=netease&type=url&id=29829683" } // 7 占位
];
window.currentMusicIdx = 0;

function initMusicPlayer() {
    const audio = document.getElementById('h5Player');
    if (!audio) return;
    window.loadMusic(0);
    // 初始化音量 (根据 range input 默认值 70)
    const vol = document.getElementById('volSlider');
    if(vol) audio.volume = vol.value / 100;
}

window.updatePlaylistUI = function() {
    for(let i = 0; i < playlist.length; i++) {
        let el = document.getElementById('song-' + i);
        if(el) {
            if(i === window.currentMusicIdx) {
                el.style.color = '#fff';
                el.style.fontWeight = 'bold';
                el.style.borderLeft = '3px solid #9b59b6';
                el.style.paddingLeft = '5px';
            } else {
                el.style.color = '#ccc';
                el.style.fontWeight = 'normal';
                el.style.borderLeft = 'none';
                el.style.paddingLeft = '0';
            }
        }
    }
};

window.loadMusic = function(idx) {
    const audio = document.getElementById('h5Player');
    if(!audio) return;
    
    document.getElementById('mTitle').innerText = playlist[idx].title;
    document.getElementById('mArtist').innerText = playlist[idx].artist;
    audio.src = playlist[idx].url;
    
    document.getElementById('recordCover').classList.add('paused');
    document.getElementById('playBtn').innerHTML = '<i class="fa-solid fa-play"></i>';
    
    window.updatePlaylistUI();
};

window.playSongFromList = function(idx) {
    window.currentMusicIdx = idx;
    window.loadMusic(idx);
    
    const audio = document.getElementById('h5Player');
    const btn = document.getElementById('playBtn');
    const record = document.getElementById('recordCover');
    
    audio.play().then(() => {
        btn.innerHTML = '<i class="fa-solid fa-pause"></i>';
        record.classList.remove('paused');
    }).catch(e => console.error(e));
};

window.toggleMusic = function() {
    const audio = document.getElementById('h5Player');
    const btn = document.getElementById('playBtn');
    const record = document.getElementById('recordCover');
    if(!audio) return;

    if (audio.paused) {
        audio.play().then(() => {
            btn.innerHTML = '<i class="fa-solid fa-pause"></i>';
            record.classList.remove('paused');
        }).catch(e => {
            console.error("播放失败：", e);
            alert("加载音频流失败，请稍后再试。");
        });
    } else {
        audio.pause();
        btn.innerHTML = '<i class="fa-solid fa-play"></i>';
        record.classList.add('paused');
    }
};

window.nextMusic = function() {
    window.currentMusicIdx = (window.currentMusicIdx + 1) % playlist.length;
    window.playSongFromList(window.currentMusicIdx); 
};

window.prevMusic = function() {
    window.currentMusicIdx = (window.currentMusicIdx - 1 + playlist.length) % playlist.length;
    window.playSongFromList(window.currentMusicIdx);
};

window.setVolume = function(val) {
    const audio = document.getElementById('h5Player');
    if(audio) {
        audio.volume = val / 100;
    }
};

// 当歌曲播放完毕自动切换下一首
document.addEventListener('DOMContentLoaded', () => {
    // 因为 renderData 会重写 DOM，所以在这里使用事件委托或等待 audio 元素生成
    setTimeout(() => {
        const audio = document.getElementById('h5Player');
        if(audio) {
            audio.addEventListener('ended', window.nextMusic);
        }
    }, 1000);
});
