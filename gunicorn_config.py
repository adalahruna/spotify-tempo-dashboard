"""
Gunicorn Configuration for Production Deployment
================================================
"""

import os
import multiprocessing

# Server Socket
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
backlog = 2048

# Worker Processes
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 120
keepalive = 5

# Logging
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = os.getenv('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process Naming
proc_name = 'spotify_api'

# Server Mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (Optional - uncomment if using HTTPS)
# keyfile = None
# certfile = None

# Restart workers when code changes (development only)
reload = os.getenv('FLASK_ENV') == 'development'

# Preload app for better performance
preload_app = True

# Server Hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    print("="*60)
    print("  SPOTIFY TEMPO ANALYSIS API - STARTING")
    print("="*60)
    print(f"Workers: {workers}")
    print(f"Bind: {bind}")
    print(f"Timeout: {timeout}s")
    print("="*60)

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    print("Reloading workers...")

def worker_int(worker):
    """Called just after a worker has been killed."""
    print(f"Worker {worker.pid} received INT or QUIT signal")

def worker_abort(worker):
    """Called when a worker fails to boot."""
    print(f"Worker {worker.pid} failed to boot")
