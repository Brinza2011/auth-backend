# ---------- Stage 1: Builder ----------
FROM python:3.12-slim AS builder

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /uvx /bin/


WORKDIR /app

# Copy dependency file(s) first for caching
COPY pyproject.toml uv.lock ./

# Install dependencies in a separate layer
RUN uv sync --frozen

# Copy application source code
COPY . .

# ---------- Stage 2: Runtime ----------
FROM python:3.12-slim AS runtime

COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /uvx /bin/

RUN useradd --create-home appuser
USER appuser

WORKDIR /app

COPY --from=builder /app /app

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0"]
