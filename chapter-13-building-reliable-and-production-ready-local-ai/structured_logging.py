# structured_logging.py
# Structured, machine-parseable logging for AI request lifecycle events.

import json
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("ai_service")


def log_event(event_type: str, **fields):
    entry = {"event": event_type, "timestamp": time.time(), **fields}
    logger.info(json.dumps(entry))


class RequestTimer:
    """Context manager that logs a request's outcome and latency automatically."""

    def __init__(self, request_id: str, model: str):
        self.request_id = request_id
        self.model = model
        self.start = None

    def __enter__(self):
        self.start = time.perf_counter()
        log_event("request_start", request_id=self.request_id, model=self.model)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        elapsed = time.perf_counter() - self.start
        if exc_type is None:
            log_event("request_success", request_id=self.request_id,
                       model=self.model, latency_seconds=round(elapsed, 3))
        else:
            log_event("request_failure", request_id=self.request_id,
                       model=self.model, latency_seconds=round(elapsed, 3),
                       error=str(exc_value))
        return False  # don't suppress the exception
