# 引数として数字(int)を渡したときに、10以下の場合にスクショして保存
# 専用ディレクトリに保存する関数の仮作成
# PyAutoGUIを使用
import time
import os
import pyautogui
from pydantic import BaseModel


# PydanticでBaseModel使用して、入力値の型チェック用のクラスを作成
class InputNumber(BaseModel):
    num_int: int  # 整数のみ許可


def get_screen_shot(input_number: InputNumber) -> bool:
    """
    It takes a screenshot and saves it to a directory if the input number is less than or equal to 10.

    Args:
        input_number (InputNumber): An instance of InputNumber class

    Returns:
        bool: True if the screenshot is taken and saved, False otherwise
    """

    if input_number.num_int <= 10:
        # ディレクトリを定義、ない場合は作成する
        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        # ファイル名用の時刻を取得する
        current_time = time.strftime("%Y%m%d%H%M%S")
        # 一応1秒待つ
        time.sleep(1)
        screenshot = pyautogui.screenshot()
        screenshot.save(os.path.join(screenshots_dir, f"screenshot_{current_time}.png"))
        print("Screenshot saved")
        return True
    else:
        # 入力された数値が10より大きい場合は撮らない
        print(f"Number is {input_number.num_int}, not taking screenshot")
        return False


# 以下はテスト用
# ユーザーにinputで数値入力させる→Pydanticの設定通す（InputNumberクラスのインスタンスに変換）
# （上記の続き）→ それ使って実行
num_int = int(input("Enter a number: "))
input_number = InputNumber(num_int=num_int)
get_screen_shot(input_number)

if __name__ == "get_screen_shot":
    get_screen_shot()
