from locale import normalize
from Recon_Dirsearch._Dirseach_ import Recon_Directory, print_result_callback
from Recon_Nmap._Nmap_ import Recon_Nmap
from Recon_Wappalyzer._Wappalyzer_ import Recon_Wappalyzer
from WP_Scan import _WP_Scan_


def main():
    # 1. Nhập URL mục tiêu
    input_URL = input("Enter URL: ") or "testphp.vulnweb.com"

    # 2. Tạo instance scanner
    scanner = Recon_Directory(
        base_url=input_URL,
        threads=5,
        timeout=5,
        callback=print_result_callback
    )

    # 3. Kiểm tra kết nối
    try:
        if scanner._test_connection():
            print("✅ Kết nối thành công đến target")
        else:
            print("❌ Không thể kết nối đến target")
            return
    except Exception as e:
        print(f"❌ Lỗi kiểm tra kết nối: {e}")
        return

    # 4. Nạp wordlist
    scanner._load_wordlist()
    print(f"📁 Wordlist file: {scanner.wordlist_file}")

    # 5. Kiểm tra một số URL mẫu (tùy chọn)
    test_urls = [
        scanner._normalize_url(input_URL + "/admin"),
        scanner._normalize_url(input_URL + "/login"),
    ]
    for url in test_urls:
        print(f"🔎 Test thử URL: {url}")
        result = scanner._check_url(url)
        if result is not None:
            print_result_callback(result)

    # 6. Quét toàn bộ (full scan)
    print("🚀 Bắt đầu quét toàn bộ...")
    scanner.start_scan()
    scanner.wait_for_completion()  # Đợi quét xong nếu muốn đồng bộ

    # 7. Lưu kết quả
    scanner.save_results("scan_results.txt")
    print("💾 Đã lưu kết quả vào scan_results.txt")

    # 8. In thông tin tổng kết
    print(f"✅ Quét hoàn tất cho: {scanner.base_url}")
    print(f"🧵 Số threads: {scanner.threads}")
    print(f"⏱️  Timeout: {scanner.timeout}s")

if __name__ == "__main__":
    main()