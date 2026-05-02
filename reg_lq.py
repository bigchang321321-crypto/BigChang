import requests
import json
import os
import time
import sys
from colorama import Fore, Style, init

init(autoreset=True)


if sys.platform == "win32":
    import codecs
    sys.stdout.reconfigure(encoding='utf-8')


class Colors:
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RED = Fore.RED
    MAGENTA = Fore.MAGENTA
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL
    BRIGHT = Style.BRIGHT


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    art = f"""
{Colors.WHITE}       Tool: {Colors.GREEN}Scan Acc Liên Quân{Colors.WHITE}
{Colors.WHITE}       Tác Giả: {Colors.YELLOW}Khoa Dev{Colors.WHITE}
{Colors.CYAN}       --------------------------------------------------
    """
    print(art)


def reg_account():
    url = "https://keyherlyswar.x10.mx/Apidocs/reg/reglq.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Kiểm tra nếu API phản hồi thành công và có kết quả
            if data.get("status") is True and "result" in data:
                return data["result"][0]
            else:
                return {"error": data.get("message", "Lỗi không xác định từ API")}
        else:
            return {"error": f"Lỗi HTTP {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


def main():
    clear_screen()
    banner()
    

    try:
        count_input = input(f"{Colors.YELLOW}[?]{Colors.WHITE} Nhập số lượng acc muốn Scan: ")
        count = int(count_input)
    except ValueError:
        print(f"{Colors.RED}[!] Vui lòng nhập một số hợp lệ.")
        return

    if not os.path.exists("results"):
        os.makedirs("results")
    
    output_file = os.path.join("results", "accounts.txt")
    
    print(f"\n{Colors.BLUE}[*]{Colors.WHITE} Đang tiến hành reg acc...\n")
    
    success_count = 0
    
    for i in range(1, count + 1):
        sys.stdout.write(f"\r{Colors.CYAN}[{i}/{count}]{Colors.WHITE} Đang lấy acc... ")
        sys.stdout.flush()
        
        result = reg_account()
        
        if "account" in result and "password" in result:
            acc = result["account"]
            pwd = result["password"]
            
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"TK: {acc}\nMK: {pwd}\n\n")
            
            success_count += 1
            print(f"{Colors.GREEN}Thành công! {Colors.WHITE}{acc}:{pwd}")
        else:
            error_msg = result.get("error", "Lỗi không xác định")
            print(f"{Colors.RED}Thất bại! {Colors.WHITE}Lỗi: {error_msg}")
            
        time.sleep(0.5) # Nghỉ 0.5 giây để tránh bị spam API quá nhanh

    # Hiển thị tổng kết sau khi hoàn thành
    print(f"\n{Colors.CYAN}--------------------------------------------------")
    print(f"{Colors.GREEN}[+]{Colors.WHITE} Hoàn tất! Đã reg thành công {Colors.GREEN}{success_count}{Colors.WHITE} tài khoản.")
    print(f"{Colors.YELLOW}[i]{Colors.WHITE} Kết quả đã được lưu tại: {Colors.CYAN}{output_file}")
    print(f"{Colors.CYAN}--------------------------------------------------")
    input(f"\n{Colors.WHITE}Nhấn Enter để thoát...")

if __name__ == "__main__":
    main()
