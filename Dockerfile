FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.4 /uv /bin/uv

ADD . /app
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
RUN uv sync --frozen

#RUN uv run streamlit /app/front/main.py
CMD ["uv", "run", "bash", "run.sh"]