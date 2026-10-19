import requests

base_url = "http://localhost:3000"
response = requests.get(base_url, timeout=5)

search_url = base_url + "/rest/products/search"
r = requests.get(search_url, params={"q": "apple"}, timeout=5)

marker = "fsct8561-marker-123"
marker_response = requests.get(search_url, params={"q": marker}, timeout=5)

if marker in marker_response.text:
    print("Marker appears in the response — investigate its context")
else:
    print("Marker was not found in this response")

test = "<u>fsct8561-test</u>"
test_response = requests.get(search_url, params={"q": test}, timeout=5)


print("test input reflected", test in test_response)

print()
print()
print("part2")

normal_input = "apple"
probe_input = "'"

normal = requests.get(search_url, params={"q": normal_input}, timeout=5)
probe = requests.get(search_url, params={"q": probe_input}, timeout=5)

print("Normal input status:", normal.status_code)
print("Probe input status:", probe.status_code)

print()
print()
print("part3")

error_phrase = "SQLITE_ERROR"

if error_phrase.lower() in probe.text.lower():
    print("Database-related error text found; manual review required")
else:
    print("No matching database error text in this response")

print()
print()
print("part4")

headers_to_check = ["Content-Security-Policy", "X-Content-Type-Options"]

for name in headers_to_check:
    if name in response.headers:
        print(name, "is present")
    else:
        print(name, "is not present; investigate its relevance")

print()
print()
print("part5")

alerts = []
seen = set()

for message in ["Missing CSP", "Missing CSP", "Missing X-Content-Type-Options"]:
    if message not in seen:
        seen.add(message)
        alerts.append(message)

print(alerts)

print()
print()
print("part6")

import csv

practice_records = [
    {"endpoint": "/", "status": 200},
    {"endpoint": "/example", "status": 404}
]

with open("practice_records.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["endpoint", "status"])
    writer.writeheader()
    writer.writerows(practice_records)

print("Saved practice_records.csv")