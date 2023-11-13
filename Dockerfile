FROM docker.io/python:3.11

WORKDIR /app

RUN adduser --system --uid 999 --group --home /app app

COPY /app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app /app /app

USER app

ARG PUBLISHED_VERSION=NOBUILD-INFO
ENV PUBLISHED_VERSION=$PUBLISHED_VERSION

ENV AWS_DEFAULT_REGION=us-east-1

EXPOSE 8000

CMD ["gunicorn", "-w 2", "-b 0.0.0.0:8000", "app:app", "--log-config", "gunicorn-logging.conf", "--timeout", "300"]