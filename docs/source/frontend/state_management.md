# State management. Frontend
Managing state in URL.

## Workflow: Updating URL state
1. Identify UI variables (page, filters, sorts).
2. Map variables to an hx-vals JSON object using the `{% hx_urlstate %}` tag.
3. Attach hx-vals to the triggering element to merge with current URL state.

## Workflow: Using `hx_urlstate` template tag
1. `{% load urlstate %}` in your template.
2. Replace `hx-vals='{"page": "{{ page_num }}", "order_by": "{{ ... }}", ...}'` with `hx-vals='{% hx_urlstate request.GET page=page_num %}'`.
3. The tag automatically forwards all existing URL query params and lets you override specific keys.
4. Adding a new URL param to your views automatically propagates to all hx-vals without template changes.
