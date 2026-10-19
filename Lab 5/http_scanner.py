import requests
import csv

BASE_URL = "http://localhost:3000"
response = requests.get(BASE_URL, timeout=5)

inspections = []

test_cases = [
{"method": "GET", "path": "/", "params": None, "data": None},
{"method": "GET", "path": "/rest/products/search", "params": {"q": "apple"}, "data": None},
{"method": "GET", "path": "/rest/products/search", "params": {"q": "banana"}, "data": None},
{"method": "POST", "path": "/rest/products/search", "params": None, "data": {"q": "apple"}},
{"method": "POST", "path": "/rest/products/search", "params": None, "data": {"q": "banana"}},
]

print("Initiating Scan...")

for test in test_cases:
    url = BASE_URL + test["path"]

    if test["params"]:
        input_val = str(test["params"])
    elif test["data"]:
        input_val = str(test["data"])
    else:
        input_val = "None"

    try:
        if test["method"] =="GET":
            response = requests.get(url, params= test["params"], timeout=5)
        elif test["method"] == "POST":
            response = requests.post(url, params= test["params"], timeout=5)
        else:
            continue

        recordings = {
            "endpoint": test["path"],
            "method": test["method"],
            "input_payload": input_val,
            "status_code": response.status_code,
            "response_length": len(response.content),
            "content_type": response.headers.get("Content-Type", "Not known"),
            "server": response.headers.get("Server", "Not known")
        }

        inspections.append(recordings)
        print(f"[{test['method']}] Endpoint: {test['path']} | Input: {input_val} | Status:"
             f" {response.status_code} | Length: {len(response.content)} bytes"
        )

    except requests.RequestException as error:
     print(f"Could to {url}: {error} failed")   

fieldnames = [
    "endpoint",
    "method",
    "input_payload",
    "status_code",
    "response_length",
    "content_type",
    "server",
]

with open(
    "http_scan_results.csv", "w", newline="", encoding="utf-8"
) as csvfile:
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
  writer.writerows(inspections)

print("Scan completed! Results have been saved to http_scan_results.csv successfully.")