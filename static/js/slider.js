// Слайдер: автопереключение каждые 3 сек, кнопки, точки
class Slider {
    constructor(wrapperId) {
        this.wrapper = document.getElementById(wrapperId);
        if (!this.wrapper) return;

        this.slides = this.wrapper.querySelectorAll('.slide');
        this.dots   = this.wrapper.querySelectorAll('.dot');
        this.total  = this.slides.length;
        this.current = 0;
        this.timer  = null;
        this.INTERVAL = 3000;

        this._bindControls();
        this._startAuto();
    }

    // Показать слайд с индексом 
    _show(index) {
        this.slides.forEach(s => s.classList.remove('slide-active'));
        this.dots.forEach(d => {
            d.classList.remove('dot-active');
            d.setAttribute('aria-selected', 'false');
        });

        this.current = (index + this.total) % this.total;

        this.slides[this.current].classList.add('slide-active');
        this.dots[this.current].classList.add('dot-active');
        this.dots[this.current].setAttribute('aria-selected', 'true');
    }

    next() {
        this._show(this.current + 1);
        this._resetAuto();
    }

    prev() {
        this._show(this.current - 1);
        this._resetAuto();
    }

    _startAuto() {
        this.timer = setInterval(() => this.next(), this.INTERVAL);
    }

    _resetAuto() {
        clearInterval(this.timer);
        this._startAuto();
    }

    _bindControls() {
        // Кнопки навигации
        const btnPrev = this.wrapper.querySelector('.slider-prev');
        const btnNext = this.wrapper.querySelector('.slider-next');
        if (btnPrev) btnPrev.addEventListener('click', () => this.prev());
        if (btnNext) btnNext.addEventListener('click', () => this.next());

        // Клики по круглешкам
        this.dots.forEach((dot, i) => {
            dot.addEventListener('click', () => {
                this._show(i);
                this._resetAuto();
            });
        });

        let touchStartX = 0;
        this.wrapper.addEventListener('touchstart', e => {
            touchStartX = e.touches[0].clientX;
        }, { passive: true });
        this.wrapper.addEventListener('touchend', e => {
            const diff = touchStartX - e.changedTouches[0].clientX;
            if (Math.abs(diff) > 40) {
                diff > 0 ? this.next() : this.prev();
            }
        }, { passive: true });
    }
}
//Загрузка слайдера
document.addEventListener('DOMContentLoaded', () => {
    new Slider('mainSlider');
});
