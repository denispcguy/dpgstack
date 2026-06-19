# Component Templates
Dpgstack uses django-cotton for reusable HTML components. Components live in `templates/cotton/`:

## Creating a component
```html
<!-- templates/cotton/fancy/button.html -->
<button type="{{ type | default:'button' }}" class="{{ class }}">
    {{ slot }}
</button>
```

## Using a component
```html
<c-fancy.button class="px-4 py-2">Click me</c-fancy.button>
```

## Component patterns
- `{{ slot }}` - Default content slot
- `<c-slot name="header">` - Named slots
- `:prop="value"` - Pass dynamic values (Alpine syntax)
- `{{ attrs }}` - Merge extra attributes from caller


## Model Templates
Model templates define how model data is displayed. Each model has a template in `templates/<app>/`.

## Template Structure
Templates use django-cotton components and partialdef for fragments:

```html
<c-base.for-table>
    <c-fancy.table.table>
        <c-slot name="tr_loop">
            {% partialdef table_row %}
                <c-fancy.table.row>
                    <!-- actions popup, then fields -->
                </c-fancy.table.row>
            {% endpartialdef %}
            {% partialdef edit_row %}
                <tr id="row-{{ piece.id }}">
                    <!-- edit form with inline fields -->
                </tr>
            {% endpartialdef %}
            {% for piece in queryset %}
                {% partial table_row %}
            {% endfor %}
        </c-slot>
    </c-fancy.table.table>
</c-base.for-table>
```

## Key patterns
- `{{ piece|get_field:field }}` - Access model field value
- `{{ form|get_item:field_name }}` - Access form field
- `{{ request.GET.order_by|figure_order:field }}` - Sorting indicator
- `{% querystring action='get-edit-row' %}` - Append query params
