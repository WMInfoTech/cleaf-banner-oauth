FROM docker.io/python:3.11

WORKDIR /app

RUN adduser --system --uid 999 --group --home /app app

COPY /app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app /app /app

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

USER app

ARG PUBLISHED_VERSION=NOBUILD-INFO
ENV PUBLISHED_VERSION=$PUBLISHED_VERSION

EXPOSE 8000

CMD ["gunicorn", "-w 2", "-b 0.0.0.0:8000", "app:app", "--log-config", "gunicorn-logging.conf", "--timeout", "300"]