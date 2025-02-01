from threading import Thread, Lock
import threading
import logger
import cv2

logger = logger.get_logger(name=__name__, debug=True)


class VideoCapture:
    def __init__(self, name, wCam, hCam):
        self.cap = cv2.VideoCapture(name)
        self.cap.set(3, wCam)
        self.cap.set(4, hCam)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = Lock()
        logger.debug("VideoCapture initialized.")
        logger.debug(f"Camera name: {name}, width: {wCam}, height: {hCam}")

    def start(self):
        logger.debug(f"current thread ID: {threading.currentThread().getName()}")
        if self.started:
            logger.info("Asynchronous video capturing has already started.")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        logger.debug(f"Video capturing started. Thread ID: {self.thread.ident}")
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame
            logger.debug("Frame updated.")

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
        logger.debug("Frame read.")
        return self.grabbed, frame

    def stop(self):
        self.started = False
        self.thread.join()
        logger.debug("Video capturing stopped.")
