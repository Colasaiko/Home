const search = document.querySelector('#brand-search');
if (search) {
    const cards = [...document.querySelectorAll('.brand-grid .brand-card')];
    const count = document.querySelector('#search-count');
    search.addEventListener('input', () => {
        const query = search.value.trim().toLocaleLowerCase();
        let visible = 0;
        for (const card of cards) {
            card.hidden = !card.querySelector('h2').textContent.toLocaleLowerCase().includes(query);
            if (!card.hidden) visible++;
        }
        count.textContent = visible ? `显示 ${visible} 个品牌` : '没有找到对应品牌，请尝试其他名称。';
    });
}
