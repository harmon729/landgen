"""
LandGen API - FastAPI Backend
Generate personal websites from GitHub profiles
Local development server
"""

from core import GenerateRequest, GenerateResponse, process_generate_request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="LandGen API",
    description="AI-powered personal website generator",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP - in production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "LandGen API is running", "version": "0.1.0"}


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_website(request: GenerateRequest):
    """
    Generate a personal website from GitHub username

    Local development endpoint
    """
    return await process_generate_request(request.username)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
