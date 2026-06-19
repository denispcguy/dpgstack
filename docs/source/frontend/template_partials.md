Define named template fragments using django-template-partials.

## Workflow: Define and render a partial
```django
{% load partialtags %}

{% partialdef table_row %}
    <tr id="row-{{ piece.id }}">
        {% for field in fields %}
            <td>{{ piece|get_field:field }}</td>
        {% endfor %}
    </tr>
{% endpartialdef table_row %}

{% for piece in queryset %}
    {% partial table_row %}
{% endfor %}
```
