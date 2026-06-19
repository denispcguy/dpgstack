# django-cotton
A library for creating reusable UI components in Django using a modern, tag-based syntax.

## Workflow: Creating a cotton component
1. Create a new HTML file within your app's `templates/cotton/` directory (e.g., `card.html`).
2. Define the outer wrapper and use `{{ attrs }}` to ensure standard HTML attributes like `class` or `id` pass through.
3. Place the `{{ slot }}` variable inside the wrapper to define where nested content will be rendered.
4. Add specific variables (e.g., `{{ title }}`) for data that should be passed as attributes.
5. Call the component in your view template using the `<c-` prefix followed by the filename (e.g., `<c-card title="Hello">World</c-card>`).

## Workflow: Adding SVG to template
1. Prompt an LLM to generate the SVG code for a specific icon or shape. Use google-ai-mode-create-svg.md
2. Create the component file `templates/cotton/svg/icon-name.html`.
3. Paste the SVG code into the file.
4. Reference the icon in your templates using the `<c-svg.icon-name />` syntax.
