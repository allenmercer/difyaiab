FROM python:3.11.2-slim

# Set the working directory in the container
WORKDIR /app

# Set PYTHONPATH so the module is discoverable
ENV PYTHONPATH="/app"

# Copy the application code to the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn as the ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]