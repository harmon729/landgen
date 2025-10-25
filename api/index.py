"""
Vercel Serverless Function Entry Point
This file is required for Vercel to recognize the API as a serverless function
"""

from api.main import app

# Export the FastAPI app for Vercel
handler = app

