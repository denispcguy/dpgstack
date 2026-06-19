# Popup
Temporary window on top of current page

## Workflow: Adding popup to page
1. Add the popup to the start of the page:
    ``` html
    <div x-show="open"
            x-cloak
            @click.self="open = false">
        <div x-transition:enter="transition ease-out duration-300"
             x-transition:enter-start="opacity-0 scale-95"
             x-transition:enter-end="opacity-100 scale-100">
            <div hx-get="{% url 'get-result' %}"
                    hx-trigger="intersect once"
                    hx-target="#result">
                <div id="result">
                    <c-svg.spinner />
                </div>
            </div>
        </div>
    </div>
    ```
2. Make sure parent tag has `x-data`:
    ``` html
    <div x-data="{open: false}">
        ...
    </div>
    ```
3. Add an activator for popup to show:
   ``` html
    <button @click="open = true">
        Open popup
    </button>
   ```


## Properties: Popup structure
- `x-data` with popup state:
    ``` html
    <div x-data="{open: false}">

    </div>
    ```
- Inside of `x-data` tag, the popup itself:
    ``` html
    <div x-show="open">

    </div>
    ```
- Popup activator
    ``` html
    <button @click="open = true">
        Open popup
    </button>
   ```

## Properties: Popup tag
- `x-show="open"`: 