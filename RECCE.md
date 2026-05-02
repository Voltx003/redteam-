# Trinh sát: Zendesk Bug Bounty (Bugcrowd)

## Quy tắc tham gia
- **Safe Harbor:** Đang hoạt động.
- **Danh tính:** Sử dụng email `@bugcrowdninja.com`.
- **Tên công ty:** `bb-<bugcrowd-username>`.
- **Định dạng Instance:** `bb-<bugcrowd-username>-<suffix>.zendesk.com`.
- **Cấm:** Không DoS/DDoS, không kỹ thuật xã hội (social engineering), không tấn công vật lý.

## Phạm vi (Scope)
- `*.zendesk.com`
- `*.zd-master.com`
- Các tính năng Zendesk AI (AI agents, Copilot, App Builder).
- Các lỗ hổng liên quan đến LLM.

## Công cụ sẵn có
- Nmap, Metasploit, SQLmap, Aircrack-ng, Dirb, Hashcat, Cewl, Proxychains4, ffuf, masscan.

## Chiến lược
- Tuân theo Phân loại Xếp hạng Lỗ hổng (VRT) của Bugcrowd.
- Tập trung vào các lỗi logic tác động cao (IDOR, SSO) hoặc các lỗ hổng đặc thù của AI.
