import cv2
from threading import Thread
from time import sleep


class Stream:

    def __init__(self,stream_uri:str):
        self.stream_uri = stream_uri
        self.cap = cv2.VideoCapture(stream_uri)

        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

        if int(major_ver)  < 3 :
            self.frame_rate = self.cap.get(cv2.CV_CAP_PROP_FPS) or 1
        else :
            self.frame_rate = self.cap.get(cv2.CAP_PROP_FPS) or 1


        t = Thread(target=self._background_fetch,daemon=True)
        t.start()

    def _background_fetch(self):


        while True:
            self.cap.grab()
            sleep(1 / self.frame_rate * 9 / 10)
    
    def get_uri(self):
        return self.stream_uri

    def read(self):

        return self.cap.retrieve()

