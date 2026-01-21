import asyncio
import datetime
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message

# Thay bằng token của bạn
TOKEN = "8523543324:AAFQ-xFbX6a-k8c7LKImU8ARamRb94dzMxQ"

# Khởi tạo bot và dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()  # Không truyền bot vào đây nữa

@dp.message()  # Bắt mọi tin nhắn (text, photo, video, file, sticker, voice,...)
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
    # Optional: skip pending updates khi khởi động lại bot
    # await bot.delete_webhook(drop_pending_updates=True)
    
    print("Bot đang chạy và theo dõi group...")
    await dp.start_polling(bot, allowed_updates=["message"])  # Chỉ nhận message updates để tối ưu


if __name__ == '__main__':
    # Cấu hình logging (tùy chọn, giúp debug dễ hơn)
    logging.basicConfig(level=logging.INFO)
    
    # Chạy bot
    asyncio.run(main())