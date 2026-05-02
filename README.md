# Thiết lập Môi trường Red Team

Kho lưu trữ này cung cấp các kịch bản để thiết lập môi trường nghiên cứu bảo mật trên Ubuntu 24.04, tập trung vào chương trình Bug Bounty của Zendesk.

## Cài đặt Công cụ Kali Linux

> **CẢNH BÁO:** Kịch bản thiết lập sẽ thêm kho lưu trữ Kali Linux vào hệ thống Ubuntu của bạn. Cấu hình "hỗn hợp" này có thể dẫn đến mất ổn định hệ thống nếu không được xử lý cẩn thận. Khuyên dùng môi trường chuyên dụng.

Để cài đặt các công cụ bảo mật Kali thiết yếu, hãy chạy kịch bản thiết lập:

```bash
chmod +x setup_kali.sh
./setup_kali.sh
```

### Các công cụ bao gồm
Kịch bản cài đặt các công cụ sau:
- **Trinh sát:** `nmap`, `netdiscover`, `onesixtyone`, `hping3`, `masscan`, `ffuf`
- **Khai thác:** `metasploit-framework`, `sqlmap`, `aircrack-ng`, `reaver`
- **Bruteforce/Wordlists:** `hashcat`, `crunch`, `cewl`
- **Tiện ích:** `proxychains4`, `macchanger`, `dirb`, `xxd`, `chntpw`, `sslscan`

## Quy tắc Trinh sát
Tham khảo `RECCE.md` và thư mục `reports/` để biết thông tin chi tiết về mục tiêu.
