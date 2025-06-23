# scrap/infra/proxy_pool.py

import json
import random
import os

PROXY_VALIDATED_PATH = "scrap/config/proxies_validated.json"

class ProxyPool:
    def __init__(self):
        self._load_validated_proxies()
        self.blacklist = set()

    def _load_validated_proxies(self):
        if not os.path.exists(PROXY_VALIDATED_PATH):
            raise FileNotFoundError(
                f"[ProxyPool] Le fichier {PROXY_VALIDATED_PATH} est introuvable. "
                "Tu dois d'abord lancer tools/validate_proxies.py pour valider tes proxies."
            )

        with open(PROXY_VALIDATED_PATH, "r", encoding="utf-8") as f:
            self.proxies = json.load(f)

        if not self.proxies:
            raise ValueError("[ProxyPool] Aucun proxy valide chargé.")

    def get_random_proxy(self):
        valid_proxies = [p for p in self.proxies if p not in self.blacklist]
        if not valid_proxies:
            return None
        return random.choice(valid_proxies)

    def blacklist_proxy(self, proxy):
        self.blacklist.add(proxy)

    def count_available(self):
        return len([p for p in self.proxies if p not in self.blacklist])
