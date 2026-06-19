# Models
Represent your data rows.

## Definition
A Django Model is a Python class that maps to a database table. Each attribute of the model maps to a database column.

## Workflow: Creating a model
1. Define a class that inherits from `models.Model`.
2. Add fields as class attributes.
3. Run `makemigrations` and `migrate` to create the database table.
4. Register the model in `admin.py` to manage it via the Django admin.

## Related
- [Field types](field.md) — available field types and their database equivalents
- [Model patterns](models.md) — common patterns like "Fat Model" and clean() validation