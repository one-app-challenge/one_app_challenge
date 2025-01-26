import os
import time
import cv2

from video_capture import VideoCapture
import hand_tracking_module as htm
from functions import set_volume, draw_hand_landmarks
import logger

# ロガーの設定
logger = logger.get_logger(name=__name__, debug=True)


detector = htm.HandDetector(
    detection_confidence=0.7,
    tracking_confidence=0.7
)

# parameters
wCam, hCam = 300, 300
resize_factor = 0.3  # リサイズの倍率


cap = VideoCapture(0, wCam=wCam, hCam=hCam).start()
pTime = 0
last_executed_time = 0
volume = 0

while True:
    success, frame = cap.read()
    if not success:
        break

    # 手のランドマークを一定間隔で検出
    if time.time() - last_executed_time > 0.2:  # 0.2秒ごとに検出
        frame = detector.find_hands(frame)
        lm_list = detector.find_position(frame)

        if len(lm_list) != 0:
            length = draw_hand_landmarks(frame, lm_list)

            # 音量の取得と設定の頻度を減らす
            if time.time() - last_executed_time > 0.4:  # 0.4秒ごとに音量を更新
                last_executed_time = time.time()
                print("Updating volume...")
                if length >= 80 and length <= 800:
                    volume = int((length - 80) / (800 - 80) * 100)
                elif length > 800:
                    volume = 100
                else:
                    volume = 0

                set_volume(volume)
                print(f"Length: {length}, Volume: {volume}")

    # フレームをリサイズ
    frame = cv2.resize(frame, (0, 0), fx=resize_factor, fy=resize_factor)

    # フレームをJPEG圧縮して画質を落とす
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]  # 画質を20%に設定
    result, encimg = cv2.imencode('.jpg', frame, encode_param)
    frame = cv2.imdecode(encimg, 1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(frame, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.putText(frame, f"Volume: {volume}", (20, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.stop()
cv2.destroyAllWindows()
