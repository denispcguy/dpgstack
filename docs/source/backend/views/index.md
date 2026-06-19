# Views
Define the logic for incoming HTTP requests.

## Definition
A view is a callable that receives an HTTP request and returns an HTTP response. Views are the entry point for all business logic in a Django application.

## Types
- **Function Based Views (FBV)** — Simple functions for single-purpose endpoints.
- **Class Based Views (CBV)** — Classes with methods per HTTP verb, for complex views.

## Related
- [FBV](fbv.md) — When and how to use function based views
- [CBV](cbv.md) — When and how to use class based views
- [Misc](misc.md) — Error handling, HTTP status codes
- [Notifications](notifications.md) — Toast notifications from views