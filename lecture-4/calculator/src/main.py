import flet as ft
import math

# --- ボタンの定義クラス ---
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, on_click, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = on_click
        self.data = text

class DigitButton(CalcButton):
    def __init__(self, text, on_click, expand=1):
        CalcButton.__init__(self, text, on_click, expand)
        # 修正: colors -> Colors (大文字)
        self.bgcolor = ft.Colors.WHITE24
        self.color = ft.Colors.WHITE

class ActionButton(CalcButton):
    def __init__(self, text, on_click):
        CalcButton.__init__(self, text, on_click)
        self.bgcolor = ft.Colors.ORANGE
        self.color = ft.Colors.WHITE

class ExtraActionButton(CalcButton):
    def __init__(self, text, on_click):
        CalcButton.__init__(self, text, on_click)
        self.bgcolor = ft.Colors.BLUE_GREY_100
        self.color = ft.Colors.BLACK

class ScienceButton(CalcButton):
    def __init__(self, text, on_click):
        CalcButton.__init__(self, text, on_click)
        self.bgcolor = ft.Colors.INDIGO_400
        self.color = ft.Colors.WHITE

# --- メイン処理 ---
def main(page: ft.Page):
    page.title = "Scientific Calculator"
    # 修正: colors -> Colors
    page.bgcolor = ft.Colors.BLACK
    
    result = ft.Text(value="0", color=ft.Colors.WHITE, size=40, text_align="right")

    # 計算の状態管理
    state = {
        "operator": None,
        "operand1": 0,
        "new_operand": True
    }

    def format_number(num):
        if num % 1 == 0:
            return int(num)
        else:
            return round(num, 8)

    def calculate(operand1, operand2, operator):
        if operator == "+": return format_number(operand1 + operand2)
        elif operator == "-": return format_number(operand1 - operand2)
        elif operator == "*": return format_number(operand1 * operand2)
        elif operator == "/":
            return "Error" if operand2 == 0 else format_number(operand1 / operand2)
        return format_number(operand2)

    def button_clicked(e):
        data = e.control.data
        print(f"Clicked: {data}")
        
        try:
            current_val = float(result.value)
        except ValueError:
            current_val = 0

        if data == "AC":
            result.value = "0"
            state["operator"] = None
            state["operand1"] = 0
            state["new_operand"] = True
        
        elif data == "+/-":
            if float(result.value) != 0:
                result.value = format_number(float(result.value) * -1)

        elif data == "%":
            result.value = format_number(float(result.value) / 100)

        # 科学計算
        elif data == "sin":
            result.value = format_number(math.sin(current_val))
            state["new_operand"] = True
        elif data == "cos":
            result.value = format_number(math.cos(current_val))
            state["new_operand"] = True
        elif data == "tan":
            result.value = format_number(math.tan(current_val))
            state["new_operand"] = True
        elif data == "log":
            # log10 を使用 (常用対数)
            result.value = format_number(math.log10(current_val)) if current_val > 0 else "Error"
            state["new_operand"] = True
        elif data == "√":
            result.value = format_number(math.sqrt(current_val)) if current_val >= 0 else "Error"
            state["new_operand"] = True

        elif data in ("+", "-", "*", "/"):
            state["operand1"] = float(result.value)
            state["operator"] = data
            state["new_operand"] = True

        elif data == "=":
            if state["operator"] is not None:
                val = calculate(state["operand1"], float(result.value), state["operator"])
                result.value = str(val)
                state["operator"] = None
                state["new_operand"] = True

        elif data in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."):
            if result.value == "0" or state["new_operand"]:
                result.value = data
                state["new_operand"] = False
            else:
                result.value = result.value + data
        
        result.update()

    page.add(
        ft.Container(
            width=350,
            bgcolor=ft.Colors.BLACK,
            border_radius=ft.border_radius.all(20),
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row(controls=[result], alignment="end"),
                    ft.Row(controls=[
                        ScienceButton("sin", button_clicked),
                        ScienceButton("cos", button_clicked),
                        ScienceButton("tan", button_clicked),
                        ScienceButton("log", button_clicked),
                        ScienceButton("√", button_clicked),
                    ]),
                    ft.Row(controls=[
                        ExtraActionButton("AC", button_clicked),
                        ExtraActionButton("+/-", button_clicked),
                        ExtraActionButton("%", button_clicked),
                        ActionButton("/", button_clicked),
                    ]),
                    ft.Row(controls=[
                        DigitButton("7", button_clicked),
                        DigitButton("8", button_clicked),
                        DigitButton("9", button_clicked),
                        ActionButton("*", button_clicked),
                    ]),
                    ft.Row(controls=[
                        DigitButton("4", button_clicked),
                        DigitButton("5", button_clicked),
                        DigitButton("6", button_clicked),
                        ActionButton("-", button_clicked),
                    ]),
                    ft.Row(controls=[
                        DigitButton("1", button_clicked),
                        DigitButton("2", button_clicked),
                        DigitButton("3", button_clicked),
                        ActionButton("+", button_clicked),
                    ]),
                    ft.Row(controls=[
                        DigitButton("0", button_clicked, expand=2),
                        DigitButton(".", button_clicked),
                        ActionButton("=", button_clicked),
                    ]),
                ]
            ),
        )
    )

ft.app(target=main)