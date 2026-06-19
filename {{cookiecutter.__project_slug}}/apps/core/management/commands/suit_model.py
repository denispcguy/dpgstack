from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import textwrap
from django.db import models
import importlib.resources
import uuid
from apps.core.sidebar_icons import icon_for_model


class Command(BaseCommand):
    """Generate CRUD files for a model using _blueprint templates."""

    BLUEPRINT_APP = 'apps._blueprint'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str)
        parser.add_argument('app', type=str)
        parser.add_argument(
            '--layout',
            type=str,
            choices=['table', 'cards'],
            default='table',
            help='Layout style for the generated view and template (table or cards). Defaults to table.',
        )
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Overwrite existing layout-specific files (view, template, tests) with the new layout. Shared files (forms, serializers, admin, factories, urls) are never overwritten.',
        )

    def _has_syntax_error(self, filepath):
        """Check if a Python file has syntax errors by trying to compile it."""
        try:
            compile(filepath.read_text(), filepath.name, 'exec')
            return False
        except SyntaxError:
            return True

    def _strip_duplicate_imports(self, existing_text, new_content):
        """Remove import lines from new_content if they already exist in existing_text."""
        if not existing_text:
            return new_content
        lines = new_content.splitlines(keepends=True)
        cleaned = []
        for line in lines:
            stripped = line.strip()
            # Skip standalone import lines (from ... import ...) that already exist
            if stripped.startswith('from ') and 'import ' in stripped:
                if stripped in existing_text:
                    continue
            # Skip single `import factory` lines that already exist
            if stripped.startswith('import ') and stripped in existing_text:
                continue
            cleaned.append(line)
        result = ''.join(cleaned)
        # If after stripping imports the result is empty or just whitespace, return nothing
        if not result.strip():
            return ''
        return result

    def _write_component(self, app_path, filename, content, marker, overwrite=False):
        f_path = app_path / filename
        if overwrite:
            f_path.write_text(content)
            self.stdout.write(self.style.SUCCESS(
                f"Overwrote {filename}"))
            return
        text = f_path.read_text() if f_path.exists() else ""

        # Validate file doesn't have pre-existing syntax errors
        if text and self._has_syntax_error(f_path):
            self.stdout.write(self.style.ERROR(
                f"SKIPPING {filename}: file has syntax errors. Fix them before running suit_model again."))
            return

        if marker not in text:
            clean_content = self._strip_duplicate_imports(text, content)
            if not clean_content.strip():
                self.stdout.write(self.style.WARNING(
                    f"{marker}: content is empty after deduplication; skipping."))
                return
            # Write new content and verify the result compiles; rollback on failure
            new_text = text + clean_content
            backup = text  # keep original in case of rollback
            f_path.write_text(new_text)
            if self._has_syntax_error(f_path):
                f_path.write_text(backup)
                self.stdout.write(self.style.ERROR(
                    f"ROLLED BACK {filename}: appending {marker} caused syntax errors. "
                    f"Fix the issue in {f_path} and retry."))
                return
            self.stdout.write(self.style.SUCCESS(
                f"Added {marker} to {filename}"))
        else:
            self.stdout.write(self.style.WARNING(
                f"{marker} already exists in {filename}."))

    def _read_blueprint_file(self, filename):
        """Read a blueprint file from the _blueprint app."""
        try:
            module = importlib.import_module(self.BLUEPRINT_APP)
            blueprint_path = Path(module.__file__).parent / filename
            return blueprint_path.read_text()
        except FileNotFoundError:
            return None

    def _register_app_in_project_urls(self, app_label):
        """Add the app's URL include to config/urls.py if not already present."""
        project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
        config_urls = project_root / "config" / "urls.py"
        if not config_urls.exists():
            self.stdout.write(self.style.WARNING(
                f"Could not find {config_urls}; skipping project URL registration."))
            return

        include_line = f"    path('{app_label}/', include('apps.{app_label}.urls')),\n"
        text = config_urls.read_text()
        if include_line.strip() in text:
            self.stdout.write(self.style.WARNING(
                f"App '{app_label}' already registered in config/urls.py."))
            return

        # Insert before the closing `] + static(...)` line
        marker = "] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"
        if marker in text:
            new_text = text.replace(
                marker,
                include_line +
                "] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"
            )
            config_urls.write_text(new_text)
            self.stdout.write(self.style.SUCCESS(
                f"Registered '{app_label}' URLs in config/urls.py."))
        else:
            self.stdout.write(self.style.WARNING(
                f"Could not locate insertion point in config/urls.py."))

    def _register_in_sidebar(self, model_name, view_name):
        """Add a sidebar entry for the model if not already present."""
        project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
        sidebar_path = project_root / "templates" / "cotton" / "fancy" / "sidebar" / "sidebar.html"
        if not sidebar_path.exists():
            self.stdout.write(self.style.WARNING(
                f"Could not find {sidebar_path}; skipping sidebar registration."))
            return

        text = sidebar_path.read_text()

        # Check if this view is already registered
        if f'view="{view_name}"' in text:
            self.stdout.write(self.style.WARNING(
                f"Sidebar entry for '{view_name}' already exists."))
            return

        # Get a deterministic SVG icon for this model
        svg_path = icon_for_model(model_name)

        # Build the sidebar piece HTML block
        piece_html = (
            f'            <c-fancy.sidebar.piece name="{model_name}" view="{view_name}">\n'
            f'                <svg xmlns="http://www.w3.org/2000/svg"\n'
            f'                     fill="none"\n'
            f'                     viewBox="0 0 24 24"\n'
            f'                     stroke-width="1.5"\n'
            f'                     stroke="currentColor"\n'
            f'                     class="size-5 shrink-0">\n'
            f'                    {svg_path}\n'
            f'                </svg>\n'
            f'            </c-fancy.sidebar.piece>\n'
        )

        # Insert before the closing </div> of the nav container
        # Find the last </c-fancy.sidebar.piece> and insert after it
        last_piece_marker = '</c-fancy.sidebar.piece>'
        last_idx = text.rfind(last_piece_marker)
        if last_idx == -1:
            self.stdout.write(self.style.WARNING(
                "Could not find a sidebar piece to anchor insertion; skipping."))
            return

        insert_pos = last_idx + len(last_piece_marker)
        new_text = text[:insert_pos] + "\n" + piece_html + text[insert_pos:]
        sidebar_path.write_text(new_text)
        self.stdout.write(self.style.SUCCESS(
            f"Added '{model_name}' to sidebar."))

    def _get_fk_info(self, model_class):
        """Detect if model has a single non-self-referential ForeignKey."""
        fk_fields = [
            field for field in model_class._meta.fields
            if isinstance(field, models.ForeignKey)
            and field.remote_field.model != model_class
        ]
        if len(fk_fields) == 1:
            fk = fk_fields[0]
            parent_model = fk.remote_field.model
            return {
                'field': fk,
                'field_name': fk.name,
                'parent_model_name': parent_model.__name__,
                'parent_snake_name': parent_model.__name__.lower(),
                'parent_factory_name': f"{parent_model.__name__}Factory",
            }
        return None

    def _get_child_relations(self, model_class):
        """Detect reverse ForeignKey relations (models that have a FK pointing TO this model)."""
        child_relations = []
        for relation in model_class._meta.related_objects:
            # Only consider ForeignKey reverse relations (ManyToOneRel), not ManyToMany or OneToOne
            if not isinstance(relation, models.fields.related.ManyToOneRel):
                continue
            child_model = relation.related_model
            # Skip self-referential
            if child_model == model_class:
                continue
            # Get the related_name (use get_accessor_name() which returns the correct default like 'book_set')
            related_name = relation.related_name or relation.get_accessor_name()
            child_relations.append({
                'related_name': related_name,
                'child_model_name': child_model.__name__,
                'child_snake_name': child_model.__name__.lower(),
                'child_app_label': child_model._meta.app_label,
                'child_url_name': f"{child_model._meta.app_label}:{child_model.__name__.lower()}",
            })
        return child_relations

    def _apply_replacements(self, content, model_name, app_label, snake_name, fields, layout='table', fk_info=None, is_package_view=False, child_relations=None):
        """Apply string replacements to blueprint content."""
        template_name = f'{app_label}/{snake_name}.html'
        url_name = f'{app_label}:{snake_name}'
        url_name_detail = f'{app_label}:{snake_name}_detail'
        replacements = {
            'BlueprintSimpleModel': model_name,
            'BlueprintSimpleModelForm': f'{model_name}Form',
            'BlueprintSimpleModelView': f'{model_name}View',
            'BlueprintSimpleModelFactory': f'{model_name}Factory',
            'BlueprintSimpleModelAdmin': f'{model_name}Admin',
            'BlueprintSimpleModelSerializer': f'{model_name}Serializer',
            'BlueprintChildModel': model_name,
            'BlueprintChildModelForm': f'{model_name}Form',
            'BlueprintChildModelFactory': f'{model_name}Factory',
            'BlueprintChildModelAdmin': f'{model_name}Admin',
            'BlueprintChildModelSerializer': f'{model_name}Serializer',
            '_blueprint_table_child.html': template_name,
            '_blueprint_cards_child.html': template_name,
            '_blueprint_table.html': template_name,
            '_blueprint_cards.html': template_name,
            "['name', 'description']": repr(fields),
            'TableView': f'{model_name}View',
            'CardView': f'{model_name}View',
            '_blueprint:table_child_detail': url_name_detail,
            '_blueprint:table_child': url_name,
            '_blueprint:cards_child': url_name,
            '_blueprint:table_detail': url_name_detail,
            '_blueprint:table': url_name,
            '_blueprint:cards': url_name,
            'forms_child': 'forms',
        }

        # Only replace relative imports when writing to views.py (single file).
        # For views/ package files, keep the existing from ..models / from ..forms.
        if not is_package_view:
            replacements['from ..models'] = 'from .models'
            replacements['from ..forms'] = 'from .forms'

        if fk_info:
            replacements['BlueprintParentModel'] = fk_info['parent_model_name']
            replacements['ParentModel'] = fk_info['parent_model_name']
            replacements['parent_field'] = fk_info['field_name']
            replacements['ParentFactory'] = fk_info['parent_factory_name']
            parent_snake = fk_info['parent_snake_name']
            parent_app_label = fk_info['field'].remote_field.model._meta.app_label
            parent_url = f'{parent_app_label}:{parent_snake}'
            # parent_url_name must be replaced BEFORE the generic _blueprint:table replacement
            # so it correctly points to the parent's URL, not the child's
            content = content.replace("parent_url_name = '_blueprint:table'", f"parent_url_name = '{parent_url}'")
            content = content.replace("parent_url_name = '_blueprint:cards'", f"parent_url_name = '{parent_url}'")

        for old, new in replacements.items():
            content = content.replace(old, new)

        # Replace child action buttons placeholder with actual buttons
        if child_relations:
            child_buttons_html = ""
            for child in child_relations:
                child_buttons_html += (
                    f'                                <c-fancy.table.action-button text="{child["related_name"]}"\n'
                    f'                                                             hx-get="{{% url \'{child["child_url_name"]}\' %}}"\n'
                    f'                                                             hx-vals=\'{{"parent_pk": "{{{{ piece.id }}}}", "action": ""}}\'\n'
                    f'                                                             hx-target="body"\n'
                    f'                                                             hx-push-url="true" />\n'
                )
            content = content.replace('CHILD_ACTION_BUTTONS', child_buttons_html)
        else:
            content = content.replace('CHILD_ACTION_BUTTONS', '')

        return content

    def _get_field_test_value(self, field, model_name, is_first=False):
        """Return a type-appropriate Python literal string for a test value."""
        if isinstance(field, models.CharField):
            return repr(f'New {model_name}') if is_first else repr(f'value_{field.name}')
        elif isinstance(field, models.TextField):
            return repr('A description')
        elif isinstance(field, (models.IntegerField, models.PositiveIntegerField,
                                models.PositiveSmallIntegerField, models.SmallIntegerField,
                                models.BigIntegerField)):
            return '42'
        elif isinstance(field, models.BooleanField):
            return 'True'
        elif isinstance(field, models.DateTimeField):
            return repr('2024-01-01 12:00:00')
        elif isinstance(field, models.DateField):
            return repr('2024-01-01')
        elif isinstance(field, models.EmailField):
            return repr('test@example.com')
        elif isinstance(field, models.URLField):
            return repr('https://example.com')
        elif isinstance(field, (models.DecimalField, models.FloatField)):
            return '1.5'
        else:
            return repr(f'value_{field.name}')

    def _apply_test_replacements(self, content, model_name, app_label, snake_name, fields, layout='table', fk_info=None, model_class=None):
        """Apply string replacements to blueprint test content."""
        # Determine test field (first concrete editable field) for PUT payloads
        test_field = fields[0] if fields else 'name'
        test_field_old_value = f'Old {model_name}'
        test_field_new_value = f'Updated {model_name}'
        test_field_wrong = f'{test_field}asfsaf'

        # Determine ordering field for sorting (use first field, fallback to id)
        order_field = fields[0] if fields else 'id'

        # URL names
        url_name = f"{app_label}:{snake_name}"
        url_name_detail = f"{app_label}:{snake_name}_detail"

        # Class name based on layout
        test_class_name = f'Test{model_name}View'

        # Build per-field typed variable declarations and dynamic POST payload
        if fields and model_class is not None:
            field_var_lines = []
            payload_items = ["'action': action"]
            for i, field_name in enumerate(fields):
                try:
                    field_obj = model_class._meta.get_field(field_name)
                    val = self._get_field_test_value(field_obj, model_name, is_first=(i == 0))
                except Exception:
                    val = repr(f'value_{field_name}')
                field_var_lines.append(f"{field_name} = {val}")
                payload_items.append(f"'{field_name}': {field_name}")
            # The first field variable declaration (replaces the single blueprint line)
            first_field_var_decl = field_var_lines[0]
            # All field variable declarations joined (for multi-field replacement)
            all_field_var_decls = "\n        ".join(field_var_lines)
            # test_field_value is the value of the first field
            first_field = fields[0]
            try:
                first_field_obj = model_class._meta.get_field(first_field)
                test_field_value = self._get_field_test_value(first_field_obj, model_name, is_first=True).strip("'\"")
            except Exception:
                test_field_value = f'New {model_name}'
        else:
            first_field = test_field
            field_var_lines = [f"{test_field} = 'New {model_name}'"]
            all_field_var_decls = field_var_lines[0]
            first_field_var_decl = field_var_lines[0]
            payload_items = ["'action': action", f"'{test_field}': {test_field}"]
            test_field_value = f'New {model_name}'

        if fk_info:
            payload_items.append("'parent_pk': parent.pk")

        dynamic_payload = "{" + ", ".join(payload_items) + "}"

        # Build dict(...) syntax version of the payload for blueprint replacement
        # payload_items are like ["'action': action", "'title': title", "'position': position"]
        # Convert to dict(...) kwargs: action=action, title=title, position=position
        def _to_kwarg(item):
            if item == "'action': action":
                return "action=action"
            if item == "'parent_pk': parent.pk":
                return "parent_pk=parent.pk"
            # "'fieldname': fieldname" -> "fieldname=fieldname"
            key = item.split("': ")[0].strip("'")
            val = item.split("': ")[1]
            return f"{key}={val}"

        dynamic_payload_dict = "dict(" + ", ".join(_to_kwarg(i) for i in payload_items) + ")"
        # Without parent_pk (for the non-child blueprint line)
        payload_items_no_fk = [i for i in payload_items if i != "'parent_pk': parent.pk"]
        dynamic_payload_dict_no_fk = "dict(" + ", ".join(_to_kwarg(i) for i in payload_items_no_fk) + ")"

        # 1. Replace imports and absolute model names first
        content = content.replace('from apps._blueprint import factories as f',
                                  f'from apps.{app_label} import factories as f')
        content = content.replace(
            'from apps._blueprint import models as m', f'from apps.{app_label} import models as m')
        content = content.replace('from apps._blueprint.models import BlueprintSimpleModel',
                                  f'from apps.{app_label}.models import {model_name}')
        content = content.replace('from apps._blueprint.models import BlueprintChildModel',
                                  f'from apps.{app_label}.models import {model_name}')

        # 2. Replace URL definitions (longer/more specific first to avoid substring matches)
        content = content.replace(
            "reverse('_blueprint:table_child_detail'", f"reverse('{url_name_detail}'")
        content = content.replace(
            "reverse('_blueprint:table_child')", f"reverse('{url_name}')")
        content = content.replace(
            "reverse('_blueprint:cards_child')", f"reverse('{url_name}')")
        content = content.replace(
            "reverse('_blueprint:table_detail'", f"reverse('{url_name_detail}'")
        content = content.replace(
            "reverse('_blueprint:table')", f"reverse('{url_name}')")
        content = content.replace(
            "reverse('_blueprint:cards')", f"reverse('{url_name}')")

        # 3. Structural replacements (Entire expressions matching the blueprint file)
        # Replace dict literal forms
        content = content.replace(
            "{'action': action, 'name': name, 'description': 'A description'}", dynamic_payload)
        content = content.replace(
            "{'action': action, 'name': name, 'description': 'A description', 'parent_pk': parent.pk}", dynamic_payload)
        # Replace dict(...) call forms (what the blueprint actually uses)
        content = content.replace(
            "dict(action=action, name=name, description='A description')", dynamic_payload_dict_no_fk)
        content = content.replace(
            "dict(action=action, name=name, description='A description', parent_pk=parent.pk)", dynamic_payload_dict)

        # 3b. Replacements that must happen BEFORE BlueprintSimpleModel substitution in step 5
        content = content.replace("name = 'New BlueprintSimpleModel'", all_field_var_decls)
        content = content.replace("name = 'New BlueprintChildModel'", all_field_var_decls)
        content = content.replace(
            f"BlueprintSimpleModel.objects.filter(name=name)",
            f"{model_name}.objects.filter({test_field}={test_field})")
        content = content.replace(
            f"BlueprintChildModel.objects.filter(name=name)",
            f"{model_name}.objects.filter({test_field}={test_field})")

        # 4. Dictionary syntax inside PUT updates
        content = content.replace("dict(action=action, name='New Name')",
                                  f"dict(action=action, {test_field}='{test_field_new_value}')")
        content = content.replace("dict(action=action, names='non existent key')",
                                  f"dict(action=action, {test_field_wrong}='non existent key')")

        # 5. Variable definitions and query updates
        replacements = {
            'BlueprintSimpleModel': model_name,
            'BlueprintSimpleModelFactory': f'{model_name}Factory',
            'BlueprintChildModel': model_name,
            'BlueprintChildModelFactory': f'{model_name}Factory',
            '_blueprint': app_label,
            'TestTableView': test_class_name,
            'TestCardView': test_class_name,
            "'nameasfsaf'": f"'{test_field_wrong}'",
            "'names'": f"'{test_field_wrong}'",

            f"filter(name={test_field})": f"filter({test_field}={test_field})",
            # Instance assignment modifications
            "piece.name = 'Old Name'": f"piece.{test_field} = '{test_field_old_value}'",
            "piece.name == 'New Name'": f"piece.{test_field} == '{test_field_new_value}'",
            "name='New Name'": f"{test_field}='{test_field_new_value}'",
            "assert 'name' in": f"assert '{test_field}' in",

            # Fallbacks and helper structural matching
            "set([piece.id for piece in p])": f"set([piece.{order_field} for piece in p])",
            "r.context['piece'] == BlueprintSimpleModel.objects.get(pk=1)": f"r.context['piece'] == {model_name}.objects.get(pk=1)",
            "r.context['fields'] == ['name', 'description']": f"r.context['fields'] == {repr(fields)}",
            "'name': name": f"'{test_field}': {test_field}",
        }

        if fk_info:
            replacements['ParentFactory'] = fk_info['parent_factory_name']
            replacements['parent_field'] = fk_info['field_name']

        for old, new in replacements.items():
            content = content.replace(old, new)

        return content

    def handle(self, *args, **options):
        model_name = options['model_name']
        if not model_name[0].isupper():
            raise CommandError(
                f"Model name '{model_name}' must start with an uppercase letter (e.g., '{model_name.capitalize()}')."
            )
        app_label = options['app']
        snake_name = model_name.lower()
        layout = options['layout']

        try:
            model_class = apps.get_model(app_label, model_name)
            app_path = Path(apps.get_app_config(app_label).path)

            # Detect ForeignKey
            fk_info = self._get_fk_info(model_class)
            has_single_fk = fk_info is not None

            # Detect child relations (reverse FK)
            child_relations = self._get_child_relations(model_class)

            fields = [
                field.name
                for field in model_class._meta.get_fields()
                if field.concrete
                and field.editable
                and not field.primary_key
                and not field.many_to_many
                and not (has_single_fk and field.name == fk_info['field_name'])
                and not getattr(field, 'auto_now', False)
                and not getattr(field, 'auto_now_add', False)
                and not (
                    isinstance(field, (models.DateTimeField, models.DateField))
                    and field.default is not models.fields.NOT_PROVIDED
                )
            ]

            # Form - read from blueprint
            form_blueprint = 'forms_child.py' if has_single_fk else 'forms.py'
            blueprint_form = self._read_blueprint_file(form_blueprint)
            if blueprint_form:
                form_content = self._apply_replacements(
                    blueprint_form, model_name, app_label, snake_name, fields, layout, fk_info)
                self._write_component(
                    app_path, "forms.py", form_content, f"{model_name}Form")

            # Serializer - read from blueprint
            blueprint_serializer = self._read_blueprint_file('serializers.py')
            if blueprint_serializer:
                serializer_content = self._apply_replacements(
                    blueprint_serializer, model_name, app_label, snake_name, fields, layout, fk_info)
                self._write_component(
                    app_path, "serializers.py", serializer_content, f"{model_name}Serializer")

            # Admin - generate directly
            list_display = ", ".join(f"'{f}'" for f in fields)
            admin_content = (
                f"from django.contrib import admin\n"
                f"from .models import {model_name}\n\n"
                f"@admin.register({model_name})\n"
                f"class {model_name}Admin(admin.ModelAdmin):\n"
                f"    list_display = [{list_display}]\n"
            )
            self._write_component(
                app_path, "admin.py", admin_content, f"@admin.register({model_name})")

            # View - read from blueprint based on layout
            view_blueprint_path = f'views/{layout}_child.py' if has_single_fk else f'views/{layout}.py'
            blueprint_view = self._read_blueprint_file(view_blueprint_path)
            if blueprint_view:
                view_content = self._apply_replacements(
                    blueprint_view, model_name, app_label, snake_name, fields, layout, fk_info, is_package_view=True)

                views_py = app_path / "views.py"
                views_dir = app_path / "views"

                if views_py.exists() and not views_dir.exists():
                    # Backward compatibility: app already has views.py
                    # Re-apply replacements for single-file imports
                    view_content = self._apply_replacements(
                        blueprint_view, model_name, app_label, snake_name, fields, layout, fk_info, is_package_view=False)
                    self._write_component(
                        app_path, "views.py", view_content, f"class {model_name}View", overwrite=options['overwrite'])
                else:
                    # Package approach (intray-style)
                    views_dir.mkdir(parents=True, exist_ok=True)
                    init_file = views_dir / "__init__.py"
                    if not init_file.exists():
                        init_file.write_text("")

                    view_file = views_dir / f"{snake_name}.py"
                    if options['overwrite'] or not view_file.exists():
                        view_file.write_text(view_content)
                        self.stdout.write(self.style.SUCCESS(
                            f"{'Overwrote' if options['overwrite'] else 'Created'} view at {view_file}"))
                    else:
                        self.stdout.write(self.style.WARNING(
                            f"View {view_file} already exists."))

                    import_line = f"from .{snake_name} import {model_name}View\n"
                    all_entry = f"    '{model_name}View',\n"
                    init_text = init_file.read_text()
                    if import_line not in init_text:
                        lines = init_text.splitlines(keepends=True)

                        # 1. Insert import at the top after the last existing import
                        last_import_idx = -1
                        for i, line in enumerate(lines):
                            if line.startswith('from .') or line.startswith('import '):
                                last_import_idx = i
                        insert_pos = last_import_idx + 1 if last_import_idx >= 0 else 0
                        lines.insert(insert_pos, import_line)

                        # 2. Add to __all__ before the closing ]
                        all_end_idx = -1
                        for i, line in enumerate(lines):
                            if line.strip() == ']':
                                all_end_idx = i
                        if all_end_idx >= 0:
                            lines.insert(all_end_idx, all_entry)

                        init_file.write_text(''.join(lines))
                        self.stdout.write(self.style.SUCCESS(
                            f"Added {model_name}View to views/__init__.py"))
                    else:
                        self.stdout.write(self.style.WARNING(
                            f"{model_name}View already in views/__init__.py"))

            # Template - read from blueprint based on layout
            template_filename = f'templates/_blueprint_{layout}_child.html' if has_single_fk else f'templates/_blueprint_{layout}.html'
            blueprint_template = self._read_blueprint_file(template_filename)
            if blueprint_template:
                tpl_dir = app_path / Path('templates') / app_label
                tpl_dir.mkdir(parents=True, exist_ok=True)
                tpl_file = tpl_dir / f"{snake_name}.html"

                if options['overwrite'] or not tpl_file.exists():
                    template_content = self._apply_replacements(
                        blueprint_template, model_name, app_label, snake_name, fields, layout, fk_info, child_relations=child_relations)
                    tpl_file.write_text(template_content)
                    self.stdout.write(self.style.SUCCESS(
                        f"{'Overwrote' if options['overwrite'] else 'Created'} template at {tpl_file}"))
                else:
                    self.stdout.write(self.style.WARNING(
                        f"Template {tpl_file} already exists."))

            # URL - generate directly
            urls_py = app_path / "urls.py"
            if urls_py.exists() and "urlpatterns" in urls_py.read_text():
                url_content = (
                    f"\nfrom django.urls import path\n"
                    f"from . import views\n\n"
                    f"app_name = '{app_label}'\n"
                    f"urlpatterns += [\n"
                    f"    path('{snake_name}/', views.{model_name}View.as_view(), name='{snake_name}'),\n"
                    f"    path('{snake_name}/<int:pk>/', views.{model_name}View.as_view(), name='{snake_name}_detail'),\n"
                    f"]\n"
                )
            else:
                url_content = (
                    f"from django.urls import path\n"
                    f"from . import views\n\n"
                    f"app_name = '{app_label}'\n"
                    f"urlpatterns = [\n"
                    f"    path('{snake_name}/', views.{model_name}View.as_view(), name='{snake_name}'),\n"
                    f"    path('{snake_name}/<int:pk>/', views.{model_name}View.as_view(), name='{snake_name}_detail'),\n"
                    f"]\n"
                )
            self._write_component(
                app_path, "urls.py", url_content, f"'{snake_name}/'")

            # Register app URLs in project config/urls.py
            self._register_app_in_project_urls(app_label)

            # Register in sidebar (skip child models that require parent_pk)
            if not has_single_fk:
                view_name = f"{app_label}:{snake_name}"
                self._register_in_sidebar(model_name, view_name)

            # Factory - generate dynamically based on field types
            field_lines = []
            for field in model_class._meta.fields:
                if field.primary_key or isinstance(field, models.AutoField):
                    continue

                if isinstance(field, models.ForeignKey):
                    parent_model = field.remote_field.model
                    parent_factory = f"{parent_model.__name__}Factory"
                    faker = f"factory.SubFactory('apps.{app_label}.factories.{parent_factory}')"
                elif isinstance(field, models.CharField):
                    faker = f"factory.Sequence(lambda n: f'obj-{{n}}-{{uuid.uuid4().hex[:6]}}')"
                elif isinstance(field, models.TextField):
                    faker = "factory.Faker('paragraph', nb_sentences=3)"
                elif isinstance(field, (models.IntegerField, models.PositiveIntegerField)):
                    faker = "factory.Faker('random_int', min=1, max=9999)"
                elif isinstance(field, models.BooleanField):
                    faker = "factory.Faker('boolean', chance_of_getting_true=50)"
                elif isinstance(field, models.DateField):
                    faker = "factory.Faker('date_this_decade')"
                elif isinstance(field, models.DateTimeField):
                    faker = "factory.Faker('date_time_this_year')"
                elif isinstance(field, models.EmailField):
                    faker = "factory.Faker('email')"
                elif isinstance(field, models.URLField):
                    faker = "factory.Faker('url')"
                else:
                    faker = f"factory.Sequence(lambda n: f'obj-{{n}}-{{uuid.uuid4().hex[:6]}}')"

                field_lines.append(f"    {field.name} = {faker}")

            factory_string = (
                f"import factory\n"
                f"from .models import {model_name}\n\n"
                f"class {model_name}Factory(factory.django.DjangoModelFactory):\n"
                f"    class Meta:\n"
                f"        model = {model_name}\n\n"
            )
            factory_string += "\n".join(field_lines) + "\n"

            self._write_component(app_path, 'factories.py',
                                  factory_string, f"class {model_name}Factory")

            # Tests - read from blueprint based on layout
            test_blueprint_path = f'tests/test_{layout}_child.py' if has_single_fk else f'tests/test_{layout}.py'
            blueprint_test = self._read_blueprint_file(test_blueprint_path)
            if blueprint_test:
                test_content = self._apply_test_replacements(
                    blueprint_test, model_name, app_label, snake_name, fields, layout, fk_info, model_class=model_class)

                # Ensure tests/test_views directory exists
                tests_dir = app_path / 'tests' / 'test_views'
                tests_dir.mkdir(parents=True, exist_ok=True)
                # Create __init__.py files if they don't exist
                for init_path in [app_path / 'tests' / '__init__.py', tests_dir / '__init__.py']:
                    if not init_path.exists():
                        init_path.write_text('')

                test_filename = f"tests/test_views/test_{snake_name}.py"
                self._write_component(
                    app_path, test_filename, test_content, f"class Test{model_name}View", overwrite=options['overwrite'])

        except LookupError:
            self.stdout.write(self.style.ERROR(
                f"Model {app_label}.{model_name} not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))