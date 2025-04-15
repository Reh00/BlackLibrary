// Carrossel
const carousel = document.querySelector('.carousel-items');
const prevBtn = document.querySelector('.carousel-btn.prev');
const nextBtn = document.querySelector('.carousel-btn.next');

prevBtn.addEventListener('click', () => {
    carousel.scrollBy({ left: -200, behavior: 'smooth' });
});

nextBtn.addEventListener('click', () => {
    carousel.scrollBy({ left: 200, behavior: 'smooth' });
});

// Ordenação dos Livros
document.addEventListener('DOMContentLoaded', () => {
    const sortSelect = document.querySelector('.sort select');
    sortSelect.addEventListener('change', (e) => {
        const sortBy = e.target.value;
        window.location.href = `/?sort=${sortBy}`; // Redireciona com o parâmetro de ordenação
    });
});