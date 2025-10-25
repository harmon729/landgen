"""
Vercel Serverless Function for /api/generate endpoint
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler

# Add api directory to path
sys.path.insert(0, os.path.dirname(__file__))

import asyncio

from core import process_generate_request


class handler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        """Send CORS headers"""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        """Handle OPTIONS for CORS preflight"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        """Handle POST requests"""
        try:
            # Read and parse request body
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"detail": "Empty request body"}).encode())
                return

            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)

            username = data.get("username", "").strip()
            if not username:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(
                    json.dumps({"detail": "Username is required"}).encode()
                )
                return

            # Process request using asyncio
            result = asyncio.run(process_generate_request(username))

            # Send success response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()

            response_data = (
                result.model_dump() if hasattr(result, "model_dump") else result.dict()
            )
            self.wfile.write(json.dumps(response_data).encode())

        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"detail": "Invalid JSON"}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            error_msg = str(e)[:200]  # Limit error message length
            self.wfile.write(
                json.dumps({"detail": f"Internal server error: {error_msg}"}).encode()
            )

    def do_GET(self):
        """Handle GET requests - return method info"""
        self.send_response(405)
        self.send_header("Content-Type", "application/json")
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(
            json.dumps({"detail": "Method GET not allowed. Use POST."}).encode()
        )
