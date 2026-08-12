import requests
from bs4 import BeautifulSoup
import time
import os
# === THÊM ĐOẠN NÀY ĐỂ RENDER WEB SERVICE KHÔNG BÁO LỖI ===
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot dang chay tot!")

def run_fake_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), SimpleServer)
    server.serve_forever()

# Chạy server ngầm để qua mặt Render
threading.Thread(target=run_fake_server, daemon=True).start()
# ========================================================

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

# Danh sách các từ khóa cần lọc (viết thường hết để bot so sánh chính xác)
DANH_SACH_KEYWORD = ["tuyển sinh 10", "tuyển sinh vào lớp 10", "tuyển sinh vào 10"]

cac_link_da_biet = set()
if os.path.exists("cac_link_da_xem.txt"):
    with open("cac_link_da_xem.txt", "r", encoding="utf-8") as f:
        cac_link_da_biet = set(f.read().splitlines())

print("🚀 Bot Săn Tin Lớp 10 qua Discord đã kích hoạt trên Server!")
gui_tin_discord("Bot đã kết nối với Server Render thành công và đang chạy ngầm 24/7!", url_scraping)

# ==========================================
# VÒNG LẶP SĂN TIN CHẠY NGẦM LIÊN TỤC
# ==========================================
while True:
    print(f"⏰ [{time.strftime('%H:%M:%S')}] Đang quét trang của Sở...")
    try:
        response = requests.get(url_scraping, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("a")
            
            for art in articles:
                title = art.text.strip()
                link = art.get("href")
                
                if title and link:
                    # Kiểm tra xem tiêu đề có chứa một trong các từ khóa trong danh sách hay không
                    co_tin_tuyen_sinh = any(kw in title.lower() for kw in DANH_SACH_KEYWORD)
                    
                    if co_tin_tuyen_sinh:
                        if not link.startswith("http"):
                            link = "https://hcm.edu.vn" + link
                            
                        if link not in cac_link_da_biet:
                            cac_link_da_biet.add(link)
                            
                            with open("cac_link_da_xem.txt", "a", encoding="utf-8") as f:
                                f.write(link + "\n")
                                
                            gui_tin_discord(title, link)
                            
    except Exception as e:
        print(f"❌ Lỗi chu kỳ: {e}")
        
    print("💤 Đã kiểm tra xong. Bot đi ngủ 1 tiếng đây...\n")
    time.sleep(3600)