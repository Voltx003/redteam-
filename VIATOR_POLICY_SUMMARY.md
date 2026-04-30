# Tóm tắt Quy chế Bug Bounty Viator (Tripadvisor) - 0xbc000349

## 1. Thông tin chung
- **Trạng thái:** Đang diễn ra (từ 09/02/2017)
- **Chính sách:** Partial safe harbor (Bảo vệ một phần cho nhà nghiên cứu).
- **Phân loại VRT:** Sử dụng Bugcrowd Vulnerability Rating Taxonomy.

## 2. Phần thưởng (Rewards)
- **P1 (Critical):** $4,100 – $4,500
- **P2 (High):** $2,000 – $2,300
- **P3 (Medium):** $600 – $850
- **P4 (Low):** $200 – $250

## 3. Phạm vi mục tiêu (In-Scope Targets)
- **API chính:** `https://viatorapi.viator.com/service/directory`
    - *Lưu ý:* Sử dụng Api Key = `6375393012636041517`.
- **Iframe Proxy:** `gtm-orn.viator.com` (Được sử dụng trên một số trang của viator.com).
- **Ứng dụng di động:** iOS Viator Tours & Activities App.
- **Tên miền:** `viator.com`, `partners.viator.com` và các subdomain liên quan.

## 4. Các mục loại trừ (Out of Scope)
- Không quan tâm đến các báo cáo về "no session expiry on logout" hoặc tương tự trên iframe.
- Các lỗ hổng liên quan đến hành vi mặc định của Firebase (Firebase-native behavior).
- Mọi lỗ hổng liên quan đến tính năng yêu cầu xác thực KYC trên `partners.viator.com`.
- Các vấn đề về throttling (giới hạn tốc độ) trên `partners.viator.com` và các subdomain (bao gồm tạo tài khoản hàng loạt, thử đăng nhập liên tục).
- Các báo cáo trùng lặp trên nhiều trang ngôn ngữ khác nhau sẽ bị tính là một.

## 5. Lưu ý quan trọng cho 0xbc000349
- **DataDome Protection:** Hệ thống được bảo vệ mạnh mẽ, cần sử dụng các kỹ thuật tinh vi hơn để vượt qua cơ chế chống bot.
- **API Key:** Đây là chìa khóa chính được cung cấp để kiểm tra các endpoint API.
- **Trọng tâm:** Viator tập trung vào tính bảo mật của các iframe và các dịch vụ API cốt lõi.

---
*Ký tên: 0xbc000349* 😈
