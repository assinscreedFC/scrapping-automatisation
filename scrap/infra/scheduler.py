### setup pour recuper les token avec playwirght puis on les passer a curl cffi pour passer les etape ou le js est obligatoir
### dans se cas precis playwright ne sera pas necessair curlcffi suffit amplament mais dans de futur contexte cela sera tres utile




import os, json, time, random
from playwright.sync_api import sync_playwright
from curl_cffi import requests


def human_delay(a=1.2, b=2.5):
    time.sleep(random.uniform(a, b))


# Dossier temporaire pour le profil utilisateur
temp_profile = r"D:\temp_playwright_profile"
os.makedirs(temp_profile, exist_ok=True)

# URL cible (page après login)
target_url = "https://www.leboncoin.fr/"

# Étape 1 : Se connecter avec Playwright
with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=temp_profile,
        channel="chrome",
        headless=False,
        args=[
            "--start-maximized",
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--disable-features=IsolateOrigins,site-per-process"
        ],
    )

    page = browser.new_page()
    page.goto("https://www.leboncoin.fr/")

    input("➡️ Connecte-toi manuellement puis appuie sur Entrée ici...")

    # Étape 2 : Récupérer les cookies
    cookies = browser.cookies()
    print("✅ Cookies récupérés")

    browser.close()

# Étape 3 : Transformer les cookies pour curl_cffi
session = requests.Session()
cookie_dict = {cookie["name"]: cookie["value"] for cookie in cookies}
session.cookies.update(cookie_dict)

# Étape 4 : Utiliser curl_cffi pour scraper une page avec les cookies
res = session.get(
    "https://www.leboncoin.fr/ad/voitures/2997258439",  # Exemple d'URL protégée
    impersonate="chrome120"  # Très utile contre les protections
)

print("✅ Status:", res.status_code)
print("✅ Contenu partiel:", res.json())
