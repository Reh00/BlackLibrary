import '../css/styles.css';
document.addEventListener('DOMContentLoaded', () => {
    // Lógica do carrossel
    const carousel = document.querySelector('.carousel-items');
    const prevBtn = document.querySelector('.carousel-btn.prev');
    const nextBtn = document.querySelector('.carousel-btn.next');

    if (carousel && prevBtn && nextBtn) {
        prevBtn.addEventListener('click', () => {
            carousel.scrollBy({ left: -200, behavior: 'smooth' });
        });
        nextBtn.addEventListener('click', () => {
            carousel.scrollBy({ left: 200, behavior: 'smooth' });
        });
    } else {
        console.error('Erro: Elementos do carrossel não encontrados.');
    }

    // Lógica da ordenação dos livros
    const sortSelect = document.querySelector('.sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', (e) => {
            const sortBy = e.target.value;
            window.location.href = `/?sort=${sortBy}`;
        });
    } else {
        console.error('Erro: Elemento de ordenação não encontrado.');
    }

    // Lógica do filtro
    const filterSelect = document.querySelector('.filter-select');
    const filterContent = document.querySelector('.filter-content');

    if (filterSelect && filterContent) {
        // Mostrar ao clicar no select
        filterSelect.addEventListener('click', () => {
            filterContent.style.display = 'block';
        });

        // Esconder ao selecionar "FILTRAR"
        filterSelect.addEventListener('change', (e) => {
            const value = e.target.value;
            if (value === 'closed') {
                filterContent.style.display = 'none';
            }
        });
    } else {
        console.error('Erro: Elementos do filtro não encontrados.');
    }
});