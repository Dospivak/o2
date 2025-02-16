import multiprocessing

# Bind to 0.0.0.0:8000
bind = "0.0.0.0:8000"

# Number of worker processes
workers = multiprocessing.cpu_count() * 2 + 1

# Use threads for concurrency
worker_class = 'sync'

# Timeout for worker processes
timeout = 120

# Access log - records incoming HTTP requests
accesslog = "/var/log/gunicorn/access.log"

# Error log - records Gunicorn server goings-on
errorlog = "/var/log/gunicorn/error.log"

# Whether to send Flask output to the error log 
capture_output = True

# How verbose the Gunicorn error logs should be 
loglevel = "info" 