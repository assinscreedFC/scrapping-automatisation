# scrap/tools/validate_proxies.py

import requests
import json
from time import sleep
from random import shuffle
from random import uniform

PROXY_INPUT = "scrap/config/proxies.json"
PROXY_OUTPUT = "scrap/config/proxies_validated.json"
TEST_URL = "https://httpbin.org/ip"
TIMEOUT = 3
MAX_VALID = 50

def load_proxies():
    with open(PROXY_INPUT, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_proxy(proxy_url):
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    try:
        response = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        if response.status_code == 200:
            ip = response.json().get("origin", "")
            print(f"[OK] {proxy_url} → {ip}")
            return True
    except Exception as e:
        print(f"[FAIL] {proxy_url} → {str(e)}")
    return False

def main():
    proxies = load_proxies()
    shuffle(proxies)  # pour ne pas tester toujours les mêmes en premier
    valid = []

    for proxy in proxies:
        if validate_proxy(proxy):
            valid.append(proxy)
            if len(valid) >= MAX_VALID:
                break
        sleep(uniform(0.5, 1.5))  # pause légère pour éviter les bannissements

    with open(PROXY_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(valid, f, indent=2)

    print(f"\n✅ {len(valid)} proxies valides écrits dans {PROXY_OUTPUT}")

if __name__ == "__main__":
    main()
