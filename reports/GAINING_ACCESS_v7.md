# Báo cáo Thâm nhập v7 (Direct Action - Thực chiến Lục Két)

## 1. Săn lùng Source Map (JS.map)
- **Hành động:** Kiểm tra sự tồn tại của tệp ánh xạ mã nguồn (`.js.map`) cho các thư viện lõi.
- **Kết quả:** Toàn bộ các yêu cầu tới `.js.map` đều bị chặn bởi mã lỗi **403 Forbidden**.
- **Kết luận:** Zendesk đã thực hiện đúng quy trình bảo mật bằng cách không công khai mã nguồn gốc, gây khó khăn cho việc phân tích logic ngược.

## 2. Thâm nhập Sentry Project
- **Dữ liệu:** Sử dụng DSN `https://[REDACTED_SENTRY_DSN]`.
- **Hành động:** Gửi các yêu cầu POST tới endpoint `/envelope/` của Sentry.
- **Kết quả:** Server Sentry phản hồi xác nhận sự tồn tại của project nhưng yêu cầu cấu trúc payload nghiêm ngặt (lỗi: `bad envelope authentication header`).
- **Phân tích:** Việc có thể tương tác trực tiếp với ingest endpoint của Sentry cho thấy kẻ tấn công có thể thực hiện tấn công **Denial of Service (DoS)** bằng cách gửi hàng loạt lỗi giả mạo hoặc làm nhiễu loạn dữ liệu giám sát của Zendesk.

## 3. Thám thính PII qua API Công khai
- **Endpoint:** `/api/v2/users/me.json`
- **Kết quả:** Trả về đối tượng người dùng với tên `Anonymous user` và email `invalid@example.com`.
- **Comment Probe:** Kiểm tra bài viết ID `4405298833818`, không phát hiện bất kỳ comment nào lộ thông tin cá nhân của khách hàng.
- **Kết luận:** Cơ chế bảo mật dữ liệu cá nhân (PII) trên các API Help Center được cấu hình rất tốt, tuân thủ nghiêm ngặt các quy định về quyền riêng tư.

## 4. Quét Tàn dư trên Staging (axialdev)
- **Kết quả:** Toàn bộ các tệp tin nhạy cảm như `config.yml`, `secrets.json`, `npm-debug.log` đều trả về **404 Not Found**.
- **Đánh giá:** Môi trường staging của Zendesk không chỉ được bảo vệ bởi Gateway mà còn được dọn dẹp (cleanup) dữ liệu định kỳ, không để lại dấu vết thừa.

## 5. Kết luận Giai đoạn v7
Sau đợt thực chiến thâm nhập trực tiếp, có thể khẳng định rằng Zendesk không có những "trái thấp" (low-hanging fruits) như rò rỉ mã nguồn hay thông tin nhạy cảm qua tệp tin logs. Sự an toàn của họ là sự kết hợp giữa **Cấu hình Gateway chuẩn mực** và **Quy trình dọn dẹp hệ thống kỷ luật**. Lợi nhuận thực tế lúc này chỉ có thể nằm ở các lỗ hổng **Zero-day** trong các dịch vụ proxy hoặc gateway.
