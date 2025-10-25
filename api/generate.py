"""
Vercel Serverless Function for /api/generate endpoint
Simple handler without FastAPI for better Vercel compatibility
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler

# Add api directory to path
sys.path.insert(0, os.path.dirname(__file__))

from core import process_generate_request


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests"""
        try:
            # Read request body
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)

            username = data.get("username", "").strip()
            if not username:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"detail": "Username is required"}).encode()
                )
                return

            # Process request (need to handle async in sync context)
            import asyncio

            result = asyncio.run(process_generate_request(username))

            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            response_data = (
                result.model_dump() if hasattr(result, "model_dump") else result.dict()
            )
            self.wfile.write(json.dumps(response_data).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"detail": str(e)}).encode())

    def do_OPTIONS(self):
        """Handle OPTIONS for CORS"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
