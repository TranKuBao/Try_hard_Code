
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options 
from selenium.webdriver.common.proxy import Proxy, ProxyType
import os
import time
import requests
import re
import random

# Lấy đường dẫn thư mục hiện tại
driver_path = os.path.join(os.getcwd(),"edgedriver_win64","msedgedriver.exe")
print("[+] Đường dẫn của Drive's Browser: ", driver_path)

# Đường dẫn tới Microsoft Edge binary (có thể cần thay đổi tùy vào vị trí cài đặt của bạn)
edge_binary_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"  # Đảm bảo đúng đường dẫn tới Edge

accourt = ['kubaoprozxc999@gmail.com','Baoprozxc999@']
Code_verify="133737"

try:
    options = Options()
    options.binary_location = edge_binary_path  # Chỉ định đường dẫn đến Edge binary      
    options.add_argument("--incognito")  # Chế độ ẩn danh
    options.add_argument("user-agent=Mozilla/5.0 (Googlebot/2.1)")
    
    # Khởi tạo trình duyệt
    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=options)
    
    # Mở edge brower và REG 
    driver.get("http://103.97.125.56:31507")
    time.sleep(2)
    # search_box = driver.find_element(By.ID, "email")
    # search_box.send_keys("Conchimnon@gmail.com")
    # search_box.send_keys(Keys.RETURN)

    # # lấy ID của cửa sổ hiện tại
    # main_hander = driver.current_window_handle    
    # time.sleep(3)
    
    # # Nhận Enter để đăng nhập
    # login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].inline-flex")
    # login_button.click()
    time.sleep(15)
    
except Exception as e:
    print(f"[+] Xảy ra lỗi {e}")
finally:
    # Đóng trình duyệt
    driver.quit()
    print("Trình duyệt đã đóng")

