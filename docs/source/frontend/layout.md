# Layout
How HTML pieces come together to form Dpgstack UI.

## Properties: Layout parts
- **Base** — contains all JS scripts in head, default attributes for body, as well as optional notifications and sidebar:
    ```html
    {% load static tailwind_tags %}
    <!DOCTYPE html>
    <html lang="en">
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <head>
            <script src="{% static 'js/darkmode.js' %}" defer></script>
            <script src="{% static 'js/notifications.js' %}" defer></script>
            <script src="{% static 'js/flatpickr.min.js' %}" defer></script>
            <script src="{% static 'js/dpg_flatpickr.js' %}" defer></script>
            <script src="{% static 'js/htmx.min.js' %}" defer></script>
            <script src="{% static 'js/htmx.sse.js' %}" defer></script>
            <script defer src="{% static 'js/alpine.focus.js' %}"></script>
            <script defer src="{% static 'js/alpine.collapse.js' %}"></script>
            <script defer src="{% static 'js/alpine.mask.js' %}"></script>
            <script src="{% static 'js/alpine.min.js' %}" defer></script>
            {% tailwind_css %}
            <link rel="stylesheet" type="text/css" href="{% static 'css/styles.css' %}" />
            <link rel="stylesheet"
                type="text/css"
                href="{% static 'css/flatpickr.min.css' %}" />
            <title>my site</title>
        </head>
        <body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'
            {{ attrs }}
            class="bg-surface dark:bg-surface-dark font-inter text-on-surface dark:text-on-surface-dark overflow-hidden transition-colors duration-300">
            <c-fancy.notifications />
            <c-fancy.sidebar.sidebar>
                {{ slot }}
            </c-fancy.sidebar.sidebar>
        </body>
    </html>
    ```

### Card layout grid
```html
<div class="h-screen flex">
    <div class="flex-1 overflow-y-auto p-6">
        <div class="grid grid-cols-3 sm:grid-cols-4 lg:grid-cols-5 gap-4 p-4">
            {% for piece in queryset %}<c-fancy.card />{% endfor %}
        </div>
    </div>
</div>
```


# Full-height scrollable tables without pixel offsets

How to make tables fill the remaining viewport height without using `h-screen`, `calc()`, or any other fixed pixel offsets.

## Workflow: Converting a table from fixed height to flex-column height

1. Identify the layout chain from `body` down to the scrollable table wrapper.
2. Confirm `body`/base has `overflow-hidden` — this is required for the chain to work.
3. Confirm the content area (`#main-content` or equivalent) has `h-svw` or `h-screen` — this anchors the chain.
4. Add `h-full` to any intermediate wrapper `<div>` that sits between the content area and the table.
5. On the outer table container (`#table-container`), set `class="flex flex-col h-full"`.
6. On the inner scrollable `<div>`, replace `h-screen` with `class="flex-1 min-h-0 overflow-y-scroll"`.
7. Remove any `h-[calc(...)]` or `h-screen` classes in the chain.

## Properties: Height propagation rules

- `h-full` resolves to the parent's computed height.
- `h-svw` resolves to exactly 100vh (dynamic viewport for mobile browsers).
- `flex-1` distributes remaining space in a flex container.
- `min-h-0` overrides the default `min-height: auto` on flex children, allowing them to shrink below their content height. **Required** on the scrollable wrapper — without it, the table can't shrink and overflows anyway.

## Definition: Table layout chain (shoppingitem example)

```
for_table.html body
  → overflow-hidden
    sidebar.html #main-content
      → h-svw          (anchors the chain to viewport height)
        shoppingitem.html flex row
          → h-full      (propagates height through padding)
            table_shopping.html #table-container
              → flex flex-col h-full
                scroll div
                  → flex-1 min-h-0 overflow-y-scroll
                    → table
```

Each layer inherits height from the parent. No pixel values, no overflow, no guessing.

## Workflow: Diagnosing a table that overflows bottom-of-screen

1. Open browser DevTools and inspect the scrollable `<div>`.
2. Check if its height is larger than the viewport minus the UI chrome (sidebar, header, padding).
3. If it uses `h-screen` or `h-[calc(100dvh-*)]`, note that those values are relative to the viewport, **not** the parent element.
4. `h-screen` does not account for parent padding, margins, or sibling elements. That's the overflow source.
5. Apply the conversion workflow above.