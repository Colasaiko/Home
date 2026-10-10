// Navigation enhancement only: the complete article and directory are static HTML.
const directoryLinks = [...document.querySelectorAll('.faq-directory a[href^="#"]')];
if ('IntersectionObserver' in window && directoryLinks.length) {
    const targets = new Map(directoryLinks.map(link => [link.hash.slice(1), link]));
    const observer = new IntersectionObserver(entries => {
        const current = entries.filter(entry => entry.isIntersecting)
            .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
        if (!current) return;
        for (const link of directoryLinks) link.removeAttribute('aria-current');
        targets.get(current.target.id)?.setAttribute('aria-current', 'location');
    }, { rootMargin: '-10% 0px -55% 0px', threshold: 0 });
    for (const id of targets.keys()) {
        const section = document.getElementById(id);
        if (section) observer.observe(section);
    }
}
