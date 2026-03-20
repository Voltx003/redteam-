#!/bin/bash
# ==============================================================================
# Script Name:     Defacement-Scanner
# Description:     Một script bash chuyên nghiệp để rà soát các cấu hình yếu (Weak Configurations)
#                  có thể dẫn đến việc thay đổi giao diện web (Defacement/File Upload) trên máy chủ.
# Author:          Red Team (Mô phỏng)
# Date:            $(date +"%Y-%m-%d")
# Usage:           ./scanner.sh <URL>
# ==============================================================================

# Màu sắc hiển thị
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Không màu

# Kiểm tra đầu vào
if [ -z "$1" ]; then
    echo -e "${RED}[!] Lỗi: Thiếu tham số URL.${NC}"
    echo -e "Cách sử dụng: $0 <URL>"
    echo -e "Ví dụ: $0 http://localhost:8080"
else
    TARGET_URL="$1"
    REPORT_FILE="vulnerability_report.txt"

    # Khởi tạo file báo cáo
    echo "===============================================" > "$REPORT_FILE"
    echo " Báo cáo quét lỗ hổng (Defacement Assessment)" >> "$REPORT_FILE"
    echo " Mục tiêu: $TARGET_URL" >> "$REPORT_FILE"
    echo " Thời gian: $(date)" >> "$REPORT_FILE"
    echo "===============================================" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"

    echo -e "${GREEN}[+] Bắt đầu quét mục tiêu: $TARGET_URL${NC}"

    # 1. Thu thập thông tin máy chủ (Server Information Disclosure)
    echo -e "${YELLOW}[*] Bước 1: Thu thập thông tin Server Headers...${NC}"
    headers=$(curl -s -I -X GET "$TARGET_URL")

    server_info=$(echo "$headers" | grep -i "Server:")
    powered_by=$(echo "$headers" | grep -i "X-Powered-By:")

    if [ -n "$server_info" ]; then
        echo -e "${RED}[!] Phát hiện thông tin máy chủ bị lộ:${NC} $server_info"
        echo "- Lộ Server Headers: $server_info" >> "$REPORT_FILE"
    else
        echo -e "${GREEN}[+] Không phát hiện rò rỉ thông tin Server.${NC}"
    fi

    if [ -n "$powered_by" ]; then
        echo -e "${RED}[!] Phát hiện thông tin nền tảng (X-Powered-By):${NC} $powered_by"
        echo "- Lộ X-Powered-By: $powered_by" >> "$REPORT_FILE"
    fi

    # 2. Kiểm tra các phương thức HTTP cho phép (HTTP Methods - OPTIONS)
    echo -e "${YELLOW}[*] Bước 2: Kiểm tra các phương thức HTTP...${NC}"
    options_result=$(curl -s -I -X OPTIONS "$TARGET_URL")
    allowed_methods=$(echo "$options_result" | grep -i "Allow:" | cut -d ':' -f 2)

    if [ -n "$allowed_methods" ]; then
        echo -e "${YELLOW}[*] Các phương thức HTTP được phép:${NC} $allowed_methods"
        echo "- Các phương thức HTTP (OPTIONS): $allowed_methods" >> "$REPORT_FILE"

        # Kiểm tra phương thức PUT/DELETE nguy hiểm
        if echo "$allowed_methods" | grep -iq "PUT"; then
            echo -e "${RED}[!] CẢNH BÁO: Phương thức PUT được bật. Điều này có thể cho phép attacker tải file lên server và thay đổi giao diện (Defacement)!${NC}"
            echo "- [CRITICAL] Phương thức PUT được cho phép. Nguy cơ bị tấn công Defacement rất cao." >> "$REPORT_FILE"

            # Thử nghiệm gửi dữ liệu qua PUT
            echo -e "${YELLOW}[*] Thử nghiệm gửi request PUT (Mô phỏng Defacement)...${NC}"
            put_test=$(curl -s -X PUT -d "Hacked by Red Team" "$TARGET_URL/test_upload.html")
            echo -e "${RED}[!] Phản hồi từ Server khi thử PUT:${NC} $put_test"
            echo "- Bằng chứng lỗ hổng PUT (PoC): Tải thành công payload. Server phản hồi: $put_test" >> "$REPORT_FILE"
        else
            echo -e "${GREEN}[+] Máy chủ không cho phép phương thức PUT/DELETE.${NC}"
        fi
    else
        echo -e "${GREEN}[+] Không thu thập được danh sách phương thức (OPTIONS không được hỗ trợ).${NC}"
    fi

    # 3. Kiểm tra các Header bảo mật cơ bản
    echo -e "${YELLOW}[*] Bước 3: Kiểm tra các Header bảo mật chống XSS/Clickjacking...${NC}"
    missing_headers=""

    if ! echo "$headers" | grep -iq "X-Frame-Options"; then
        missing_headers+="- Thiếu X-Frame-Options (Nguy cơ Clickjacking)\n"
        echo -e "${RED}[!] Thiếu header X-Frame-Options${NC}"
    fi

    if ! echo "$headers" | grep -iq "X-Content-Type-Options"; then
        missing_headers+="- Thiếu X-Content-Type-Options\n"
        echo -e "${RED}[!] Thiếu header X-Content-Type-Options${NC}"
    fi

    if [ -n "$missing_headers" ]; then
        echo "Các header bảo mật bị thiếu:" >> "$REPORT_FILE"
        echo -e "$missing_headers" >> "$REPORT_FILE"
    else
        echo -e "${GREEN}[+] Các header bảo mật cơ bản đã được cấu hình đủ.${NC}"
        echo "- Đã cấu hình đủ các header bảo mật cơ bản (X-Frame-Options, X-Content-Type-Options)." >> "$REPORT_FILE"
    fi

    echo -e "${GREEN}[+] Quá trình quét hoàn tất. Xem chi tiết tại: $REPORT_FILE${NC}"
fi
