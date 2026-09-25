import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta

url_scraping = "https://hcm.edu.vn/tin-tuc-su-kien/c/41021"
headers = {"User-Agent": "Mozilla/5.0"}
DANH_SACH_KEYWORD = ["tuyển sinh 10", "tuyển sinh vào lớp 10", "tuyển sinh vào 10"]

duong_dan_file_txt = "cac_link_da_xem.txt"
cac_link_da_biet = set()
if os.path.exists(duong_dan_file_txt):
    with open(duong_dan_file_txt, "r", encoding="utf-8") as f:
        cac_link_da_biet = set(f.read().splitlines())

danh_sach_tin_tim_duoc = []
try:
    response = requests.get(url_scraping, headers=headers, timeout=15)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for art in soup.find_all("a"):
            title = art.text.strip()
            link = art.get("href")
            if title and link and any(kw in title.lower() for kw in DANH_SACH_KEYWORD):
                if not link.startswith("http"):
                    link = "https://hcm.edu.vn" + link
                danh_sach_tin_tim_duoc.append({"title": title, "link": link})
                if link not in cac_link_da_biet:
                    cac_link_da_biet.add(link)
                    with open(duong_dan_file_txt, "a", encoding="utf-8") as f:
                        f.write(link + "\n")
except Exception as e:
    print(f"❌ Lỗi: {e}")

gio_viet_nam = datetime.utcnow() + timedelta(hours=7)
thoi_gian_cap_nhat = gio_viet_nam.strftime('%H:%M:%S - %d/%m/%Y')

with open("templates/index.html", "r", encoding="utf-8") as f:
    html_template = f.read()

if danh_sach_tin_tim_duoc:
    items_html = "".join(
        f'            <li>🚨 <a href="{t["link"]}" target="_blank">{t["title"]}</a></li>\n'
        for t in danh_sach_tin_tim_duoc
    )
else:
    items_html = '            <p class="no-news">✅ Hiện tại chưa quét thấy tin tuyển sinh 10 mới nào.</p>\n'

html_output = (html_template
    .replace("{{ thoi_gian_cap_nhat }}", thoi_gian_cap_nhat)
    .replace("{{ danh_sach_tin }}", items_html))

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("✨ Xong!")
