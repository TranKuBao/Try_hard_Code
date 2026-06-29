import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# 1. Cấu hình các bộ lọc dành riêng cho nhà báo
KHU_VUC = ["Đà Nẵng", "Quảng Nam", "Quảng Ngãi", "Bình Định", "Phú Yên", "Khánh Hòa", "Ninh Thuận", "Bình Thuận", "Kon Tum", "Gia Lai", "Đắk Lắk", "Đắk Nông", "Lâm Đồng", "Tây Nguyên", "Nam Trung Bộ"]
CHU_DE = ["kinh tế", "doanh nghiệp", "đầu tư", "khoa học", "công nghệ", "nghiên cứu", "chuyển đổi số", "khởi nghiệp", "GDP", "quy hoạch"]

def kiem_tra_noi_dung(title):
    title_lower = title.lower()
    # Kiểm tra xem tiêu đề có chứa từ khóa khu vực và chủ đề không
    co_khu_vuc = any(kv.lower() in title_lower for kv in KHU_VUC)
    co_chu_de = any(cd.lower() in title_lower for cd in CHU_DE)
    return co_khu_vuc and co_chu_de

def quet_tin_tuc_vung():
    # Sử dụng trang tin tức tổng hợp/kinh tế của Báo Chính Phủ làm mẫu
    url = "https://baochinhphu.vn/kinh-te.htm" 
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    print("🔄 Đang kết nối và thu thập dữ liệu từ nguồn...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Không thể truy cập website. Mã lỗi: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    tin_tuc_list = []

    # Tìm các khối bài viết (Cấu hình theo cấu trúc HTML của Báo Chính Phủ)
    cac_bai_viet = soup.find_all(['div', 'article'], class_=['story', 'zone-timeline-item', 'timeline-item'])

    for index, bai in enumerate(cac_bai_viet):
        title_tag = bai.find(['a', 'h2', 'h3'])
        if title_tag and title_tag.text:
            tieu_de = title_tag.text.strip()
            
            # Kiểm tra bộ lọc nhà báo
            if kiem_tra_noi_dung(tieu_de):
                # Lấy link bài viết
                link = title_tag.get('href', '')
                if link and not link.startswith('http'):
                    link = "https://baochinhphu.vn" + link
                
                # Tác giả (Báo điện tử thường để tác giả cuối bài hoặc lấy tên Tòa soạn/Phóng viên)
                # Ở trang danh sách thường không có tên tác giả, ta để mặc định hoặc lấy theo nguồn
                tac_gia = "Theo PV / Tòa soạn" 
                nguon = "Báo Chính Phủ"
                
                tin_tuc_list.append({
                    "STT": len(tin_tuc_list) + 1,
                    "Tiêu đề": tieu_de,
                    "Tác giả": tac_gia,
                    "Nguồn": nguon,
                    "Đường dẫn (URL)": link,
                    "Ngày quét": datetime.now().strftime("%d/%m/%Y")
                })

    # 2. Xuất dữ liệu ra file Excel phục vụ viết bài
    if tin_tuc_list:
        df = pd.DataFrame(tin_tuc_list)
        file_name = f"tin_tuc_kinh_te_tech_{datetime.now().strftime('%Y%m%d')}.xlsx"
        df.to_excel(file_name, index=False)
        print(f"🎉 Đã lọc được {len(tin_tuc_list)} bài viết phù hợp!")
        print(f"💾 File Excel đã được lưu với tên: {file_name}")
    else:
        print("🤷 Không tìm thấy bài viết nào khớp với từ khóa khu vực và chủ đề trong hôm nay.")

if __name__ == "__main__":
    quet_tin_tuc_vung()