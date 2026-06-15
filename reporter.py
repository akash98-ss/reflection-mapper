import json

def save_report(results, filename="report.json"):
    with open(filename, "w") as f:
        json.dump(results, f, indent=4)