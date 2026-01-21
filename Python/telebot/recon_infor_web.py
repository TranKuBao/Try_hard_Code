import asyncio
import logging
import requests
import datetime
from bs4 import BeautifulSoup
import whois  # Hoặc import pythonwhois nếu dùng cái khác
from urllib.parse import urlparse

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

# Token của bạn
TOKEN = "8523543324:AAFQ-xFbX6a-k8c7LKImU8ARamRb94dzMxQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=["check"]))
async def check_website(message: Message):
    # Lấy URL từ tin nhắn (ví dụ: /check https://example.com)
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Vui lòng cung cấp URL, ví dụ: /check https://example.com")
        return
    
    url = args[1].strip()
    domain = urlparse(url).netloc  # Lấy domain như example.com
    
    try:
        # 1. Lấy owner (whois)
        w = whois.whois(domain)
        owner_info = f"Chủ sở hữu: {w.name or 'Không công khai'}\nEmail: {w.email or 'Không công khai'}\nĐăng ký tại: {w.registrar or 'N/A'}"
        
        # 2. Lấy nội dung chính (scrape HTML)
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'N/A'
        description = soup.find('meta', attrs={'name': 'description'})
        desc_text = description['content'] if description else 'Không tìm thấy meta description'
        main_content = ' '.join([p.text for p in soup.find_all('p')][:5])  # Lấy 5 đoạn đầu làm tóm tắt
        content_info = f"Tiêu đề: {title}\nMô tả: {desc_text}\nNội dung chính (tóm tắt): {main_content[:500]}..."  # Giới hạn độ dài
        
        # 3. Lấy engine/web tech (check headers và source)
        server = response.headers.get('Server', 'N/A')
        powered_by = response.headers.get('X-Powered-By', 'N/A')
        # Check CMS phổ biến qua source
        cms = 'N/A'
        if 'wordpress' in response.text.lower():
            cms = 'WordPress'
        elif 'shopify' in response.text.lower():
            cms = 'Shopify'
        # Có thể dùng API BuiltWith miễn phí (nhưng cần key): requests.get(f"https://api.builtwith.com/v19/api.json?KEY=your_key&LOOKUP={domain}")
        engine_info = f"Server: {server}\nPowered by: {powered_by}\nCMS/Engine ước đoán: {cms}"
        
        # 4. Thu thập từ group Telegram (nếu bot đang ở group)
        # Giả sử bot lắng nghe tất cả tin nhắn chứa URL (từ code cũ của bạn)
        # Bạn có thể lưu log và search trong file "group_log.txt" cho mention về URL
        group_mentions = "Chưa có mention từ group (cần tích hợp search log)."
        # Ví dụ code search: with open("group_log.txt", "r") as f: ... tìm dòng chứa url
        
        # 5. Thu thập từ mạng xã hội (ví dụ X/Twitter)
        # Dùng web_search hoặc API (ở đây dùng requests scrape đơn giản, nhưng tốt hơn dùng Tweepy)
        twitter_search = f"https://twitter.com/search?q={domain}"
        # Hoặc dùng API: nhưng cần auth. Kết quả giả định: mentions = "Tìm thấy X posts đề cập domain này."
        social_info = f"Trên X/Twitter: Kiểm tra {twitter_search} để xem mentions.\nTrên Reddit: Tìm subreddit liên quan đến {domain}."
        
        # Tổng hợp và reply
        result = f"Thông tin về {url}:\n\n{owner_info}\n\n{content_info}\n\n{engine_info}\n\nTừ group Tele: {group_mentions}\n\nTừ MXH: {social_info}"
        await message.reply(result)
        
    except Exception as e:
        await message.reply(f"Lỗi khi thu thập: {str(e)}")

# Handler cũ của bạn (log all messages) giữ nguyên nếu cần
@dp.message()
async def handle_all_messages(message: Message):
    user = message.from_user
    username = user.username if user.username else "Không có"
    full_name = user.full_name
    chat_title = message.chat.title if message.chat.title else "Private chat"
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # In ra console
    print(f"[{time}] Group: {chat_title}")
    print(f"   Từ: {full_name} (@{username}) - ID: {user.id}")
    
    if message.text:
        print(f"   Nội dung: {message.text}")
    elif message.photo:
        print(f"   Gửi ảnh (caption: {message.caption or 'Không có'})")
    elif message.document:
        print(f"   Gửi file: {message.document.file_name}")
    elif message.video:
        print("   Gửi video")
    else:
        print(f"   Loại tin nhắn khác: {message.content_type}")
    
    print("-" * 50)

    # Nếu muốn lưu vào file
    with open("group_log.txt", "a", encoding="utf-8") as f:
        content = message.text or f"[Media: {message.content_type}]"
        f.write(f"[{time}] {chat_title} | {full_name} (@{username}): {content}\n")

async def main():
    print("Bot đang chạy và sẵn sàng check web...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())