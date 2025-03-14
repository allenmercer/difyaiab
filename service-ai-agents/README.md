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
# Install project dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# OpenAI API Configuration
LLM_API_KEY=your_api_key_here 
LLM_URL=your_api_url 
LLM_MODEL=your_model_name 

# API Settings
# Additional settings as needed
```

⚠️ **IMPORTANT**: Never commit your `.env` file or any sensitive credentials to version control!

### 4. Run the Application

```bash
# Run the FastAPI application using Uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables hot reloading during development, which automatically restarts the server when code changes are detected.

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
  dify-ai-agents:latest
```

Alternatively, you can use Docker Compose for more complex setups.

## API Documentation

Once the service is running, you can access the FastAPI auto-generated documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## WebSocket Endpoint

### Chat Endpoint

Connect to the WebSocket endpoint at `/api/v1/chat` to interact with the LLM.