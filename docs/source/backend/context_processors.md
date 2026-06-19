# Context processors
System for making data globally available to all templates without manual passing.

## Workflow: Creating a custom context processor
1. Create `apps/my_app/context_processors.py`:
    ```python
    def site_info(request):
        return {
            'site_name': 'My Awesome Project',
            'support_email': 'support@example.com',
        }
    ```
2. Add the dotted path of your function to the `context_processors` list in `settings.py`:
    ```python
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'apps.my_app.context_processors.site_info',
                ],
            },
        },
    ]
    ```
