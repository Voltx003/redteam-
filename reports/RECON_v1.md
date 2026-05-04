# Báo cáo Trinh sát v1: Zendesk

## 1. Cơ sở hạ tầng tên miền
- **Tên miền chính:**
  - `zendesk.com`
  - `zd-master.com` (Được quản lý bởi Cloudflare)
- **Khám phá tên miền phụ (Mẫu):**
  - `developer.zendesk.com`
  - `api-packlink.zendesk.com`
  - `admin-lemontech.zendesk.com`
  - `axialdev.zendesk.com`
  - `test.zendesk.com` (Không phân giải được)
- **Máy chủ tên miền (Name Servers):**
  - `ns1.p01.dynect.net`
  - `ns2.p01.dynect.net`
  - `ns3.p01.dynect.net`
  - `ns4.p01.dynect.net`

## 2. Dấu vết mạng
- **ASN:** AS11404 (Zendesk, Inc.)
- **Dải IP (từ bản ghi SPF):**
  - `216.198.0.0/18`
  - `185.12.80.0/22`
  - `188.172.128.0/20`
  - `192.161.144.0/20`
- **Cơ sở hạ tầng đám mây:**
  - Sử dụng nhiều **Cloudflare** để bảo vệ biên và SSL.
  - **Okta** để xác thực (`zendesk.okta.com`).
  - **Mimecast** cho bảo mật email.

## 3. Ngôn ngữ công nghệ (Quan sát được)
- **Gateway:** Gateway nội bộ tên là `zorg` (Thông qua tiêu đề `Via: zorg`).
- **Máy chủ:** Envoy (Thông qua tiêu đề `x-envoy-upstream-service-time`), classic-app-server.
- **Tiêu đề đáng chú ý:**
  - `x-zendesk-zorg: yes`
  - `x-request-id`: Theo dõi yêu cầu duy nhất.
  - `zendesk-service`: Xác định dịch vụ backend (ví dụ: `developer-docs`).

## 4. Cổng đang mở
- `80/tcp` (HTTP)
- `443/tcp` (HTTPS)
- `8080/tcp` (HTTP Proxy)
- `8443/tcp` (HTTPS-alt)

## 5. Các vectơ tấn công tiềm năng
- **Cấu hình sai SSO/SAML:** Các điểm tích hợp Okta.
- **IDOR xuyên Tenant (Cross-Tenant IDOR):** Kiến trúc đa người dùng trên `*.zendesk.com`.
- **Tài liệu API:** Các điểm cuối trên `developer.zendesk.com`.
