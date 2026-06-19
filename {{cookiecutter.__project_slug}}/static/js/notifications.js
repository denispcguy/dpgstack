document.addEventListener('alpine:init', () => {
    Alpine.data('notifications', () => ({
        notifications: [],
        displayDuration: 8000,

        addNotification({ variant = 'info', sender = null, title = null, message = null }) {
            const id = Date.now();
            const notification = { id, variant, sender, title, message };

            if (this.notifications.length >= 20) {
                this.notifications.splice(0, this.notifications.length - 19);
            }
            this.notifications.push(notification);
        },

        removeNotification(id) {
            setTimeout(() => {
                this.notifications = this.notifications.filter(n => n.id !== id);
            }, 400);
        }
    }));
});