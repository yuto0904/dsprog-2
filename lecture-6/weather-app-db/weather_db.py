import sqlite3

DB_NAME = "weather.db"

def init_db():
    """データベースとテーブルを作成する"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. 地域テーブル 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS areas (
        code TEXT PRIMARY KEY,
        name TEXT
    )
    """)

    # 2. 予報テーブル 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forecasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        area_code TEXT,
        date TEXT,
        weather TEXT,
        high_temp TEXT,
        low_temp TEXT,
        UNIQUE(area_code, date)
    )
    """)
    
    conn.commit()
    conn.close()

def save_area(code, name):
    """地域情報を保存"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # INSERT OR IGNORE: 
    cursor.execute("INSERT OR IGNORE INTO areas (code, name) VALUES (?, ?)", (code, name))
    conn.commit()
    conn.close()

def save_forecasts(area_code, forecast_list):
    """
    予報リストを保存する
    forecast_list は [{"date":..., "weather":..., "high":..., "low":...}, ...] の形式
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for item in forecast_list:
        # INSERT OR REPLACE: 
        cursor.execute("""
        INSERT OR REPLACE INTO forecasts (area_code, date, weather, high_temp, low_temp)
        VALUES (?, ?, ?, ?, ?)
        """, (area_code, item["date"], item["weather"], item["high"], item["low"]))
    
    conn.commit()
    conn.close()

def get_forecasts_from_db(area_code):
    """DBから特定の地域の予報を取り出す"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 日付順に取得
    cursor.execute("""
    SELECT date, weather, high_temp, low_temp 
    FROM forecasts 
    WHERE area_code = ? 
    ORDER BY date ASC
    """, (area_code,))
    
    rows = cursor.fetchall()
    conn.close()
    
    # 使いやすい辞書のリストに変換して返す
    result = []
    for row in rows:
        result.append({
            "date": row[0],
            "weather": row[1],
            "high": row[2],
            "low": row[3]
        })
    return result