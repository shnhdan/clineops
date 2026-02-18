def analyze_failure(error, data):
    if error and "price" in error:
        return {
            "suggestion": "Schema drift detected — field renamed",
            "fix": "return data.get('price') or data.get('cost')",
            "confidence": 0.91,
            "preview": data.get("cost") if isinstance(data, dict) else None
        }

    return {
        "suggestion": "Unknown failure",
        "fix": None,
        "confidence": 0.3,
        "preview": None
    }
