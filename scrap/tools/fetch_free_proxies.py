# scrap/tools/fetch_free_proxies.py

from scrap.infra.http_client import HttpClient
import re
import json
import os

URL = "https://free-proxy-list.net/"
OUTPUT = "scrap/config/proxies.json"
MAX_PROXIES = 100

def fetch_proxies():
    print("📡 Récupération brute des proxys via HttpClient...")

    client = HttpClient()
    html = client.get(URL)

    if not html:
        print("❌ Échec de récupération de la page.")
        return

    # Regex pour IP:PORT
    pattern = re.compile(r'(\d{1,3}(?:\.\d{1,3}){3})</td><td>(\d{2,5})')
    matches = pattern.findall(html)

    proxies = []
    for ip, port in matches:
        proxy = f"http://{ip}:{port}"
        proxies.append(proxy)
        print(f"🟢 {proxy}")
        if len(proxies) >= MAX_PROXIES:
            break

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(proxies, f, indent=2)

    print(f"\n✅ {len(proxies)} proxies HTTPS sauvegardés dans {OUTPUT}")

if __name__ == "__main__":
    fetch_proxies()
