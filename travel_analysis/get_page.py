import requests
import time

url = "https://travel.rakuten.co.jp/"
response = requests.get(url)

time.sleep(2)  # サーバ負荷対策（課題で重要）

html = response.text

with open("rakuten_sample.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTMLを保存しました")
