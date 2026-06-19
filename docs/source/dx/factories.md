# Factories
Generate mock data for models.

## Properties: Quirks
- `.create_batch()` does not work well with `models.DateTimeField(auto_now_add=True)`.
