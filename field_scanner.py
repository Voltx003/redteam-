import requests
import argparse
import threading
from queue import Queue

class FieldScanner:
    def __init__(self, targets, threads=20):
        self.targets = targets
        self.threads = threads
        self.queue = Queue()
        self.results = []
        self.lock = threading.Lock()

    def check_cors(self, subdomain):
        # Tập trung vào endpoint đã xác nhận có wildcard
        url = f"https://{subdomain}.zendesk.com/api/v2/users/me.json"
        headers = {
            "Origin": "https://evil-attacker.com",
            "Access-Control-Request-Method": "GET"
        }
        try:
            # support.zendesk.com trả về wildcard trên OPTIONS
            response = requests.options(url, headers=headers, timeout=5)
            allow_origin = response.headers.get("Access-Control-Allow-Origin")

            if allow_origin == "*":
                with self.lock:
                    print(f"[!] VULNERABLE CORS (Wildcard): {url}")
                    self.results.append({"url": url, "vulnerability": "CORS Wildcard"})
            elif allow_origin == "https://evil-attacker.com":
                with self.lock:
                    print(f"[!!] CRITICAL CORS (Reflected): {url}")
                    self.results.append({"url": url, "vulnerability": "CORS Reflected"})
        except Exception:
            pass

    def worker(self):
        while not self.queue.empty():
            subdomain = self.queue.get()
            self.check_cors(subdomain)
            self.queue.task_done()

    def run(self):
        print(f"[*] Đang quét thực địa {len(self.targets)} subdomain...")
        for t in self.targets:
            sub = t.strip().split(".")[0]
            if sub:
                self.queue.put(sub)

        for _ in range(self.threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()

        self.queue.join()
        print(f"[*] Hoàn tất. Tìm thấy {len(self.results)} mục tiêu có cấu hình CORS lỏng lẻo.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zendesk Field Scanner - 0xbc000349")
    parser.add_argument("--file", required=True)
    parser.add_argument("--limit", type=int, default=100)

    args = parser.parse_args()

    try:
        with open(args.file, 'r') as f:
            all_targets = f.readlines()

        # Lọc bỏ các subdomain rác hoặc trùng
        targets = list(set([t.strip() for t in all_targets if "zendesk.com" in t]))

        scanner = FieldScanner(targets[:args.limit])
        scanner.run()
    except Exception as e:
        print(f"[-] Lỗi: {e}")
