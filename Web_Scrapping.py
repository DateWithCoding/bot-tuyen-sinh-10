import requests
from bs4 import BeautifulSoup
import time
import os

# ==========================================
# 🔑 LINK DISCORD WEBHOOK CỦA BẠN
# ==========================================
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1536751451026751660/uXONmefadIMO3jYnSxV5C8ICkdO24kZHuMmJ0YTGErhPfT1KxoawHxa8iSIBgs4h3zSM"

def gui_tin_discord(tieu_de, link):
    noi_dung = (
        f"🚨 **PHÁT HIỆN TIN TUYỂN SINH 10 MỚI!**\n\n"
        f"📌 **Tiêu đề:** {tieu_de}\n"
        f"🔗 **Xem chi tiết tại:** {link}\n"
        f"⏰ *Cập nhật lúc: {time.strftime('%H:%M:%S - %d/%m/%Y')}*"
    )
    payload = {"content": noi_dung}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code in [200, 204]:
            print("🤖 Đã bắn thông báo tin mới lên Discord thành công!")
    except Exception as e:
        print(f"❌ Không thể gửi tin nhắn đến Discord: {e}")

# ==========================================
# 🎯 CẤU HÌNH BỘ LỌC TỪ KHÓA
# ==========================================
url_scraping = "https://hcm.edu.vn/tin-tuc-su-kien/c/41021"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

DANH_SACH_KEYWORD = ["tuyển sinh 10", "tuyển sinh vào lớp 10", "tuyển sinh vào 10"]

# PythonAnywhere lưu file trên server nên mình chỉ định đường dẫn chính xác luôn
duong_dan_file = "/home/CoderPlayChess/cac_link_da_xem.txt"

cac_link_da_biet = set()
if os.path.exists(duong_dan_file):
    with open(duong_dan_file, "r", encoding="utf-8") as f:
        cac_link_da_biet = set(f.read().splitlines())

print(f"⏰ [{time.strftime('%H:%M:%S')}] Đang quét trang của Sở...")

try:
    # Sử dụng proxy của PythonAnywhere để không bị chặn (dành cho tài khoản Free)
    proxy_url = "http://proxy.server:3128"
    proxies = {"http": proxy_url, "https": proxy_url}
    
    response = requests.get(url_scraping, headers=headers, proxies=proxies, timeout=15)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("a")
        
        for art in articles:
            title = art.text.strip()
            link = art.get("href")
            
            if title and link:
                co_tin_tuyen_sinh = any(kw in title.lower() for kw in DANH_SACH_KEYWORD)
                
                if co_tin_tuyen_sinh:
                    if not link.startswith("http"):
                        link = "https://hcm.edu.vn" + link
                        
                    if link not in cac_link_da_biet:
                        cac_link_da_biet.add(link)
                        
                        with open(duong_dan_file, "a", encoding="utf-8") as f:
                            f.write(link + "\n")
                            
                        gui_tin_discord(title, link)
                        
except Exception as e:
    print(f"❌ Lỗi: {e}")

print("✨ Quét xong! Bot tự động đóng để đợi chu kỳ tiếp theo.")