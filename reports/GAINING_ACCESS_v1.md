# Báo cáo Thâm nhập v1 (Gaining Access)

## 1. Khai thác CORS Wildcard
- **Kịch bản:** Tạo một tệp `cors_poc.html` giả lập trang web độc hại thực hiện các yêu cầu `fetch` tới các API nhạy cảm của Zendesk (`/users/me.json`, `/tickets.json`).
- **Kết quả:** Mặc dù `Access-Control-Allow-Origin` là `*`, các trình duyệt hiện đại sẽ chặn việc gửi cookie xác thực khi sử dụng wildcard. Tuy nhiên, nếu người dùng sử dụng API key hoặc nếu Header `Authorization` được cấu hình sai để cho phép tất cả các nguồn, dữ liệu vẫn có thể bị rò rỉ.
- **Tệp PoC:** `reports/cors_poc.html`

## 2. Thâm nhập AI Agent (Prompt Injection)
- **Kịch bản:** Gửi chuỗi các lệnh "System Override" và "Debug Mode" tới endpoint của Zea AI Agent thông qua các tham số `widgetInput1-5`.
- **Kết quả:** Toàn bộ các yêu cầu trực tiếp tới `https://api.ultimate.ai/converse/chat` đều bị chặn với mã lỗi **401 Authorization Required** từ Kong Gateway.
- **Phân tích:** Việc thâm nhập qua Prompt Injection không thể thực hiện ở mức API mạng nếu không có token hợp lệ. Giai đoạn tiếp theo cần tập trung vào việc chiếm đoạt token người dùng hoặc thực thi payload thông qua giao diện widget chính thức.

## 3. Thử nghiệm IDOR Xuyên Tenant
- **Kịch bản:** Sử dụng công cụ `idor_tester.py` để truy cập các tài nguyên (vé hỗ trợ) của tenant A từ tài khoản của tenant B.
- **Kết quả:** Các thử nghiệm trên tài khoản giả định (`bb-jules-a`) trả về **404 Not Found**.
- **Kết luận:** Zendesk có cơ chế kiểm tra quyền sở hữu tài nguyên (Ownership Check) khá tốt ở cấp độ API cơ bản. Tuy nhiên, các endpoint API v2 mới hoặc các tham số không chuẩn vẫn cần được rà soát thêm.

## 4. Kết luận Giai đoạn v1
Giai đoạn Gaining Access đầu tiên cho thấy Zendesk có lớp bảo vệ gateway và phân tách dữ liệu khá mạnh mẽ. Mặc dù có các sơ hở về CORS, nhưng việc khai thác chúng bị hạn chế bởi các chính sách bảo mật của trình duyệt. Trọng tâm của các đợt thâm nhập tới nên tập trung vào **Chiếm đoạt Token (Token Theft)** hoặc khai thác các **Logic Business phức tạp** hơn.
