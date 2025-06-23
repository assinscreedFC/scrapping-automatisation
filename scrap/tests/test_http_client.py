from scrap.infra.http_client import HttpClient

def test_homepage_leboncoin():
    client = HttpClient()
    url = "https://www.leboncoin.fr/"
    html = client.get(url)

    if html:
        print("✅ Requête réussie.")
        print("🔎 Début du HTML :")
        print(html[:500])
    else:
        print("❌ Échec de la requête.")

if __name__ == "__main__":
    test_homepage_leboncoin()
