import requests

def debug_cors(subdomain):
    url = f"https://{subdomain}.zendesk.com/api/v2/users/me.json"
    headers = {
        "Origin": "https://evil.com",
        "Access-Control-Request-Method": "GET"
    }
    print(f"Testing {url}...")
    try:
        r = requests.options(url, headers=headers, timeout=10)
        print(f"Status: {r.status_code}")
        print("Headers:")
        for k, v in r.headers.items():
            if "access-control" in k.lower():
                print(f"  {k}: {v}")
    except Exception as e:
        print(f"Error: {e}")

debug_cors("support")
debug_cors("axialdev")
