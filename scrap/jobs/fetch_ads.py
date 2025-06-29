from scrap.infra.http_client import HttpClient
from scrap.tests.test_http_client import extraire_ads_et_sauvegarder
from time import sleep

from scrap.tools.sleep_between import sleep_between
from scrap.tools.replace_page_number import remplacer_page


def fetch_ads(url:str,nbr_page:str):
    client = HttpClient()
    ### first step feetch all  informetion about the annonce
    ### comme fetch la description peut etre une etape plus longe car ont doit chercher manuellment dans chaque annonce je ne vais pas
    ### l'applique ici mais tout de meme je je vais integrer une fonction qui permert de recuper la description d'une annonce a la demande

    for i in range(nbr_page):
        sleep(sleep_between(5,10))
        url = remplacer_page(url,i+1)
        html = client.get(url)
        extraire_ads_et_sauvegarder(html, f"ads_{i + 1}.json")

def fetch_description_ads(url:str):
    client = HttpClient()
    texte = client.get(url)
    import re

    # Regex pour capturer la chaîne entre "description": " et le guillemet fermant correspondant,
    # en gérant le fait que la description peut contenir des retours à la ligne, accents, ponctuations, etc.
    pattern = r'"description"\s*:\s*"((?:[^"\\]|\\.)*)"'

    match = re.search(pattern, texte, re.DOTALL)
    if match:
        description = match.group(1)
        # Optionnel : déséchapper les éventuels caractères échappés JSON
        import codecs
        description = codecs.decode(description, 'unicode_escape')
        print(description)
    else:
        print("Description non trouvée")

fetch_description_ads("https://www.leboncoin.fr/ad/voitures/2997258439")
