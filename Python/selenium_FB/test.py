from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
from dotenv import load_dotenv

# Load thông tin đăng nhập từ biến môi trường
load_dotenv()
EMAIL = os.getenv('FB_EMAIL', 'meomlemkem@gmail.com')
PASSWORD = os.getenv('FB_PASSWORD', 'P@ssw0rd123')

# Đường dẫn đến EdgeDriver và Edge binary
current_dir = os.getcwd()
edgedriver_path = os.path.join(current_dir, "edgedriver_win64", "msedgedriver.exe")
edge_binary_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"

# URL bài viết công khai
POST_URL = "https://www.facebook.com/Theanh28/posts/pfbid0yaZn7Q1BHoAtjfkXvBzW9v79xNJ8phqwjrtXQfKFkymWpiqTwdkS8WGV57TZW74cl"

class FacebookPostViewer:
    def __init__(self, headless=False, wait_time=15):
        self.wait_time = wait_time
        self.driver = None
        self.setup_driver(headless)
        
    def setup_driver(self, headless):
        """Thiết lập Edge driver"""
        edge_options = Options()
        
        if headless:
            edge_options.add_argument("--headless=new")
        else:
            edge_options.add_argument("--start-maximized")
        
        # Các tùy chọn để tránh detection
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option('useAutomationExtension', False)
        edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.95 Safari/537.36 Edg/135.0.0.0")
        
        # Chỉ định đường dẫn đến Edge binary
        edge_options.binary_location = edge_binary_path
        
        # Tắt thông báo lưu mật khẩu
        edge_options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        })
        
        try:
            self.driver = webdriver.Edge(
                service=Service(edgedriver_path),
                options=edge_options
            )
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("Khởi tạo EdgeDriver thành công")
        except Exception as e:
            print(f"Lỗi khi khởi tạo EdgeDriver: {str(e)}")
            raise
        
        self.wait = WebDriverWait(self.driver, self.wait_time)
    
    def login(self):
        """Đăng nhập vào Facebook"""
        try:
            print("Đang truy cập trang đăng nhập Facebook...")
            self.driver.get("https://www.facebook.com/")
            
            print("Đang đợi trường email...")
            email_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='email' or @name='email']")))
            email_field.send_keys(EMAIL)
            print("Đã điền email")
            
            print("Đang đợi trường mật khẩu...")
            pass_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='pass' or @name='pass']")))
            pass_field.send_keys(PASSWORD)
            print("Đã điền mật khẩu")
            
            print("Đang đợi nút đăng nhập...")
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='login' or @data-testid='royal_login_button']")))
            login_button.click()
            print("Đã nhấn nút đăng nhập")
            
            print("Đang đợi trang Facebook tải...")
            self.wait.until(EC.url_contains("facebook.com"))
            print("Đăng nhập thành công")
            
        except Exception as e:
            print(f"Lỗi khi đăng nhập: {str(e)}")
    
    def mouse_wheel_scroll(self, direction="down", times=3):
        """Scroll bằng mouse wheel - mô phỏng thực tế nhất"""
        try:
            # Focus vào giữa màn hình
            window_size = self.driver.get_window_size()
            center_x = window_size['width'] // 2
            center_y = window_size['height'] // 2
            
            actions = ActionChains(self.driver)
            
            # Di chuyển chuột vào giữa màn hình
            actions.move_by_offset(center_x - 100, center_y - 100).perform()
            
            # Reset offset
            actions = ActionChains(self.driver)
            
            for i in range(times):
                if direction == "down":
                    # Scroll xuống bằng mouse wheel
                    self.driver.execute_script("window.scrollBy(0, 300);")
                    # Hoặc thử cách khác
                    actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).perform()
                else:
                    # Scroll lên
                    self.driver.execute_script("window.scrollBy(0, -300);")
                    actions.send_keys(Keys.ARROW_UP).send_keys(Keys.ARROW_UP).send_keys(Keys.ARROW_UP).perform()
                
                print(f"Mouse wheel scroll {direction} lần {i+1}")
                time.sleep(1)
            
            return True
        except Exception as e:
            print(f"Lỗi mouse wheel scroll: {e}")
            return False
    
    def keyboard_navigation_scroll(self):
        """Scroll bằng các phím điều hướng - tự nhiên nhất"""
        try:
            # Click vào body để focus
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.click()
            time.sleep(1)
            
            actions = ActionChains(self.driver)
            
            scroll_keys = [Keys.SPACE, Keys.PAGE_DOWN, Keys.ARROW_DOWN]
            
            for key in scroll_keys:
                print(f"Thử scroll bằng phím: {key}")
                for i in range(3):
                    actions.send_keys(key).perform()
                    time.sleep(1)
                    print(f"  - Lần {i+1}")
                
                # Kiểm tra xem có scroll được không
                current_position = self.driver.execute_script("return window.pageYOffset;")
                print(f"  - Vị trí hiện tại: {current_position}px")
                
                if current_position > 0:
                    print(f"Thành công với phím: {key}")
                    return True
            
            return False
        except Exception as e:
            print(f"Lỗi keyboard navigation: {e}")
            return False
    
    def find_and_focus_content(self):
        """Tìm và focus vào nội dung chính của bài viết"""
        try:
            # Các selector có thể chứa nội dung bài viết
            content_selectors = [
                "[data-pagelet]",
                "[role='main']",
                "[role='article']",
                "div[data-ad-preview]",
                ".x1yztbdb",  # Facebook content wrapper
                ".x1n2onr6.x1ja2u2z",  # Post container
                "div[style*='transform']",  # Modal transform
                ".fb-post",
                "[data-testid]"
            ]
            
            for selector in content_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        element = elements[0]
                        # Focus vào element
                        self.driver.execute_script("arguments[0].focus();", element)
                        self.driver.execute_script("arguments[0].click();", element)
                        print(f"Đã focus vào element: {selector}")
                        time.sleep(2)
                        return element
                except Exception:
                    continue
            
            print("Không tìm thấy element để focus, sử dụng body")
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.click()
            return body
            
        except Exception as e:
            print(f"Lỗi khi focus content: {e}")
            return None
    
    def smart_scroll_detection(self):
        """Phát hiện và scroll thông minh"""
        try:
            print("=== BẮT ĐẦU SMART SCROLL DETECTION ===")
            
            # Lấy thông tin ban đầu
            initial_scroll = self.driver.execute_script("return window.pageYOffset;")
            initial_inner_height = self.driver.execute_script("return window.innerHeight;")
            
            print(f"Vị trí scroll ban đầu: {initial_scroll}px")
            print(f"Chiều cao cửa sổ: {initial_inner_height}px")
            
            # Focus vào nội dung
            content_element = self.find_and_focus_content()
            
            # Thử các phương pháp scroll khác nhau
            methods = [
                ("Keyboard Navigation", self.keyboard_navigation_scroll),
                ("Mouse Wheel Scroll", lambda: self.mouse_wheel_scroll("down", 5)),
                ("Direct Element Scroll", lambda: self.scroll_element_directly(content_element)),
                ("Combination Scroll", self.combination_scroll)
            ]
            
            for method_name, method_func in methods:
                print(f"\n--- Thử phương pháp: {method_name} ---")
                
                before_scroll = self.driver.execute_script("return window.pageYOffset;")
                
                success = method_func()
                
                after_scroll = self.driver.execute_script("return window.pageYOffset;")
                scroll_diff = after_scroll - before_scroll
                
                print(f"Scroll trước: {before_scroll}px")
                print(f"Scroll sau: {after_scroll}px") 
                print(f"Thay đổi: {scroll_diff}px")
                
                if abs(scroll_diff) > 50:  # Có thay đổi đáng kể
                    print(f"✅ THÀNH CÔNG với {method_name}!")
                    return True
                else:
                    print(f"❌ Không hiệu quả với {method_name}")
            
            print("❌ Tất cả phương pháp đều không hiệu quả")
            return False
            
        except Exception as e:
            print(f"Lỗi smart scroll detection: {e}")
            return False
    
    def scroll_element_directly(self, element):
        """Scroll trực tiếp trên element"""
        try:
            if not element:
                return False
            
            # Thử scroll trực tiếp trên element
            self.driver.execute_script("""
                arguments[0].scrollTop += 500;
                arguments[0].scrollLeft = 0;
            """, element)
            
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Lỗi scroll element directly: {e}")
            return False
    
    def combination_scroll(self):
        """Kết hợp nhiều phương pháp scroll"""
        try:
            actions = ActionChains(self.driver)
            
            # 1. Click và focus
            body = self.driver.find_element(By.TAG_NAME, "body")
            actions.move_to_element(body).click().perform()
            time.sleep(1)
            
            # 2. Thử Space nhiều lần
            for i in range(5):
                actions.send_keys(Keys.SPACE).perform()
                time.sleep(0.5)
            
            # 3. Thử Page Down
            for i in range(3):
                actions.send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(0.5)
            
            # 4. Thử mũi tên xuống
            for i in range(10):
                actions.send_keys(Keys.ARROW_DOWN).perform()
                time.sleep(0.2)
            
            return True
        except Exception as e:
            print(f"Lỗi combination scroll: {e}")
            return False
    
    def open_post_and_scroll(self):
        """Mở bài viết và scroll để xem"""
        try:
            print(f"Đang truy cập bài viết: {POST_URL}")
            self.driver.get(POST_URL)
            
            print("Đang đợi bài viết tải...")
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(8)  # Đợi lâu hơn để trang load hoàn toàn
            
            print("Trang đã tải xong. Bắt đầu phân tích và scroll...")
            
            # Chạy smart scroll detection
            success = self.smart_scroll_detection()
            
            if success:
                print("\n🎉 Đã tìm ra cách scroll hiệu quả!")
            else:
                print("\n😞 Không tìm ra cách scroll tự động hiệu quả")
                print("Bạn có thể thử scroll thủ công bằng các phím sau:")
                print("- Space: Scroll xuống")
                print("- Page Down: Scroll xuống nhanh") 
                print("- Mũi tên lên/xuống: Scroll từ từ")
            
            print("\n=== ĐIỀU KHIỂN THỦ CÔNG ===")
            print("s - Space scroll | p - Page Down | d - Arrow Down | u - Arrow Up | q - Thoát")
            
            # Điều khiển thủ công
            actions = ActionChains(self.driver)
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.click()  # Focus
            
            while True:
                user_input = input("Lệnh: ").strip().lower()
                
                if user_input == 'q':
                    break
                elif user_input == 's':
                    actions.send_keys(Keys.SPACE).perform()
                    print("Đã nhấn Space")
                elif user_input == 'p':
                    actions.send_keys(Keys.PAGE_DOWN).perform()
                    print("Đã nhấn Page Down")
                elif user_input == 'd':
                    for i in range(5):
                        actions.send_keys(Keys.ARROW_DOWN).perform()
                    print("Đã nhấn Arrow Down x5")
                elif user_input == 'u':
                    for i in range(5):
                        actions.send_keys(Keys.ARROW_UP).perform()
                    print("Đã nhấn Arrow Up x5")
                else:
                    actions.send_keys(Keys.SPACE).perform()
                    print("Đã nhấn Space (mặc định)")
                
                time.sleep(0.5)
            
        except Exception as e:
            print(f"Lỗi khi mở bài viết: {str(e)}")
    
    def close(self):
        """Đóng trình duyệt"""
        if self.driver:
            try:
                self.driver.quit()
                print("Đã đóng trình duyệt")
            except Exception as e:
                print(f"Lỗi khi đóng trình duyệt: {str(e)}")


if __name__ == "__main__":
    viewer = None
    try:
        viewer = FacebookPostViewer(headless=False)
        viewer.login()
        viewer.open_post_and_scroll()
        
    except Exception as e:
        print(f"Lỗi trong quá trình chạy: {str(e)}")
    finally:
        if viewer:
            viewer.close()