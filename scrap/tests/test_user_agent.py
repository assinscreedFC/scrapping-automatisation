from scrap.infra.http_client import load_headers

def test_user_agent():
    user_agent, headers = load_headers()
    print("User-Agent sélectionné :", user_agent)
    print("Headers correspondants :")
    for k, v in headers.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    test_user_agent()