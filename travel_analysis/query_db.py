import sqlite3

# DBに接続
conn = sqlite3.connect("travel.db")
cur = conn.cursor()

# データ件数を取得
cur.execute("SELECT COUNT(*) FROM prices")
count = cur.fetchone()[0]

# 平均価格を取得
cur.execute("SELECT AVG(price) FROM prices")
avg_price = cur.fetchone()[0]

# 全データを取得
cur.execute("SELECT price FROM prices")
prices = cur.fetchall()

conn.close()

print("データ件数:", count)
print("平均宿泊料金:", int(avg_price))
print("最初の10件:", prices[:10])
