1. These domains are binded to ip of the server
- {{cookiecutter.domain_name}}
- jenkins.{{cookiecutter.domain_name}}
- prometheus.{{cookiecutter.domain_name}}
- grafana.{{cookiecutter.domain_name}}
2. Server is accessible via `ssh {{cookiecutter.domain_name}}`, local pub key is added to ~/.ssh/authorized_keys of the server. Server user has root priveleges