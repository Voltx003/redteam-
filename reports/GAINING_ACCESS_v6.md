# Báo cáo Thâm nhập v6 (Intelligence & Strategy - Tư duy Đa diện)

## 1. Thám thính Hạ tầng GraphQL
- **Phát hiện:** Endpoint `https://support.zendesk.com/api/v2/graphql` tồn tại.
- **Trạng thái:** Yêu cầu xác thực (Chuyển hướng 302 về trang đăng nhập).
- **Đánh giá:** GraphQL là một bề mặt tấn công hiện đại. Mặc dù yêu cầu đăng nhập, nhưng nếu có thể thâm nhập với quyền người dùng thấp (end-user), ta có thể khai thác các lỗi thiếu kiểm tra phân quyền (IDOR/BOLA) trên các query/mutation phức tạp.

## 2. Phân tích Luồng Điều hướng (Redirection)
- **Tham số nhạy cảm:** Phát hiện tham số `return_to` được sử dụng rộng rãi trong luồng xác thực tại `/access/login` và `/hc/en-us/signin`.
- **Lớp bảo vệ:** Zendesk sử dụng một dịch vụ trung tâm (`/auth/v3/signin`) để xử lý điều hướng. Các URL điều hướng được mã hóa và kiểm tra so với whitelist nội bộ.
- **Tiềm năng:** Một lỗi Open Redirect ở đây có thể được dùng làm "mồi nhử" trong một cuộc tấn công lừa đảo (Phishing) hoặc kết hợp với lỗ hổng CORS để đánh cắp token.

## 3. Giải mã Sandbox của Zendesk Apps (ZAF)
- **Mã nguồn:** `zaf_sdk.js`
- **Cơ chế Bảo mật:** ZAF SDK sử dụng `addEventListener("message", ...)` để giao tiếp giữa các khung hình (iframes).
- **Whitelist Origin:** Phát hiện một danh sách các regex nghiêm ngặt để xác thực nguồn gửi tin nhắn:
    - `^https?:\/\/127.0.0.1(:\d+)?$`
    - `^https?:\/\/localhost(:\d+)?$`
    - `^https:\/\/.+\.zendesk\.com$`
    - `^https:\/\/.+\.zd-staging\.com$`
- **Lỗ hổng logic:** Cơ chế này phụ thuộc hoàn toàn vào tính toàn vẹn của các subdomain trong whitelist. Nếu một subdomain của Zendesk (ví dụ một trang staging cũ) bị chiếm quyền hoặc có lỗi XSS, kẻ tấn công có thể giả mạo tin nhắn postMessage để điều khiển các ứng dụng Zendesk khác hoặc trích xuất dữ liệu từ context của nhân viên hỗ trợ.

## 4. Chuỗi Tấn công Lý thuyết (Theoretical Attack Chain)
0xbc000349 đề xuất chuỗi tấn công sau để chiếm đoạt dữ liệu két sắt:
1. **Bước 1:** Tìm kiếm một lỗi XSS hoặc Subdomain Takeover trên một subdomain "vùng xám" thuộc whitelist của ZAF (ví dụ: một trang dev/staging cũ).
2. **Bước 2:** Sử dụng subdomain bị chiếm quyền đó để gửi tin nhắn `postMessage` độc hại tới ZAF SDK trong trình duyệt của nhân viên hỗ trợ Zendesk.
3. **Bước 3:** Lợi dụng ZAF SDK để trích xuất API Token hoặc thực hiện các yêu cầu API với quyền hạn cao thông qua `client.request()`.
4. **Bước 4:** Kết hợp với lỗ hổng CORS wildcard để chuyển dữ liệu trích xuất được về máy chủ của kẻ tấn công mà không bị WAF phát hiện.

## 5. Kết luận Giai đoạn v6
Tư duy Đa diện đã chỉ ra rằng sức mạnh của Zendesk nằm ở sự đồng bộ, nhưng điểm yếu lại nằm ở **quy mô quá lớn**. Việc duy trì bảo mật tuyệt đối trên hàng ngàn subdomain và các ứng dụng bên thứ ba là bất khả thi. Chuỗi tấn công qua **postMessage + Subdomain Compromise** là con đường khả dĩ nhất để thâm nhập vào "két sắt" dữ liệu nội bộ.
