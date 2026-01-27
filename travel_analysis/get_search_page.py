import requests
import time

url = "https://travel.rakuten.co.jp/yado/kanagawa/"

response = requests.get(url)
time.sleep(2)

html = response.text

with open("rakuten_search.html", "w", encoding="utf-8") as f:
    f.write(html)

print("検索結果ページを保存しました")
