import cv2
import time
import threading

class VideoStream:
    def __init__(self, src=0):
        """
        Initialize the video stream.
        :param src: Source of the video stream (0 for webcam, or path to video file).
        """
        self.stream = cv2.VideoCapture(src)
        self.grabbed, self.frame = self.stream.read()
        self.stopped = False
        self.thread = None

    def start(self):
        """Start the thread to read frames from the video stream."""
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def update(self):
        """Keep looping infinitely until the stream is stopped."""
        while True:
            if self.stopped:
                return

            (grabbed, frame) = self.stream.read()
            if not grabbed:
                self.stop()
                return 
            
            self.grabbed = grabbed
            self.frame = frame
            time.sleep(0.001) # Small sleep to prevent CPU hogging

    def read(self):
        """Return the most recently read frame."""
        return self.frame

    def stop(self):
        """Indicate that the thread should be stopped."""
        self.stopped = True
        if self.stream.isOpened():
            self.stream.release()

    def is_running(self):
        return not self.stopped and self.stream.isOpened()
