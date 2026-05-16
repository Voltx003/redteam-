# Báo cáo Thâm nhập v2 (Deep Penetration - Quy tắc 1 & Lặp)

## 1. Khai thác CORS Chuyên sâu
- **Phát hiện:** Các endpoint API v2 nhạy cảm chấp nhận Header `Authorization` và `X-CSRF-Token` từ bất kỳ nguồn nào (`*`).
- **Lợi nhuận:** Mặc dù trình duyệt chặn việc gửi thông tin xác thực tự động (cookies), nhưng nếu kẻ tấn công lừa được người dùng thực hiện một yêu cầu chứa custom headers (ví dụ qua một ứng dụng độc hại hoặc tiện ích trình duyệt), dữ liệu sẽ bị trích xuất toàn bộ.
- **Bằng chứng:** `reports/cors_headers_v2.txt`

## 2. Chiếm đoạt JWT & AI Agent
- **Chiến thuật:** Giả mạo nguồn gốc từ môi trường Staging (`axialdev.zendesk.com`) để yêu cầu token từ `guide-jwt-service`.
- **Kết quả:** Hệ thống vẫn yêu cầu xác thực phiên (401), nhưng việc xác định được dịch vụ backend (`guide-jwt-service`) và sự chấp nhận các header từ staging cho thấy một hướng tấn công **Account Takeover** nếu chiếm được phiên trên subdomain staging.
- **Bằng chứng:** `reports/jwt_theft_v2.txt`

## 3. IDOR trên Vùng tối (Search & Bulk Update)
- **Kịch bản:** Thử nghiệm thao túng tham số tìm kiếm và cập nhật hàng loạt để tác động lên dữ liệu của tenant khác.
- **Kết quả:** Hệ thống trả về **404**, xác nhận logic phân tách dữ liệu được thực thi nghiêm ngặt tại Gateway. Không tìm thấy sơ hở "trái thấp" (low-hanging fruit) trong đợt quét này.

## 4. Truy quét Rò rỉ Thông tin Staging
- **Kết quả:** Các tệp cấu hình nhạy cảm như `.env`, `.git/config` đều được bảo vệ bằng mã lỗi **403/404**.
- **Đánh giá:** Lớp bảo mật của Zendesk được áp dụng đồng bộ, giảm thiểu rủi ro rò rỉ mã nguồn hoặc thông tin nội bộ qua các tệp cấu hình công khai.

## 5. Kết luận Giai đoạn v2
Kích hoạt **Quy tắc 1** và **Quy tắc Lặp** đã giúp xác định rằng Zendesk không có những lỗ hổng logic cơ bản dễ khai thác. Lợi nhuận lớn nhất hiện nay nằm ở việc **Khai thác CORS qua Custom Headers** và **Tấn công chuỗi cung ứng/staging**. Các đợt lặp tiếp theo nên tập trung vào việc tìm kiếm các **API v2 ẩn** hoặc các **Endpoint chưa được bảo vệ** bởi Gateway zorg.
