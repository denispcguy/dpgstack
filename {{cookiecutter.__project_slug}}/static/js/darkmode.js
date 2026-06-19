document.addEventListener('alpine:init', () => {
    Alpine.store('darkMode', {
        on: document.documentElement.classList.contains('dark'),

        toggle() {
            this.on = !this.on;
            localStorage.setItem('darkMode', this.on);
            document.documentElement.classList.toggle('dark', this.on);
        }
    });

    Alpine.store('columnFlash', {
        flashingColumn: null,

        flashColumn(columnIndex) {
            this.flashingColumn = columnIndex;
            setTimeout(() => {
                this.flashingColumn = null;
            }, 300);
        }
    });
});
(function () {
    const darkMode = localStorage.getItem('darkMode') === 'true' ||
        (!localStorage.getItem('darkMode') && window.matchMedia('(prefers-color-scheme: dark)').matches);
    if (darkMode) {
        document.documentElement.classList.add('dark');
    }
})();