from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import chat, dify_integration
from app.utils.logger import Logger

app = FastAPI(title="Dify-POC-Agent", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Allow only specific origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

logger = Logger("Dify-POC-Agent")
# Register WebSocket routes for chat
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(dify_integration.router, prefix="/api/v1", tags=["dify_integration"])

@app.get("/")
def health_check():
    return {"status": "Hello from Dify-POC"}