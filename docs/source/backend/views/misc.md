# Views
Define the logic for incoming HTTP requests.

## Workflow: Return HTTP errors
1. `from django.http import (error)`
2. Return the class instance directly to terminate the view.
   - `return HttpResponseBadRequest()` for 400.
   - `return HttpResponseForbidden()` for 403.
   - `return HttpResponseNotFound()` for 404.
   - `return HttpResponseNotAllowed()` for 405.
