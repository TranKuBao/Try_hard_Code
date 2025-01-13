
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


# Lấy đường dẫn thư mục hiện tại
driver_path = os.path.join(os.getcwd(),"edgedriver_win64","msedgedriver.exe")
print("[+] Đường dẫn của Drive's Browser: ", driver_path)

# Đường dẫn tới Microsoft Edge binary (có thể cần thay đổi tùy vào vị trí cài đặt của bạn)
edge_binary_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"  # Đảm bảo đúng đường dẫn tới Edge
Email_Login="conchimnon@gmail.com"
Code_verify="111111"
API_KEY = 'f013c816cc19efd97c03837d346429cb' # api key cur proxy

def parse_proxy(proxy_line):
    """
    Parses a proxy line in the format 'username:password@host:port' and returns a dictionary with its components.
    """
    try:
        # Remove any leading/trailing whitespace and split the line into user credentials and proxy address
        user_pass, proxy_address = proxy_line.strip().split('@')
        # Split the user credentials into username and password
        username, password = user_pass.split(':')
        # Split the proxy address into host and port
        host, port = proxy_address.split(':')
        # Return a dictionary containing the parsed proxy information
        return {
            'username': username,
            'password': password,
            'host': host,
            'port': port
        }
    except ValueError:
        # If the proxy line is not in the expected format, print an error message
        print(f"proxy format error：{proxy_line}")
        return None  # Return None to indicate parsing failure

def rotate_proxy():
    '''Chuyển đổi Proxy'''
    api = "https://tmproxy.com/api/proxy/get-new-proxy"
    res = requests.post(api,headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'api_key':f'{API_KEY}'})
    proxy_data = res.json()
    pattern = r"retry after (\d+) second\(s\)"
    if proxy_data['code'] != 0:
        time.sleep(re.search(pattern, proxy_data['message']).group(1))
        rotate_proxy()
    print(f"Đã đổi proxy: {proxy_data['data']['https']}")
    print(f"New User&Pass: '{proxy_data['data']['username']}:{proxy_data['data']['password']}' ")
    # proxies={
    #         'username': proxy_data['data']['username'],
    #         'password': proxy_data['data']['password'],
    #         'https': proxy_data['data']['https'],
    #         'socks5': proxy_data['data']['socks5']
    #     } 
    return f"{proxy_data['data']['username']}:{proxy_data['data']['password']}@{proxy_data['data']['https']}"

def get_current_proxy():
    '''Lấy proxy hiện tại'''
    # có thể curl để test với cái này       https://api.ipify.org?format=json
    api = 'https://tmproxy.com/api/proxy/get-current-proxy'
    res = requests.post(api, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'api_key':f'{API_KEY}'})
    proxy_data = res.json()
    if proxy_data['data']['https'] == '':
        proxy = rotate_proxy()
        print(f"Proxy đang sử dụng: {proxy}")
        return proxy
    else:
        print(f"Proxy đang sử dụng: {proxy_data['data']['https']}")        
        print(f"New User&Pass: {proxy_data['data']['username']}:{proxy_data['data']['password']} ")
        # proxy={
        #     'username': proxy_data['data']['username'],
        #     'password': proxy_data['data']['password'],
        #     'https': proxy_data['data']['https'],
        #     'socks5': proxy_data['data']['socks5']
        # } 
        return f"{proxy_data['data']['username']}:{proxy_data['data']['password']}@{proxy_data['data']['https']}"
    
def create_background_js(proxy_info):
    """
    Creates a background.js file for a Chrome extension to configure proxy settings with authentication.
    """
    # Define the content of the background.js file with the proxy configuration
    background_js_content = f"""
var config = {{
    mode: "fixed_servers",
    rules: {{
      singleProxy: {{
        scheme: "http",
        host: "{proxy_info['host']}",
        port: parseInt("{proxy_info['port']}")
      }},
      bypassList: ["localhost"]
    }}
}};

chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

function callbackFn(details) {{
    return {{
        authCredentials: {{
            username: "{proxy_info['username']}",
            password: "{proxy_info['password']}"
        }}
    }};
}}

chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {{urls: ["<all_urls>"]}},
    ['blocking']
);
    """

    extension_dir = 'proxy_auth_extension'  # Define the directory name for the extension
    if not os.path.exists(extension_dir):
        os.makedirs(extension_dir)  # Create the extension directory if it doesn't exist

    # Define the content of the manifest.json file for the Chrome extension
    manifest_content = '''
{
  "version": "1.0.0",
  "manifest_version": 2,
  "name": "Auto Proxy Auth",
  "permissions": [
    "proxy",
    "tabs",
    "unlimitedStorage",
    "storage",
    "<all_urls>",
    "webRequest",
    "webRequestBlocking"
  ],
  "background": {
    "scripts": ["background.js"]
  }
}
    '''
    # Define the path for the manifest.json file
    manifest_path = os.path.join(extension_dir, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(manifest_content)  # Write the manifest content to the file

    # Define the path for the background.js file
    background_js_path = os.path.join(extension_dir, 'background.js')
    with open(background_js_path, 'w', encoding='utf-8') as f:
        f.write(background_js_content)  # Write the background.js content to the file

    # Print a message indicating that the files have been generated
    print(f"{background_js_path} and {manifest_path} have been generated")
   

try:
    options = Options()
    options.binary_location = edge_binary_path  # Chỉ định đường dẫn đến Edge binary      
    options.add_argument("--incognito")  # Chế độ ẩn danh
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    #options.add_argument("--headless") #không hiển thị trình duyệt
    
    #proxy => tạo extenxion để play nó
    #chọn proxy
    available_proxy = parse_proxy(get_current_proxy()) # lấy proxy hiện tại => phân tích thành list(user:pass:host:pass)
    print(f"[+] Proxy được chọn：{available_proxy}") 
    create_background_js(available_proxy) # tạo extension
    extension_path = os.path.abspath('proxy_auth_extension')  # Get the absolute path to the extension directory
    print(f"[+] Đường dẫn tuyệt đối của extension：{extension_path}")  # Print the extension path
    
    #config Proxy
    options.use_chromium = True  # Specify that Edge should use the Chromium engine
    options.add_argument('--disable-extensions-except=' + extension_path)
    options.add_argument('--load-extension=' + extension_path)
    
    # Khởi tạo trình duyệt
    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=options)
    
    # Mở edge brower và REG 
    driver.get("https://bless.network/dashboard/login")
    time.sleep(15)
    
    # Tìm hộp tìm kiếm và nhập từ khóa
    search_box = driver.find_element(By.ID, "email")
    search_box.send_keys("Conchimnon@gmail.com")
    search_box.send_keys(Keys.RETURN)

    # lấy ID của cửa sổ hiện tại
    main_hander = driver.current_window_handle    
    time.sleep(3)
    
    # Nhận Enter để đăng nhập
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].inline-flex")
    login_button.click()
    time.sleep(3)
    
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
    print("Kết thúc")