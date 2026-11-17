"""
WSGI Entry Point for Production Deployment
==========================================
This file is used by Gunicorn to run the Flask application
"""

import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app
from api.search_api import app

# This is what Gunicorn will use
application = app

if __name__ == "__main__":
    # For local testing with: python wsgi.py
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
