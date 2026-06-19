# Alpine.js
Handling browser state. 

## Properties: Alpine.js behavior
- Does not fetch data from server. Only [HTMX](htmx.md) does.
- State's father is `x-data`. Keep the scope within one html file.
- Event driven. `$dispatch('event-name')` to dispatch. `@htmx:after-request` to listen.

## Workflow: Creating global components
1. Create ./static/js/*componentName*.js:
    ```js
    document.addEventListener('alpine:init', () => {
        Alpine.data('componentName', () => ({
            count: 0,
            increment() { this.count++ }
        }));
    });
    ```
2. Customize as needed:
3. Load into base: `<script src="{% static 'js/componentName.js' %}"></script>`
4. Use `x-data="componentName"` to invoke:
    ```html
    <div x-data="componentName">
        <span x-text="count"></span>
        <button @click="increment">Click Me</button>
    </div>
    ```

## Properties: Insides of `Alpine.data('componentName', () => ({ ... }))`
- Variables: `count: 0`
- Methods: `increment() { this.count++ }`
- The constructor: `init() {console.log('hello!')}`
  
## Properties: Magics
- `$refs`: Accesses DOM elements marked with `x-ref`.
- `$el`: References the current element where the expression is executed.
- `$dispatch`: Fires custom browser events that can bubble up.
- `$nextTick`: Executes code only after Alpine has finished updating the DOM.
- `$watch`: Monitors changes to a specific data property.

## Workflow: Using $refs to access DOM elements directly:
1. Select the target element inside an `x-data` scope.
2. Assign a reference name using the `x-ref="name"` attribute.
3. Call the element using $refs.name within your Alpine expressions.
4. Perform standard DOM operations like .focus(), .scrollIntoView(), or .innerHTML = ''.