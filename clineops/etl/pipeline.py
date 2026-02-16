from fetch import fetch_data
from transform import transform
import json

def run():
    data = fetch_data()
    value = transform(data)

    with open("output.json","w") as f:
        json.dump({"value": value}, f)

if __name__ == "__main__":
    run()
