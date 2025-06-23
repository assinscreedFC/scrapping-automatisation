def format_raw_proxies(input_file="scrap/data/raw/raw_proxies.txt", output_file="scrap/config/proxies.json"):
    with open(input_file, "r") as f:
        lines = f.readlines()

    proxies = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            proxies.append(f"http://{line}")

    with open(output_file, "w", encoding="utf-8") as f:
        import json
        json.dump(proxies, f, indent=2)

    print(f"✅ {len(proxies)} proxies enregistrés dans {output_file}")

if __name__ == "__main__":
    format_raw_proxies()
