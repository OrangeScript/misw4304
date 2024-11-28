FROM python:3.10.11

ENV NEW_RELIC_APP_NAME="Entrega_4"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=INGEST_PLACEHOLDER
ENV NEW_RELIC_LOG_LEVEL=info

WORKDIR /

RUN pip install pipenv

COPY Pipfile* ./

RUN pipenv install --deploy --system

RUN pipenv sync

RUN pipenv requirements > requirements.txt

COPY . .

EXPOSE 9000

CMD [ "pipenv", "run", "python", "application.py", "production"]

ENTRYPOINT [ "newrelic-admin", "run-program" ]
