import json
import os
from urllib.request import Request, urlopen


BASE_URL = os.getenv(
    "COZY_GECKO_BASE_URL",
    "http://localhost:8000"
).rstrip("/")


def get_json(path: str, timeout: int = 10) -> dict:
    with urlopen(f"{BASE_URL}{path}", timeout=timeout) as response:
        return json.load(response)


def post_json(path: str, payload: dict, timeout: int = 180) -> dict:
    request = Request(
        f"{BASE_URL}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )

    with urlopen(request, timeout=timeout) as response:
        return json.load(response)


def main():
    health = get_json("/health")
    assert health["status"] == "ok"
    print("[OK] FastAPI health")

    ready = get_json("/ready")
    assert ready["status"] == "ready"
    print(f"[OK] Model ready: {ready['model']}")

    generation = post_json(
        "/generate",
        {"prompt": "Respond with exactly two words: Cozy Gecko"}
    )
    assert generation["response"].strip()
    assert generation["model"] == ready["model"]
    print(f"[OK] Generation completed in {generation['duration_ms']} ms")


if __name__ == "__main__":
    main()