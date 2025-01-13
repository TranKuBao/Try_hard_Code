import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style

# Hàm để kiểm tra URL
def check_url(base_url, path):
    url = f"{base_url}/{path}"
    try:
        response = requests.get(url)
        if str(response.status_code)[0] == '2':
            print(Fore.GREEN+f"[+] Found: {path}"+Fore.WHITE)
        else:
           print(Fore.RED+f"[-] Not found: {path} (Status code: {response.status_code})"+Fore.WHITE)
    except requests.RequestException as e:
        print(f"[!] Error with URL {path}: {e}")

# Hàm chính để đọc wordlist và thực hiện quét
def scan_urls(base_url, wordlist_file, threads=5):
    try:
        with open(wordlist_file, "r") as f:
            paths = f.read().splitlines()
        
        # Sử dụng ThreadPoolExecutor để quét nhiều URL cùng lúc
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for path in paths:
                executor.submit(check_url, base_url, path.strip())
    
    except FileNotFoundError:
        print(f"[!] Wordlist file '{wordlist_file}' not found.")

if __name__ == "__main__":
    # URL gốc mà bạn muốn quét
    base_url = "http://localhost:8888"  # Thay URL của bạn vào đây
    
    # File chứa các đường dẫn cần quét
    wordlist_file = "D:\TryHardCode\Python\TrinhSat\Dirsearch\dicc.txt"  # Thay file wordlist của bạn vào đây
    
    # Số lượng thread chạy song song
    threads = 10
    
    # Bắt đầu quá trình quét
    scan_urls(base_url, wordlist_file, threads)
