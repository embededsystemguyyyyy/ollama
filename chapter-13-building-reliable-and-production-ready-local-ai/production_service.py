# production_service.py
# A hardened version of the Chapter 7 tool assistant: bounded
# concurrency, structured logging, and a warm model.

import uuid
from tool_assistant import chat_with_tools
from structured_logging import RequestTimer, log_event
from concurrency_guard import ConcurrencyGuard
from model_warmer import keep_warm

MODEL = "llama3.2:3b"
guard = ConcurrencyGuard(max_concurrent=2)


def handle_request(messages: list[dict]) -> dict:
    request_id = str(uuid.uuid4())[:8]

    try:
        with guard:
            with RequestTimer(request_id, MODEL):
                answer = chat_with_tools(messages)
        return {"request_id": request_id, "status": "ok", "answer": answer}

    except TimeoutError as exc:
        log_event("request_rejected", request_id=request_id, reason="capacity")
        return {"request_id": request_id, "status": "error", "error": str(exc)}

    except Exception as exc:
        log_event("request_error", request_id=request_id, error=str(exc))
        return {"request_id": request_id, "status": "error",
                "error": "An internal error occurred. Please try again."}


def health_check() -> dict:
    """A simple liveness check a load balancer or monitor could poll."""
    import ollama
    try:
        ollama.chat(model=MODEL, messages=[{"role": "user", "content": "ping"}],
                    options={"num_predict": 1})
        return {"status": "healthy", "model": MODEL}
    except Exception as exc:
        return {"status": "unhealthy", "error": str(exc)}


if __name__ == "__main__":
    keep_warm(MODEL)

    print("Production-style service ready. Health check:", health_check())

    messages = [{"role": "user", "content": "What's 42 times 17?"}]
    result = handle_request(messages)
    print(result)
