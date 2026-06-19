# Notifications
Toast notifications triggered from Django view.

## Properties: Dpg notification parts
- Custom JS: ./static/js/notifications.js
    ```js
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
    ```
- `./templates/cotton/fancy/notifications.html`:
    ```html
    <div x-data="notifications"
        x-on:notify.window="addNotification($event.detail)"
        x-on:notify-success.window="$dispatch('notify', { variant: 'success', title: 'Success!', message: 'Strip deleted successfully.' })"
        x-on:notify-danger.window="$dispatch('notify', { variant: 'danger', title: 'Error', message: 'Could not delete the strip. Try again.' })">
        <div x-on:mouseenter="$dispatch('pause-auto-dismiss')"
            x-on:mouseleave="$dispatch('resume-auto-dismiss')"
            class="group pointer-events-none fixed inset-x-8 bottom-0 z-50 flex max-w-full flex-col gap-2 bg-transparent px-6 py-6 md:left-auto md:right-0 md:top-auto md:max-w-sm">
            <template x-for="(notification, index) in notifications" :key="notification.id">
                <div>
                    <template x-if="notification.variant === 'success'">
                        <div x-data="{ isVisible: false, timeout: null }"
                            x-cloak
                            x-show="isVisible"
                            class="pointer-events-auto relative border border-success bg-surface text-on-surface dark:bg-surface-dark dark:text-on-surface-dark"
                            role="alert"
                            x-on:pause-auto-dismiss.window="clearTimeout(timeout)"
                            x-on:resume-auto-dismiss.window="timeout = setTimeout(() => { isVisible = false; removeNotification(notification.id) }, displayDuration)"
                            x-init="$nextTick(() => { isVisible = true }); timeout = setTimeout(() => { isVisible = false; removeNotification(notification.id) }, displayDuration)"
                            x-transition:enter="transition duration-300 ease-out"
                            x-transition:enter-end="translate-y-0"
                            x-transition:enter-start="translate-y-8"
                            x-transition:leave="transition duration-300 ease-in"
                            x-transition:leave-end="-translate-x-24 opacity-0 md:translate-x-24"
                            x-transition:leave-start="translate-x-0 opacity-100">
                            <div class="flex w-full items-center gap-2.5 bg-success/10 p-4 transition-all duration-300">
                                <!-- Icon -->
                                <div class="rounded-full bg-success/15 p-0.5 text-success">
                                    <svg xmlns="http://www.w3.org/2000/svg"
                                        viewBox="0 0 20 20"
                                        fill="currentColor"
                                        class="size-5">
                                        <path fill-rule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm3.857-9.809a.75.75 0 0 0-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 1 0-1.06 1.061l2.5 2.5a.75.75 0 0 0 1.137-.089l4-5.5Z" clip-rule="evenodd" />
                                    </svg>
                                </div>
                                <!-- Title & Message -->
                                <div class="flex flex-col gap-2">
                                    <h3 x-show="notification.title"
                                        class="text-sm font-semibold text-success"
                                        x-text="notification.title"></h3>
                                    <p x-show="notification.message"
                                    class="text-pretty text-sm"
                                    x-text="notification.message"></p>
                                </div>
                                <!-- Dismiss -->
                                <button type="button"
                                        class="ml-auto"
                                        x-on:click="(isVisible = false), removeNotification(notification.id)">
                                    <svg xmlns="http://www.w3.org/2000/svg"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                        fill="none"
                                        stroke-width="2"
                                        class="size-5">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </template>
                    <template x-if="notification.variant === 'danger'">
                        <div x-data="{ isVisible: false, timeout: null }"
                            x-cloak
                            x-show="isVisible"
                            class="pointer-events-auto relative border border-danger bg-surface text-on-surface dark:bg-surface-dark dark:text-on-surface-dark"
                            role="alert"
                            x-on:pause-auto-dismiss.window="clearTimeout(timeout)"
                            x-on:resume-auto-dismiss.window="timeout = setTimeout(() => { isVisible = false; removeNotification(notification.id) }, displayDuration)"
                            x-init="$nextTick(() => { isVisible = true }); timeout = setTimeout(() => { isVisible = false; removeNotification(notification.id) }, displayDuration)"
                            x-transition:enter="transition duration-300 ease-out"
                            x-transition:enter-end="translate-y-0"
                            x-transition:enter-start="translate-y-8"
                            x-transition:leave="transition duration-300 ease-in"
                            x-transition:leave-end="-translate-x-24 opacity-0 md:translate-x-24"
                            x-transition:leave-start="translate-x-0 opacity-100">
                            <div class="flex w-full items-center gap-2.5 bg-danger/10 p-4 transition-all duration-300">
                                <!-- Icon -->
                                <div class="rounded-full bg-danger/15 p-0.5 text-danger">
                                    <svg xmlns="http://www.w3.org/2000/svg"
                                        viewBox="0 0 20 20"
                                        fill="currentColor"
                                        class="size-5">
                                        <path fill-rule="evenodd" d="M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0Zm-8-5a.75.75 0 0 1 .75.75v4.5a.75.75 0 0 1-1.5 0v-4.5A.75.75 0 0 1 10 5Zm0 10a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z" clip-rule="evenodd" />
                                    </svg>
                                </div>
                                <div class="flex flex-col gap-2">
                                    <h3 x-show="notification.title"
                                        class="text-sm font-semibold text-danger"
                                        x-text="notification.title"></h3>
                                    <p x-show="notification.message"
                                    class="text-pretty text-sm"
                                    x-text="notification.message"></p>
                                </div>
                                <button type="button"
                                        class="ml-auto"
                                        x-on:click="(isVisible = false), removeNotification(notification.id)">
                                    <svg xmlns="http://www.w3.org/2000/svg"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                        fill="none"
                                        stroke-width="2"
                                        class="size-5">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </template>
                </div>
            </template>
        </div>
    </div>
    ```
- view helper function:
    ```python
    def _toast(response, message, variant="success", title="Notification", extra_triggers=None):
        trigger_data = {
            "notify": {
                "variant": variant,
                "title": title,
                "message": message
            }
        }
        if extra_triggers:
            trigger_data.update(extra_triggers)
        response['HX-Trigger'] = json.dumps(trigger_data)
        return response
    ```

## Workflow: Adding Dpg notification
1. Make sure Dpg notification parts are in place.
2. Add `<c-fancy.notifications />` to beginning of `<body>`.
3. From view, return custom `response`, modified by `_toast`:
    ```python
    response = HttpResponse('')
    response = _toast(response, 'Book added!', title='Success')
    return response
    ```