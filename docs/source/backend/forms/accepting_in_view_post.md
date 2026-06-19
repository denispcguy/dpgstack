# You are in BookView/post()
You want to accept a form data coming from template.

## Example: Simple save
```python
class BookView:
    ...
    def post(self, request, pk=None):
        payload = extract_payload(request)
        match payload.pop('action', ''):
            case '':
                form = BookForm(payload)
                if form.is_valid():
                    piece = form.save()
                else:
                    response = HttpResponse("Invalid Data", status=400)
                    return toast(
                        form.errors.as_text() or "Invalid data",
                        response,
                        title="Error",
                        variant="danger"
                    )
```

## Walkthrough of Example: Simple save.
1. Initialize a form with payload.
2. Check if form is valid.
3. If it is, save the data.
4. If it is not, return form errors.

