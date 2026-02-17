import time
import json
import os
from clineops.etl.fetch import fetch_data
from clineops.etl.transform import transform

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
METRICS_PATH = os.path.join(BASE_DIR, "..", "dashboard", "metrics.json")


def load_history():
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH) as f:
                data = json.load(f)
                if isinstance(data, dict) and "runs" in data:
                    return data
        except:
            pass
    return {"runs": []}


def run():
    history = load_history()

    start = time.time()

    status = "success"
    error_msg = None
    suggestion = None
    preview = None
    old_code = None
    new_code = None

    try:
        data = fetch_data()
        value = transform(data)

    except Exception as e:
        status = "failed"
        error_msg = str(e)

        if "price" in error_msg:
            suggestion = "Schema drift detected — field renamed."
            old_code = "return data['price']"
            new_code = "return data.get('price') or data.get('cost')"
            preview = data.get("cost") if isinstance(data, dict) else None

    entry = {
        "status": status,
        "runtime_sec": round(time.time() - start, 3),
        "timestamp": time.time(),
        "error": error_msg,
        "suggestion": suggestion,
        "preview": preview,
        "old_code": old_code,
        "new_code": new_code
    }

    history["runs"].append(entry)

    history["runs"] = history["runs"][-20:]

    os.makedirs(os.path.dirname(METRICS_PATH), exist_ok=True)

    with open(METRICS_PATH, "w") as f:
        json.dump(history, f, indent=2)


if __name__ == "__main__":
    run()
