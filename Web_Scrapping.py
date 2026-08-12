import requests
from bs4 import BeautifulSoup
import time
import os

# ==========================================
# 🎯 CẤU HÌNH BỘ LỌC TỪ KHÓA
# ==========================================
url_scraping = "https://hcm.edu.vn/tin-tuc-su-kien/c/41021"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
DANH_SACH_KEYWORD = ["tuyển sinh 10", "tuyển sinh vào lớp 10", "tuyển sinh vào 10"]

duong_dan_file_txt = "cac_link_da_xem.txt"
cac_link_da_biet = set()

if os.path.exists(duong_dan_file_txt):
    with open(duong_dan_file_txt, "r", encoding="utf-8") as f:
        cac_link_da_biet = set(f.read().splitlines())

print("🔍 Đang quét dữ liệu từ trang của Sở...")
danh_sach_tin_tim_duoc = []

try:
    response = requests.get(url_scraping, headers=headers, timeout=15)
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
                    
                    # Lưu vào danh sách để hiển thị lên Web
                    danh_sach_tin_tim_duoc.append({"title": title, "link": link})
                    
                    if link not in cac_link_da_biet:
                        cac_link_da_biet.add(link)
                        with open(duong_dan_file_txt, "a", encoding="utf-8") as f:
                            f.write(link + "\n")
except Exception as e:
    print(f"❌ Lỗi khi quét: {e}")

# ==========================================
# 🌐 TỰ ĐỘNG XUẤT RA FILE INDEX.HTML ĐỂ LÀM WEBSITE
# ==========================================
thoi_gian_cap_nhat = time.strftime('%H:%M:%S - %d/%m/%Y')

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cập Nhật Tuyển Sinh 10 - Phan Đỗ Minh Hoàng</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        h1 {{ color: #d32f2f; border-bottom: 3px solid #d32f2f; padding-bottom: 10px; font-size: 28px; }}
        .time {{ color: #666; font-style: italic; margin-bottom: 20px; }}
        .tin-tuc {{ list-style: none; padding: 0; }}
        .tin-tuc li {{ background: #fff; margin-bottom: 12px; padding: 15px; border-left: 5px solid #29b6f6; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.02); transition: 0.2s; }}
        .tin-tuc li:hover {{ transform: translateX(5px); box-shadow: 0 4px 8px rgba(0,0,0,0.08); }}
        .tin-tuc a {{ text-decoration: none; color: #0288d1; font-weight: bold; font-size: 16px; }}
        .tin-tuc a:hover {{ color: #01579b; }}
        .no-news {{ color: #2e7d32; font-weight: bold; background: #e8f5e9; padding: 15px; border-radius: 6px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Cổng Thông Tin Tuyển Sinh Vào Lớp 10</h1>
        <p class="time">🕒 Cập nhật tự động lần cuối lúc: {thoi_gian_cap_nhat}</p>
        <ul class="tin-tuc">
"""

if danh_sach_tin_tim_duoc:
    for tin in danh_sach_tin_tim_duoc:
        html_content += f'            <li>🚨 <a href="{tin["link"]}" target="_blank">{tin["title"]}</a></li>\n'
else:
    html_content += '            <p class="no-news">✅ Hiện tại chưa quét thấy tin tuyển sinh 10 mới nào từ Sở Giáo Dục.</p>\n'

html_content += """        </ul>
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✨ Đã tạo xong trang web index.html hoàn chỉnh!")