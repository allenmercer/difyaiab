# Dify AI Agents - Service

## Introduction

Dify AI Agents is a FastAPI-based WebSocket service that enables real-time, streaming conversations with LLMs (Large Language Models). This service provides a foundation for building domain-specific language (DSL) applications that leverage the capabilities of an LLM through a WebSocket interface, allowing for real-time, bidirectional communication between clients and AI models.

## Requirements

- Python 3.11.2
- LLM API Key
- Docker (optional, for containerized deployment)

## Local Development Setup

### 1. Set Up Python Environment

This project requires Python 3.11.2. We'll use the built-in `venv` module to create a virtual environment:

```bash
# Make sure you have Python 3.11.2 installed on your system
# You can check your Python version with:
python3 --version

# Navigate to the project directory
cd /path/to/service-ai-agents

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Verify Python version
python --version  # Should output Python 3.11.2
```

### 2. Install Dependencies

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# if you already have a virtual environment, instruct poetry to not create another virtual env
poetry config virtualenvs.create false

# Install Dependencies
poetry install
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory with the following variables:
```
cp .env.example .env
```
Make sure to update the env variables for the BE to properly work.

**NOTE**: If you are running a docker image as your backend, you will need to use your computers local IP address (usually looks like 192.168.x.x) and not localhost for the DIFY_BACKEND variable.

```
LLM_API_KEY=
LLM_URL=
LLM_MODEL=
LLM_API_VERSION=
DIFY_BACKEND=

# Optional
LOG_LEVEL=setting for log level
```

⚠️ **IMPORTANT**: Never commit your `.env` file or any sensitive credentials to version control!

If you add more environment variables, please update the .env.example with the new variable.

### 4. Run the Application

```bash
# Run the FastAPI application using Uvicorn
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

The `--reload` flag enables hot reloading during development, which automatically restarts the server when code changes are detected.

**NOTE**: If you change environment variables you will need to reload them. The following command will help with that.
```
source .env
```

## Docker Deployment

This service can be containerized using Docker for easier deployment and scalability.

### Building the Docker Image

```bash
# Build the Docker image
docker build -t dify-ai-agents:latest .
```

### Running the Docker Container

```bash
# Run the container with environment variables
docker run -p 8000:8000 \
  -e LLM_API_KEY=your_api_key_here \
  -e LLM_URL=your_api_url \
  -e LLM_MODEL=your_model_name \
  -e LLM_API_VERSION=your_api_version \
  -e DIFY_BACKEND=Dify_backend_url \
  --name dify-ai-agents \
  dify-ai-agents:latest

# alternatively, run the container with .env file created earlier
docker run -p 8000:8000 \
  --env-file .env \
  --name dify-ai-agents \
  dify-ai-agents:latest
```

## API Documentation

Once the service is running, you can access the FastAPI auto-generated documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## WebSocket Endpoint

### Chat Endpoint

Connect to the WebSocket endpoint at `/api/v1/chat` to interact with the LLM.
