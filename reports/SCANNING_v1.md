# Báo cáo Quét & Liệt kê v1 (Scanning & Enumeration)

## 1. Cổng & Dịch vụ có khả năng khai thác
- **Kết quả Masscan:** Toàn bộ dải IP Zendesk (`216.198.53.0/24`, `216.198.54.0/24`) chỉ lộ diện các cổng web (80, 443, 8080, 8443).
- **Banner Grabbing:** Xác nhận các cổng 8080 và 8443 là Cloudflare Proxy.
- **Kết luận:** Không có dịch vụ quản trị (SSH) hoặc cơ sở dữ liệu (MySQL/Redis) bị lộ trực tiếp.

## 2. Khám phá Thư mục Ẩn (Directory Brute-force)
- **Công cụ:** `ffuf` với wordlist directories_common.txt.
- **Kết quả:** Các đường dẫn nhạy cảm như `/admin`, `/backup`, `/config` đều trả về **403 Forbidden** hoặc **302 Redirect** về trang login.
- **Nhận định:** Cấu trúc thư mục được bảo vệ tốt bởi Gateway và WAF.

## 3. Liệt kê Hợp lệ (Valid Enumeration)
- **API công khai:** Có thể liệt kê bài viết, danh mục trong Help Center mà không cần xác thực.
- **API nhạy cảm:** Các endpoint `/api/v2/users` và `/api/v2/organizations` yêu cầu xác thực đầy đủ.
- **Leakage:** Không phát hiện rò rỉ email hoặc ID người dùng qua các trang lỗi.

## 4. Phân tích WAF & Security Controls
- **WAF:** Cloudflare chặn hiệu quả SQLi, XSS cơ bản.
- **Rate Limiting:** Áp dụng chặt chẽ cho các hành vi quét tự động tốc độ cao.
- **Trang lỗi:** Trả về "Unprocessable Entity" (422) hoặc "Forbidden" (403) tiêu chuẩn, không lộ stack trace hoặc thông tin backend.

## 5. Trái thấp (Low Hanging Fruits)
- **CORS:** Đã xác nhận cấu hình Wildcard trên `support.zendesk.com` (Xem RECON_v7.md).
- **Info Disclosure:** Các tệp cấu hình quan trọng (.env, .git) không được tìm thấy.
- **Headers:** Không có tiêu đề `X-Powered-By` hoặc thông tin phiên bản phần mềm backend bị lộ.

## 6. Phân tích Tích hợp bên thứ ba (OneTrust/GTM)
- **OneTrust ID:** `3823159c-d94a-456f-9c66-6d2b3e9ee0d6`.
- **Cấu hình:** Sử dụng cho việc quản lý cookie và tuân thủ GDPR.
- **GTM:** Sử dụng rộng rãi trên toàn bộ hệ sinh thái để quản lý tag và script theo dõi.
