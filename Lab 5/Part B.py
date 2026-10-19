import requests

base_url = "http://localhost:3000"
response = requests.get(base_url, timeout=5)

search_url = base_url + "/rest/products/search"
r = requests.get(search_url, params={"q": "apple"}, timeout=5)

print("Requested URL:", r.url)
print("Status:", r.status_code)
print("Content type:", r.headers.get("Content-Type"))


search_terms = ["apple", "banana", "orange"]

for term in search_terms:
    print("Search term:", term)

print()
print("Part2")

observation = {
    "method": "GET",
    "endpoint": "/rest/products/search",
    "status_code": r.status_code,
    "response_length": len(r.content),
    "content_type": r.headers.get("Content-Type")
}

print(observation)
print("Status:", observation["status_code"])

print()
print()
print("Part3")

records = []

for term in ["apple", "banana"]:
    result = requests.get(search_url, params={"q": term}, timeout=5)
    records.append({"input": term, "status_code": result.status_code, "response_length": len(result.content)})

print(records)

print()
print()
print("Part4")

def get_status(search_word):
    result = requests.get(search_url, params={"q": search_word}, timeout=5)
    return result.status_code

print(get_status("apple"))

print()
print()
print("Part5")

try:
    test_response = requests.get(base_url, timeout=5)
    print("Connected. Status:", test_response.status_code)
except requests.RequestException as error:
    print("Could not connect:", error)