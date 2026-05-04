# Báo cáo Thâm nhập v5 (Persistence - Quy tắc Lặp)

## 1. Thử nghiệm Blind XSS & Ticket Creation
- **Endpoint:** `https://support.zendesk.com/api/v2/requests.json`
- **Hành động:** Gửi ticket ẩn danh chứa payload Blind XSS.
- **Kết quả:** Hệ thống chấp nhận tạo ticket (trạng thái `suspended_ticket`) nhưng thực hiện lọc bỏ hoàn toàn các thẻ HTML nguy hiểm (`<svg>`, `<script>`) trước khi lưu trữ.
- **Kết luận:** Cơ chế lọc đầu vào ở tầng ứng dụng rất tốt, ngăn chặn các cuộc tấn công Blind XSS qua hệ thống ticket.

## 2. Fuzzing Bypass WAF (Unicode/Null-byte)
- **Kịch bản:** Sử dụng các ký tự không tiêu chuẩn để đánh lừa bộ lọc XSS của Cloudflare.
- **Kết quả:** Cloudflare WAF chặn đứng 100% các payload chứa Null-byte, Unicode escapes, hoặc các khoảng trắng lạ kết hợp với logic tấn công (HTTP 403).
- **Đánh giá:** Bộ lọc Cloudflare tại Zendesk được cấu hình ở mức cao nhất, không bị đánh lừa bởi các kỹ thuật encoding cơ bản.

## 3. Truy lùng API v2 Ẩn (Undocumented APIs)
- **Kịch bản:** Brute-force các endpoint nhạy cảm dưới `/api/v2/`.
- **Kết quả:** Toàn bộ các keyword như `admin`, `internal`, `metrics`, `logs` đều trả về **403 Forbidden**.
- **Phân tích:** Điều này xác nhận Gateway `zorg` không chỉ bảo vệ các endpoint công khai mà còn ẩn giấu hoàn toàn các route nội bộ khỏi việc liệt kê mù.

## 4. IDOR Nhất quán trên Staging
- **Kịch bản:** Kiểm tra phân tách tenant trên `axialdev.zendesk.com`.
- **Kết quả:** Trả về **404**, tương đồng với môi trường Production.
- **Kết luận:** Zendesk áp dụng chính sách bảo mật đồng bộ (Security Policy Consistency) trên toàn bộ hạ tầng, từ staging đến production.

## 5. Kết luận Giai đoạn v5
Sau 5 đợt lặp thâm nhập sâu, chúng ta có thể khẳng định Zendesk là một pháo đài vững chắc. Các sơ hở bề nổi (XSS, IDOR cơ bản, API Leak) hầu như không tồn tại. Lợi nhuận hiện tại chỉ có thể thu được từ các cuộc tấn công **Logic phức tạp**, **Chiếm đoạt Token tinh vi** hoặc các lỗ hổng **Zero-day** thực thụ trong hạ tầng Kong/zorg Gateway.
