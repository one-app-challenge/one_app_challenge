# 引数として数字(int)を渡したときに、10以下の場合にスクショして保存
# 専用ディレクトリに保存する関数の仮作成
# PyAutoGUIを使用したい
import time
import os
import pyautogui


def get_screen_shot(num_int):
    if num_int <= 10:
        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        current_time = time.strftime("%Y%m%d%H%M%S")
        time.sleep(1)  # 一応1秒待つ
        screenshot = pyautogui.screenshot()
        screenshot.save(os.path.join(screenshots_dir, f"screenshot_{current_time}.png"))
        print("Screenshot saved")
        return True
    else:
        print(f"Number is {num_int}, not taking screenshot")
        return False


# 以下はテスト用
num_int = int(input("Enter a number: "))
get_screen_shot(num_int)


if __name__ == "get_screen_shot":
    get_screen_shot()
