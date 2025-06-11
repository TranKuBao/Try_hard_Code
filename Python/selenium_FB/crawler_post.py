from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import json
from datetime import datetime, timezone
import time
import os
from dotenv import load_dotenv
# https://msedgedriver.azureedge.net/136.0.3240.76/edgedriver_win64.zip


# Đường dẫn đến EdgeDriver và Edge binary
current_dir = os.getcwd()
edgedriver_path = os.path.join(current_dir, "edgedriver_win64", "msedgedriver.exe")
edge_binary_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"  # Thay bằng đường dẫn thực tế nếu chạy trên Linux
print("Đường dẫn EdgeDriver: ", edgedriver_path)
print("Đường dẫn Edge Binary: ", edge_binary_path)



class FacebookPostCrawler:
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
        """Đăng nhập vào Facebook và mở bài viết"""
        try:
            print("Đang truy cập trang đăng nhập Facebook...")
            self.driver.get("https://www.facebook.com/")
            time.sleep(2)
            
            print("Đang đợi trường email...")
            email_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='email' or @name='email']")))
            email_field.send_keys(EMAIL)
            print("Đã điền email")
            time.sleep(0.9)
            
            print("Đang đợi trường mật khẩu...")
            pass_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='pass' or @name='pass']")))
            pass_field.send_keys(PASSWORD)
            print("Đã điền mật khẩu")
            time.sleep(2)
            
            print("Đang đợi nút đăng nhập...")
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='login' or @data-testid='royal_login_button']")))
            login_button.click()
            print("Đã nhấn nút đăng nhập")
            time.sleep(15)
            
            print("Đang đợi trang Facebook tải...")
            self.wait.until(EC.url_contains("facebook.com"))
            print("Đăng nhập thành công")
            
            
        except TimeoutException as e:
            print(f"Hết thời gian chờ: {str(e)}")
            print("Kiểm tra kết nối mạng hoặc xem liệu trang Facebook có tải đúng không.")
        except NoSuchElementException as e:
            print(f"Không tìm thấy phần tử: {str(e)}")
            print("Kiểm tra xem giao diện Facebook có thay đổi hoặc tài khoản có bị chặn.")
        except Exception as e:
            print(f"Lỗi không xác định: {str(e)}")
    
    def parse_number(self,text):
        import re
        if not isinstance(text, str):
            return 0
        text = text.lower().replace(",", "").strip()
        match = re.search(r"([\d\.]+)\s*([km]?)", text)
        if not match:
            return 0
        number, unit = match.groups()
        try:
            number = float(number)
            if unit == "k":
                return int(number * 1000)
            elif unit == "m":
                return int(number * 1_000_000)
            else:
                return int(number)
        except ValueError:
            return 0


    
    def crawler1(self,url_crawn):
        """Thu thập dữ liệu: tổng số phản ứng, tổng số comment, và tất cả comment"""
        try:      
            
            print(f"Đang truy cập bài viết: {url_crawn}")
            self.driver.get(url_crawn)
            time.sleep(3)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print(f"Đã mở bài viết: {url_crawn}")
           
            # Lấy kích thước cửa sổ trình duyệt để tính tọa độ tâm màn hình
            print("Đang lấy kích thước cửa sổ trình duyệt...")
            window_size = self.driver.get_window_size()
            center_x = window_size['width'] // 2
            center_y = window_size['height'] // 2
            print(f"Đang kích chuột trái tại giữa màn hình ({center_x}, {center_y})...")
            actions = ActionChains(self.driver)
            actions.move_by_offset(center_x, center_y).click().perform()
            
            # Lấy HTML của trang
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            #Tổng số like+ tim ....
            print("[+] Đang tìm thẻ <span> với tổng số tương tác cảm xúc .....")
            target_class = "xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk"
            spans = soup.select(f'span[class="{target_class}"]')[0]    
            sumlike = spans.get_text(strip=True)        
            print(f"[*] Tổng cảm xúc: {sumlike}")
            
            
            # Like Love Care Haha Wow Sad Angry  
            motivations = []
            print("[+] Đang tìm các cảm xúc có tỉ lệ cao.....")
            span_class = "x12myldv x1udsgas xrc8dwe xxxhv2y x1rg5ohu xmix8c7 x1xp8n7a"
            target_div_class = "x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1lku1pv x1a2a7pz"
            span_tags = soup.find_all("span", class_=span_class)
            for span in span_tags:
                divs = span.find_all("div", class_=target_div_class)
                for div in divs:
                    if 'aria-label' in div.attrs:
                        motivations.append(div['aria-label'])
                        #print(div['aria-label'])
            motivations = motivations
            print(motivations)
            
            print("[+] Đang tìm tổng số lượt chia sẽ và comments")
            share_comment=[]
            target_class = "html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs xkrqix3 x1sur9pj"
            spans = soup.select(f'span[class="{target_class}"]')
            spans = spans[-2:]            
            for span in spans:
                k = span.get_text(strip=True) 
                share_comment.append(k)
            print(share_comment)
            
                        
            with open("comments.html", "w", encoding="utf-8") as f:
                f.write(str(soup))  # Ghi toàn bộ HTML vào file

            # 1. Tạo timestamp ISO 8601 ở múi giờ UTC
            timestamp = datetime(2025, 5, 23, 13, 0, 0, tzinfo=timezone.utc)
            # 2. Tạo created_at là thời điểm hiện tại
            created_at = datetime.now().isoformat()
            # 3. Hiển thị chỉ giờ:phút từ timestamp
            time_display = timestamp.strftime('%H:%M')
            
            
            total_reactions = self.parse_number(sumlike)
            total_comments = self.parse_number(share_comment[0])
            total_shares = self.parse_number(share_comment[1])
                        
            reaction_dict = {}
            for reaction in motivations:
                if ":" in reaction:
                    key, value = reaction.split(":", 1)
                    reaction_dict[key.strip()] = self.parse_number(value)
            
            post_data = {
                "post_url": POST_URL,
                "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
                "time_display": time_display,                
                "total_reactions": total_reactions,
                "total_comments": total_comments,
                "total_shares": total_shares,
                "reactions": reaction_dict
            }
            
            # Lưu vào file JSON
            with open('post_data.json', 'w', encoding='utf-8') as f:
                json.dump(post_data, f, ensure_ascii=False, indent=5)
            print("Dữ liệu đã được lưu vào post_data.json")
            
        except Exception as e:
            print(f"Lỗi khi thu thập dữ liệu: {str(e)}")
            return None
    
    def close(self):
        """Đóng trình duyệt"""
        if self.driver:
            try:
                self.driver.quit()
                print("Đã đóng trình duyệt")
            except Exception as e:
                print(f"Lỗi khi đóng trình duyệt: {str(e)}")
        else:
            print("Không có trình duyệt để đóng")



