import time, json, shutil
from fetch import fetch_data
from transform import transform

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
        value = None

    metrics = {
        "status": status,
        "runtime_sec": round(time.time() - start, 3),
        "timestamp": time.time(),
        "error": error_msg
    }

    with open("etl/metrics.json","w") as f:
        json.dump(metrics,f,indent=2)

    # copy for dashboard
    shutil.copy("etl/metrics.json","dashboard/metrics.json")

if __name__ == "__main__":
    run()
