# reference:
# https://qiita.com/kotai2003/items/466b2be885ff4cdbbde2
# https://www.youtube.com/watch?v=1CVmjTcSpIw
# https://gitlab.com/duder1966/youtube-projects/-/tree/master/OpenCV


import cv2
import numpy as np
import threading
import queue
import time

# Camera Thread Class from your provided code
class Camera_Thread:

    def __init__(self,buffer_all = False):
        # Initialize camera
        self.camera_source = 0
        self.camera_width = 640
        self.camera_height = 480
        self.camera_frame_rate = 30
        self.camera_fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        self.buffer_length = 5
        self.buffer_all = buffer_all

        self.camera = None
        self.buffer = None
        self.frame_grab_run = False
        self.frame_grab_on = False
        self.frame_count = 0
        self.frames_returned = 0
        self.current_frame_rate = 0
        self.loop_start_time = 0
        self.thread = None

    def start(self):
        if self.buffer_all:
            self.buffer = queue.Queue(self.buffer_length)
        else:
            self.buffer = queue.Queue(1)

        self.camera = cv2.VideoCapture(self.camera_source)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
        self.camera.set(cv2.CAP_PROP_FPS, self.camera_frame_rate)
        self.camera.set(cv2.CAP_PROP_FOURCC, self.camera_fourcc)

        time.sleep(0.5)  # Allow camera to initialize

        self.frame_grab_run = True
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def stop(self):
        self.frame_grab_run = False
        if self.thread:
            self.thread.join()

        if self.camera:
            self.camera.release()
        self.buffer = None

    def loop(self):
        self.frame_grab_on = True
        while self.frame_grab_run:
            if not self.buffer.full():
                ret, frame = self.camera.read()
                if not ret:
                    break
                self.buffer.put(frame)
                self.frame_count += 1

        self.frame_grab_on = False

    def next(self, black=True, wait=1):
        frame = np.zeros((self.camera_height, self.camera_width, 3), np.uint8) if black else None
        try:
            frame = self.buffer.get(timeout=wait)
            self.frames_returned += 1
        except queue.Empty:
            pass
        return frame

# Main function to start the camera and measure FPS
def main():
    camera_thread = Camera_Thread(buffer_all=True)
    camera_thread.start()

    frame_count = 0
    start_time = time.time()

    while True:
        frame = camera_thread.next(black=False)
        if frame is not None:
            cv2.imshow("Camera Thread", frame)
            frame_count += 1

            if frame_count >= 100:
                elapsed_time = time.time() - start_time
                fps = frame_count / elapsed_time
                print(f"Measured FPS: {fps:.2f}")
                frame_count = 0
                start_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera_thread.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


