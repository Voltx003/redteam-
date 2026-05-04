import requests

def probe_zdusercontent(app_id):
    # Thử nghiệm truy cập manifest hoặc config của app trên hạ tầng zdusercontent
    url = f"https://{app_id}.apps.zdusercontent.com/manifest.json"
    print(f"[*] Probing {url}...")
    try:
        r = requests.get(url, timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("[!] APP CONFIG EXPOSED!")
            print(r.text[:500])
    except Exception as e:
        print(f"Error: {e}")

# Các App ID phổ biến thu thập từ scanning
apps = ["harvest", "salesforce", "wordpress"]
for app in apps:
    probe_zdusercontent(app)
