# 品牌目录与 FAQ

这是无需 npm 或服务端渲染的静态 HTML 目录，可沿用项目的 GitHub Pages 部署方式。

站内导航显式链接到各目录的 `index.html`，兼容直接双击 HTML 的本地预览，避免 `file://` 打开目录而进入文件列表。部署后各目录的简洁网址仍可访问。

- `brands/index.html`：完整品牌库。
- `brands/<品牌 slug>/index.html`：套餐标价与品牌资料。
- `brands/FAQ<number>/index.html`：该品牌的完整问答。
- `brands/FAQ<number>/content.md`：迁移时保留的问答文本；页面由品牌源资料生成。
- `faq_routes.json`：固定品牌与 FAQ 编号，新增品牌不会改变已有编号。
- `brand_reference.json`：用户提供旧照片 Excel 的资料快照，29 个品牌、185 条套餐；已按要求移除 AFF 链接。

价格主表采用 `brands/*.md` 的 `pricing`。品牌页不再展示旧照片套餐与资料参考，历史 Excel 快照仅作为内部参考保留。

执行 `python scripts/build_brands.py` 可重新生成所有页面。脚本只读取原有品牌 MD，不修改其中任何文字；网页展示时从品牌正文抽出 FAQ 到独立页面。原文没有 FAQ 的品牌使用现有套餐及服务字段生成基础问答。

修改问答时编辑对应 `brands/<品牌 slug>.md` 的 FAQ 区域，再重新构建；`FAQ<number>/content.md` 是保留副本，不是第二套编辑来源。

新增资料后需要自行核验价格、优惠与入口，再更新源文件。这个生成器不会进行实时价格抓取，也不会自动提交或推送 Git。
