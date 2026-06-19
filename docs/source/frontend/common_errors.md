# Common frontend errors
Always seen in browser, while working on templates.

## Properties: Errors shown by django
- "'BookForm' object has no attribute 'get'": *Probably missing get_item table tag. You need to load it with `{% load form_tags %}`*
- "cannot unpack non-iterable NoneType object": *Usually missing cotton component*

## Properties: Errors in browser
- "Tailwind class does not work with hovering over the tag in Gimli Tailwind works?"
    1. Delete ./static/css/dist/styles.css
    2. Regenerate styles.css with `uv run manage.py tailwind start`
