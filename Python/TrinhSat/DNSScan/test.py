import requests
from concurrent.futures import ThreadPoolExecutor

# Hàm quét subdomain
def scan_subdomain(subdomain, domain_name):
    url = f"https://{subdomain}.{domain_name}"
    try:
        # Gửi request đến URL
        requests.get(url)
        print(f'[+] {url}')
    except requests.ConnectionError:
        # Bỏ qua nếu không kết nối được
        pass

# Hàm quản lý quét các subdomain
def domain_scanner(domain_name):
    print('----URL after scanning subdomains----')

    # Đọc file chứa danh sách subdomains
    with open('dicc_sub.txt', 'r') as file:
        subdomains = file.read().splitlines()

    # Sử dụng ThreadPoolExecutor để quét đồng thời các subdomains
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Gọi hàm scan_subdomain trên mỗi subdomain
        for subdomain in subdomains:
            executor.submit(scan_subdomain, subdomain, domain_name)

# Hàm chính
if __name__ == '__main__':
    # Nhập tên domain từ người dùng
    domain_name = input("Enter the Domain Name: ")

    # Gọi hàm quét subdomain
    domain_scanner(domain_name)
