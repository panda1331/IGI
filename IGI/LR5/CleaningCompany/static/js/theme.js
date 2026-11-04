document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement; 

    const savedTheme = localStorage.getItem('theme');

    if (savedTheme === 'dark') {
        htmlElement.setAttribute('data-theme', 'dark');
        toggle.checked = true;
    } else {
        htmlElement.removeAttribute('data-theme');
        toggle.checked = false;
    }

    toggle.addEventListener('change', () => {
        if (toggle.checked) {
            htmlElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            htmlElement.removeAttribute('data-theme');
            localStorage.setItem('theme', 'light');
        }
    });
});