
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
import os
import time
import bs4 

# Lấy đường dẫn thư mục hiện tại
current_dir = os.getcwd()
driver_path = os.path.join(current_dir,"edgedriver_win64","msedgedriver.exe")
print("Đường dẫn của Drive's Browser: ", driver_path)

# Đường dẫn tới Microsoft Edge binary (có thể cần thay đổi tùy vào vị trí cài đặt của bạn)
edge_binary_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"  # Đảm bảo đúng đường dẫn tới Edge
Email_Login="conchimnon@gmail.com"
Code_verify="111111"
try:
    options = Options()
    options.binary_location = edge_binary_path  # Chỉ định đường dẫn đến Edge binary
    # proxy_server_url = "http://tmproxyxhOvL:JIEI800EwL@14.184.55.108:24483"
    # options.add_argument(f'--proxy-server={proxy_server_url}')
    
    
    # Khởi tạo trình duyệt
    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=options)
    
    # Mở edge brower
    driver.get("https://bless.network/dashboard/login")
        
    # Tìm hộp tìm kiếm và nhập từ khóa
    search_box = driver.find_element(By.ID, "email")
    search_box.send_keys("Conchimnon@gmail.com")
    search_box.send_keys(Keys.RETURN)

    # lấy ID của cửa sổ hiện tạic
    main_hander = driver.current_window_handle
    
    # Đợi một chút để trang tải
    time.sleep(3)
    
    # Nhận Enter để đăng nhập
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].inline-flex")
    login_button.click()
    time.sleep(10)
    
    #vaò cửa sổ phụ để input code number
    for window in driver.window_handles:
        if window != main_hander:
            
            #chuyển handler
            driver.switch_to.window(window)
            
            input_code = driver.find_elements(By.XPATH,"//input[@autocomplete='one-time-code']")
            print("số phân tử: ", len(input_code))
            for i in range(0,len(input_code)):
                input_code[i].send_keys(Code_verify[i])
                
        time.sleep(10)        
        
except Exception as e:
    print("Lỗi:", str(e))
finally:
    # Đóng trình duyệt
    driver.quit()
