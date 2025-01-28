import os
import cv2
import math
import time
import pyautogui
from pydantic import BaseModel


class DistanceInput(BaseModel):
    distance_of_two_fingers: float  # floatのみ許可


class ThresholdInput(BaseModel):
    threshold: float  # floatのみ許可


class Functions:
    @staticmethod
    def set_volume(volume: int):
        try:
            os.system(f"osascript -e 'set volume output volume {volume}'")
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def draw_hand_landmarks(frame, lm_list):
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(frame, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 5)
        cv2.circle(frame, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        if length < 80:
            cv2.circle(frame, (cx, cy), 40, (0, 255, 0), cv2.FILLED)

        return length

    @staticmethod
    def get_screen_shot(
        distance_input: DistanceInput,
        threshold_input: ThresholdInput,
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
            screenshot.save(
                os.path.join(screenshots_dir, f"screenshot_{current_time}.png")
            )
            print("Screenshot saved")
            return True
        else:
            # distance_of_two_fingersがthresholdより大きいので、スクショは撮らない
            print(
                f"Number is {distance_input.distance_of_two_fingers}, not taking screenshot"
            )
            return False


# ユーザーにdistance_of_two_fingersを入力させる
# distance_of_two_fingers = float(input("Enter the distance of two fingers: "))
# distance_input = DistanceInput(distance_of_two_fingers=distance_of_two_fingers)

# デフォルトのthresholdの値を設定
# threshold_input = ThresholdInput(threshold=10)

# printで一言表示したうえで、get_screen_shot関数を実行
# print(
#     f"Distance is {distance_input.distance_of_two_fingers}, threshold is {threshold_input.threshold} (this is default)"
)
# Functions.get_screen_shot(distance_input, threshold_input)


# if __name__ == "get_screen_shot":
#     get_screen_shot()
