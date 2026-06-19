# Definition: Function Based View (FBV)
A view that is too small to be part of a Class.

## When to use
- The view handles a single action (one HTTP method, one response).
- The logic is simple enough that a class with `get`/`post`/`put` methods would be overkill.
- You don't need shared state across multiple actions.

## Workflow: Writing an FBV
1. Define a function that takes `request` as the first parameter.
2. Return an `HttpResponse` (or `render`, `redirect`, `JsonResponse`).
3. Decorate with `@require_http_methods` if you want to restrict allowed methods.