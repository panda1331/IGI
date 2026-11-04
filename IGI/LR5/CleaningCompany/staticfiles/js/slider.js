class Slider {
    constructor(element) {
        this.slider = element;
        this.track = this.slider.querySelector('.slider__track');
        this.originalSlides = Array.from(this.track.querySelectorAll('.slide'));
        this.totalSlides = this.originalSlides.length;
        
        this.prevBtn = this.slider.querySelector('.slider__btn--prev');
        this.nextBtn = this.slider.querySelector('.slider__btn--next');
        this.counter = this.slider.querySelector('.slider__counter');
        this.pagination = this.slider.querySelector('.slider__pagination');
        
        this.loop = this.slider.dataset.loop === 'true';
        this.navs = this.slider.dataset.navs === 'true';
        this.pags = this.slider.dataset.pags === 'true';
        this.auto = this.slider.dataset.auto === 'true';
        this.stopHover = this.slider.dataset.stopMouseHover === 'true';
        this.delay = parseInt(localStorage.getItem('sliderDelay')) || parseInt(this.slider.dataset.delay) || 5;
        
        this.timer = null;
        this.isAnimating = false;
        this.transitionDuration = 600; 
        
        if (this.loop) {
            this.setupClones();
        }
        
        this.currentIndex = this.loop ? 1 : 0;
        
        this.init();
    }
    
    setupClones() {
        const firstClone = this.originalSlides[0].cloneNode(true);
        const lastClone = this.originalSlides[this.totalSlides - 1].cloneNode(true);
        
        firstClone.classList.add('slide--clone');
        lastClone.classList.add('slide--clone');
        
        this.track.appendChild(firstClone);
        this.track.insertBefore(lastClone, this.originalSlides[0]);
        
        this.slides = Array.from(this.track.querySelectorAll('.slide'));
    }
    
    init() {
        if (!this.navs) this.slider.classList.add('no-navs');
        if (!this.pags) this.slider.classList.add('no-pags');

        if (this.pags) {
            this.originalSlides.forEach((_, index) => {
                const dot = document.createElement('div');
                dot.classList.add('slider__dot');
                if (index === 0) dot.classList.add('active');
                dot.addEventListener('click', () => this.goToSlide(index));
                this.pagination.appendChild(dot);
            });
        }
        this.dots = Array.from(this.slider.querySelectorAll('.slider__dot'));

        if (this.prevBtn) this.prevBtn.addEventListener('click', () => {
            this.prevSlide();
            this.resetTimer();
        });
        if (this.nextBtn) this.nextBtn.addEventListener('click', () => {
            this.nextSlide();
            this.resetTimer();
        });

        if (this.auto && this.stopHover) {
            this.slider.addEventListener('mouseenter', () => this.stopAuto());
            this.slider.addEventListener('mouseleave', () => this.startAuto());
        }

        const form = document.getElementById('slider-delay-form');
        if (form) {
            const input = document.getElementById('slider-delay-input');
            input.value = this.delay;
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const newDelay = parseInt(input.value);
                if (newDelay >= 1) this.setDelay(newDelay);
            });
        }

        this.updateUI(false);
        
        if (this.auto) this.startAuto();
    }

    getRealIndex() {
        if (!this.loop) return this.currentIndex;
        if (this.currentIndex === 0) return this.totalSlides - 1;
        if (this.currentIndex === this.totalSlides + 1) return 0;
        return this.currentIndex - 1;
    }

    updateUI(animate = true) {
        if (animate) {
            this.track.style.transition = `transform ${this.transitionDuration}ms ease-in-out`;
        } else {
            this.track.style.transition = 'none';
            void this.track.offsetWidth;
        }
        
        this.track.style.transform = `translateX(-${this.currentIndex * 100}%)`;
        
        const realIndex = this.getRealIndex();
        this.counter.textContent = `${realIndex + 1} / ${this.totalSlides}`;
        
        if (this.pags) {
            this.dots.forEach((dot, index) => {
                dot.classList.toggle('active', index === realIndex);
            });
        }
    }

    nextSlide() {
        if (this.isAnimating) return;
        
        if (!this.loop) {
            if (this.currentIndex < this.totalSlides - 1) {
                this.currentIndex++;
                this.updateUI(true);
            }
            return;
        }

        this.isAnimating = true;
        this.currentIndex++;
        this.updateUI(true);

        if (this.currentIndex === this.totalSlides + 1) {
            setTimeout(() => {
                this.currentIndex = 1; 
                this.updateUI(false);
                this.isAnimating = false;
            }, this.transitionDuration);
        } else {
            setTimeout(() => { 
                this.isAnimating = false; 
            }, this.transitionDuration);
        }
    }

    prevSlide() {
        if (this.isAnimating) return;
        
        if (!this.loop) {
            if (this.currentIndex > 0) {
                this.currentIndex--;
                this.updateUI(true);
            }
            return;
        }

        this.isAnimating = true;
        this.currentIndex--;
        this.updateUI(true);

        if (this.currentIndex === 0) {
            setTimeout(() => {
                this.currentIndex = this.totalSlides; 
                this.updateUI(false);
                this.isAnimating = false;
            }, this.transitionDuration);
        } else {
            setTimeout(() => { 
                this.isAnimating = false;
            }, this.transitionDuration);
        }
    }

    goToSlide(realIndex) {
        if (this.isAnimating) return;
        
        this.currentIndex = this.loop ? realIndex + 1 : realIndex;
        
        this.updateUI(true);
        this.resetTimer();
    }

    startAuto() {
        if (!this.auto) return;
        this.stopAuto();  
        this.timer = setInterval(() => {
            this.nextSlide();
        }, this.delay * 1000);
    }

    stopAuto() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;                     
        }
    }

    resetTimer() {
        if (this.auto) {
            this.stopAuto();
            this.startAuto();
        }
    }

    setDelay(newDelay) {
        this.delay = newDelay;
        localStorage.setItem('sliderDelay', newDelay);
        this.resetTimer();
        alert(`Interval changed to ${newDelay} seconds`);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const sliderElement = document.getElementById('main-slider');
    if (sliderElement) new Slider(sliderElement);
});