import requests

def inspect_loot(subdomain, query):
    url = f"https://{subdomain}.zendesk.com/api/v2/help_center/articles/search.json"
    params = {"query": query}
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            results = r.json().get("results", [])
            for article in results[:3]:
                print(f"\n--- LOOT FOUND in {subdomain} ---")
                print(f"Title: {article['title']}")
                print(f"URL: {article['html_url']}")
                print(f"Snippet: {article['snippet']}")
    except Exception as e:
        print(f"Error: {e}")

inspect_loot("3manager", "api_key")
inspect_loot("37solutions", "password")
