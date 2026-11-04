class CatalogPagination {
    constructor() {
        this.allCards = [];
        this.validCards = [];
        
        this.currentPage = 1;
        this.itemsPerPage = 3;
        
        this.paginationContainer = document.getElementById('catalog-pagination');
        this.perPageSelect = document.getElementById('per-page-select');
        
        this.init();
    }

    init() {
        this.allCards = Array.from(document.querySelectorAll('.service-card'));
        this.validCards = this.allCards.filter(card => !card.classList.contains('service-card--empty'));
        
        if (this.validCards.length === 0) {
            return;
        }

        const savedPerPage = localStorage.getItem('catalogPerPage');
        if (savedPerPage) {
            this.itemsPerPage = parseInt(savedPerPage);
            if (this.perPageSelect) this.perPageSelect.value = savedPerPage;
        }

        this.bindEvents();
        this.render();
    }

    bindEvents() {
        if (this.perPageSelect) {
            this.perPageSelect.addEventListener('change', (e) => {
                this.itemsPerPage = parseInt(e.target.value);
                this.currentPage = 1; 
                localStorage.setItem('catalogPerPage', this.itemsPerPage); 
                this.render();
            });
        }
    }

    render() {
        this.allCards.forEach(card => {
            card.style.display = 'none';
        });

        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        const cardsOnPage = this.validCards.slice(start, end);

        cardsOnPage.forEach(card => {
            card.style.display = '';
        });

        document.querySelectorAll('.catalog-category').forEach(category => {
            const hasVisible = Array.from(category.querySelectorAll('.service-card'))
                .some(c => c.style.display !== 'none');
            category.style.display = hasVisible ? '' : 'none';
        });

        this.renderPagination();
    }

    renderPagination() {
        this.paginationContainer.innerHTML = '';
        const totalPages = Math.ceil(this.validCards.length / this.itemsPerPage);

        if (totalPages <= 1) return;

        const prevBtn = document.createElement('button');
        prevBtn.textContent = 'Prev';
        prevBtn.disabled = this.currentPage === 1;
        prevBtn.addEventListener('click', () => this.goToPage(this.currentPage - 1));
        this.paginationContainer.appendChild(prevBtn);

        for (let i = 1; i <= totalPages; i++) {
            const btn = document.createElement('button');
            btn.textContent = i;
            if (i === this.currentPage) btn.classList.add('active');
            btn.addEventListener('click', () => this.goToPage(i));
            this.paginationContainer.appendChild(btn);
        }

        const nextBtn = document.createElement('button');
        nextBtn.textContent = 'Next';
        nextBtn.disabled = this.currentPage === totalPages;
        nextBtn.addEventListener('click', () => this.goToPage(this.currentPage + 1));
        this.paginationContainer.appendChild(nextBtn);
    }

    goToPage(page) {
        this.currentPage = page;
        this.render();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('catalog-pagination')) {
        new CatalogPagination();
    }

    const cards = document.querySelectorAll(".service-card");
    cards.forEach(card_w => {
        const card = card_w.querySelector(".card");  
        if (!card) return; 

        let ticking = false;

        card_w.addEventListener('mousemove', event => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    const [x, y] = [event.offsetX, event.offsetY];
                    const rect = card_w.getBoundingClientRect();
                    const [width, height] = [rect.width, rect.height];
                    
                    const middleX = width / 2;
                    const middleY = height / 2;
                    
                    const offsetX = ((x - middleX) / middleX);
                    const offsetY = ((y - middleY) / middleY);
                    
                    const tiltX = offsetX * 15; 
                    const tiltY = offsetY * 15;
                    
                    card.style.setProperty("--rotateX", tiltX + "deg");
                    card.style.setProperty("--rotateY", -tiltY + "deg");
                    
                    ticking = false;
                });
                ticking = true;
            }
        });

        card_w.addEventListener('mouseleave', () => {
            card.style.setProperty("--rotateX", "0deg");
            card.style.setProperty("--rotateY", "0deg");
        });
    });
});

