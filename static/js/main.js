/* Main JavaScript functionality */

// ── Dismiss Alerts ──
document.querySelectorAll('.alert-close').forEach(btn => {
    btn.addEventListener('click', function() {
        this.closest('.alert').remove();
    });
});

// ── Auto-dismiss Success Messages ──
document.querySelectorAll('.alert-success').forEach(alert => {
    setTimeout(() => {
        alert.style.animation = 'fadeOut 0.5s ease-in-out');
        setTimeout(() => alert.remove(), 500);
    }, 5000);
});

// ── Mobile Menu Toggle ──
function toggleMenu() {
    const menu = document.getElementById('navbarMenu');
    menu.classList.toggle('active');
}

// Close menu when clicking outside
document.addEventListener('click', function(event) {
    const navbar = document.querySelector('.navbar');
    if (!navbar.contains(event.target)) {
        const menu = document.getElementById('navbarMenu');
        if (menu) menu.classList.remove('active');
    }
});

// ── Confirmation Dialogs ──
document.querySelectorAll('[data-confirm]').forEach(element => {
    element.addEventListener('click', function(e) {
        if (!confirm(this.dataset.confirm)) {
            e.preventDefault();
        }
    });
});

// ── Active Navigation Link ──
const currentLocation = location.pathname;
document.querySelectorAll('.navbar-link').forEach(link => {
    if (link.getAttribute('href') === currentLocation) {
        link.classList.add('active');
    }
});

// ── Form Validation ──
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', function() {
        const inputs = this.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            if (!input.value.trim() && input.required) {
                input.classList.add('is-invalid');
                input.addEventListener('input', function() {
                    this.classList.remove('is-invalid');
                });
            }
        });
    });
});

// ── Smooth Scroll ──
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// ── Format Currency ──
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toFixed(2);
}

// ── Loading Spinner ──
function showLoading() {
    const loader = document.getElementById('loadingOverlay');
    if (loader) loader.classList.add('active');
}

function hideLoading() {
    const loader = document.getElementById('loadingOverlay');
    if (loader) loader.classList.remove('active');
}

// Hide loading overlay on page load
window.addEventListener('load', hideLoading);

// ── Keydown Handler ──
document.addEventListener('keydown', function(e) {
    // Close modals on ESC
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.active').forEach(modal => {
            modal.classList.remove('active');
        });
    }
});

// ── Init tooltips and popovers (if using Bootstrap) ──
document.addEventListener('DOMContentLoaded', function() {
    if (typeof bootstrap !== 'undefined') {
        // Initialize Bootstrap tooltips
        document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
            new bootstrap.Tooltip(el);
        });
        
        // Initialize Bootstrap popovers
        document.querySelectorAll('[data-bs-toggle="popover"]').forEach(el => {
            new bootstrap.Popover(el);
        });
    }
});
