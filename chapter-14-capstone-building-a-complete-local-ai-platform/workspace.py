# workspace.py
# The complete Private Local AI Workspace: routes requests to the right
# capability, with production-style logging and error handling.

import uuid
from workspace_router import route_request
from workspace_capabilities import HANDLERS, handle_image
from structured_logging import RequestTimer, log_event


def handle_workspace_request(user_input: str, image_path: str | None = None) -> dict:
    request_id = str(uuid.uuid4())[:8]
    capability = route_request(user_input, has_image=image_path is not None)

    log_event("routed", request_id=request_id, capability=capability)

    try:
        with RequestTimer(request_id, capability):
            if capability == "IMAGE":
                if not image_path:
                    answer = "I'd need an image to answer that."
                else:
                    answer = handle_image(user_input, image_path)
            else:
                handler = HANDLERS.get(capability, HANDLERS["CHAT"])
                answer = handler(user_input)

        return {"request_id": request_id, "capability": capability, "answer": answer}

    except Exception as exc:
        log_event("workspace_error", request_id=request_id, capability=capability, error=str(exc))
        return {
            "request_id": request_id,
            "capability": capability,
            "answer": "Something went wrong handling that request. Please try again or rephrase it.",
        }


def main():
    print("Private Local AI Workspace")
    print("Type your question. To include an image: <question> | <image_path>")
    print("Type 'exit' to quit.\n")

    while True:
        raw_input_line = input("You: ").strip()
        if raw_input_line.lower() == "exit":
            break
        if not raw_input_line:
            continue

        if "|" in raw_input_line:
            question, image_path = [p.strip() for p in raw_input_line.split("|", 1)]
        else:
            question, image_path = raw_input_line, None

        result = handle_workspace_request(question, image_path)
        print(f"[{result['capability']}] {result['answer']}\n")


if __name__ == "__main__":
    main()
