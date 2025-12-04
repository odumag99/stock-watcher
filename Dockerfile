#sha로
FROM ghcr.io/astral-sh/uv@sha256:adc592e435810113bd4ec5c40db799cf41dca012d13530d9cd643077bd8cca88

WORKDIR /app

COPY pyproject.toml uv.lock /app/
ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

COPY ./src/ /app/src/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

COPY ./watchers/ /app/watchers/
COPY main.py /app/

ENTRYPOINT ["uv", "run"]
CMD ["main.py"]