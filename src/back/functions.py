import os
import cv2
import math


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
