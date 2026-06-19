## Testing `views.py`
Send requests to views, analyze the response and any side effects. **View tests are single source of truth for the backend and a blueprint for ui to follow on how to interact with backend**

### Workflow: Writing a test for a FBV
1. Create `./apps/my_app/tests/test_views.py`, load `pytest-django` plugin:
    ```python
    import pytest
    pytestmark = [pytest.mark.django_db]
    ```
2. Define descriptive name, load `client` fixture:
    ```py
    def test_book_author_create_form_success(client):
    ```
3. Define url name, [make sure it is registered in `urls.py`](../backend/urls.md#workflow-register-a-view):
    ```py
        from django.urls import reverse
        url = reverse('books:get_authors')
    ```
4. Define [payload](#properties-payload-types) for the view
5. [Assert](#properties-assertion-types) the response and side effects:
    ```python
        assert r.status_code == 200
        assert Author.objects.filter(name=payload['new_author_name']).exists()
    ```

### Workflow: Writing a test for a CBV:
1. Name it `class TestThoughtView`
2. Define data fixture whole class will use:
    ```python
    @pytest.fixture
    def thoughts(self):
        return f.ThoughtFactory.create_batch(22)
    ```
3. Define test method name: `test_(http method)_(action name)_(desired outcome)`
*Other steps are similar to [FBV](#workflow-writing-a-test-for-a-fbv)*
1. Within method, start with url:
    ```python
    url = reverse('intray:thought')
    ```
2. Define `action`:
    ```python
    action = 'get-new-page'
    ```
3. Define `payload`:
    ```python
    payload = reverse('intray:thought')
    ```

### Properties: Payload types
- File:
    ```python
    from django.core.files.uploadedfile import SimpleUploadedFile

    file = SimpleUploadedFile(
        name="notes.txt",
        content=b'Dummy content of file',
        content_type="text/plain"
    )
    payload = {
        'file': file
    }
    r = client.post(url, data=payload)
    ```
    views.py
    ```python
    file = request.FILES.get('file')
    ```
- GET:
    ```py
        payload = {
            'page': '1'
        }
        r = client.get(url, data=payload)
    ```
    views.py
    ```python
    page = request.GET.get('page')
    ```
- POST:
    ```py
        payload = {
            'new_author_name': 'Jim'
        }
        r = client.post(url, data=payload)
    ```
    views.py
    ```python
    name = request.POST.get('new_author_name')
    ```
*See how `url` changes to hit specific author*
- PUT:
    ```py
        url = reverse('books:author_detail', args=[author.pk])
        payload = 'name=Updated+Name'
        r = client.post(url, data=payload, content_type='application/x-www-form-urlencoded')
    ```
    views.py
    ```python
    from django.http import QueryDict
    put_data = QueryDict(request.body)
    name = put_data.get('name')
    ```
- DELETE:
    ```py
        url = reverse('books:author_detail', args=[author.pk])
        r = client.delete(url)
    ```
    views.py
    ```python
    author = Author.objects.get(pk=pk).delete()
    ```

### Properties: Assertion types
- Status code:
    ```python
    assert r.status_code == 200
    ```
- Returned template context:
    ```python
    payload = {
            'new_author_name': 'Jim'
        }
    r = client.post(url, data=payload)
    assert r.context['queryset'].filter(name='Jim').exists()
    ```
- Proper notification triggered:
    ```python
    trigger_data = json.loads(r.headers['HX-Trigger'])
    assert trigger_data['notify']['message'] == 'Success!'
    ```
- DB Side effects:
    ```python
    assert Author.objects.filter(name='Jim').exists()
    ```


### Workflow: Create HttpRequest instance
1. Use `rf` fixture provided by `pytest-django`:
    ```python
    test_r(rf):
        request = rf.post('no-need-to-have-url', data={'hello': 'yes'})
    ```
