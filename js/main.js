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
    }, 20000);
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

    bgElement.style.transition = 'background-image 0.8s ease, transform 0.1s linear';
    bgElement.style.background = targetUrl + ' no-repeat center center';
    bgElement.style.backgroundSize = 'cover'; 
}

window.addEventListener('resize', () => {
    changeBackground(false); 
});

// 鼠标跟随视差效果
document.addEventListener('mousemove', (e) => {
    const bgElement = document.getElementById('background');
    if(!bgElement) return;
    
    // 计算鼠标距离屏幕中心的比例 (-1 到 1)
    const x = (window.innerWidth / 2 - e.pageX) / (window.innerWidth / 2);
    const y = (window.innerHeight / 2 - e.pageY) / (window.innerHeight / 2);
    
    // 控制背景移动的幅度 (比如最大偏移 20px)
    const moveX = x * 20;
    const moveY = y * 20;
    
    // 使用 scale 放大一点点背景避免漏出黑边，并加上平移
    bgElement.style.transform = 'scale(1.05) translate(' + moveX + 'px, ' + moveY + 'px)';
});

function renderData() {
    if (typeof profileData !== 'undefined') {
        const welcomeTitle = document.querySelector('.welcome-title');
        // Keep the title authored in HTML; use profile data only as a fallback.
        if (welcomeTitle && !welcomeTitle.textContent.trim()) {
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
        const projectsGrid = document.querySelector('[data-projects-grid]') || document.querySelector('.projects-grid');
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
const playlist = (window.radioPlaylist && window.radioPlaylist.length > 0) ? window.radioPlaylist : [
    { title: "【华语】起风了", artist: "买辣椒也用券", url: "https://api.injahow.cn/meting/?server=netease&type=url&id=1330348068" }
];
window.currentMusicIdx = 0;


// 格式化时间辅助函数 (分:秒)
function formatTime(seconds) {
    if (isNaN(seconds) || seconds < 0) return "00:00";
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return (m < 10 ? '0' + m : m) + ':' + (s < 10 ? '0' + s : s);
}

window.isSeeking = false;
window.updateSeekTime = function(percent) {
    const audio = document.getElementById('h5Player');
    const curTimeEl = document.getElementById('currentTime');
    if (audio && audio.duration && curTimeEl) {
        const previewTime = (percent / 100) * audio.duration;
        curTimeEl.innerText = formatTime(previewTime);
    }
};

window.commitSeek = function(percent) {
    const audio = document.getElementById('h5Player');
    if (audio && audio.duration) {
        audio.currentTime = (percent / 100) * audio.duration;
    }
    window.isSeeking = false;
};

function initMusicPlayer() {
    // The shared radio owns playback, including the homepage controls.
    if (document.querySelector('script[src*="js/site-radio.js"]')) return;
    const audio = document.getElementById('h5Player');
    if (!audio) return;
    
    // 监听播放进度与时间更新
    audio.addEventListener('timeupdate', () => {
        if (!audio.duration) return;
        const progress = document.getElementById('progressBar');
        const curTimeEl = document.getElementById('currentTime');
        const durEl = document.getElementById('totalDuration');
        
        if (!window.isSeeking && progress) {
            progress.value = (audio.currentTime / audio.duration) * 100;
        }
        if (curTimeEl) curTimeEl.innerText = formatTime(audio.currentTime);
        if (durEl) durEl.innerText = formatTime(audio.duration);
    });
    
    // 监听总时长加载
    audio.addEventListener('loadedmetadata', () => {
        const durEl = document.getElementById('totalDuration');
        if (durEl && audio.duration) durEl.innerText = formatTime(audio.duration);
    });
    
    audio.addEventListener('durationchange', () => {
        const durEl = document.getElementById('totalDuration');
        if (durEl && audio.duration) durEl.innerText = formatTime(audio.duration);
    });

    audio.addEventListener('ended', window.nextMusic);

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
                el.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
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
    
    // 重置进度条与时间显示
    const progress = document.getElementById('progressBar');
    if (progress) progress.value = 0;
    const curTimeEl = document.getElementById('currentTime');
    if (curTimeEl) curTimeEl.innerText = "00:00";
    const durEl = document.getElementById('totalDuration');
    if (durEl) durEl.innerText = "00:00";

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


