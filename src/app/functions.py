import os
import cv2  # Ensure OpenCV is installed
import math
import time
import pyautogui  # Ensure PyAutoGUI is installed
from pydantic import BaseModel  # Ensure Pydantic is installed


class DistanceInput(BaseModel):
    distance_of_two_fingers: float  # floatのみ許可


class ThresholdInput(BaseModel):
    threshold: float  # floatのみ許可


def set_volume(volume: int):
    try:
        os.system(f"osascript -e 'set volume output volume {volume}'")
    except Exception as e:
        print(f"Error: {e}")


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


def get_screen_shot(
    to_take_screenshot: bool,
) -> bool:
    """
    It takes a screenshot and saves it to a directory if the distance of two
    fingers is less than or equal to the threshold.

    Args:
        distance_input (DistanceInput): An instance of DistanceInput class
        threshold_input (ThresholdInput): An instance of ThresholdInput class

    Returns:
        bool: True if the screenshot is taken and saved, False otherwise
    """

    if to_take_screenshot:
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
        return False


def draw_fox_hand_sign(lm_list, threshold=80):
    """
    狐のハンドサイン（親指、中指、薬指をくっつける動作）を検出して描画する関数

    Args:
        lm_list: 手のランドマークのリスト
        threshold: 指が「くっついている」と判定する距離の閾値（ピクセル）

    Returns:
        is_fox_sign: 狐のサインを検出したかどうかのブール値
    """
    if len(lm_list) < 21:  # すべてのランドマークが検出されているか確認
        return False

    # 各指の先端のインデックス
    THUMB_TIP = 4       # 親指の先端
    MIDDLE_TIP = 12     # 中指の先端
    RING_TIP = 16       # 薬指の先端

    # 各指の座標を取得
    thumb_tip = (lm_list[THUMB_TIP][1], lm_list[THUMB_TIP][2])
    middle_tip = (lm_list[MIDDLE_TIP][1], lm_list[MIDDLE_TIP][2])
    ring_tip = (lm_list[RING_TIP][1], lm_list[RING_TIP][2])

    # 指同士の距離を計算
    def calc_distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    thumb_to_middle = calc_distance(thumb_tip, middle_tip)
    thumb_to_ring = calc_distance(thumb_tip, ring_tip)
    middle_to_ring = calc_distance(middle_tip, ring_tip)

    # 狐のサインの判定
    is_fox_sign = (
        thumb_to_middle < threshold and
        thumb_to_ring < threshold and
        middle_to_ring < threshold
    )
    return is_fox_sign
