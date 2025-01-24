import os
import cv2
import time
import numpy as np
import math
from threading import Thread, Lock

import hand_tracking_module as htm

class VideoCapture:
    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.cap.set(3, wCam)
        self.cap.set(4, hCam)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = Lock()

    def start(self):
        if self.started:
            print("[INFO] Asynchronous video capturing has already started.")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
        return self.grabbed, frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()

detector = htm.HandDetector(
    detection_confidence=0.7,
    tracking_confidence=0.7
)

# parameters
wCam, hCam = 300, 300
resize_factor = 0.3  # リサイズの倍率

# 現在の音量を取得する関数
# def get_current_volume():
#     result = os.popen("osascript -e 'output volume of (get volume settings)'").read().strip()
#     return int(result)

# 音量を設定する関数
def set_volume(volume: int):
    os.system(f"osascript -e 'set volume output volume {volume}'")

cap = VideoCapture(0).start()
pTime = 0
last_executed_time = 0
volume = 0

while True:
    success, frame = cap.read()
    if not success:
        break

    # 手のランドマークを検出
    frame = detector.find_hands(frame)
    lm_list = detector.find_position(frame)

    if len(lm_list) != 0:
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

        # # 音量の取得と設定の頻度を減らす
        if time.time() - last_executed_time > 0.4:  # 0.1秒ごとに音量を更新
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
