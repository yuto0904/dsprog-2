from bs4 import BeautifulSoup

# HTMLファイルを開く
with open("rakuten_sample.html", "r", encoding="utf-8") as f:
    html = f.read()

# 解析
soup = BeautifulSoup(html, "html.parser")

# price を含む li タグを探す
items = soup.find_all("li", class_="item-price")

print("見つかった数:", len(items))

# 最初の1個だけ表示
if items:
    print(items[0])
