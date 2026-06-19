# Frontend Forms
Frontend implementation of Django forms using HTMX, AlpineJS, and django-cotton components.

## Definition: Cotton Form Component
A reusable template partial that encapsulates label rendering, error handling, and Tailwind styling for a single Django form field.

## Workflow: Rendering a form with Cotton
1. Pass the form instance from the Django view to the template context.
2. Iterate through fields or call them individually:
    ```html
    {% for field in form %}
        <c-fancy.form.field :field="field" label="{{ field.label }}" />
    {% endfor %}
    ```

## Workflow: Implementing a [Popup](popup.md) Form
1. Wrap the form in a popup component using an AlpineJS variable for visibility:
    ```html
    <div x-data="{ formShown: false }">
        <button @click="formShown = true">Open Form</button>
        
        <c-fancy.form.popup x-show="formShown">
            <form hx-post="{% url 'app:create' %}"
                  hx-target="#item-list"
                  hx-swap="afterbegin"
                  @submit="formShown = false"
                  @htmx:after-request="$event.target.reset()">
                
                <c-fancy.form.field :field="form.name" label="Item Name" />
                <c-fancy.form.submit-button />
            </form>
        </c-fancy.form.popup>
    </div>
    ```
