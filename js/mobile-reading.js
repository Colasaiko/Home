(() => {
  function labelTables() {
    document.querySelectorAll('table:not(.mobile-reading-table)').forEach(table => {
      const header = table.tHead?.rows[0];
      if (!header) return;
      const labels = [...header.cells].map(cell => cell.textContent.trim());
      [...table.tBodies].forEach(body => [...body.rows].forEach(row => {
        let column = 0;
        [...row.cells].forEach(cell => {
          cell.dataset.mobileLabel = labels[column] || '';
          column += cell.colSpan;
        });
      }));
      table.classList.add('mobile-reading-table');
    });
  }
  document.addEventListener('DOMContentLoaded', () => {
    queueMicrotask(labelTables);
    const observer = new MutationObserver(records => {
      if (records.some(record => [...record.addedNodes].some(node => node.nodeType === 1 && (node.matches('table') || node.querySelector('table'))))) labelTables();
    });
    observer.observe(document.body, { childList: true, subtree: true });
  });
})();
