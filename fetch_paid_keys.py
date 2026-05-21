import os
import requests

url = os.environ.get("PAID_URL")
if not url:
    raise Exception("No PAID_URL")

headers = {"User-Agent": "v2rayN/6.23"}
r = requests.get(url, headers=headers, timeout=15)
r.raise_for_status()

os.makedirs("results", exist_ok=True)
with open("results/paid.txt", "w") as f:
    f.write(r.text)
