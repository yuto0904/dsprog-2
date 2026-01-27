import sqlite3
import matplotlib.pyplot as plt

# DBに接続
conn = sqlite3.connect("travel.db")
cur = conn.cursor()

# 価格データを取得
cur.execute("SELECT price FROM prices")
data = cur.fetchall()
conn.close()

# [(4091,), (21210,), ...] → [4091, 21210, ...]
prices = [d[0] for d in data]

# グラフ作成（ヒストグラム）
plt.hist(prices, bins=10)
plt.xlabel("宿泊料金（円）")
plt.ylabel("件数")
plt.title("宿泊料金の分布")

plt.show()
