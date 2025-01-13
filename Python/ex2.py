import requests
import time
import re

API_KEY = 'f013c816cc19efd97c03837d346429cb'

def rotate_proxy():
    api = "https://tmproxy.com/api/proxy/get-new-proxy"
    res = requests.post(api,headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'api_key':f'{API_KEY}'})
    proxy_data = res.json()
    pattern = r"retry after (\d+) second\(s\)"
    if proxy_data['code'] != 0:
        time.sleep(re.search(pattern, proxy_data['message']).group(1))
        rotate_proxy()
    print(f"Đã đổi proxy https: {proxy_data['data']['https']}")
    print(f"New User&Pass: '{proxy_data['data']['username']}:{proxy_data['data']['password']}' ")
    return f"http://{proxy_data['data']['username']}:{proxy_data['data']['password']}@{proxy_data['data']['https']}"

def get_current_proxy():
    api = 'https://tmproxy.com/api/proxy/get-current-proxy'
    res = requests.post(api, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, json={'api_key':f'{API_KEY}'})
    proxy_data = res.json()
    if proxy_data['data']['https'] == '':
        proxy = rotate_proxy()
        print(f"Proxy đang sử dụng: {proxy}")
        return proxy
    else:
        print(f"Proxy đang sử dụng https: {proxy_data['data']['https']}")        
        print(f"New User&Pass: {proxy_data['data']['username']}:{proxy_data['data']['password']} ")
        return f"http://{proxy_data['data']['username']}:{proxy_data['data']['password']}@{proxy_data['data']['https']}"
    
    
print("tiến hành với: ", get_current_proxy())
#test_url='https://api.ipify.org?format=json',

