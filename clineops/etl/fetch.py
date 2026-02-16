import random

def fetch_data():
    if random.choice([True, False]):
        return {"price": 100}
    else:
        return {"cost": 100}
