
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
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Khởi tạo trình duyệt
    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=options)
    
    # Mở edge brower và REG 
    driver.get("https://sosovalue.com/join/QRRKH61U")
    time.sleep(2)
    
    # Tìm kiếm Nút Login để bấm
    Login_button = driver.find_element(By.CSS_SELECTOR, ".flex.flex-1.justify-center.h-inherit.items-center.transition-colors.cursor-pointer.text-neutral-fg-4-rest")
    Login_button.click()
    time.sleep(2)
    
    #Tìm Username và password để nhập 
    username = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Enter email'].MuiInputBase-input.MuiOutlinedInput-input")
    username.send_keys(accourt[0])
    username.send_keys(Keys.RETURN)
    
    password = driver.find_element(By.CSS_SELECTOR,"input[placeholder='Enter password'].MuiInputBase-input.MuiOutlinedInput-input")
    password.send_keys(accourt[1])
    password.send_keys(Keys.RETURN)
    time.sleep(2)
    
    submit_login =driver.find_element(By.CSS_SELECTOR,"button[tabindex='0'].MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-colorPrimary.MuiButton-fullWidth.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary")
    submit_login.click()
    time.sleep(2)
    
    #Tìm và Nhập code verify
    Code_verify_input = driver.find_elements(By.CSS_SELECTOR, ".flex-1.flex.items-center.justify-center.h-full.text-neutral-fg-2-rest")
    print(len(Code_verify_input))
    for i in range(0,len(Code_verify_input)):
        Code_verify_input[i].send_keys(Code_verify[i])
        time.sleep(1)
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

