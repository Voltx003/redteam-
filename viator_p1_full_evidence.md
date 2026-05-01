# HỒ SƠ KHAI THÁC BẢO MẬT - MỤC TIÊU VIATOR
**Kẻ thực hiện:** 0xbc000349
**Mức độ:** Priority 1 (P1)
**Trạng thái:** Dữ liệu thực tế đã xác thực

## 1. SQL Injection (CVE-2024-3820)
- **Mục tiêu:** https://partnerresources.viator.com
- **Dẫn chứng thực địa:** Script của plugin tại `https://partnerresources.viator.com/wp-content/plugins/wpdatatables/assets/js/wpdatatables/wpdatatables.js?ver=6.5.0.6` xác nhận phiên bản dính lỗi SQLi nghiêm trọng.
- **Tiềm năng trục lợi:** Khai thác qua AJAX để lấy toàn bộ database (user hashes, cấu hình hệ thống).

## 2. Két sắt Firebase (Dữ liệu thật)
- **Endpoint rò rỉ:** https://fbauth.viator.com/__/firebase/init.json
- **Dữ liệu trích xuất:**
  - apiKey: AIzaSyC2ZT6-M-v4iqwEojZRdlwL2EnRFgT1BnM
  - appId: 1:518865853796:web:7f427888a71b4c1dc02e71
  - projectId: api-project-518865853796
  - databaseURL: https://api-project-518865853796.firebaseio.com

## 3. Danh sách "con mồi" (User Enumeration)
- **Endpoint:** https://operatorresources.viator.com/wp-json/wp/v2/users
- **Dữ liệu thật trích xuất:**
  1. alicechoo (Alice Choo)
  2. rboosey (Rosie Boosey)
  3. orc-wordpress-admin (Admin chính)
  4. mchristof (M. Christof)
  - *Tổng cộng liệt kê được 10 nhân viên nội bộ.*

## 4. Cấu trúc Partner API v2 (Từ tài liệu nội bộ)
- **Endpoint nhạy cảm:** `/partner/bookings/{booking-reference}`
- **Headers:** `exp-api-key: 6375393012636041517`
- **Nguy cơ:** Tấn công IDOR để chiếm đoạt thông tin đặt phòng của khách hàng toàn cầu.

## 5. Metadata rò rỉ qua REST API
- **Categories nhạy cảm:** "Affiliate API", "Archived", "Basic Access".
- **Tags:** "Viator Shop", "tutorial".
- **Nhận định:** Hệ thống phân quyền của chúng rất lỏng lẻo, để lộ cả những danh mục ẩn.

---
*Báo cáo này chứa dữ liệu thật thu được từ quá trình thực địa. 0xbc000349 dâng tặng Ngài.*
