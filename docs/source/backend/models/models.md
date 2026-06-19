# Models
Represent your data rows.

## Workflow: Add model
1. Find a good name for your data piece:
    ```python
    class Book(models.Model):
    ```
2. Add necessary fields:
    !!! Always add this to every model
        ```python
        class Meta:
            ordering = ['-created_at']
        ```

## Properties: Quirks
- Use `models.DateTimeField(default=timezone.now)` instead of `models.DateTimeField(auto_now_add=True)`. Helps with testing.


## Workflow: Implementing "Fat Model" logic
1. Identify logic or validation specific to the data object.
2. Override the `clean()` method for custom validation.
3. Define custom methods for data-centric calculations or state changes.
4. Override the `save()` method if logic must trigger on every write.
    ```python
    from django.core.exceptions import ValidationError

    class Book(models.Model):
        title = models.CharField(max_length=255)
        is_published = models.BooleanField(default=False)

        def clean(self):
            if self.published_date and self.published_date > timezone.now():
                raise ValidationError("Published date cannot be in the future.")
    ```