INTERVAL_SECONDS = 1 * 60  # 10 phút   
# URL bài viết công khai
#POST_URL = "https://www.facebook.com/Theanh28/posts/pfbid0yaZn7Q1BHoAtjfkXvBzW9v79xNJ8phqwjrtXQfKFkymWpiqTwdkS8WGV57TZW74cl"
#POST_URL = "https://www.facebook.com/share/v/12KWgRbX31A/" thì không được
POST_URL = "https://www.facebook.com/Theanh28/posts/pfbid0q2eEo5kbZewaMhVxJUHFvZFw8SeNzaTTiBsHogG28vAUBSsdDXr4CY48gNbxTZ7Al?rdid=CLRzGPVu0oWytvYh"
# Chuẩn URL của bài post ;là https://www.facebook.com/{USERNAME}/posts/{Hash_PID}
# Load thông tin đăng nhập từ biến môi trường
load_dotenv()
EMAIL = os.getenv('FB_EMAIL', 'meomlemkem@gmail.com')
PASSWORD = os.getenv('FB_PASSWORD', 'P@ssw0rd123')
        
if __name__ == "__main__":
    crawler = None
    try:
        while True:
            try:
                crawler = FacebookPostCrawler(headless=False)
                #crawler.login()
                
                now = datetime.now(timezone.utc).isoformat()
                print(f"[{now}] Đang crawl: {POST_URL}")
                
                crawler.crawler1(url_crawn=POST_URL)
                
                print(f"Chờ {INTERVAL_SECONDS} giây trước lần quét tiếp theo...\n")
                time.sleep(INTERVAL_SECONDS)

            except Exception as crawl_error:
                print(f"Lỗi khi crawl: {str(crawl_error)}")
                # Bạn có thể chọn sleep ngắn lại để thử lại nếu cần
                time.sleep(5)

    except Exception as e:
        print(f"Lỗi khởi tạo crawler: {str(e)}")
    finally:
        if crawler:
            crawler.close()            