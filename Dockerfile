FROM python:3.8.2

SHELL ["/bin/bash", "-c"]

COPY ./src /webapp
COPY ./docker/supervisord.conf /etc/supervisord.conf
COPY ./docker/entrypoint.sh /etc/entrypoint.sh
COPY ./docker/crontab /etc/cron.d/etl-cron
WORKDIR /webapp

RUN chmod 0644 /etc/cron.d/etl-cron && \
    mkdir /webapp/logs && \
    apt-get update && apt-get install -y cron && \
    pip install --no-cache-dir pipenv gunicorn supervisor && \
    crontab /etc/cron.d/etl-cron && \
    pipenv install --system --deploy

CMD ["/etc/entrypoint.sh"]