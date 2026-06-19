# Web Push Notifications
Browser push notifications sent from the server to the user's device, even when the browser is not in focus.

## Setup
1. Add `{% webpush_header %}` to the `<head>` of your base template — this loads the required JavaScript.
2. Add `{% webpush_button with_class="..." %}` where you want the subscribe button to appear.

## Workflow: Adding web push to a template
```html
<div>{% webpush_header %}</div>
<div>{% webpush_button with_class="bg-amber-800 cursor-pointer p-2" %}</div>
```

The `{% webpush_header %}` tag loads the service worker and client JS. The `{% webpush_button %}` tag renders a subscribe/unsubscribe button that the user clicks to enable push notifications.