# Blueprint App

The `_blueprint` app is a template app used by `suit_model` to generate CRUD code for your models.

## How it works

`suit_model` reads Python source files from `apps/_blueprint/` and applies string replacements (model name, field names, URL names) to produce working CRUD code for your model.

## Included Blueprints

| Blueprint | Purpose | FK support |
|-----------|---------|------------|
| `_blueprint_table.html` | Table layout for simple models | No |
| `_blueprint_table_child.html` | Table layout for models with a ForeignKey | Yes |
| `_blueprint_cards.html` | Card layout for simple models | No |
| `_blueprint_cards_child.html` | Card layout for models with a ForeignKey | Yes |
| `views/table.py` | Table View class (CBV) | No |
| `views/cards.py` | Cards View class (CBV) | No |
| `views/table_child.py` | Table View with FK context handling | Yes |
| `views/cards_child.py` | Cards View with FK context handling | Yes |
| `forms.py` | ModelForm for simple models | No |
| `forms_child.py` | ModelForm including FK field | Yes |
| `serializers.py` | DRF ModelSerializer | Both |
| `factories.py` | Factory Boy factory | Both |
| `tests/test_table.py` | Test suite for table layout | No |
| `tests/test_cards.py` | Test suite for cards layout | No |
| `tests/test_table_child.py` | Test suite for table with FK | Yes |
| `tests/test_cards_child.py` | Test suite for cards with FK | Yes |
| `migrations/0001_initial.py` | Initial migration with both `BlueprintSimpleModel` and `BlueprintChildModel` | - |

## Browsing the Blueprint App

After running the project, these URLs let you see the blueprint views working live:

```
http://localhost:8000/blueprint/table/
http://localhost:8000/blueprint/cards/
```

## Customizing Blueprints

You can modify any file in `apps/_blueprint/` to change how `suit_model` generates code for all future models. The blueprint files use placeholder identifiers like:

- `BlueprintSimpleModel` → replaced with your model name
- `['name', 'description']` → replaced with your model's field list
- `_blueprint:table` → replaced with your app's URL name