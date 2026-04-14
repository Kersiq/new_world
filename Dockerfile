FROM python:3.12-slim

ENV PATH="/code/.venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:0.11.2 /uv /uvx /bin/

WORKDIR /code
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . /code
