# Progress Indication
Signaling background request activity

## Properties: Types
- Ephemeral indicator: Temporary element overwritten by the response
- Consistent indicator: Persistent tag toggled via `hx-indicator`

## Workflow: How to add Ephemeral Indicator
1. Place placeholder inside the `hx-target` container:
    ```html
    <div id="ping-result">
        <c-svg.spinner />
    </div>
    ```
2. Trigger request to swap placeholder with HTML:
   ```html
    <div hx-get="{% url 'get-result' %}"
            hx-trigger="intersect once"
            hx-target="#result">
        <div id="result">
            <c-svg.spinner />
        </div>
    </div>
   ```

## Workflow: How to add Consistent Indicator
1. Create an element with `htmx-indicator` class and a unique ID:
    ``` html
    <div id="google-progress-bar" class="htmx-indicator fixed top-0 left-0 w-full h-1 z-50">
        <div class="h-full bg-gray-500 animate-google-progress"></div>
    </div>
    ```
2. Add the keyframe animation to ./static/css/styles.css:
    ```css
    @keyframes googleProgress {
        0% { left: 0%; width: 0%; opacity: 0.3; }
        50% { left: 0%; width: 100%; opacity: 0.9; }
        100% { left: 100%; width: 0%; opacity: 0.3; }
    }

    .animate-google-progress {
        position: relative;
        animation: googleProgress 1.2s ease-in-out infinite;
    }
    ```
3. Add `hx-indicator="#bar"` to the element initiating the request:
    ```html
    <button hx-get="/data/" hx-indicator="#google-progress-bar">
        Load Data
    </button>
    ```