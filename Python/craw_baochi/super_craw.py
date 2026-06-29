import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

# 1. Các bộ lọc từ khóa chuyên ngành để tránh bị loãng thông tin
KHU_VUC = ["Đà Nẵng", "Quảng Nam", "Quảng Ngãi", "Bình Định", "Quy Nhơn", "Phú Yên", "Khánh Hòa", "Nha Trang", 
           "Ninh Thuận", "Bình Thuận", "Kon Tum", "Gia Lai", "Pleiku", "Đắk Lắk", "Buôn Ma Thuột", "Đắk Nông", 
           "Lâm Đồng", "Đà Lạt", "Tây Nguyên", "Miền Trung", "Nam Trung Bộ", "Liên Chiểu", "Chu Lai", "Vân Phong"]

CHU_DE = ["kinh tế", "doanh nghiệp", "đầu tư", "khoa học", "công nghệ", "nghiên cứu", "chuyển đổi số", 
          "khởi nghiệp", "GRDP", "quy hoạch", "bán dẫn", "vi mạch", "fdi", "logistics", "ai", "nông nghiệp công nghệ cao"]

def kiem_tra_tu_khoa(text):
    """Kiểm tra xem tiêu đề có chứa từ khóa khu vực hoặc chủ đề hay không"""
    if not text:
        return False
    text_lower = text.lower()
    co_khu_vuc = any(kv.lower() in text_lower for kv in KHU_VUC)
    co_chu_de = any(cd.lower() in text_lower for cd in CHU_DE)
    # Ưu tiên bài viết thỏa mãn cả địa bàn và chủ đề, hoặc chứa từ khóa cốt lõi
    return co_khu_vuc or co_chu_de

def quet_mot_trang(url, ten_bao):
    """Hàm quét tiêu đề và link của một trang báo cụ thể"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    tin_tuc_trang = []
    
    try:
        # Giới hạn thời gian chờ (timeout) để tránh tool bị treo nếu báo lỗi mạng
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"⚠️ Không thể truy cập {ten_bao} (Mã lỗi: {response.status_code})")
            return tin_tuc_trang
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Hầu hết các báo điện tử hiện nay đều đặt tiêu đề bài viết trong các thẻ h2, h3 hoặc thẻ a có class
        # Cơ chế quét thông minh: Tìm tất cả các thẻ tiêu đề phổ biến
        cac_the_tieu_de = soup.find_all(['h2', 'h3', 'h4', 'a'], class_=True)
        
        # Nếu trang web quá đơn giản không dùng class, quét các thẻ tiêu đề thô
        if len(cac_the_tieu_de) < 5:
            cac_the_tieu_de = soup.find_all(['h2', 'h3'])

        links_da_quet = set() # Tránh trùng lặp link trên cùng 1 trang

        for the in cac_the_tieu_de:
            # Lấy text tiêu đề
            tieu_de = the.text.strip()
            if len(tieu_de) < 15: # Bỏ qua các text quá ngắn (như menu, danh mục)
                continue
                
            # Tìm thẻ chứa link (href)
            a_tag = the if the.name == 'a' else the.find('a')
            if a_tag and a_tag.has_attr('href'):
                link = a_tag['href']
                
                # Chuẩn hóa đường dẫn URL tuyệt đối
                if link.startswith('//'):
                    link = 'https:' + link
                elif link.startswith('/'):
                    # Tách lấy domain gốc của tờ báo
                    from urllib.parse import urlparse
                    parsed_url = urlparse(url)
                    link = f"{parsed_url.scheme}://{parsed_url.netloc}{link}"
                
                if link in links_da_quet:
                    continue
                    
                # Áp dụng bộ lọc nghiệp vụ nhà báo
                if kiem_tra_tu_khoa(tieu_de):
                    links_da_quet.add(link)
                    tin_tuc_trang.append({
                        "Tiêu đề bài viết": tieu_de,
                        "Nguồn cơ quan": ten_bao,
                        "Tác giả / Phóng viên": "Theo Tòa soạn",
                        "Đường dẫn (URL)": link,
                        "Thời gian quét": datetime.now().strftime("%d/%m/%Y %H:%M")
                    })
                    
    except Exception as e:
        print(f"❌ Lỗi khi xử lý trang {ten_bao}: {str(e)}")
        
    return tin_tuc_trang

def chay_he_thong_crawler():
    file_nguon = "danh_sach_nguon_tin_kinh_te_khcn_mientrung_taynguyen.xlsx"
    
    if not os.path.exists(file_nguon):
        print(f"❌ Không tìm thấy file cấu hình '{file_nguon}'!")
        print("Vui lòng đảm bảo file Excel danh sách nguồn tin nằm chung thư mục với file code này.")
        return

    print("📖 Đang đọc danh sách nguồn báo từ file Excel...")
    df_nguon = pd.read_excel(file_nguon)
    
    tat_ca_tin_tuc = []
    
    # Duyệt qua từng hàng trong file Excel nguồn tin
    for index, row in df_nguon.iterrows():
        ten_bao = row['Tên cơ quan / Nguồn tin']
        url_quet = row['Chuyên mục đề xuất quét']
        khu_vuc = row['Khu vực / Phân loại']
        
        print(f"🔄 [{index + 1}/{len(df_nguon)}] Đang quét nguồn: {ten_bao} ({khu_vuc})...")
        
        tin_quet_duoc = quet_mot_trang(url_quet, ten_bao)
        
        if tin_quet_duoc:
            print(f"   🔹 Tìm thấy {len(tin_quet_duoc)} tin phù hợp.")
            tat_ca_tin_tuc.extend(tin_quet_duoc)
        else:
            print("   🔸 Không có tin mới phù hợp bộ lọc.")
            
        # Nghỉ 1-2 giây giữa các lần quét để không làm nghẽn băng thông của các báo (Lập trình lịch sự)
        time.sleep(1.5)

    # 2. Xuất toàn bộ kết quả ra một file Excel tổng hợp để nhà báo viết bài
    if tat_ca_tin_tuc:
        df_ket_qua = pd.DataFrame(tat_ca_tin_tuc)
        
        # Thêm cột STT ở đầu bảng
        df_ket_qua.insert(0, 'STT', range(1, len(df_ket_qua) + 1))
        
        ngay_hien_tai = datetime.now().strftime("%Y%m%d_%H%M")
        file_xuat = f"BAO_CAO_TIN_TUC_TONG_HOP_{ngay_hien_tai}.xlsx"
        
        # Định dạng file xuất đẹp mắt bằng pandas và openpyxl
        with pd.ExcelWriter(file_xuat, engine='openpyxl') as writer:
            df_ket_qua.to_excel(writer, index=False, sheet_name="Tin Tức Đã Lọc")
            
            # Tự động căn chỉnh chiều rộng cột vừa vặn
            workbook = writer.book
            worksheet = writer.sheets["Tin Tức Đã Lọc"]
            worksheet.views.sheetView[0].showGridLines = True
            for col in worksheet.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                col_letter = col[0].column_letter
                worksheet.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 50)

        print("\n" + "="*50)
        print(f"🎉 HOÀN THÀNH XUẤT SẮC!")
        print(f"📊 Tổng số tin tức kinh tế, KHCN đã thu thập và lọc: {len(tat_ca_tin_tuc)} bài viết.")
        print(f"💾 File Excel tổng hợp báo cáo đã lưu tại: {file_xuat}")
        print("="*50)
    else:
        print("\n🤷 Quét hoàn tất nhưng không tìm thấy bài viết nào khớp từ khóa trong hôm nay.")

if __name__ == "__main__":
    chay_he_thong_crawler()