Welcome to Dpgstack's documentation!
=====================================

It's a heavily opinionated production-ready platform for creating data-driven web applications.

Features
------------------
* All-in-one solution, everything is pre-configured, even IDE settings.
* Define your model and run one command to generate Views, URL routing, Forms, and Factories automatically.
* Use extensible library of HTML components via django-cotton to get your data displayed nicely right away. Customize later without leaving your HTML.
* Deploy with one command. All you need is a server and domain name.
* Monitor your app with dashboards, get notifications if something went wrong, track errors in production.

Notable parts
------------------

1. Backend:

   * `Django <https://docs.djangoproject.com/>`_
   * `PostgreSQL <https://www.postgresql.org/docs/current/index.html>`_

2. Frontend:

   * `HTMX <https://htmx.org/docs/>`_
   * `AlpineJS <https://alpinejs.dev/start-here>`_
   * `TailwindCSS <https://tailwindcss.com/docs>`_

3. Deployment:

   * `Docker <https://docs.docker.com/>`_
   * `NGINX <https://nginx.org/en/docs/>`_
   * `Prometheus <https://prometheus.io/docs/introduction/overview/>`_
   * `Grafana <https://grafana.com/docs/>`_

4. Developer Experience:

   * `Visual Studio Code <https://code.visualstudio.com/docs>`_
   * `Just <https://just.systems/man/en/>`_
   * `UV <https://docs.astral.sh/uv/>`_
   * `Pytest <https://docs.pytest.org/>`_


Get started
------------

#. Install `UV <https://docs.astral.sh/uv/>`_: ::

    curl -LsSf https://astral.sh/uv/install.sh | sh

#. Get the template: ::

    uvx cookiecutter gh:denispcguy/dpgstack


.. toctree::
   :maxdepth: 2
   :caption: Overview
   :hidden:

   overview/approach_to_documentation
   overview/frontend
   usage

.. toctree::
   :maxdepth: 2
   :caption: 1. Backend
   :hidden:

   backend/views
   backend/views/cbv
   backend/views/fbv
   backend/views/misc
   backend/views/notifications
   backend/models/index
   backend/models/models
   backend/models/field
   backend/forms/forms
   backend/forms/accepting_in_view_post
   backend/urls
   backend/settings
   backend/asgi
   backend/context_processors
   backend/core_views_utils
   backend/sse
   backend/state_management
   backend/tasks

.. toctree::
   :maxdepth: 2
   :caption: 2. Frontend
   :hidden:

   frontend/templates
   frontend/forms
   frontend/htmx
   frontend/alpinejs
   frontend/layout
   frontend/notifications
   frontend/sse
   frontend/state_management
   frontend/popup
   frontend/progress_indication
   frontend/django-cotton
   frontend/template_partials
   frontend/events
   frontend/flatpickr
   frontend/common_errors
   frontend/howtos
   frontend/web_push_notifications

.. toctree::
   :maxdepth: 2
   :caption: 3. Deployment
   :hidden:

   deployment/docker
   deployment/gitops
   deployment/monitoring
   deployment/tools

.. toctree::
   :maxdepth: 2
   :caption: 4. Developer Experience
   :hidden:

   dx/vscode
   dx/just
   dx/uv
   dx/suit_model
   dx/blueprint
   dx/builder
   dx/factories
   dx/ai
   dx/human
   dx/zsh
   dx/testing/testing
   dx/testing/views