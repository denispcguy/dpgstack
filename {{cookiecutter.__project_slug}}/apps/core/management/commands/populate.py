import importlib
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps


class Command(BaseCommand):
    """uv run manage.py my_app.Book 15"""

    help = 'Populate any model using its corresponding Factory'

    def add_arguments(self, parser):
        parser.add_argument('model_label', type=str,
                            help='Format: app_label.ModelName')
        parser.add_argument('count', type=int, default=10,
                            nargs='?', help='Number of records')

    def handle(self, *args, **options):
        label = options['model_label']
        count = options['count']

        try:
            model_class = apps.get_model(label)
            app_label = model_class._meta.app_label
            model_name = model_class.__name__

            factory_module_path = f"apps.{app_label}.factories"
            factory_module = importlib.import_module(factory_module_path)

            factory_name = f"{model_name}Factory"
            factory_class = getattr(factory_module, factory_name, None)

            if not factory_class:
                raise CommandError(
                    f"Found {factory_module_path} but it has no {factory_name}")

            factory_class.create_batch(count)
            self.stdout.write(self.style.SUCCESS(
                f"Created {count} {model_name}s"))

        except LookupError:
            raise CommandError(
                f"Model '{label}' not found. Did you include the app label?")
        except ImportError:
            raise CommandError(
                f"Could not find factory module at apps.{app_label}.factories")
