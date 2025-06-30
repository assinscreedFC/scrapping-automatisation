import re

def remplacer_page(url, nouvelle_valeur):
    # Remplace les chiffres après "page=" jusqu'à un caractère non-chiffre
    return re.sub(r'(?<=page=)\d+', str(nouvelle_valeur), url)

if __name__ == '__main__':
    print(remplacer_page("https://www.leboncoin.fr/recherche?text=clio+4&page=0",2))
