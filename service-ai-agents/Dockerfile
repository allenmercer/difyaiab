FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy Poetry config files for dependency installation
COPY ./service-ai-agents /app/service-ai-agents
COPY ./core /app/core

WORKDIR /app/service-ai-agents

# Configure Poetry to install packages into the global environment
RUN poetry config virtualenvs.create false

# Install Python dependencies using Poetry
RUN poetry install --no-interaction --no-ansi

# Set PYTHONPATH so the module is discoverable
ENV PYTHONPATH="/app"

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn as the ASGI server
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]