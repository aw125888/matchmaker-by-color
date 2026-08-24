import requests

url = (
    "https://nrs.harvard.edu/urn-3:HUAM:760994"
    "/full/full/0/default.jpg"
)

response = requests.get(url, timeout=30)

print("Status:", response.status_code)
print("Type:", response.headers.get("content-type"))
print("Bytes:", len(response.content))