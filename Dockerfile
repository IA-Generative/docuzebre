# Start from a Python slim image
FROM python:3.12-slim-bookworm

# Copy the `uv` binary from the UV image
COPY --from=ghcr.io/astral-sh/uv:0.4 /uv /bin/uv

# Copy application code to /app
ADD . /app
WORKDIR /app

# Set up virtual environment path
ENV PATH="/app/.venv/bin:$PATH"

# Add /app to PYTHONPATH
ENV PYTHONPATH="/app:$PYTHONPATH"

# Install dependencies using UV
RUN uv lock && \
    uv sync --frozen

# Define the default command to run your script
CMD ["uv", "run", "bash", "run.sh"]
