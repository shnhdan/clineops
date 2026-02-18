import time, json, os
from clineops.etl.fetch import fetch_data
from clineops.etl.transform import transform
from clineops.engine import analyze_failure

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
METRICS_PATH = os.path.join(BASE_DIR, "..", "dashboard", "metrics.json")


def load():
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH) as f:
                data=json.load(f)
                if "runs" in data:
                    return data
        except:
            pass
    return {"runs":[]}


def reliability(runs):
    if not runs:
        return 0
    ok=sum(1 for r in runs if r["status"]=="success")
    return round(ok/len(runs)*100)


def run():
    history=load()
    start=time.time()

    status="success"
    err=None
    analysis={}

    try:
        data=fetch_data()
        transform(data)

    except Exception as e:
        status="failed"
        err=str(e)
        analysis=analyze_failure(err,data)

    entry={
        "status":status,
        "runtime":round(time.time()-start,3),
        "time":time.time(),
        "error":err,
        **analysis
    }

    history["runs"].append(entry)
    history["runs"]=history["runs"][-20:]
    history["score"]=reliability(history["runs"])

    os.makedirs(os.path.dirname(METRICS_PATH),exist_ok=True)

    with open(METRICS_PATH,"w") as f:
        json.dump(history,f,indent=2)


if __name__=="__main__":
    run()
