import requests

base_url = "http://localhost:3000"
response = requests.get(base_url, timeout=5)

print("HTTP status:", response.status_code)
print("Response length:", len(response.content), "bytes")
print()
print()
print("Content type:", response.headers.get("Content-Type"))
print("First 50 characters:", response.text[:50])
print()
print()
search_url = base_url + "/rest/products/search"
r = requests.get(search_url, params={"q": "banana"}, timeout=5)

print("Requested URL:", r.url)
print("Status:", r.status_code)
print("Content type:", r.headers.get("Content-Type"))
print("First 150 characters:", r.text[:150])
print()
print()
post_response = requests.post(
    search_url,
    data={"q": "apple"},
    timeout=5
)
print("POST status:", post_response.status_code)
print("POST response length:", len(post_response.content))
