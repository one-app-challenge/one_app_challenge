# 引数として数字(int)を渡したときに、10以下の場合にスクショして保存
# 専用ディレクトリに保存する関数の仮作成
# PyAutoGUIを使用
import time
import os
import pyautogui
from pydantic import BaseModel


# PydanticでBaseModel使用して、入力値の型チェック用のクラスを作成
# それぞれ２つのinput変数用に作成
class DistanceInput(BaseModel):
    distance_of_two_fingers: float  # floatのみ許可


class ThresholdInput(BaseModel):
    threshold: float  # floatのみ許可


def get_screen_shot(
    distance_input: DistanceInput,
    threshold_input: ThresholdInput = ThresholdInput(threshold=10),
) -> bool:
    """
    It takes a screenshot and saves it to a directory if the distance of two fingers is less than or equal to the threshold.

    Args:
        distance_input (DistanceInput): An instance of DistanceInput class
        threshold_input (ThresholdInput): An instance of ThresholdInput class

    Returns:
        bool: True if the screenshot is taken and saved, False otherwise
    """

    if distance_input.distance_of_two_fingers <= threshold_input.threshold:
        # ディレクトリを定義、ない場合は作成する
        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        # ファイル名用の時刻を取得する
        current_time = time.strftime("%Y%m%d%H%M%S")
        # スクショを撮って保存
        screenshot = pyautogui.screenshot()
        screenshot.save(os.path.join(screenshots_dir, f"screenshot_{current_time}.png"))
        print("Screenshot saved")
        return True
    else:
        # distance_of_two_fingersがthresholdより大きいので、スクショは撮らない
        print(
            f"Number is {distance_input.distance_of_two_fingers}, not taking screenshot"
        )
        return False


# [以下はテスト用]
# ユーザーにinputで数値入力させる→Pydanticの設定通す（DistanceInputクラスのインスタンスに変換）
# （上記の続き）→ それ使って実行

# ユーザーにdistance_of_two_fingersを入力させる
distance_of_two_fingers = float(input("Enter the distance of two fingers: "))
distance_input = DistanceInput(distance_of_two_fingers=distance_of_two_fingers)

# デフォルトのthresholdの値を設定
threshold_input = ThresholdInput(threshold=10)

# printで一言表示したうえで、get_screen_shot関数を実行
print(
    f"Distance is {distance_input.distance_of_two_fingers}, threshold is {threshold_input.threshold} (this is default)"
)
get_screen_shot(distance_input, threshold_input)


if __name__ == "get_screen_shot":
    get_screen_shot()
