# Báo cáo Trinh sát v4: Phân tích Hạ tầng Đa tầng (Super Deep)

## 1. Phân mảnh POD (POD Segmentation)
Zendesk sử dụng kiến trúc POD để phân chia khách hàng và dịch vụ. Các POD được xác định qua bản ghi TXT:
- **POD 26:** support, chat
- **POD 20:** internal, vpn, prometheus
- **POD 19:** grafana
- **POD 28:** gitlab
Việc xác định POD giúp thu hẹp phạm vi tấn công khi phát hiện lỗ hổng trên một cluster cụ thể.

## 2. Dấu vết OSINT & Public Artifacts
- **App Keys:** Đã xác định 2 khóa API quan trọng từ Frontend:
  - `[REDACTED_PROD_KEY]` (Production)
  - `[REDACTED_STAGING_KEY]` (Staging)
- **GitHub Leaks:** Không phát hiện rò rỉ công khai trực tiếp từ API GitHub (cần công cụ chuyên dụng hơn để quét sâu các commit history).

## 3. Thám thính Kỹ thuật (Technical Fingerprinting)
- **WAF/CDN:** Sử dụng Cloudflare. Truy cập Direct IP (216.198.53.2) bị chặn bởi quy tắc 403 của Cloudflare (có thể do cấu hình Cloudflare Authenticated Origin Pulls).
- **Cổng Dịch vụ:** Các cổng 8080 và 8443 đang mở trên IP trực tiếp, cho thấy sự hiện diện của các proxy hoặc dịch vụ alt-http.
- **Gateway:** Tiêu đề `Via: zorg` và `x-envoy-decorator-operation` xác nhận sử dụng Envoy Proxy tích hợp sâu trong hệ thống.

## 4. Bề mặt Tích hợp Bên thứ ba (Integration Surface)
- **Okta Identity Cloud:** Tích hợp xác thực tập trung. Các lỗi trong cấu hình SAML hoặc OIDC có thể dẫn đến truy cập trái phép vào toàn bộ hệ sinh thái Zendesk.
- **Webhook Security:** Zendesk sử dụng chữ ký HMAC-SHA256 để xác thực Webhook. Việc thiếu kiểm tra chữ ký ở phía nhận (client side) có thể cho phép giả mạo dữ liệu ticket.
- **App Marketplace:** Các ứng dụng bên thứ ba cài đặt trong Zendesk có thể có các quyền (scopes) quá mức, tạo điều kiện cho việc trích xuất dữ liệu nếu ứng dụng bị chiếm quyền.

## 5. Chuỗi Tấn công Logic Tiềm năng (Complex Logic Chains)
- **SSO POD Pivot:** Nếu một POD (ví dụ POD 19 - Grafana) có cấu hình SSO lỏng lẻo, kẻ tấn công có thể chiếm quyền truy cập vào các POD khác thông qua việc tái sử dụng session hoặc token.
- **AI RAG Injection:** Sử dụng AI Agent làm "bàn đạp" để truy vấn các tài liệu nội bộ được lưu trữ trong cùng một POD thông qua cơ chế RAG (Retrieval-Augmented Generation).

## 6. Sunshine Platform Analysis
Zendesk Sunshine là nền tảng CRM mở được xây dựng trên AWS.
- **Data Schema:** Sử dụng các Custom Objects và Profiles. Tấn công vào schema có thể cho phép rò rỉ dữ liệu quan hệ khách hàng.
- **Event Streaming:** Tích hợp với Amazon EventBridge. Các lỗi trong cấu hình IAM hoặc chính sách tin cậy (Trust Policy) của EventBridge có thể dẫn đến việc rò rỉ luồng sự kiện (event stream) của khách hàng.

## 7. Thám thính Kỹ thuật Nâng cao
- **SSL/TLS:** Hỗ trợ TLS 1.2, 1.3 với cipher suite hiện đại.
- **Backend Fingerprinting:** Các máy chủ backend được định danh là `classic-app-server-5d8ff47898-v8bc4` (và các biến thể khác).
- **API Gateway:** Ultimate.ai sử dụng **Kong 3.0.2**, cho thấy một lớp quản lý API riêng biệt so với Zendesk Core.

## 6. Chuỗi Tấn công Logic & Khai thác Mở rộng
Chi tiết xem tại `METHODOLOGY.md`. Các hướng đi siêu sâu bao gồm:
- **POD Lateral Movement:** Khai thác sự tin tưởng giữa các dịch vụ trong cùng một cluster POD.
- **AI Token Extraction:** Tấn công vào AI Agent để trích xuất token truy cập API nội bộ.

## 7. Kết luận Giai đoạn v4
Zendesk có một bề mặt tấn công cực kỳ phức tạp và được bảo vệ tốt. Tuy nhiên, việc sử dụng kiến trúc đa tầng (Envoy, Kong, Zorg) và phân mảnh POD tạo ra các **vùng biên bảo mật** (security boundaries) tiềm ẩn cấu hình sai. Trọng tâm của các đợt tấn công SIÊU SÂU nên nhắm vào **sự tương tác giữa các tầng** này.
