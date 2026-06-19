### Properties: Dpgstack CBV
- Inherited from View, named after Model: `class ThoughtView(View)`.
- Define class attributes:
   ```python
   template_name = 'thought.html'
   fields = ['text', 'created_at']
   ```
- Define `_get_context` helper:
   ```python
    def _get_context(self, page=1, order_by='-created_at', **kwargs):
        context = {
            'fields': self.fields,
            'url_name': 'intray:thought',
            'form': ThoughtForm(),
        }
        queryset = Thought.objects.all().order_by(order_by or '-created_at')
        items, page_obj = get_paginated_queryset(queryset, page, paginate_by=8)
        context.update({
            'queryset': items,
            'page_obj': page_obj
        })
        return {**context, **kwargs}
   ```
  - methods: in beginning for every one:
    ```python
    payload = extract_payload(request)
    match payload.pop('action', ''):
    ```
    - http get:
        ```python
        def get(self, request, pk=None):
            payload = request.GET

            common_state = {
                'page': payload.get('page', 1),
                'order_by': payload.get('order_by', '-created_at')
            }
            match payload.pop('action'):
                case '':
                    context = self._get_context(**state)
                    return render(request, self.template_name, context)

                case 'normal-row':
                    piece = get_object_or_404(Thought, pk=pk)
                    context = self._get_context(
                        **state, piece=piece)
                    return render(request, f'{self.template_name}#table_row', context)

                case 'edit-row':
                    piece = get_object_or_404(Thought, pk=pk)
                    context = self._get_context(**state, piece=piece)
                    return render(request, f'{self.template_name}#edit_row', context)

                case 'project-picker':
                    piece = get_object_or_404(Thought, pk=pk)
                    form = ProjectPickerForm()
                    form.fields['parent_project'].queryset = form.fields['parent_project'].queryset.filter(
                        completed=False
                    )
                    context = self._get_context(
                        **state, piece=piece, form=form)
                    return render(request, f'{self.template_name}#project_picker', context)

                case _:
                    return HttpResponseBadRequest()
        ```
    - http put:
      - `instance = get_object_or_404(Thought, pk=pk)` in beginning of method, since `pk` is essential
      - Use `extract_payload(request)` to get the data, then update the instance



## Workflow: Writing view action case
1. Define computation flow:
    ```python
    piece = get_object_or_404(Thought, pk=pk)
    ```
2. Get context, pass needed computed values:
    ```python
    local_state = {'piece': piece}
    context = self._get_context(**shared_state | local_state)
    ```
3. Return rendered Response:
    ```python
    return render(request, f'{self.template_name}#table_row', context)
    ```

### Workflow: Getting `payload` from request.
1. `from apps.core.utils import extract_payload`
2. Pass `request` into it.
3. Get extracted payload as `dict`.
