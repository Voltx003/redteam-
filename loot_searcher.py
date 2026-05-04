import requests
import argparse
import threading
from queue import Queue
import re

class LootSearcher:
    def __init__(self, targets, threads=10):
        self.targets = targets
        self.threads = threads
        self.queue = Queue()
        self.loot = []
        self.lock = threading.Lock()
        # Từ khóa "vàng"
        self.keywords = ["password", "api_key", "internal only", "confidential", "secret", "credentials", "login"]

    def search_hc(self, subdomain):
        # Kiểm tra API bài viết công khai để tìm loot
        url = f"https://{subdomain}.zendesk.com/api/v2/help_center/articles/search.json"
        for word in self.keywords:
            params = {"query": word}
            try:
                r = requests.get(url, params=params, timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    if data.get("count", 0) > 0:
                        with self.lock:
                            print(f"[!] LOOT FOUND in {subdomain} for '{word}': {data['count']} results")
                            self.loot.append({
                                "subdomain": subdomain,
                                "keyword": word,
                                "count": data["count"],
                                "sample_url": data["results"][0]["html_url"]
                            })
            except Exception:
                pass

    def worker(self):
        while not self.queue.empty():
            subdomain = self.queue.get()
            self.search_hc(subdomain)
            self.queue.task_done()

    def run(self):
        print(f"[*] Bắt đầu lùng sục {len(self.targets)} mục tiêu...")
        for t in self.targets:
            sub = t.strip().split(".")[0]
            if sub:
                self.queue.put(sub)

        for _ in range(self.threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()

        self.queue.join()
        print(f"[*] Hoàn tất. Tìm thấy {len(self.loot)} nơi chứa tiềm năng dữ liệu nhạy cảm.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zendesk Loot Searcher - 0xbc000349")
    parser.add_argument("--file", required=True)
    parser.add_argument("--limit", type=int, default=50)

    args = parser.parse_args()

    try:
        with open(args.file, 'r') as f:
            targets = f.readlines()

        searcher = LootSearcher(targets[:args.limit], threads=10)
        searcher.run()
    except Exception as e:
        print(f"[-] Lỗi: {e}")
