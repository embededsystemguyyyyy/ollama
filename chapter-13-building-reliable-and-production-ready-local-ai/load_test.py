# load_test.py
# A simple concurrent load test to empirically find how many simultaneous
# requests your hardware can actually sustain.

import time
import concurrent.futures
from production_service import handle_request

def run_load_test(num_requests: int = 10, max_workers: int = 5):
    messages = [{"role": "user", "content": "What's 12 * 8?"}]

    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(handle_request, messages) for _ in range(num_requests)]
        results = [f.result() for f in futures]
    elapsed = time.perf_counter() - start

    successes = sum(1 for r in results if r["status"] == "ok")
    failures = num_requests - successes

    print(f"Completed {num_requests} requests in {elapsed:.2f}s")
    print(f"Successes: {successes}, Failures: {failures}")
    print(f"Throughput: {num_requests / elapsed:.2f} requests/sec")


if __name__ == "__main__":
    run_load_test(num_requests=10, max_workers=5)
