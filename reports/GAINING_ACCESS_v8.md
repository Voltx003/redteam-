# Báo cáo Thâm nhập v8 (Marginal Surface - Quy tắc Lặp)

## 1. Thám thính Mobile Surface
- **Phát hiện:** Ứng dụng Android `com.zendesk.android` được liên kết chính thức qua `assetlinks.json`.
- **Endpoint di động:** Các API như `/api/v2/mobile/device_tokens.json` và `/api/v2/sdk/settings.json` đều tồn tại nhưng yêu cầu xác thực **401 Unauthorized**.
- **Đánh giá:** Không có sự phân biệt đối xử trong chính sách bảo mật giữa các yêu cầu từ Web và Mobile SDK.

## 2. Phân tích ZAF Apps (Apps Marketplace)
- **Danh sách:** Thu thập được danh sách ứng dụng phổ biến như Salesforce, Harvest, WordPress.
- **Tài sản:** Các ứng dụng được lưu trữ tại `p*.apps.zdusercontent.com`. Các nỗ lực truy cập trực tiếp file `manifest.json` đều trả về lỗi **422 Unprocessable Entity**.
- **Kết luận:** Việc thâm nhập vào các ứng dụng bên thứ ba yêu cầu kẻ tấn công phải có một `installation_id` hợp lệ và một session đang hoạt động.

## 3. Luồng OAuth & Điều hướng
- **Chuỗi chuyển hướng:** `/hc/en-us/signin` -> `/access` -> `/auth/v3/signin`.
- **Cấu hình:** Zendesk đã vô hiệu hóa `login.zendesk.com` để tập trung vào luồng xác thực mới (v3). Các tham số `return_to` được kiểm duyệt nghiêm ngặt qua nhiều lớp proxy.

## 4. Kết luận Giai đoạn v8
Đợt lặp thứ 8 khẳng định rằng các bề mặt "vùng biên" như Mobile API và App Framework cũng được Zendesk bảo vệ cực kỳ nghiêm ngặt. Hệ thống không chỉ có bộ lọc mạnh mà còn có cấu hình nhất quán trên toàn bộ các phương thức truy cập. Lợi nhuận từ việc khai thác cấu hình sai (misconfiguration) là gần như bằng không. Chiến thuật tiếp theo cần chuyển sang các cuộc tấn công **Client-side tinh vi** hơn hoặc tìm kiếm kẽ hở trong **Logic tích hợp của các App bên thứ ba**.
