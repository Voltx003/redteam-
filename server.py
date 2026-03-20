import http.server
import socketserver

PORT = 8080

class InsecureHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.send_header('Allow', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_PUT(self):
        # Mô phỏng lỗ hổng cho phép upload/thay đổi file (Defacement)
        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length)
        # Trong thực tế nó sẽ ghi file, ở đây ta chỉ in log
        print(f"[!] Dữ liệu nhận được qua PUT: {content.decode('utf-8')}")

        self.send_response(200, "OK")
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"File created/updated successfully (Simulated)")

    def end_headers(self):
        # Mô phỏng việc lộ thông tin Server (Information Disclosure)
        self.send_header('Server', 'Apache/2.2.8 (Ubuntu) PHP/5.2.4')
        self.send_header('X-Powered-By', 'PHP/5.2.4')
        super().end_headers()

with socketserver.TCPServer(("", PORT), InsecureHandler) as httpd:
    print(f"Máy chủ giả lập đang chạy tại cổng {PORT}")
    httpd.serve_forever()
