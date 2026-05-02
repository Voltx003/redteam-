# Báo cáo Trinh sát v7: Xác thực & Kết luận

## 1. Xác thực Hạ tầng (Validation)
- **POD Consistency:** Xác nhận sự nhất quán của các bản ghi POD (POD 26 cho support/chat, POD 20 cho internal). Dải IP của POD 20 thuộc sở hữu trực tiếp của Zendesk (AS11404).
- **Gateway Validation:** Xác nhận toàn bộ hạ tầng sử dụng `zorg` làm Gateway trung tâm và `envoy` làm proxy xử lý.

## 2. Phát hiện Quan trọng về CORS (Critical Finding)
- **CORS Wildcard:** Phát hiện `access-control-allow-origin: *` trên các endpoint API của `support.zendesk.com`.
- **Đánh giá:** Mặc dù wildcard thường ngăn chặn việc sử dụng `Access-Control-Allow-Credentials: true`, nhưng nó vẫn cho phép các trang web bên thứ ba đọc dữ liệu từ các API công khai hoặc API yêu cầu App Key mà không yêu cầu cookie phiên.

## 3. Xác thực WAF & Chặn (WAF Validation)
- **Cloudflare Behavior:** Cloudflare áp dụng cơ chế `Authenticated Origin Pulls`, ngăn chặn việc truy cập trực tiếp vào backend qua IP. Các cổng 8080 và 8443 đóng vai trò là các điểm cuối proxy thay thế nhưng vẫn nằm dưới sự kiểm soát của Cloudflare.

## 4. Tổng hợp Chức năng (Functional Summary)
- Hệ thống có sự phân tách rõ rệt giữa **Dữ liệu Người dùng (zdusercontent.com)** và **Tài nguyên Tĩnh (zdassets.com)**.
- Tích hợp AI thông qua **Ultimate.ai** được quản lý bởi một lớp Kong Gateway riêng biệt.

## 5. Kết luận Cuối cùng (Final Conclusion)
Bề mặt tấn công của Zendesk rất rộng lớn nhưng được bảo vệ bởi nhiều lớp. Điểm yếu nhất nằm ở **Cấu hình CORS lỏng lẻo** trên một số subdomain và **Logic xử lý của AI Agent**. Các đợt tấn công tiếp theo nên tập trung vào việc khai thác CORS wildcard để trích xuất thông tin hoặc Prompt Injection để thao túng AI.
