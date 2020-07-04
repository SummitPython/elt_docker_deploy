FROM python:3.8.2

SHELL ["/bin/bash", "-c"]

# Copia os arquivos de configuração para seus lugares
# Configuração do Supervisor
COPY ./docker/supervisord.conf /etc/supervisor/supervisord.conf
# Configuração do agendamento - cron
COPY ./docker/crontab /etc/cron.d/etl-cron
# Script de inicialização do container
COPY ./docker/entrypoint.sh /etc/entrypoint.sh

# Copia os arquivos python
COPY ./src /webapp
COPY ./Pipfile /webapp
COPY ./Pipfile.lock /webapp

WORKDIR /webapp

# Instala as e configura dependencias necessárias para o container
RUN chmod 0644 /etc/cron.d/etl-cron && \
    mkdir /webapp/logs && \
    apt-get update && apt-get install -y cron && \
    pip install --no-cache-dir pipenv gunicorn supervisor && \
    crontab /etc/cron.d/etl-cron && \
    mkdir -p /data/trusted && mkdir /data/raw

# Instala as dependências para a aplicação executar
RUN pipenv install --system --deploy

CMD ["/etc/entrypoint.sh"]