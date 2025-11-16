# observability.py - logging + prometheus metrics
import logging
from prometheus_client import Counter, Gauge, start_http_server
import threading

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("uto")

_submissions = Counter("submissions_total", "Total submissions")
_jobs = Gauge("active_jobs", "Active orchestrations")

def setup_logging():
    def _start():
        start_http_server(8001)
    t = threading.Thread(target=_start, daemon=True)
    t.start()
    logger.info("Observability ready. Prometheus metrics on :8001")

def record_metric(name, amount=1):
    if name == "submissions_total": _submissions.inc(amount)
    if name == "active_jobs": 
        if amount>0: _jobs.inc(amount)
        else: _jobs.dec()
