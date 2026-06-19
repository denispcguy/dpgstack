from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Creates an app in /apps'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str,
                            help='Name of the app to create')

    def handle(self, *args, **options):
        app_name = options['app_name']

        if not app_name.replace('_', '').replace('-', '').isalnum():
            self.stderr.write(self.style.ERROR(
                'App name can only contain letters, numbers, underscores, and hyphens'))
            return

        app_dir = os.path.join(settings.BASE_DIR, 'apps', app_name)
        migrations_dir = os.path.join(app_dir, 'migrations')

        if os.path.exists(app_dir):
            self.stderr.write(self.style.ERROR(
                f'App "{app_name}" already exists'))
            return

        os.makedirs(app_dir, exist_ok=True)
        os.makedirs(migrations_dir, exist_ok=True)

        self.create_file(os.path.join(app_dir, '__init__.py'), '')
        self.create_file(os.path.join(migrations_dir, '__init__.py'), '')

        apps_py_content = f"""from django.apps import AppConfig

class {app_name.title().replace('_', '').replace('-', '')}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
"""
        self.create_file(os.path.join(app_dir, 'apps.py'), apps_py_content)

        empty_files = [
            'models.py',
            'admin.py',
            'forms.py',
            'views.py',
            'urls.py',
            'factories.py'
        ]

        for file_name in empty_files:
            self.create_file(os.path.join(app_dir, file_name), '')

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created app "{app_name}"'))
        self.stdout.write(f'App created at: {app_dir}')
        self.stdout.write('Files created:')
        for file_name in ['__init__.py', 'apps.py'] + empty_files + ['migrations/__init__.py']:
            self.stdout.write(f'  - {file_name}')

    def create_file(self, file_path, content):
        """Helper method to create a file with given content"""
        with open(file_path, 'w') as f:
            f.write(content)
