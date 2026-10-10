(() => {
    const rows = [...document.querySelectorAll('tbody tr')];
    const search = document.querySelector('#compare-search');
    const scope = document.querySelector('#compare-scope');
    const budget = document.querySelector('#compare-budget');
    const selected = document.querySelector('#compare-selected');
    let selectedOnly = false;
    const initial = new URLSearchParams(location.search).get('select');
    rows.forEach(row => {
        const path = row.querySelector('h3 a').getAttribute('href');
        if (initial && path === `brands/${initial}/index.html`) row.querySelector('input').checked = true;
    });
    function update() {
        const picked = rows.filter(row => row.querySelector('input').checked).length;
        selected.textContent = selectedOnly ? '返回品牌列表' : `比较已选品牌（${picked}）`;
        selected.disabled = !selectedOnly && picked < 2;
        selected.setAttribute('aria-pressed', String(selectedOnly));
        const names = rows.filter(row => row.querySelector('input').checked).map(row => row.querySelector('h3').textContent);
        document.querySelector('#compare-selection').textContent = picked ? `已选：${names.join('、')}${picked === 1 ? '。再勾选一个品牌，就能开始对比。' : '。点击「比较已选品牌」集中查看。'}` : '先在表格中勾选至少 2 个品牌，再点击「比较已选品牌」。';
        const query = search.value.trim().toLocaleLowerCase();
        let visible = 0;
        rows.forEach(row => {
            row.classList.toggle('is-picked', row.querySelector('input').checked);
            const match = selectedOnly ? row.querySelector('input').checked :
                row.dataset.search.includes(query) && (scope.value === 'all' || row.dataset.featured === 'true') &&
                (budget.value === 'all' || (row.dataset.monthly !== '' && Number(row.dataset.monthly) <= Number(budget.value)));
            row.hidden = !match;
            if (match) visible++;
        });
        document.querySelector('#compare-count').textContent = `显示 ${visible} 个品牌 · 已选 ${picked} 个${selectedOnly ? '（当前显示已选品牌）' : ''}`;
        document.querySelector('#compare-empty').hidden = visible !== 0;
    }
    search.addEventListener('input', update);
    scope.addEventListener('change', update);
    budget.addEventListener('change', update);
    rows.forEach(row => row.querySelector('input').addEventListener('change', update));
    selected.addEventListener('click', () => { selectedOnly = !selectedOnly; update(); });
    document.querySelector('#compare-reset').addEventListener('click', () => {
        search.value = ''; scope.value = 'all'; budget.value = 'all'; selectedOnly = false;
        rows.forEach(row => { row.querySelector('input').checked = false; });
        update();
    });
    update();
})();
