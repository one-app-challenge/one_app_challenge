import os
import cv2
import time
import numpy as np
import math

import hand_tracking_module as htm

detector = htm.HandDetector(
    detection_confidence=0.7,
    tracking_confidence=0.7
)

# parameters
wCam, hCam = 640, 480


# 現在の音量を取得する関数
def get_current_volume():
    result = os.popen("osascript -e 'output volume of (get volume settings)'").read().strip()
    return int(result)


# 音量を設定する関数, using osascript? applescript not sure...
def set_volume(volume: int):
    os.system(f"osascript -e 'set volume output volume {volume}'")


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
volume = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = detector.find_hands(frame)
    lm_list = detector.find_position(frame)
    if len(lm_list) != 0:
        # print(lm_list[4], lm_list[8])
        # この辺りの番号はmediapipeのドキュメントを参照, 4は親指、8は人差し指?
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]
        # 親指と人差し指の間の長さの半分を計算
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        # 親指と人差し指に色違いの丸を描画
        cv2.circle(frame, (x1, y1), 10, (255, 255, 0), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 10, (255, 255, 0), cv2.FILLED)
        # 線を引く
        cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 0), 3)
        # 中心に丸を描画
        cv2.circle(frame, (cx, cy), 10, (255, 255, 0), cv2.FILLED)

        # 親指と人差し指の間の長さを計算
        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        if length < 10:
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        # 現在の音量を取得
        current_volume = get_current_volume()

        # # length に基づいて音量を調整
        if length >= 20 and length <= 220:
            # 20-220の範囲を0-100の範囲にマッピング
            # int()はfloatに対して切り捨て処理を実施
            volume = int((length - 20) / (220 - 20) * 100)
        elif length > 220:
            volume = 100
        else:
            volume = 0

        set_volume(volume)
        print(f"Length: {length}, Volume: {volume}")

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(frame, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.putText(frame, f"Volume: {volume}", (20, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("frame", frame)

# TODO:処理が重いからかqで終了しないためwaitKeyを25に変更した。効果があるのかは確認が必要
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break
