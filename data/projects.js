// 其他网站合集/项目卡片配置
const projectsData = [
    { 
        title: "导航站点", 
        desc: "常用网址与极客资源收录：", 
        tagText: "工具类", 
        tagColor: "#3572A5",
        icon: "fa-solid fa-compass",
        fullWidth: true,
        links: [
            { name: "客户端下载", url: "./clients.html" },
            { name: "极客工具箱", url: "./tools.html" },
            { name: "节点监控墙", url: "./status.html" },
            { name: "宝藏书签库", url: "./bookmarks.html" }
        ]
    },

    { 
        title: "硬核节点体检中心", 
        url: "api.html", 
        desc: "涵盖智能订阅转换、Clash 语法除错、以及深度的 WebRTC 与 DNS 安全测漏。购买机场后必做的全套网络体检套餐：", 
        tagText: "安全探测", 
        tagColor: "#e34c26",
        icon: "fa-solid fa-shield-halved",
        fullWidth: true,
        links: [
            { name: "🔀 一键智能订阅转换", url: "api.html" },
            { name: "🛠️ Clash 语法查错", url: "api.html" },
            { name: "🛡️ WebRTC 测漏", url: "api.html" },
            { name: "🌐 DNS 解析评估", url: "api.html" }
        ]
    },
    { 
        title: "私人音乐电台", 
        url: "#", 
        desc: "与你分享我最爱的 ACG 神曲与电音，点击下方直接播放 🎵", 
        tagText: "个人爱好", 
        tagColor: "#9b59b6",
        icon: "fa-solid fa-headphones-simple",
        fullWidth: true,
        isWidget: true,
        widgetHtml: `
            <div style="background: rgba(0,0,0,0.4); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.1);">
                <!-- 主播放器界面 -->
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="width: 60px; height: 60px; border-radius: 50%; background: #222; border: 2px solid #9b59b6; display: flex; justify-content: center; align-items: center; overflow: hidden; animation: spin 5s linear infinite; flex-shrink: 0;" id="recordCover">
                        <div style="width: 20px; height: 20px; background: #9b59b6; border-radius: 50%;"></div>
                    </div>
                    <div style="flex-grow: 1;">
                        <div id="mTitle" style="color: #fff; font-weight: bold; font-size: 1.1rem; margin-bottom: 5px;">【华语】起风了</div>
                        <div id="mArtist" style="color: #aaa; font-size: 0.85rem;">买辣椒也用券</div>
                    </div>
                    <div style="display: flex; gap: 10px; align-items: center;">
                        <button onclick="window.prevMusic()" style="background:none; border:none; color:#fff; cursor:pointer; font-size:1.2rem; transition:0.3s;" onmouseover="this.style.color='#9b59b6'" onmouseout="this.style.color='#fff'"><i class="fa-solid fa-backward-step"></i></button>
                        <button id="playBtn" onclick="window.toggleMusic()" style="background:#9b59b6; border:none; color:#fff; cursor:pointer; width:40px; height:40px; border-radius:50%; font-size:1.2rem; display:flex; justify-content:center; align-items:center; transition:0.3s; box-shadow:0 0 10px rgba(155,89,182,0.5);" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'"><i class="fa-solid fa-play"></i></button>
                        <button onclick="window.nextMusic()" style="background:none; border:none; color:#fff; cursor:pointer; font-size:1.2rem; transition:0.3s;" onmouseover="this.style.color='#9b59b6'" onmouseout="this.style.color='#fff'"><i class="fa-solid fa-forward-step"></i></button>
                    </div>
                </div>

                <!-- 音量控制拉线 -->
                <div style="display: flex; align-items: center; gap: 10px; margin-top: 15px; color:#aaa; font-size:0.8rem; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 15px;">
                    <i class="fa-solid fa-volume-low"></i>
                    <input type="range" id="volSlider" min="0" max="100" value="70" oninput="window.setVolume(this.value)" style="flex-grow:1; cursor:pointer; height:4px; accent-color:#9b59b6;">
                    <i class="fa-solid fa-volume-high"></i>
                </div>

                <!-- 分类播放列表 -->
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 20px; font-size: 0.85rem; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px;">
                    
                    <div style="display: flex; flex-direction: column;">
                        <div style="color:#9b59b6; margin-bottom:8px; font-weight:bold; border-bottom:1px solid rgba(155,89,182,0.3); padding-bottom:5px; flex-shrink: 0; white-space: nowrap;"><i class="fa-solid fa-music"></i> 华语区</div>
                        <div class="custom-scroll" style="max-height: 90px; overflow-y: auto; padding-right: 5px;">
                            <div id="song-0" onclick="window.playSongFromList(0)" style="cursor:pointer; color:#fff; margin-bottom:5px; transition:0.2s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" onmouseover="this.style.color='#9b59b6'" onmouseout="if(window.currentMusicIdx!==0) this.style.color='#ccc'">起风了</div>
                            <div id="song-4" onclick="window.playSongFromList(4)" style="cursor:pointer; color:#ccc; margin-bottom:5px; transition:0.2s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" onmouseover="this.style.color='#9b59b6'" onmouseout="if(window.currentMusicIdx!==4) this.style.color='#ccc'">平凡之路</div>
                            <div style="cursor:pointer; color:#ccc; opacity:0.5; margin-bottom:5px;">+ 添加新歌</div>
                            <div style="cursor:pointer; color:#ccc; opacity:0.5; margin-bottom:5px;">+ 添加新歌</div>
                        </div>
                    </div>

                    <div style="display: flex; flex-direction: column;">
                        <div style="color:#9b59b6; margin-bottom:8px; font-weight:bold; border-bottom:1px solid rgba(155,89,182,0.3); padding-bottom:5px; flex-shrink: 0; white-space: nowrap;"><i class="fa-solid fa-earth-americas"></i> 欧美区</div>
                        <div class="custom-scroll" style="max-height: 90px; overflow-y: auto; padding-right: 5px;">
                            <div id="song-1" onclick="window.playSongFromList(1)" style="cursor:pointer; color:#ccc; margin-bottom:5px; transition:0.2s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" onmouseover="this.style.color='#9b59b6'" onmouseout="if(window.currentMusicIdx!==1) this.style.color='#ccc'">Faded</div>
                            <div id="song-5" onclick="window.playSongFromList(5)" style="cursor:pointer; color:#ccc; margin-bottom:5px; transition:0.2s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" onmouseover="this.style.color='#9b59b6'" onmouseout="if(window.currentMusicIdx!==5) this.style.color='#ccc'">Shape of You</div>
                            <div style="cursor:pointer; color:#ccc; opacity:0.5; margin-bottom:5px;">+ 添加新歌</div>
                            <div style="cursor:pointer; color:#ccc; opacity:0.5; margin-bottom:5px;">+ 添加新歌</div>
                        </div>
                    </div>

                    <div style="display: flex; flex-direction: column;">
                        <div style="color:#9b59b6; margin-bottom:8px; font-weight:bold; border-bottom:1px solid rgba(155,89,182,0.3); padding-bottom:5px; flex-shrink: 0; white-space: nowrap;"><i class="fa-solid fa-torii-gate"></i> 日语区</div>
                        <div class="custom-scroll" style="max-height: 90px; overflow-y: auto; padding-right: 5px;">
                            <div id="song-2" onclick="window.playSongFromList(2)" style="cursor:pointer; color:#ccc; margin-bottom:5px; transition:0.2s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" onmouseover="this.style.color='#9b59b6'" onmouseout="if(window.currentMusicIdx!==2) this.style.color='#ccc'">Lemon</div>
                            <div id="song-6" onclick="window.playSongFromList(6)" style="cursor:pointer; color:#ccc; margin-bottom:5px; transition:0.2s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" onmouseover="this.style.color='#9b59b6'" onmouseout="if(window.currentMusicIdx!==6) this.style.color='#ccc'">打上花火</div>
                            <div style="cursor:pointer; color:#ccc; opacity:0.5; margin-bottom:5px;">+ 添加新歌</div>
                            <div style="cursor:pointer; color:#ccc; opacity:0.5; margin-bottom:5px;">+ 添加新歌</div>
                        </div>
                    </div>

                    <div style="display: flex; flex-direction: column;">
                        <div style="color:#9b59b6; margin-bottom:8px; font-weight:bold; border-bottom:1px solid rgba(155,89,182,0.3); padding-bottom:5px; flex-shrink: 0; white-space: nowrap;"><i class="fa-solid fa-won-sign"></i> 韩语区</div>
                        <div class="custom-scroll" style="max-height: 90px; overflow-y: auto; padding-right: 5px;">
                            <div id="song-3" onclick="window.playSongFromList(3)" style="cursor:pointer; color:#ccc; margin-bottom:5px; transition:0.2s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" onmouseover="this.style.color='#9b59b6'" onmouseout="if(window.currentMusicIdx!==3) this.style.color='#ccc'">LOSER</div>
                            <div id="song-7" onclick="window.playSongFromList(7)" style="cursor:pointer; color:#ccc; margin-bottom:5px; transition:0.2s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" onmouseover="this.style.color='#9b59b6'" onmouseout="if(window.currentMusicIdx!==7) this.style.color='#ccc'">STAY</div>
                            <div style="cursor:pointer; color:#ccc; opacity:0.5; margin-bottom:5px;">+ 添加新歌</div>
                            <div style="cursor:pointer; color:#ccc; opacity:0.5; margin-bottom:5px;">+ 添加新歌</div>
                        </div>
                    </div>

                </div>
            </div>
            
            <audio id="h5Player" src="https://api.injahow.cn/meting/?server=netease&type=url&id=1330348068"></audio>
            <style>
                @keyframes spin { 100% { transform: rotate(360deg); } } 
                .paused { animation-play-state: paused !important; }
                input[type=range] { -webkit-appearance: none; background: rgba(255,255,255,0.2); outline: none; border-radius: 2px; }
                input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; appearance: none; width: 12px; height: 12px; border-radius: 50%; background: #9b59b6; cursor: pointer; }
                
                /* 定制音乐列表的极简赛博滚动条 */
                .custom-scroll::-webkit-scrollbar { width: 4px; }
                .custom-scroll::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); border-radius: 4px; }
                .custom-scroll::-webkit-scrollbar-thumb { background: rgba(155,89,182,0.5); border-radius: 4px; }
                .custom-scroll::-webkit-scrollbar-thumb:hover { background: rgba(155,89,182,0.8); }
            </style>
        `
    }
];
