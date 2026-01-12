import flet as ft
import requests
import weather_db  

def main(page: ft.Page):
    page.title = "天気予報アプリ (DB連動版)"
    
    # アプリ起動時にDBの準備をする
    weather_db.init_db()

    # --- 画面パーツ ---
    result_column = ft.Column(scroll="auto", expand=True)

    # --- API等の処理関数 ---
    
    def get_weather_from_api(area_code):
        url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
        try:
            return requests.get(url).json()
        except:
            return None

    def get_area_list():
        url = "http://www.jma.go.jp/bosai/common/const/area.json"
        try:
            return requests.get(url).json()
        except:
            return None

    def get_weather_icon(weather_text):
        """天気の文字からアイコンを決める"""
        text = weather_text.lower()
        if "雨" in text: return ft.Icons.UMBRELLA, "blue"
        elif "曇" in text: return ft.Icons.CLOUD, "grey"
        elif "雪" in text: return ft.Icons.AC_UNIT, "cyan"
        else: return ft.Icons.WB_SUNNY, "orange"

    # --- ボタンクリック時の処理 ---
    def on_area_clicked(e):
        area_code = e.control.data
        area_name = e.control.title.value

        # 1. 読み込み中表示
        result_column.controls.clear()
        result_column.controls.append(ft.ProgressRing())
        page.update()

        # 2. APIからデータ取得
        api_data = get_weather_from_api(area_code)

        if api_data:
            # 3. データを解析して整形
            try:
                # DBに保存するためにデータをきれいなリストにする
                formatted_list = []
                
                report = api_data[0]["timeSeries"][0]
                temp_report = api_data[0]["timeSeries"][2] # 気温データ
                
                time_defines = report["timeDefines"]
                
                # 東京地方など、エリア内の詳細を取得
                # 今回は簡略化のため、リストの先頭(代表地点)のデータだけ使う
                weather_area = report["areas"][0]
                temp_area = temp_report["areas"][0]
                
                weathers = weather_area["weathers"]
                temps_high = temp_area.get("temps", [])
                temps_low = temp_area.get("tempsMin", [])

                for i in range(len(weathers)):
                    date = time_defines[i][:10]
                    w_text = weathers[i]
                    
                    # 気温データの取得
                    high = temps_high[i] if i < len(temps_high) else "--"
                    low = temps_low[i] if i < len(temps_low) else "--"
                    
                    formatted_list.append({
                        "date": date,
                        "weather": w_text,
                        "high": high,
                        "low": low
                    })

                # DBに保存する
                weather_db.save_area(area_code, area_name) # 地域名を保存
                weather_db.save_forecasts(area_code, formatted_list) # 天気を保存
                
                print(f"DBに保存しました: {area_name}")

            except Exception as err:
                print(f"解析エラー: {err}")

        # 4. DBからデータを読み込んで表示する
        # APIの結果ではなく、必ずDBの結果を使うこと
        db_data = weather_db.get_forecasts_from_db(area_code)
        
        result_column.controls.clear()
        result_column.controls.append(ft.Text(f"{area_name}の予報 (DBから取得)", size=24, weight="bold"))

        if not db_data:
            result_column.controls.append(ft.Text("データがありません"))
        else:
            # カードを表示
            row = ft.Row(scroll="auto")
            for item in db_data:
                icon, color = get_weather_icon(item["weather"])
                
                card = ft.Container(
                    content=ft.Column([
                        ft.Text(item["date"], weight="bold"),
                        ft.Icon(icon, color=color, size=40),
                        ft.Text(item["weather"], size=12),
                        ft.Text(f"{item['low']}°C / {item['high']}°C", color="blue")
                    ], alignment="center", horizontal_alignment="center"),
                    padding=10,
                    width=150,
                    height=160,
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=10
                )
                row.controls.append(card)
            result_column.controls.append(row)
        
        page.update()

    # --- サイドバー作成 ---
    sidebar_items = []
    area_data = get_area_list()
    if area_data:
        centers = area_data["centers"]
        offices = area_data["offices"]
        for center in centers.values():
            btns = []
            for child in center["children"]:
                if child in offices:
                    btns.append(ft.ListTile(
                        title=ft.Text(offices[child]["name"]),
                        data=child,
                        on_click=on_area_clicked
                    ))
            sidebar_items.append(ft.ExpansionTile(
                title=ft.Text(center["name"]),
                controls=btns
            ))

    sidebar = ft.Container(
        content=ft.Column(sidebar_items, scroll="auto"),
        width=250,
        bgcolor=ft.Colors.GREY_200
    )

    page.add(ft.Row([sidebar, ft.VerticalDivider(width=1), result_column], expand=True))

ft.app(target=main)