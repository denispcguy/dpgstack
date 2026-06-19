# URLs
Since most of the urls simply point to model's view that's typically generated automatically, the urls are quite simple:
```
urlpatterns += [
    path('thought/', views.ThoughtView.as_view(), name='thought'),
    path('thought/<int:pk>/', views.ThoughtView.as_view(),
         name='thought_detail'),
]
```
You first define `urlpatterns = []` and then use `+=` to dynamically populate it as more models are being created and suited.

## URL Namespaces

For apps with multiple related URLs, use `app_name` for namespacing:

```python
# apps/server/urls.py
from django.urls import path
from .views import android_ping

app_name = 'server'

urlpatterns = [
    path('android-ping/', android_ping, name='android-ping'),
]
```

Then include it in `config/urls.py`:
```python
path('server/', include('apps.server.urls')),
```

Templates use namespaced URLs: `{% url 'server:android-ping' %}`


## Properties: `urls.py`
- Imports:
    ```python
    from django.urls import path
    from . import views
    ```
- App name (./apps/<name>/):
    ```python
    app_name = 'server'
    ```
- Urls themselves:
    ```python
    urlpatterns = [
        path('server_ping/', views.server_ping, name='server_ping'),
    ]
    ```

## Workflow: Register a view
1. Make sure `urls.py` is [set up](urls.md#properties-urlspy).
2. Add `path()` to `urlpatterns`
3. Add the arguments to `path()`:
   - route string: `'server_ping/',`
   - view function: `views.server_ping,`
   - url name: `name='server_ping'`
  *all the same names most likely. use `url_dpg` snippet*

