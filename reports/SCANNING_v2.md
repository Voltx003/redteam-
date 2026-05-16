# Báo cáo Quét & Liệt kê v2 (Advanced Scanning)

## 1. Thám thính API Nâng cao (Advanced API Fuzzing)
- **Kết quả:** Thử nghiệm hàng loạt các endpoint API v2 không được tài liệu hóa (exports, debug, diagnostics) trên nhiều subdomain. Tất cả đều trả về **403 Forbidden** hoặc **401 Unauthorized**.
- **HTTP Methods:** Xác nhận việc hạn chế phương thức HTTP (PUT, PATCH, DELETE) trên các endpoint nhạy cảm khi không có token hợp lệ.

## 2. Hoán vị Tên miền phụ (Subdomain Permutations)
- **Cấu trúc tìm thấy:** Các tên miền kết hợp như `dev-api`, `stage-sso`, `pod26-api` đều tồn tại và trỏ về hạ tầng chính.
- **Nhận định:** Zendesk sử dụng một hệ thống định tuyến tên miền phụ thống nhất, giúp duy trì bảo mật đồng bộ trên toàn bộ các môi trường phát triển và vận hành.

## 3. Phân tích Metadata & Evasion
- **Metadata Deep Dive:** Không phát hiện rò rỉ thông tin qua các tệp chính sách cũ hoặc sitemap mở rộng.
- **WAF Evasion:** Các kỹ thuật bypass phổ biến (IP Spoofing qua header, User-Agent giả mạo bot) đều thất bại trước Cloudflare WAF.
- **Bot Verification:** Xác nhận Zendesk/Cloudflare sử dụng cơ chế kiểm tra bot nghiêm ngặt (không thể bypass chỉ bằng cách thay đổi User-Agent).

## 4. Kết luận Giai đoạn v2
Hệ thống thể hiện sự trưởng thành cao trong việc kiểm soát bề mặt tấn công. Lớp bảo vệ **Cloudflare + zorg Gateway** tạo thành một rào cản vững chắc trước các nỗ lực thám thính và quét tự động. Các bước tiếp theo sẽ chuyển từ quét hạ tầng sang phân tích sâu các **phiên làm việc (Session)** và **logic API cụ thể** trên các instance trial.
