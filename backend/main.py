import sys
from pathlib import Path

# Add project root to sys.path to allow absolute imports of the 'backend' package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.router import router as api_router

# Set up logging format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("trait-trace")

app = FastAPI(
    title="TraitTrace API",
    description="Privacy-First Zero-Party AdTech Personalization Graph & Inference Engine",
    version="1.0.0"
)

# CORS configuration
# Pin origin to dev port 3000. Do not set allow_credentials to True with allow_origins=["*"]!
# We set allow_credentials=False since ephemeral session ID travels in the JSON payload body.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount router
app.include_router(api_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "trait-trace"}

if __name__ == "__main__":
    import uvicorn
    # In-memory NetworkX state relies on a single worker process!
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
