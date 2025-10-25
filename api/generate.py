"""
Vercel Serverless Function for /api/generate endpoint
"""

from core import GenerateRequest, GenerateResponse, process_generate_request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/", response_model=GenerateResponse)
async def generate_website(request: GenerateRequest):
    """
    Generate a personal website from GitHub username

    Vercel Serverless endpoint - routes from /api/generate to this handler
    """
    return await process_generate_request(request.username)
