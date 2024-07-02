FROM python:3.12 as builder

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.12-slim as runtime

RUN useradd -m myuser

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:/app/l2d:$PATH"

COPY --from=builder --chown=myuser:myuser ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY --chown=myuser:myuser l2d ./l2d

USER myuser

CMD ["python", "-m", "l2d", "run"]