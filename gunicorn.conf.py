# python3 -m gunicorn main:app

import multiprocessing

max_requests = 1000
max_requests_Jitter = 50
log_file = "_"
bind = "0.0.0.0:8000"
worker_class = "uvicorn.workers.UvicornWorker"
# count the number of cpu
workers = (multiprocessing.cpu_count() * 2) + 1
