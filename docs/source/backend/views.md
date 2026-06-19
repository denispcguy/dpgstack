# Views
Accept the data, compute it, and return a response.

## Definition
A view is a callable (function or class) that receives an HTTP request and returns an HTTP response. Views are the core logic layer of a Django application.

## Types
- **Function Based View (FBV)** — A simple function that takes `request` and returns `response`. Best for simple, single-purpose endpoints.
- **Class Based View (CBV)** — A class with methods for each HTTP verb (`get`, `post`, `put`). Best for complex views with multiple actions and shared state.

## Workflow: Choosing between FBV and CBV
- Use FBV when the view does one thing (one action, one response).
- Use CBV when the view needs multiple actions (create, read, update, delete) or shared context across several response types.