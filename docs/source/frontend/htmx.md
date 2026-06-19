# HTMX
Server-rendered partial page swaps.

## Definition: HATEOAS
User interacts with a network application entirely through hypermedia provided dynamically by the server.

## Definition: Locality of Behavior
Behavior of a unit of code should be as obvious as possible by looking only at that unit of code.

## Properties: Managing state via URL parameters
- Store UI state (pagination, sorting, search) in the query string: `?page=2&order_by=-created_at`.
- Use `{% hx_urlstate %}` template tag to merge new state with existing parameters automatically.
- Avoid the Django `{% querystring %}` tag to prevent "tainted state" from stale values.
- Avoid passing around state pieces between view and template.

## Workflow: Passing state variable from template to view.
 (https://www.lorenstew.art/blog/bookmarkable-by-design-url-state-htmx/) (https://www.lorenstew.art/blog/eta-htmx-lit-stack)
1. Define what value to pass. For example, in case of a table, it would be something like `order_by` or `page` or `show_completed`.
2. The State has to be in URL! Or in form inputs.
3. Use `{% hx_urlstate request.GET key=override %}` to auto-generate hx-vals JSON from URL params.

## Workflow: Using `hx_urlstate` template tag.
1. `{% load urlstate %}` in your template.
2. Replace manual JSON `hx-vals='{"key": "val", ...}'` with `hx-vals='{% hx_urlstate request.GET key=override %}'`.
3. The tag automatically forwards all URL query parameters and lets you override specific keys.
4. Example: `hx-vals='{% hx_urlstate request.GET page=1 action="sort" order_by=request.GET.order_by|figure_order:field %}'`
5. New URL params are automatically inherited everywhere — no need to touch templates when adding new state.
