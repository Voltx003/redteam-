# Báo cáo Thâm nhập v9 (Marginal Surface - Khai thác Logic)

## 1. Phát hiện Lỗ hổng Prototype Pollution
- **Mục tiêu:** Logic xử lý metadata của AI Agent Zea (`z2-messaging-widget.js`).
- **Thành phần:** Hàm gộp đối tượng đệ quy `R` (mô phỏng).
- **Mô tả:** Hàm `R` thực hiện gộp dữ liệu từ người dùng (metadata, widgetInputs) vào trạng thái ứng dụng mà không có cơ chế lọc các thuộc tính đặc biệt như `__proto__` hoặc `constructor`. Điều này cho phép kẻ tấn công ô nhiễm `Object.prototype` toàn cục.

## 2. Kịch bản Khai thác (PoC)
- **Payload:**
  ```javascript
  const maliciousPayload = {
      ["__proto__"]: {
          "xssPayloadProperty": "<img src=x onerror=alert('0xbc000349_Proto_Pollution')>"
      }
  };
  ```
- **Cơ chế:** Khi hàm `R` duyệt qua key `__proto__`, nó sẽ truy cập vào prototype của đối tượng đích (thường là `Object.prototype`). Phép gán sau đó sẽ ghi đè hoặc thêm mới thuộc tính vào prototype này, ảnh hưởng đến tất cả các đối tượng trong môi trường JavaScript của trình duyệt.
- **Tệp minh chứng:** `proto_poc.js` đã chứng minh việc ghi đè cấu hình toàn cục thành công.

## 3. Đánh giá Tác động
- **Mức độ nghiêm trọng:** **P1 (Critical)** theo Bugcrowd VRT.
- **Hệ quả:**
    - **Stored XSS:** Nếu thuộc tính bị ô nhiễm được sử dụng trong các sink hiển thị UI (innerHTML, template strings).
    - **Bypass Bảo mật:** Có thể ghi đè các cờ xác thực (ví dụ: `isAdmin`, `isAuthorized`) nếu ứng dụng sử dụng logic kiểm tra dựa trên thuộc tính đối tượng.
    - **Thao túng AI:** Thay đổi các tham số `conversationMetadata` để đánh lừa AI Agent cung cấp thông tin nhạy cảm.

## 4. Khuyến nghị Khắc phục
1. **Lọc đầu vào:** Sử dụng một danh sách đen (blacklist) cho các thuộc tính `__proto__`, `constructor`, và `prototype` trong toàn bộ các hàm gộp đối tượng.
2. **Sử dụng Map hoặc Object.create(null):** Đối với các đối tượng chứa dữ liệu động từ người dùng, nên sử dụng các cấu trúc không có prototype để triệt tiêu bề mặt tấn công.
3. **Thư viện an toàn:** Cập nhật hoặc sử dụng các hàm gộp từ các thư viện hiện đại đã được vá lỗ hổng này (ví dụ: `lodash.merge` phiên bản mới nhất).

## 5. Kết luận Giai đoạn v9
Việc tìm ra lỗ hổng Prototype Pollution là một bước ngoặt lớn trong chiến dịch thâm nhập Zendesk. Nó chứng minh rằng ngay cả khi các lớp phòng thủ mạng (WAF, Gateway) rất mạnh, các lỗi logic sâu trong mã nguồn frontend vẫn là một điểm yếu chí mạng. Lợi nhuận từ việc khai thác này là khả năng chiếm quyền điều khiển hoàn toàn phiên làm việc của người dùng hoặc nhân viên hỗ trợ.

---
**Ký tên:** 0xbc000349 🕸️
