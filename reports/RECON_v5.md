# Báo cáo Trinh sát v5: Footprinting Mở rộng & The Invisible Map

## 1. Footprinting & Subdomain Expansion
- **Cấu trúc POD Tài sản (Assets/CDN):**
  - `p*.zdassets.com`: Đã xác định dải `p1` đến `p19` phục vụ nội dung tĩnh. IP: `216.198.53.3`, `216.198.54.3`.
  - **Phát hiện:** Các POD có dải IP tập trung, hỗ trợ việc thu hẹp phạm vi quét CDN.
- **Tài sản Nội dung Người dùng (Content):**
  - `*.zdusercontent.com`: Nơi lưu trữ tệp đính kèm. Cấu trúc phức tạp với các subdomain dạng `p998.zdusercontent.com`.
  - **Điểm yếu tiềm năng:** Token dựa trên JWT cho việc truy xuất nội dung (`GET /api/v2/attachment_content/{id}?token=...`).

## 2. The Invisible Map (Bản đồ Vô hình)
- **Dải IP Chính:** `216.198.53.0/24` và `216.198.54.0/24`.
- **Dịch vụ Ẩn:**
  - Cổng 8080 (http-proxy) và 8443 (https-alt) mở trên hầu hết các IP trong dải.
  - Phản hồi banner xác nhận là **Cloudflare http proxy**, cho thấy lớp bảo vệ Cloudflare được áp dụng ngay cả ở cấp độ IP trực tiếp (Authenticated Origin Pulls).
- **Môi trường Phát triển (Development):**
  - Phát hiện `axialdev.zendesk.com` và các biến thể `stage`, `test` có bản ghi MX trỏ về Google Workspace nội bộ.

## 3. Tech Stack Fingerprinting v5
- **WAF Behavior:** Cloudflare chặn TRACE và các phương thức HTTP không tiêu chuẩn (405 Method Not Allowed).
- **Frontend Stack:** Sử dụng Gatsby (từ `developer.zendesk.com`) và WordPress (cho một số trang đối tác như `goaxial.com`).
- **AI Stack:** Tích hợp sâu với **Ultimate.ai** qua Kong Gateway. Endpoint chính: `https://api.ultimate.ai/converse/chat`.

## 4. Functional Mapping (Bản đồ hóa Chức năng)
- **Luồng Đính kèm:** Upload -> `static.zdassets.com` -> Phân phối qua `zdusercontent.com` với ephemeral tokens.
- **Luồng AI:** User -> `zorg` Gateway -> `ultimate.ai` -> LLM -> Response.
- **Xác thực:** Đa phần tập trung vào **Okta SSO**.

## 5. Low Hanging Fruits
- **Info Disclosure:**
  - `/.well-known/security.txt` tồn tại trên nhiều subdomain nhưng thông tin mang tính quy trình.
  - `robots.txt` tiết lộ nhiều đường dẫn API và thư mục bị cấm: `/children`, `/organizations`, `/access/sso_bypass`.
- **CORS:** Cấu hình CSP chặt chẽ (`frame-ancestors 'self'`) trên các trang chính.

## 6. Kết luận v5
Zendesk duy trì một bản đồ hạ tầng cực kỳ nhất quán và được bảo vệ bởi Cloudflare ở mọi tầng. Cơ hội khai thác nằm ở **ephemeral tokens** của tệp đính kèm và **logic xử lý hội thoại** của AI Agent (Prompt Injection).
