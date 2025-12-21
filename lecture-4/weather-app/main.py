import flet as ft
import requests

# --- 1. データを取ってくる関数 ---
def get_area_list():
    url = "http://www.jma.go.jp/bosai/common/const/area.json"
    try:
        return requests.get(url).json()
    except:
        return None

def get_weather(area_code):
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
    try:
        return requests.get(url).json()
    except:
        return None


def main(page: ft.Page):
    page.title = "天気予報アプリ"
    
    # --- 2. 画面のパーツを作る ---

    # 結果を表示するエリア (最初は空っぽ)
    result_column = ft.Column(scroll="auto", expand=True)

    # --- 3. ボタンが押されたときの動き ---
    def show_weather(e):
        # 1. 押されたボタンの情報を受け取る
        area_code = e.control.data   # 地域コード 
        area_name = e.control.title.value  # 地域名 

        # 2. 画面をリセットして「読み込み中」にする
        result_column.controls.clear()
        result_column.controls.append(ft.Text("データを取得中..."))
        page.update()

        # 3. ネットから天気を取ってくる
        weather_data = get_weather(area_code)

        # 4. データを画面に表示する準備
        result_column.controls.clear() 
        
        if weather_data is None:
            result_column.controls.append(ft.Text("エラー：データが取れませんでした"))
            page.update()
            return

        # タイトルを表示
        result_column.controls.append(
            ft.Text(f"{area_name}の天気", size=30, weight="bold")
        )

        # 5. 複雑なデータから必要な情報を取り出す
        try:
            report = weather_data[0]["timeSeries"][0]
            time_defines = report["timeDefines"] # 日付のリスト
            
            # 地域内の細かいエリアごとのループ 
            for area in report["areas"]:
                detail_name = area["area"]["name"] # 詳細エリア名
                weathers = area["weathers"]        # 天気のリスト

                # カードの中身を作る
                forecast_row = ft.Row(scroll="auto")
                
                for i in range(len(weathers)):
                    date = time_defines[i][:10] # 日付 
                    weather_text = weathers[i]  # 天気 

                    # 1日分の四角いカード
                    card = ft.Container(
                        content=ft.Column([
                            ft.Text(date, weight="bold"),
                            ft.Icon(ft.Icons.WB_SUNNY, color="orange"),
                            ft.Text(weather_text)
                        ]),
                        padding=10,
                        bgcolor=ft.Colors.BLUE_50, # 薄い青
                        border_radius=10
                    )
                    forecast_row.controls.append(card)

                # 画面に追加
                result_column.controls.append(ft.Text(detail_name, size=20, weight="bold"))
                result_column.controls.append(forecast_row)
                result_column.controls.append(ft.Divider()) # 区切り線

        except:
            result_column.controls.append(ft.Text("データの解析に失敗しました"))
        
        page.update()


    # --- 4. サイドバーを作る ---
    sidebar_items = []
    
    # データを取ってくる
    area_data = get_area_list()

    if area_data:
        centers = area_data["centers"] # 大きな地方 
        offices = area_data["offices"] # 都道府県 

        # 地方ごとにループ
        for center_code, center_info in centers.items():
            
            # その地方の中にある県ボタンのリストを作る
            pref_buttons = []
            for office_code in center_info["children"]:
                if office_code in offices:
                    office_name = offices[office_code]["name"]
                    
                    # 個別の県ボタン
                    btn = ft.ListTile(
                        title=ft.Text(office_name),
                        data=office_code,      # 裏でコードを持っておく
                        on_click=show_weather  # 押したら show_weather を実行
                    )
                    pref_buttons.append(btn)
            
            # 地方のアコーディオンに県ボタンを入れる
            group = ft.ExpansionTile(
                title=ft.Text(center_info["name"]),
                controls=pref_buttons
            )
            sidebar_items.append(group)

    # サイドバーのコンテナ
    sidebar = ft.Container(
        content=ft.Column(sidebar_items, scroll="auto"),
        width=200,
        bgcolor=ft.Colors.GREY_200
    )

    # --- 5. 最後に全部並べる ---
    page.add(
        ft.Row(
            controls=[
                sidebar,       # 左
                ft.VerticalDivider(width=1),
                result_column  # 右
            ],
            expand=True
        )
    )

ft.app(target=main)