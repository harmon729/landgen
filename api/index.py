"""
Vercel Serverless Function Entry Point
This file is required for Vercel to recognize the API as a serverless function
"""

from mangum import Mangum
from main import app

# Wrap FastAPI app with Mangum adapter for Vercel compatibility
handler = Mangum(app, lifespan="off")

