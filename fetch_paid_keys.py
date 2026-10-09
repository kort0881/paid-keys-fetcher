import os
import time
import requests

USER_AGENT = os.environ.get("UA", "v2rayN/6.23")
MAX_RETRIES = 5
BASE_DELAY = 5
RETRY_STATUSES = {502, 503, 504}
OUTPUT_PATH = "results/paid.txt"

url = os.environ.get("PAID_URL")
if not url:
    raise RuntimeError("Переменная окружения PAID_URL не задана")

headers = {"User-Agent": USER_AGENT}
delay = BASE_DELAY
response = None
last_error = None

for attempt in range(1, MAX_RETRIES + 1):
    try:
        print(f"Попытка {attempt}/{MAX_RETRIES}...")
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code in RETRY_STATUSES:
            raise requests.exceptions.HTTPError(
                f"Сервер вернул {response.status_code}",
                response=response,
            )

        response.raise_for_status()
        break

    except requests.exceptions.RequestException as e:
        last_error = e
        if attempt == MAX_RETRIES:
            raise
        print(f"Ошибка: {e}. Повтор через {delay} сек")
        time.sleep(delay)
        delay *= 2

if response is None or not response.text.strip():
    raise RuntimeError("Пустой ответ от сервера")

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"Ключи сохранены: {OUTPUT_PATH} ({len(response.text)} байт)")
