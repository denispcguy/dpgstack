# Flatpickr
Date(time) user input through nice calendar.

## Properties: DPG Flatpickr parts.
- Flatpickr Library Files:
  - /static/js/flatpickr.min.js
  - /static/css/flatpickr.min.css

- Custom JS: ./static/js/dpg_flatpickr.js
    ```js
    document.addEventListener('alpine:init', () => {
        Alpine.data('flatpickr', () => ({
            init() {
                flatpickr(this.$el, {
                    enableTime: true,
                    dateFormat: 'H.i d.m.Y',
                    time_24hr: true,
                });
            }
        }));
    });
    ```

- Field Component: /templates/cotton/fancy/form/field_flatpickr.html
    ```html
    {% load widget_tweaks %}
    <div class="relative mt-4">
        <label for="{{ field.id_for_label }}"
            class="absolute left-3 top-1 text-xs transition-all {% if field.errors %}text-error dark:text-red-400{% else %}text-primary dark:text-neutral-400{% endif %}">
            {{ label }}
        </label>
        {% render_field field x-data="flatpickr" class="peer block w-full border-b-2 bg-surface-variant px-3 pt-6 pb-2 focus:outline-none dark:text-neutral-100" %}
    </div>
    ```

## Workflow: Add a flatpickr field to my form.
1. Create a [DPG form](../philosophy/forms.md).
2. Make sure the form has `forms.DateTimeField()`
3. Add that field to the form in template:
    `<c-fancy.form.field_flatpickr :field="filter_form.end_date" label="Created Before" />`
