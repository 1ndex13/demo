document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
        new bootstrap.Tooltip(el, { trigger: 'hover focus' });
    });
    document.querySelectorAll('.toast').forEach(toastEl => {
        const toast = bootstrap.Toast.getOrCreateInstance(toastEl, {
            autohide: true,
            delay: 4500,
        });
        toast.show();
        toastEl.addEventListener('hidden.bs.toast', () => {
            toastEl.remove();
        });
    });
    const navbar = document.querySelector('.navbar-custom');
    if (navbar) {
        const onScroll = () => {
            navbar.classList.toggle('shadow-sm', window.scrollY > 8);
        };
        window.addEventListener('scroll', onScroll, { passive: true });
    }
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function () {
            const btn = this.querySelector('[type="submit"]');
            if (btn && !btn.dataset.noLoader) {
                btn.disabled = true;
                const orig = btn.innerHTML;
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Отправка...';
                setTimeout(() => {
                    if (btn.disabled) {
                        btn.disabled = false;
                        btn.innerHTML = orig;
                    }
                }, 8000);
            }
        });
    });
    document.querySelectorAll('.alert-dismissible').forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });
    const currentPath = window.location.pathname;
    document.querySelectorAll('.navbar-custom .nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href && href !== '/' && currentPath.startsWith(href)) {
            link.classList.add('active');
        }
    });
});
