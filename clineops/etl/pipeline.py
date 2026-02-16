import time, json, shutil, os
from clineops.etl.fetch import fetch_data
from clineops.etl.transform import transform

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
METRICS_PATH = os.path.join(BASE_DIR, "etl", "metrics.json")
DASHBOARD_PATH = os.path.join(BASE_DIR, "dashboard", "metrics.json")

def run():
    start = time.time()
    status = "success"
    error_msg = None

    try:
        data = fetch_data()
        value = transform(data)
    except Exception as e:
        status = "failed"
        error_msg = str(e)

    metrics = {
        "status": status,
        "runtime_sec": round(time.time() - start, 3),
        "timestamp": time.time(),
        "error": error_msg
    }

    os.makedirs(os.path.dirname(METRICS_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(DASHBOARD_PATH), exist_ok=True)

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    shutil.copy(METRICS_PATH, DASHBOARD_PATH)

if __name__ == "__main__":
    run()
