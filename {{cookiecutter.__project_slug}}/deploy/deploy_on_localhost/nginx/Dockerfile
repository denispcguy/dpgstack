FROM nginx:1.29.4

RUN rm /etc/nginx/conf.d/default.conf

COPY {{cookiecutter.__project_slug}}.conf /etc/nginx/conf.d/{{cookiecutter.__project_slug}}.conf
