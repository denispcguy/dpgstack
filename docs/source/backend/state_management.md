# State management. Backend
Processing stateful requests in Django views.

## Workflow: Reading state from HTMX
1. Access state via request.GET for filtered queries.
2. Use request.POST or request.body for data mutations.
3. Return specific HTML fragments based on the state detected in headers or query strings.
