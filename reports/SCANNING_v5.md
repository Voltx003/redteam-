# Báo cáo Quét & Liệt kê v5 (Thâm nhập vùng xám)

## 1. Mở rộng Bề mặt Tấn công (Subdomain Enumeration)
- **Kết quả:** Sử dụng CT logs, đã liệt kê hàng ngàn subdomain của Zendesk.
- **Phát hiện quan trọng:** Các môi trường Staging/Dev như `axialdev.zendesk.com`, `unisport-dev.zendesk.com`, và `test-care.zendesk.com` đã được lộ diện. Các môi trường này thường có cấu hình bảo mật lỏng lẻo hơn môi trường production và là mục tiêu lý tưởng để thám thính sâu hơn.
- **Danh sách chi tiết:** Được lưu trữ trong `reports/subdomains_v5.txt`.

## 2. Thăm dò Endpoint Xác thực (Auth Probe)
- **Endpoint:** `/hc/api/v2/integration/token`
- **Phương thức:** PUT, DELETE, PATCH đều trả về **404 Not Found** từ Gateway `zorg/envoy`.
- **Tham số:** Fuzzing các tham số như `app_id`, `client_id`, `user_id` đều trả về **403 Forbidden**.
- **Kết luận:** Cơ chế bảo vệ tầng Gateway rất vững chắc, ngăn chặn các truy cập trái phép hoặc các phương thức HTTP không được hỗ trợ.

## 3. Giải mã AI Agent Zea (Widget Analysis)
- **Mã nguồn:** `z2-messaging-widget.js`
- **Cấu trúc Dữ liệu:**
    - Zea thu thập metadata bao gồm: `categoryId`, `lang`, `productInstanceJwt`, `referrer`, `userAgent`, và các tham số đầu vào tùy chỉnh `widgetInput1` đến `widgetInput5`.
    - Dữ liệu được gửi về backend qua cơ chế `messenger:set` và `conversationMetadata`.
- **Cơ chế Xác thực:** Sử dụng JWT thông qua hàm `loginUser`. Phát hiện các biến như `jwtAuth` và `productInstanceJwt` quản lý trạng thái xác thực của người dùng trong widget.
- **Logic Ẩn:** Widget có khả năng tự động mở hội thoại mới (`newConversation`) dựa trên tham số `deepLinkParam` hoặc trạng thái `openWidgetToNewConversation`.

## 4. Kết luận v5
Giai đoạn v5 đã thâm nhập thành công vào "vùng xám" bằng cách xác định các môi trường staging tiềm năng và giải mã logic hoạt động của AI Agent. Việc phát hiện các tham số đầu vào của widget (widgetInput1-5) mở ra hướng tấn công **Prompt Injection** hoặc **XSS** thông qua việc thao túng các giá trị này trước khi chúng được gửi về AI backend.
