# Báo cáo Quét & Liệt kê v3 (Deep Scanning)

## 1. Thám thính Dịch vụ Chuyên sâu
- **Cổng 8443 (Handshake Failure):** Cổng này yêu cầu cấu hình SSL/TLS đặc thù (có thể là Authenticated Origin Pulls). Điều này ngăn chặn việc quét nội dung trực tiếp qua IP.
- **Tính nhất quán của Banner:** Toàn bộ dải IP đều trả về banner Cloudflare, xác nhận lớp bảo vệ đồng bộ.

## 2. Quét Thư mục Ẩn Đệ quy
- **Kết quả:** Quét đệ quy trên các thư mục như `/assets/logs` hoặc `/data/config` đều trả về **403 Forbidden**.
- **Backup Files:** Không phát hiện rò rỉ tệp sao lưu trên các tên miền đối tác chính.

## 3. Liệt kê Tính năng Nâng cao (App Marketplace)
- **Marketplace Enumeration:** API `/api/v2/apps.json` tiết lộ danh sách các ứng dụng tích hợp. Tài sản của ứng dụng được lưu trữ trên các POD riêng biệt (`p*.apps.zdusercontent.com`), giúp giảm thiểu rủi ro rò rỉ chéo giữa các ứng dụng.

## 4. Thử nghiệm Evasion WAF Nâng cao
- **URL Manipulation:** Các kỹ thuật bypass qua encoding (%61dmin) đều bị phát hiện và chuyển hướng về trang xác thực.
- **Header Injection:** Cloudflare chặn đứng các payload tiêm vào tiêu đề HTTP.

## 5. Trái thấp - Cloud Assets
- **S3 Buckets:** Xác nhận sự tồn tại của `zendesk-support.s3.amazonaws.com` và `zendesk-chat.s3.amazonaws.com`. Cả hai đều được cấu hình **403 Forbidden** cho truy cập công khai, đảm bảo an toàn dữ liệu.

## 6. Kết luận Giai đoạn v3
Các nỗ lực quét sâu và đệ quy không phát hiện thêm các điểm yếu nghiêm trọng mới, khẳng định cấu hình bảo mật hiện tại của Zendesk là rất chặt chẽ. Trọng tâm của các giai đoạn tới nên chuyển hoàn toàn sang **Khai thác Logic AI** và **CORS Exploitation** dựa trên các phát hiện từ giai đoạn Trinh sát.
