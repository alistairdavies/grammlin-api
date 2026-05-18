FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"
ENV UV_PYTHON_DOWNLOADS=never

COPY . .

ENV STANZA_RESOURCES_DIR=/app/stanza_resources
RUN chmod +x ./scripts/build.sh && ./scripts/build.sh


FROM python:3.13-slim AS app

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/api ./api
COPY --from=builder /app/language ./language
COPY --from=builder /app/folkets_sv_en.db .
COPY --from=builder /app/stanza_resources /app/stanza_resources

ENV STANZA_RESOURCES_DIR=/app/stanza_resources
ENV PATH="/app/.venv/bin:$PATH"

CMD ["sh", "-c", "exec uvicorn api.main:api --host 0.0.0.0 --port ${PORT:-8080}"]
