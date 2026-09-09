# test_routing.py
# Confirms the router sends a representative set of requests to the
# expected capability.

from workspace_router import route_request

TEST_CASES = [
    ("What does the contract say about termination?", "DOCUMENTS"),
    ("Calculate 15% of 340", "TOOLS"),
    ("Research the best programming languages for beginners in 2026", "RESEARCH"),
    ("How many products do we have in inventory?", "DATABASE"),
    ("What's your favorite color?", "CHAT"),
]


def run_routing_test():
    correct = 0
    for text, expected in TEST_CASES:
        actual = route_request(text)
        match = "✓" if actual == expected else "✗"
        print(f"{match} '{text[:50]}' -> {actual} (expected {expected})")
        if actual == expected:
            correct += 1

    accuracy = correct / len(TEST_CASES) * 100
    print(f"\nRouting accuracy: {accuracy:.0f}% ({correct}/{len(TEST_CASES)})")


if __name__ == "__main__":
    run_routing_test()
