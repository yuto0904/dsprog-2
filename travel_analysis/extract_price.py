from bs4 import BeautifulSoup
import re

with open("rakuten_search.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

prices = []

# 最安値価格を取得
price_tags = soup.find_all("span", class_="htlLowprice")

for tag in price_tags:
    text = tag.get_text()
    match = re.search(r"[0-9,]+", text)
    if match:
        price = int(match.group().replace(",", ""))
        prices.append(price)

print("取得した宿泊料金（最初の10件）")
print(prices[:10])
print("件数:", len(prices))
