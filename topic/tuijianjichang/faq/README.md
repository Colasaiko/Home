# 通用 FAQ 文章

总库有 215 个不同问题，每个问题有独立 HTML 地址。正文顺序为问题的重要性、直接回答、按需展开的处理步骤、完成判断与相关阅读；目录、步骤锚点和上一篇/下一篇均直接存在于 HTML 中。

`faq-articles.json` 保存每篇完整的可编辑正文。可以修改其中的 why、answer、steps、check 等字段，再执行 `python -B scripts/build_faq_articles.py`。

直接修改 HTML 后，浏览器刷新即可看到修改。生成器会通过 `article-output-hashes.json` 检查手动改动；发现差异时停止，而不会默默覆盖。确定要用 JSON 内容覆盖手动 HTML 时才使用 `--force`。新文章无需 `faq-enhancer.js` 改写标题，也不依赖 JavaScript 生成正文或目录。

`scripts/faq_content.py` 是本次初始稿的主题流程和逐题编辑说明；首次生成以后，正文以 `faq-articles.json` 为准。原有空白页和历史草稿不作为新的内容来源。

每篇的 `brandContext` 保存正文中的品牌衔接段落，`afterStep` 决定出现在哪一步之后；`{weifeng}`、`{firefly}` 等占位符生成品牌介绍页的普通站内链接。排障与账号风险文章在处理步骤完成后再介绍候选资料。主推榜入口始终指向 `topic/tuijianjichang/index.html`，不改动主推榜页面。

新增的 26 篇搜索问题稿件初始保存在 `scripts/add_faq_search_topics.py`，发布文件位于根目录 `FAQ/`，例如 `/FAQ/WhatIsHysteria2.html`。加入资料库后，以 `faq-articles.json` 为编辑来源。生成器按每篇页面位置计算资源、品牌、相关问题和翻页链接，原有文章地址保留。

新文章采用 5—6 个环节；以后可继续增加或减少，目录与编号自动适配。`searchTerms` 保存同义搜索词，列表页搜索与分类会一起匹配标题和这些词；同义词不另外生成重复页面。

`relatedArticles` 逐篇保存三个相关问题的编号和内容提示，可以直接编辑。初始关系由 `scripts/faq_connections.py` 人工选择，并非固定取同分类的前三篇。生成后运行 `python -B scripts/verify_faq_articles.py` 检查正文、目录与本地链接。

本次处理前的完整 FAQ 备份位于 `C:/Users/USER/AppData/Local/Temp/faq-before-qnifn_dp/faq`。
