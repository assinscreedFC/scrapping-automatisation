from curl_cffi import requests
import random
import logging
import json
import os

COOKIES_PATH = "scrap/data/cookies.json"

class HttpClient:
    def __init__(self, proxies=None, timeout=15):
        self.session = requests.Session(
            impersonate="chrome110",
            timeout=timeout
        )
        self.logger = logging.getLogger("HttpClient")
        self.proxies = proxies or []

        self._load_cookies()

    def _load_cookies(self):
        if os.path.exists(COOKIES_PATH):
            try:
                with open(COOKIES_PATH, "r", encoding="utf-8") as f:
                    cookies = json.load(f)
                    for name, value in cookies.items():
                        self.session.cookies.set(name, value)
                self.logger.info("Cookies chargés depuis le fichier.")
            except Exception as e:
                self.logger.warning(f"Erreur chargement cookies: {e}")

    def _save_cookies(self):
        try:
            cookies = {c.name: c.value for c in self.session.cookies.jar}
            with open(COOKIES_PATH, "w", encoding="utf-8") as f:
                json.dump(cookies, f, indent=2)
            self.logger.info("Cookies sauvegardés.")
        except Exception as e:
            self.logger.warning(f"Erreur sauvegarde cookies: {e}")

    def get_random_proxy(self):
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def get(self, url, params=None, headers=None ,proxy=None):
        if not proxy:
            proxy = self.get_random_proxy()
            print ("pas de random proxy")
        try:
            response = self.session.get(url, params=params, headers=headers, proxy=proxy)
            response.raise_for_status()
            self._save_cookies()

            # Crée le dossier si besoin
            fetch_path = "scrap/data/fetch.html"
            os.makedirs(os.path.dirname(fetch_path), exist_ok=True)

            # Écrit le contenu HTML dans le fichier (écrase l'ancien)
            with open(fetch_path, "w", encoding="utf-8") as f:
                f.write(response.text)

            self.logger.info(f"✅ Contenu sauvegardé dans {fetch_path}")
            return response.text

        except requests.RequestsError as e:
            self.logger.error(f"Erreur GET {url} : {e}")
            return None

    def post(self, url, data=None, json=None, headers=None):
        proxy = self.get_random_proxy()
        try:
            response = self.session.post(url, data=data, json=json, headers=headers, proxy=proxy)
            response.raise_for_status()
            self._save_cookies()
            return response.text
        except requests.RequestError as e:
            self.logger.error(f"Erreur POST {url} : {e}")
            return None
