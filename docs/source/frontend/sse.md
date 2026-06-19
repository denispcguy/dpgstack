# SSE
Frontend half of SSE (there is also *[backend part](../backend/sse.md)*)

## Properties: SSE Frontend Pieces
- HTMX SSE extension in base.html: `<script src="{% static 'js/htmx.sse.js' %}" defer></script>`
- Template:
  ```
  <div hx-ext="sse" sse-connect="{% url 'my_app:book_updates' %}">
    <div>
      <span sse-swap="message">Waiting for server...</span>
    </div>
  </div>
  ```

## Properties: SSE Use Cases
- Real-time table (`hx-trigger="sse:<message-name>"`)
- Status indicator (`sse-swap`)

## Definition: `sse-swap`
Put the sse result text into the tag.

## Definition: `hx-trigger="sse:<message-name>"`
Trigger tag's request whenever new sse result appears.

## Workflow: How to add SSE to UI?
1. Determine if type of sse is `sse-swap` or `hx-trigger="sse:<>"`.
   - `sse-swap`
      1. Make sure view returns correct text.
      2. Put it on element and have it swapped
   - `hx-trigger="sse:<>"`
      1. Make sure you got `hx-get` or similar on that tag
      2. Add the trigger to the element: hx-trigger="sse:your-message-name".
      3. Ensure the backend sends an event with the matching name.