# Testing
Powered by Pytest. Used for surgically poking the application to verify desired responses.

## Properties: Pytest files
- `./pytest.ini`
- `./apps/conftest.py`

## Properties: VSCode shortcuts
- `Ctrl + R`: Refresh tests
- `Ctrl + S`: Run all
- `Ctrl + E`: Run at cursor
- `Ctrl + Tab`: Debug last
- `Ctrl + \``: Debug at cursor

## Properties: Pytest plugins
- pytest-django: the man.
- pytest-playwright
- pytest-base-url
- pytest-cov
- pytest-env
- pytest-factoryboy
- pytest-redis
- pytest-xdist

## Testing `utils.py`
Provide input to utility functions, verify if output corresponds with expectations.

### Workflow: Writing a test for a utility function
1. Create `./apps/my_app/tests/test_utils.py`, load `pytest-django` plugin:
    ```python
    import pytest
    pytestmark = [pytest.mark.django_db]
    ```
2. Import the utility function:
    ```python
    from apps.my_app.utils import my_utility_function
    ```
3. Define the test function with a clear name. Load setup fixtures if needed:
    ```python
    def test_my_utility_function_returns_expected_value():
    ```
4. Define input data and call the function:
    ```python
        input_data = "example"
        result = my_utility_function(input_data)
    ```
5. Assert that the output matches expectations:
    ```python
        assert result == "expected_output"
    ```

## Fixtures
Function to get reusable context for tests.

### Workflow: Create customizable fixture to setup test context
1. Create base fixture 
    ```py
    @pytest.fixture
    def create_author(request):
        Author.objects.create(name=f'Author 1')
    ```
2. Identify the need of customization.
3. Customize to meet the need:
    ```py
    @pytest.fixture
    def create_author(request):
        params = getattr(request, 'param', {})
        if 'author_count' in params:
            for i in range(params['author_count']):
                Author.objects.create(name=f'Author {i}')
        return client
        
    @pytest.mark.parametrize('create_author', [{'author_count': 3}], indirect=True)
    def test_create_many_authors(create_author):
        ...
    ```

### Definition: client fixture with logged in `TestClient`
Always logged in client
```py
from django.contrib.auth.models import User

@pytest.fixture
def client(client):
    username='testuser'
    password='testpassword123'
    user = User.objects.create_user(
        username=username,
        password=password
    )
    client.login(
        username=username,
        password=password
    )
    return client
```
