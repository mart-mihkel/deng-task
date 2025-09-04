FROM python:3.12-alpine

COPY --from=ghcr.io/astral-sh/uv:0.8.15 /uv /uvx /bin/

ADD . /app

WORKDIR /app

RUN apk add --no-cache libpq postgresql-dev python3-dev
RUN uv sync --locked
RUN cat << 'EOF' > /entrypoint.sh
#!/bin/sh
uv run flask --app flaskr init-db
uv run waitress-serve --call flaskr:create_app
EOF

RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
