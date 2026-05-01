# Báo cáo Trinh sát v3: Phân tích Sâu API & Frontend

## 1. Phân tích Frontend & App Keys
- **Zendesk Messaging Snippet:** Đã trích xuất các App Keys từ `static.zdassets.com`.
  - **Production Key:** `7e7de6fa-f07e-4231-8f8d-454e095d1794`
  - **Staging Key:** `ab473e89-4f16-4124-af2f-72356cfa41dc`
- **Biến cấu hình:** Tìm thấy các biến quan trọng như `productInstanceJwt`, `platformConversationId`, và `categoryId`.

## 2. Bản đồ hóa API Ultimate.ai
- **Base URL:** `https://api.ultimate.ai`
- **Tích hợp:** Sử dụng Kong Gateway (server: kong/3.0.2).
- **Endpoint thám thính:**
  - `POST /converse/chat`: Yêu cầu `botid` (UUID tìm thấy ở trên) và `Authorization` header.
  - `GET /hc/api/v2/integration/token`: Điểm cuối lấy token tích hợp cho Help Center.

## 3. Phân tích Logic Phiên (Session)
- **Cookie Security:**
  - `_zendesk_shared_session`, `_zendesk_session`: Được bảo vệ bởi `HttpOnly`, `Secure`, `SameSite=None`.
  - **Referrer-Policy:** `same-origin` trên tên miền chính, giúp ngăn chặn rò rỉ URL qua tiêu đề Referer.
- **SSO Flow:** Luồng xác thực chuyển hướng qua Okta (`zendesk.okta.com`) với CSP chặt chẽ.

## 4. Kịch bản Tấn công AI (Prompt Injection)
- Đã soạn thảo các kịch bản thử nghiệm trong `AI_ATTACK_SCENARIOS.md`, bao gồm:
  - Trích xuất System Prompt.
  - Rò rỉ dữ liệu PII xuyên tenant qua RAG.
  - Vượt qua các hạn chế của bot AI.

## 5. Kết luận Giai đoạn Trinh sát
Hệ thống có bề mặt tấn công tập trung vào **Logic API** và **AI Agent**. Cơ sở hạ tầng mạng được bảo vệ tốt bởi Cloudflare và WAF, do đó các cuộc tấn công kỹ thuật (Exploit) sẽ khó khăn hơn so với các cuộc tấn công logic (Business Logic Flaws).
