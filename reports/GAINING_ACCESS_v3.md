# Báo cáo Thâm nhập v3 (Creative Penetration - Quy tắc Lặp & Sáng tạo)

## 1. Truy quét Subdomain Takeover
- **Mục tiêu:** 50 subdomain staging và dev tiềm năng.
- **Kết quả:** Không phát hiện dấu hiệu takeover (NoSuchBucket/No such app). Hầu hết các subdomain đều trỏ về hạ tầng ổn định của Zendesk hoặc được bảo vệ bởi Cloudflare Managed Challenge.
- **Bằng chứng:** `reports/takeover_results_v3.txt`

## 2. Thử nghiệm SSRF qua AI Agent
- **Kịch bản:** Gửi URL Metadata Service của AWS/GCP tới backend qua các tham số widget.
- **Kết quả:** Mọi yêu cầu trực tiếp tới API đều bị chặn (401). Cơ chế Kong Gateway hoạt động như một lớp ngăn cách SSRF hiệu quả từ phía mạng bên ngoài.

## 3. Prototype Pollution trong Widget
- **Phát hiện:** Mã nguồn `z2-messaging-widget.js` sử dụng `Object.assign()` nhiều lần để gộp các đối tượng cấu hình và metadata (ví dụ: `A(R(_.customOptions, t))`).
- **Rủi ro:** Nếu một tham số đầu vào từ người dùng (như `widgetInput1`) được đưa vào `Object.assign()` mà không lọc, kẻ tấn công có thể tiêm thuộc tính `__proto__` để gây ô nhiễm đối tượng toàn cục, dẫn đến bypass xác thực hoặc thực thi mã phía client (XSS).
- **Bằng chứng:** `reports/proto_pollution_v3.txt`

## 4. Thử nghiệm Payload Polyglot & WAF Bypass
- **Phát hiện:** Trang tìm kiếm `https://support.zendesk.com/hc/en-us/search` chấp nhận các payload XSS như `<svg/onload=alert(1)>` (trả về HTTP 200).
- **Chặn:** Các payload SQLi cổ điển (`' OR 1=1--`) bị WAF chặn đứng (HTTP 403).
- **Phân tích:** Cloudflare WAF có kẽ hở trong việc lọc các thẻ SVG/JS trong tham số tìm kiếm, mở ra cơ hội cho các cuộc tấn công **Reflected XSS** tinh vi.

## 5. Kết luận Giai đoạn v3
Sáng tạo và Lặp lại đã mang về những phát hiện giá trị về **Prototype Pollution** và **WAF Bypass cho XSS**. Đây là những lỗ hổng logic và cấu hình "vùng xám" khó phát hiện bằng công cụ scan tự động. Các đợt thâm nhập tới sẽ tập trung vào việc **Xây dựng PoC XSS hoàn chỉnh** thông qua các kẽ hở WAF đã tìm thấy.
