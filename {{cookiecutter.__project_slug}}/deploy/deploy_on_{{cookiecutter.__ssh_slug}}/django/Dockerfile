FROM python:3.13

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY manage.py pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY apps apps
COPY config config
COPY templates templates
COPY theme theme
COPY static static

COPY deploy/deploy_on_localhost/django/entrypoint.sh entrypoint.sh

RUN chmod +x entrypoint.sh

ENTRYPOINT ./entrypoint.sh
