# Báo cáo Trinh sát v2: Zendesk & AI Infrastructure

## 1. Hạ tầng AI (Mục tiêu ưu tiên)
- **Ultimate.ai (Zendesk AI):** Zendesk đã mua lại Ultimate.ai để tích hợp AI Agent.
  - **API Base URL:** `https://api.ultimate.ai`
  - **Endpoint quan trọng:** `POST /converse/chat`
  - **Tham số nhạy cảm:** `platformConversationId`, `metaData` (có thể chứa PII nếu không được sanitize).
- **Zendesk AI Agents:** Tích hợp trực tiếp vào `*.zendesk.com`.
  - Kiểm tra các đường dẫn: `/hc/api/v2/chat`, `/api/v2/ai_agents`.

## 2. Điểm cuối Xác thực & Quản lý (Auth & Admin)
- **Okta Integration:** `https://zendesk.okta.com`
  - Sử dụng cho SSO của nhân viên Zendesk.
  - Các endpoint SAML: `/app/zendesk_aiagentsazurezig_1/...` (tìm thấy trong bản ghi TXT).
- **SSO Bypass:** `/access/sso_bypass` tồn tại trên các instance khách hàng, có thể là mục tiêu cho brute-force hoặc bypass nếu cấu hình sai.

## 3. Phân tích Tên miền phụ & Lưu lượng (Subdomains)
- **Sensitive Subdomains:**
  - `grafana.zendesk.com`, `prometheus.zendesk.com`: Chuyển hướng về trang login của Zendesk qua `zorg`.
  - `vpn.zendesk.com`, `internal.zendesk.com`: Sử dụng Cloudflare Proxy, chặn truy cập trực tiếp.
  - `api-packlink.zendesk.com/attachments`: Trả về 403, nhưng là điểm cuối tiềm năng cho IDOR.
- **Cloud Assets:**
  - Bucket S3 được xác định: `zendesk.s3.amazonaws.com`, `zendesk-assets.s3.amazonaws.com` (Tồn tại, Access Denied).
- **DNS Analysis:**
  - Zone Transfer (AXFR) bị chặn.
  - Không phát hiện Subdomain Takeover trên các CNAME công khai (`stage`, `prod`, `axialdev`).

## 4. Bảo mật & Chống Scan
- **Rate Limiting:** Rất mạnh (429 Too Many Requests) khi sử dụng các công cụ brute-force như `dirb`. Cần chuyển sang brute-force phân tán hoặc sử dụng proxy xoay vòng.
- **WAF:** Cloudflare được cấu hình chặt chẽ, chặn các truy cập bất thường và công cụ scan tự động.
- **Security Headers:** Hầu hết các subdomain đều có CSP và HSTS chặt chẽ.

## 5. Chiến lược Tiếp theo (v2.1)
- Tập trung vào **AI Agent Testing**: Thử nghiệm Prompt Injection trên các instance trial.
- **IDOR Testing**: Sử dụng `idor_tester.py` trên endpoint `/attachments` và `/api/v2/tickets`.
- **DMARC/SPF**: Chính sách `p=reject` được thiết lập, khó giả mạo email trực tiếp từ tên miền chính.
