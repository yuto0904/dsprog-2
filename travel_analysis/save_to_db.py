import sqlite3
from bs4 import BeautifulSoup
import re

# --- HTML読み込み ---
with open("rakuten_search.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# --- 価格抽出 ---
prices = []
price_tags = soup.find_all("span", class_="htlLowprice")

for tag in price_tags:
    text = tag.get_text()
    match = re.search(r"[0-9,]+", text)
    if match:
        price = int(match.group().replace(",", ""))
        prices.append(price)

# --- DB接続（なければ自動作成） ---
conn = sqlite3.connect("travel.db")
cur = conn.cursor()

# --- テーブル作成 ---
cur.execute("""
CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    price INTEGER
)
""")

# --- データ保存 ---
for price in prices:
    cur.execute(
        "INSERT INTO prices (price) VALUES (?)",
        (price,)
    )

conn.commit()
conn.close()

print("DBに保存しました。保存件数:", len(prices))
