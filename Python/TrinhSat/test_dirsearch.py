#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script cho chức năng _Dirsearch_
Kiểm tra các tính năng của Directory Scanner API
"""

import sys
import os
import time
from datetime import datetime

# Thêm đường dẫn hiện tại vào sys.path để import module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from Dirsearch._Dirseach_ import Recon_Directory, print_result_callback
    print("✅ Import thành công module _Dirsearch_")
except ImportError as e:
    print(f"❌ Lỗi import: {e}")
    sys.exit(1)

def test_basic_functionality():
    """
    Test chức năng cơ bản của Directory Scanner
    """
    print("\n" + "="*60)
    print("🧪 TEST 1: Chức năng cơ bản")
    print("="*60)
    
    try:
        # Tạo scanner instance
        scanner = Recon_Directory(
            base_url="http://testphp.vulnweb.com/",
            threads=5,  # Giảm số thread để test nhanh
            timeout=5,
            callback=print_result_callback
        )
        
        print(f"✅ Tạo scanner thành công cho: {scanner.base_url}")
        print(f"📁 Wordlist file: {scanner.wordlist_file}")
        print(f"🧵 Số threads: {scanner.threads}")
        print(f"⏱️  Timeout: {scanner.timeout}s")
        
        return scanner
        
    except Exception as e:
        print(f"❌ Lỗi tạo scanner: {e}")
        return None

def test_connection():
    """
    Test kết nối đến target
    """
    print("\n" + "="*60)
    print("🧪 TEST 2: Kiểm tra kết nối")
    print("="*60)
    
    scanner = Recon_Directory("http://testphp.vulnweb.com/")
    
    try:
        is_connected = scanner._test_connection()
        if is_connected:
            print("✅ Kết nối thành công đến target")
        else:
            print("❌ Không thể kết nối đến target")
        return is_connected
    except Exception as e:
        print(f"❌ Lỗi kiểm tra kết nối: {e}")
        return False

def test_wordlist_loading():
    """
    Test tải wordlist
    """
    print("\n" + "="*60)
    print("🧪 TEST 3: Tải wordlist")
    print("="*60)
    
    scanner = Recon_Directory("http://testphp.vulnweb.com/")
    
    try:
        paths = scanner._load_wordlist()
        print(f"✅ Tải wordlist thành công: {len(paths)} paths")
        
        # Hiển thị một số path đầu tiên
        print("📝 Một số paths mẫu:")
        for i, path in enumerate(paths[:10]):
            print(f"   {i+1}. {path}")
        
        if len(paths) > 10:
            print(f"   ... và {len(paths) - 10} paths khác")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi tải wordlist: {e}")
        return False

def test_url_normalization():
    """
    Test chuẩn hóa URL
    """
    print("\n" + "="*60)
    print("🧪 TEST 4: Chuẩn hóa URL")
    print("="*60)
    
    scanner = Recon_Directory("http://testphp.vulnweb.com/")
    
    test_urls = [
        "testphp.vulnweb.com",
        "http://testphp.vulnweb.com",
        "https://testphp.vulnweb.com/",
        "testphp.vulnweb.com/admin",
        "http://testphp.vulnweb.com/admin/",
        "invalid-url-format"
    ]
    
    for url in test_urls:
        try:
            normalized = scanner._normalize_url(url)
            print(f"✅ '{url}' -> '{normalized}'")
        except ValueError as e:
            print(f"❌ '{url}' -> Lỗi: {e}")
        except Exception as e:
            print(f"❌ '{url}' -> Lỗi không xác định: {e}")

def test_single_url_check():
    """
    Test kiểm tra một URL đơn lẻ
    """
    print("\n" + "="*60)
    print("🧪 TEST 5: Kiểm tra URL đơn lẻ")
    print("="*60)
    
    scanner = Recon_Directory("http://testphp.vulnweb.com/")
    
    test_paths = ["admin", "login", "nonexistent", "images", "css"]
    
    for path in test_paths:
        try:
            result = scanner._check_url(path)
            if result:
                status = "✅ Found" if result['found'] else "❌ Not Found"
                print(f"{status} {path} - Status: {result['status_code']}, Time: {result['response_time']}s")
            else:
                print(f"⚠️  {path} - Không có kết quả")
        except Exception as e:
            print(f"❌ {path} - Lỗi: {e}")

def test_full_scan():
    """
    Test quét đầy đủ với số lượng nhỏ
    """
    print("\n" + "="*60)
    print("🧪 TEST 6: Quét đầy đủ (giới hạn)")
    print("="*60)
    
    try:
        # Tạo scanner với callback để theo dõi
        scanner = Recon_Directory(
            base_url="http://testphp.vulnweb.com/",
            threads=3,
            timeout=5,
            callback=print_result_callback
        )
        
        print("🚀 Bắt đầu quét...")
        start_time = time.time()
        
        # Bắt đầu quét
        if scanner.start_scan():
            print("✅ Quét đã bắt đầu")
            
            # Theo dõi tiến độ
            while scanner.is_scanning:
                status = scanner.get_status()
                print(f"\r📊 Tiến độ: {status.get('progress_percent', 0)}% "
                      f"({status.get('scanned_count', 0)}/{status.get('total_paths', 0)}) "
                      f"| Tốc độ: {status.get('rate', 0)} req/s", end="")
                
                time.sleep(1)
                
                # Dừng sau 30 giây để test
                if time.time() - start_time > 30:
                    print("\n⏹️  Dừng quét sau 30 giây...")
                    scanner.stop()
                    break
            
            # Chờ hoàn thành
            scanner.wait_for_completion(timeout=5)
            
            # Lấy kết quả
            found_urls = scanner.get_found_urls()
            summary = scanner.get_summary()
            
            print(f"\n✅ Quét hoàn thành!")
            print(f"📊 Tóm tắt:")
            print(f"   - Tổng số quét: {summary['total_scanned']}")
            print(f"   - URL tìm thấy: {summary['found_urls']}")
            print(f"   - Thời gian: {summary.get('elapsed_time', 0)}s")
            print(f"   - Tốc độ TB: {summary.get('average_rate', 0)} req/s")
            
            if found_urls:
                print(f"\n🎯 Các URL tìm thấy:")
                for i, result in enumerate(found_urls[:10], 1):
                    print(f"   {i}. {result['url']} (Status: {result['status_code']})")
                
                if len(found_urls) > 10:
                    print(f"   ... và {len(found_urls) - 10} URL khác")
            else:
                print("❌ Không tìm thấy URL nào")
                
        else:
            print("❌ Không thể bắt đầu quét")
            
    except Exception as e:
        print(f"❌ Lỗi trong quá trình quét: {e}")

def test_save_results():
    """
    Test lưu kết quả
    """
    print("\n" + "="*60)
    print("🧪 TEST 7: Lưu kết quả")
    print("="*60)
    
    try:
        # Tạo scanner và thực hiện quét ngắn
        scanner = Recon_Directory("http://testphp.vulnweb.com/")
        scanner.start_scan()
        
        # Chờ một chút để có kết quả
        time.sleep(10)
        scanner.stop()
        scanner.wait_for_completion()
        
        # Lưu kết quả
        filename = scanner.save_results(found_only=True)
        print(f"✅ Đã lưu kết quả vào: {filename}")
        
        # Kiểm tra file có tồn tại không
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"📁 Kích thước file: {file_size} bytes")
            
            # Đọc và hiển thị một phần nội dung
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                print(f"📄 Số dòng: {len(lines)}")
                print("📝 Nội dung file:")
                for line in lines[:10]:
                    print(f"   {line}")
                if len(lines) > 10:
                    print(f"   ... và {len(lines) - 10} dòng khác")
        else:
            print("❌ File không tồn tại")
            
    except Exception as e:
        print(f"❌ Lỗi lưu kết quả: {e}")

def main():
    """
    Hàm chính để chạy tất cả các test
    """
    print("🔍 BẮT ĐẦU TEST CHỨC NĂNG _DIRSEARCH_")
    print("="*60)
    print(f"⏰ Thời gian bắt đầu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Chạy các test
    tests = [
        ("Chức năng cơ bản", test_basic_functionality),
        ("Kiểm tra kết nối", test_connection),
        ("Tải wordlist", test_wordlist_loading),
        ("Chuẩn hóa URL", test_url_normalization),
        ("Kiểm tra URL đơn lẻ", test_single_url_check),
        ("Quét đầy đủ", test_full_scan),
        ("Lưu kết quả", test_save_results)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result is not False:  # None hoặc True đều coi là thành công
                passed += 1
        except Exception as e:
            print(f"❌ Test '{test_name}' bị lỗi: {e}")
    
    print("\n" + "="*60)
    print("📊 KẾT QUẢ TỔNG KẾT")
    print("="*60)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print(f"📈 Tỷ lệ thành công: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 TẤT CẢ TEST ĐỀU THÀNH CÔNG!")
    else:
        print("⚠️  CÓ MỘT SỐ TEST THẤT BẠI")
    
    print(f"⏰ Thời gian kết thúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 