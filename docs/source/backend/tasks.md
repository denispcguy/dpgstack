# Tasks
Tasks are used for operations outside request/response cycle. Huey is a great library for task queues. Unlike Celery, Huey has everything you need out of the box: a queue and a consumer. Here is how to set it up:
    
1. add 'huey.contrib.djhuey', to INSTALLED_APPS
2. add this config to settings.py:
```python
from pathlib import Path

HUEY = {
    'huey_class': 'huey.SqliteHuey',
    'name': 'myapp_huey.db',
    'filename': Path('data') / 'myapp_huey.db',
    'results': True,
    'store_none': False,
    'immediate': False,
}
```
3. create tasks.py:
```
from huey.contrib.djhuey import db_task
from django.contrib.auth.models import User
from webpush import send_user_notification

@db_task()
def send_push_notification(user, head, body):
    payload = {"head": head, "body": body}
    send_user_notification(user=user, payload=payload, ttl=1000)
    return 'ok'
```
4. run consumer: `uv run manage.py run_huey`