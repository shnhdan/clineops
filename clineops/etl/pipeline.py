import time, json, shutil, os, random
from clineops.etl.fetch import fetch_data
from clineops.etl.transform import transform

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
METRICS_PATH = os.path.join(BASE_DIR, "..", "dashboard", "metrics.json")

def load_history():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH) as f:
            return json.load(f)
    return {"runs": []}

def run():
    history = load_history()
    start = time.time()

    status = "success"
    error_msg = None
    suggestion = None
    fix_code = None
    preview = None
    old_code = None
    new_code = None

    try:
        data = fetch_data()
        value = transform(data)

    except Exception as e:
        status = "failed"
        error_msg = str(e)

        # simulate AI analysis
        if "price" in error_msg:
            suggestion = "Schema drift detected. API field renamed."
            old_code = "return data['price']"
            new_code = "return data.get('price') or data.get('cost')"
            fix_code = new_code
            preview = data.get("cost")

    entry = {
        "status": status,
        "runtime_sec": round(time.time() - start, 3),
        "timestamp": time.time(),
        "error": error_msg,
        "suggestion": suggestion,
        "fix_code": fix_code,
        "preview": preview,
        "old_code": old_code,
        "new_code": new_code
    }

    history["runs"].append(entry)

    # keep last 20 runs
    history["runs"] = history["runs"][-20:]

    os.makedirs(os.path.dirname(METRICS_PATH), exist_ok=True)

    with open(METRICS_PATH, "w") as f:
        json.dump(history, f, indent=2)

if __name__ == "__main__":
    run()
