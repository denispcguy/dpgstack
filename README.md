# Dpgstack

A heavily opinionated, production-ready platform for creating data-driven web applications.

## 🚀 Features

* **All-in-One Solution:** Everything is pre-configured out of the box, including your IDE settings.
* **Code Generation:** Define your model and run a single command to automatically generate Views, URL routing, Forms, and Factories.
* **Modern Frontend:** Uses an extensible library of HTML components via `django-cotton` to display data beautifully right away. Customize later directly inside your HTML.
* **One-Command Deployment:** Deploy instantly. All you need is a server and a domain name.
* **Production Monitoring:** Track errors, monitor your application with built-in dashboards, and receive instant failure notifications.

## 🛠️ Tech Stack & Notable Parts

### 1. Backend
* [Django](https://docs.djangoproject.com/) - The web framework for perfectionists with deadlines.
* [PostgreSQL](https://www.postgresql.org/docs/current/index.html) - Powerful, open-source object-relational database.

### 2. Frontend
* [HTMX](https://htmx.org/docs/) - High-power tools for HTML.
* [AlpineJS](https://alpinejs.dev/start-here) - Rugged, minimal framework for composing JavaScript behavior.
* [TailwindCSS](https://tailwindcss.com/docs) - A utility-first CSS framework.

### 3. Deployment & Operations
* [Docker](https://docs.docker.com/) - Containerization platform.
* [NGINX](https://nginx.org/en/docs/) - High-performance HTTP server and reverse proxy.
* [Prometheus](https://prometheus.io/docs/introduction/overview/) - Systems monitoring and alerting toolkit.
* [Grafana](https://grafana.com/docs/) - Operational dashboards for your metrics.

### 4. Developer Experience (DX)
* [Visual Studio Code](https://code.visualstudio.com/docs) - Pre-configured IDE ecosystem.
* [Just](https://just.systems/man/en/) - Handy command runner for project tasks.
* [UV](https://docs.astral.sh/uv/) - Ultra-fast Python package installer and resolver.
* [Pytest](https://docs.pytest.org/) - Mature, full-featured Python testing tool.

## 🏁 Get Started

### Prerequisites

First, install **UV** on your system:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Bootstrap Your Project

Generate your new application using the official project template:

```bash
uvx cookiecutter gh:denispcguy/dpgstack
```
