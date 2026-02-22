"""
Gunicorn configuration for production deployment.

Usage:
    gunicorn -c gunicorn.conf.py portfolio_backend.wsgi:application
"""

import multiprocessing
import os

# =============================================================================
# SERVER SOCKET
# =============================================================================

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8000')
backlog = 2048

# =============================================================================
# WORKER PROCESSES
# =============================================================================

# Rule of thumb: (2 * CPU cores) + 1
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 5

# =============================================================================
# LOGGING
# =============================================================================

accesslog = '-'  # stdout
errorlog = '-'   # stderr
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# =============================================================================
# PROCESS NAMING
# =============================================================================

proc_name = 'portfolio_backend'

# =============================================================================
# SERVER MECHANICS
# =============================================================================

preload_app = True
max_requests = 1000
max_requests_jitter = 50
graceful_timeout = 30
