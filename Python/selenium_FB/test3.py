from bs4 import BeautifulSoup


with open("comments.html", "r", encoding="utf-8") as f:
    page_craw = f.read()
    
soup = BeautifulSoup(page_craw,"html.parser")

# Tìm tất cả các thẻ span có đầy đủ class như bạn chỉ định
# target_class = "xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk"
## Dùng CSS selector để tìm chính xác chuỗi class
# spans = soup.select(f'span[class="{target_class}"]')[1]
# sumlike = spans.get_text(strip=True)
# print(f"{sumlike}")



# # Like Love Care Haha Wow Sad Angry  
# Class của span chứa các div
span_class = "x12myldv x1udsgas xrc8dwe xxxhv2y x1rg5ohu xmix8c7 x1xp8n7a"
target_div_class = "x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1lku1pv x1a2a7pz"
span_tags = soup.find_all("span", class_=span_class)
for span in span_tags:
    divs = span.find_all("div", class_=target_div_class)
    for div in divs:
        if 'aria-label' in div.attrs:
            print(div['aria-label'])
# capture = False
# results = []

# for div in soup.select(f'div[class="{target_class}"]'):
#     aria_label = div.get("aria-label", "")
    
#     if aria_label.startswith("Send this to friends or post it on your profile"):
#         capture = True  # Bắt đầu lấy từ đây

#     if capture and aria_label:
#         results.append(aria_label)

#     if aria_label.startswith("Leave a comment"):
#         break  # Dừng tại đây
# results =results[1:-1]
# for label in results:
#     print( label)





# target_class = "html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs xkrqix3 x1sur9pj"
# #Dùng CSS selector để tìm chính xác chuỗi class
# spans = soup.select(f'span[class="{target_class}"]')
# spans = spans[-3:-1]
# #print(spans)
# for span in spans:
#     k = span.get_text(strip=True)    
#     text = k.replace(" ", "")
#     text = text.replace("\n", " ")
#     print(text)
    