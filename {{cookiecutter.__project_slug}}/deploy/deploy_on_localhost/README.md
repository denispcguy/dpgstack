# To deploy project locally:
Step 1. Setup. `just deploy_on_localhost`
Step 2. Push. `just c-l`
Step 3. Monitor. Check out the result:
- http://localhost:{{cookiecutter.local_nginx_port}}/
- http://jenkins.localhost:{{cookiecutter.local_nginx_port}}/
- http://prometheus.localhost:{{cookiecutter.local_nginx_port}}/
- http://grafana.localhost:{{cookiecutter.local_nginx_port}}/
