# scrap/infra/proxy_pool.py

import json
import random
import os
from scrap.tools.fetch_free_proxies import fetch_proxies
from scrap.tools.test_proxy import generater_proxy_json

PROXY_VALIDATED_PATH = "../tests/proxies_validated.json"

class ProxyPool:
    def __init__(self):
        self._load_validated_proxies()
        self.blacklist = set()

    def _load_validated_proxies(self):


        with open(PROXY_VALIDATED_PATH, "r", encoding="utf-8") as f:
            self.proxies = json.load(f)

        if not self.proxies:
            raise ValueError("[ProxyPool] Aucun proxy valide chargé.")

    def get_random_proxy(self ):
        valid_proxies = [p for p in self.proxies if p not in self.blacklist]
        if not valid_proxies:
            return None
        return random.choice(valid_proxies)

    def get_first_proxy(self):
            return self.proxies[0]

    def round_proxy(self):
        self.proxies=self.proxies[1:] + self.proxies[:1]

    def extract_proxy(self):
        fetch_proxies()
        generater_proxy_json()
        self._load_validated_proxies()



    def blacklist_proxy(self, proxy):
        self.blacklist.add(proxy)

    def count_available(self):
        return len([p for p in self.proxies if p not in self.blacklist])
