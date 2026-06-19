FROM jenkins/jenkins:alpine-jdk25

ENV CASC_JENKINS_CONFIG="/var/jenkins_home/casc_configs/jenkins.yaml"
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false \
    -Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true"

USER root
RUN apk update
RUN apk add docker-cli docker-cli-compose
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

RUN curl -L https://updates.jenkins.io/update-center.json -o /dev/null
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

RUN git config --global --add safe.directory /{{cookiecutter.__project_slug}}_bare_repo
