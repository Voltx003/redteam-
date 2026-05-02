# Báo cáo Trinh sát v6: Tích hợp & Mobile Surface

## 1. Phân tích Chuỗi Cung ứng & Tích hợp
- **Hệ sinh thái Marketplace:** Các ứng dụng thường sử dụng OAuth Access Tokens với các scope rộng như `read`, `write`, `impersonate`.
- **SDK & Thư viện:**
  - Web Widget tải các tài nguyên từ `static.zdassets.com`.
  - Phát hiện sử dụng Google Tag Manager (GTM) và các thư viện phân tích của bên thứ ba.
  - Tích hợp với **Ultimate.ai** sử dụng endpoint `https://api.ultimate.ai`.

## 2. API Di động (Mobile Surface)
- **App Package:** `com.zendesk.android`
- **Fingerprint:** Đã xác định SHA256 cert fingerprint từ `assetlinks.json`.
- **Endpoint tiềm năng:**
  - `/api/v2/sdk/...`
  - `/api/v2/mobile/...`
- **Sự khác biệt:** API Mobile thường có cơ chế xác thực dựa trên thiết bị hoặc SDK token, đôi khi ít bị áp dụng Rate Limiting hơn so với API Web.

## 3. Phân tích Token & JWT
- **Integration Tokens:** Được sử dụng cho các tích hợp Help Center (`/hc/api/v2/integration/token`).
- **JWT Usage:** Zendesk sử dụng JWT để xác thực người dùng trong Chat và Help Center.
- **Rủi ro:** TTL của JWT nếu quá dài có thể bị lợi dụng nếu token bị rò rỉ qua tiêu đề `Referer`.

## 4. Tấn công AI Nâng cao (LLM Security)
- **Model Extraction:** Thử nghiệm trích xuất các quy tắc hệ thống thông qua Prompt Injection (đã tài liệu hóa phương pháp luận).
- **AI DoS:** Gửi các yêu cầu phức tạp hoặc lặp lại để làm cạn kiệt tài nguyên xử lý của AI Agent.

## 5. Kết luận Giai đoạn v6
Bề mặt tấn công mở rộng sang các **ứng dụng di động** và **ứng dụng Marketplace**. Các điểm tích hợp OAuth và cơ chế xác thực SDK là những vùng biên cần được chú ý đặc biệt.
