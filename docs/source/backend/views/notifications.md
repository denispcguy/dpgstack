## Workflow: Triggering Toast notifications
1. ```python
    from apps.core.utils import toast
   ```
2. ```python
    response = render(request, f'{self.template_name}#table_row', context)
    return toast(response, 'Done!')
    ```
