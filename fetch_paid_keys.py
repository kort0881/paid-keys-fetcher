import os
import time
import requests

url = os.environ.get("PAID_URL")
if not url:
    raise Exception("No PAID_URL")

headers = {"User-Agent": "v2rayN/6.23"}
retries = 5
delay = 5

for attempt in range(1, retries + 1):
    try:
        print(f"Попытка {attempt}/{retries}...")
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        break  # успех
    except requests.exceptions.HTTPError as e:
        if e.response.status_code in (502, 503, 504):
            print(f"Сервер вернул {e.response.status_code}, повтор через {delay} сек")
            time.sleep(delay)
            if attempt == retries:
                raise
        else:
            raise
    except Exception as e:
        print(f"Ошибка: {e}, повтор через {delay} сек")
        time.sleep(delay)
        if attempt == retries:
            raise

os.makedirs("results", exist_ok=True)
with open("results/paid.txt", "w") as f:
    f.write(r.text)
print("Ключи сохранены")
