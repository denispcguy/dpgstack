# Events
Communication between Django, HTMX, and AlpineJS.

## Workflow: Triggering client-side events from Django
1. In django view, add the HX-Trigger header to the HttpResponse.
2. Set the header value to the name of your custom event: response["HX-Trigger"] = "entity-updated".
3. Listen for this event in AlpineJS using @entity-updated.window="handleUpdate()".

## Workflow: Communicating between AlpineJS components
1. Use $dispatch('event-name', { data: 'value' }) within an AlpineJS function.
2. Ensure the event bubbles if the listener is a parent or sibling.
3. Catch the data in the receiving component with @event-name.window="myData = $event.detail.data".

## Workflow: Handling HTMX lifecycle hooks
1. Identify the specific phase (e.g., @htmx:after-request or @htmx:before-swap).
2. Attach an AlpineJS listener to the element making the request:
    ```html
    <button hx-get="{% url 'data-endpoint' %}"
            @htmx:after-request="console.log('Status:', event.detail.xhr.status)">
        Check Status
    </button>
    ```

## Properties: Event Scoping
- `.window`: Listens on the global window object.
- `.document`: Listens on the document level.
- `.stop`: Prevents the event from bubbling further.