# Phương pháp luận Kiểm thử Bảo mật Zendesk

## 1. Kiểm thử Logic Nghiệp vụ (Business Logic Testing)
- **IDOR:** Kiểm tra khả năng truy cập đối tượng xuyên tenant bằng cách sử dụng các tham số ID trong API.
- **SSO/Auth:** Phân tích cấu hình Okta, SAML và các endpoint bypass xác thực.

## 2. Kiểm thử AI & LLM
- **Prompt Injection:** Sử dụng các kỹ thuật Adversarial Prompts để kiểm tra ranh giới của AI Agent.
- **RAG Data Leakage:** Đánh giá khả năng AI truy xuất dữ liệu không được phép từ cơ sở kiến thức (Knowledge Base).

## 3. Phân tích Hạ tầng Đa tầng
- **POD Isolation:** Xác định sự phân tách giữa các cluster POD của Zendesk.
- **Gateway & Proxy:** Phân tích các tiêu đề Envoy và Kong để tìm kiếm cấu hình sai.

## 4. Tích hợp Bên thứ ba
- **Webhook Authenticity:** Luôn xác minh chữ ký HMAC-SHA256 trên các endpoint nhận Webhook.
- **App Scopes:** Kiểm soát chặt chẽ các quyền được cấp cho ứng dụng trong Zendesk Marketplace.
