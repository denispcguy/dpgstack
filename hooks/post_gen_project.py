import subprocess
import sys
import time
import secrets
from pathlib import Path


def generate_django_postgres_prod_env():
    django_env_path = Path('deploy') / \
        'deploy_on_{{cookiecutter.__ssh_slug}}' / 'django' / '.env'
    postgres_exporter_env_path = Path('deploy') / \
        'deploy_on_{{cookiecutter.__ssh_slug}}' / \
        'prometheus' / 'exporters' / '.postgres.env'
    postgres_pass = secrets.token_urlsafe(32)
    env_content = [
        f'POSTGRES_PASSWORD={postgres_pass}',
        f'DJANGO_SECRET_KEY={secrets.token_urlsafe(50)}',
        'DJANGO_DEBUG=0',
        'DJANGO_SETTINGS_MODULE=config.settings',
        'POSTGRES_USER=postgres',
        'POSTGRES_HOST=postgres',
        'POSTGRES_PORT=5432',
        'DJANGO_ALLOWED_HOSTS={{ cookiecutter.domain_name }},localhost,127.0.0.1',
        'POSTGRES_DB={{ cookiecutter.__project_slug }}_prod',
    ]
    django_env_path.write_text("\n".join(env_content) + "\n")

    postgres_exporter_env_context = [
        f'DATA_SOURCE_PASS={postgres_pass}',
        'DATA_SOURCE_USER=postgres',
        f'DATA_SOURCE_URI=postgres:5432/postgres?sslmode=disable'
    ]

    postgres_exporter_env_path.write_text(
        "\n".join(postgres_exporter_env_context) + "\n")

    print('Generated production Django and Postgres .env!')


def generate_jenkins_prod_env():
    jenkins_env_path = Path(
        'deploy') / 'deploy_on_{{cookiecutter.__ssh_slug}}' / 'jenkins' / '.env'

    env_content = [
        f'ADMIN_PASSWORD={secrets.token_urlsafe(32)}',
    ]
    jenkins_env_path.write_text("\n".join(env_content) + "\n")
    print('Generated production Jenkins .env!')


def generate_monitoring_prod_env():
    grafana_env_path = Path(
        'deploy') / 'deploy_on_{{cookiecutter.__ssh_slug}}' / 'grafana' / '.env'

    env_content = [
        f"GF_SECURITY_ADMIN_USER=admin",
        f"GF_SECURITY_ADMIN_PASSWORD={secrets.token_urlsafe(32)}",
    ]

    grafana_env_path.write_text("\n".join(env_content) + "\n")
    print('Generated production Grafana .env!')


def run(command: str):
    print(f'Running: {command}')
    as_list = command.strip().split(' ')
    process = subprocess.Popen(
        as_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    output_lines = []

    for line in process.stdout:
        print(line, end='')
        output_lines.append(line)

    process.wait()

    if process.returncode != 0:
        print(f'\nERROR: Command failed with exit code {process.returncode}')
        sys.exit(1)
    else:
        print('\nSuccess!')


generate_django_postgres_prod_env()
generate_jenkins_prod_env()
generate_monitoring_prod_env()

run('uv sync')
run('uv run --env-file .env manage.py tailwind install')
run('docker volume create {{ cookiecutter.__project_slug }}-pgdata')
run('docker rm -f {{ cookiecutter.__project_slug }}-postgres')
run('docker run --restart always -d --name {{ cookiecutter.__project_slug }}-postgres --env-file .env -v {{ cookiecutter.__project_slug }}-pgdata:/var/lib/postgresql/data -p {{ cookiecutter.local_postgres_port }}:5432 postgres:17.5')
print('Waiting for database to warm up...')
time.sleep(10)
run('uv run --env-file .env just migrate')
run('uv run --env-file .env just populate Book my_app')
run('git init --initial-branch=main')
run('git add .')
run('git commit -m 1st')
