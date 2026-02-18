from clineops.engine import analyze_failure

def analyze(payload):
    return analyze_failure(payload["error"], payload["data"])
