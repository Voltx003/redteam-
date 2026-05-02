# Báo cáo Thâm nhập v4 (Cường độ cao - Quy tắc Lặp)

## 1. Lặp lại thử nghiệm XSS (Iterative XSS)
- **Kịch bản:** Sử dụng `ffuf` với danh sách payload Polyglot và bypass WAF để càn quét trang tìm kiếm.
- **Kết quả:** Mặc dù máy chủ trả về mã lỗi **200 OK** cho một số payload, nhưng việc kiểm tra nội dung phản hồi cho thấy Zendesk thực hiện HTML Encoding rất tốt. Các nỗ lực bypass bằng encoding (`%3Csvg...`) cũng bị Cloudflare chặn đứng với mã lỗi **403**.
- **Kết luận:** Trang tìm kiếm được bảo vệ tốt trước XSS reflected thông thường.

## 2. Truy vết sâu Prototype Pollution
- **Hành động:** Tải lại và mổ xẻ mã nguồn `z2-messaging-widget.js`.
- **Phát hiện:** Biến `widgetInputs` (có thể được điều khiển bởi người dùng qua URL hoặc API tích hợp) được đưa trực tiếp vào hàm `Object.assign()` để tạo `conversationMetadata`.
- **Rủi ro:** Đây là một "sink" tiềm năng cho Prototype Pollution. Nếu kẻ tấn công có thể chèn thuộc tính `__proto__` vào `widgetInputs`, họ có thể thay đổi các thuộc tính toàn cục của widget, dẫn đến bypass các kiểm tra xác thực hoặc thực thi mã.
- **Bằng chứng:** `reports/proto_pollution_v3.txt` (vẫn còn giá trị trong v4).

## 3. Lặp lại thám thính JWT (JWT Iteration)
- **Chiến thuật:** Thử nghiệm hàng loạt 50+ subdomain staging làm Origin cho endpoint lấy token.
- **Kết quả:** Hệ thống duy trì sự nhất quán tuyệt đối. Mọi yêu cầu không có session hợp lệ đều bị chặn (401) và không có tiêu đề CORS nào được lộ ra cho các Origin không xác định.
- **Phân tích:** Lớp Gateway `zorg` và dịch vụ `guide-jwt-service` có whitelist Origin được quản lý rất chặt chẽ.

## 4. Kết luận Giai đoạn v4
Sự kiên trì qua **Quy tắc Lặp** đã xác nhận rằng các rào cản kỹ thuật của Zendesk là rất đồng nhất. Kẽ hở khả dĩ nhất hiện nay không nằm ở cấu hình sai (misconfiguration) mà nằm ở **Logic xử lý đối tượng trong JavaScript (Prototype Pollution)**. Đợt thâm nhập tiếp theo nên tập trung hoàn toàn vào việc xây dựng một kịch bản khai thác logic hoàn chỉnh cho Prototype Pollution trong Widget.
