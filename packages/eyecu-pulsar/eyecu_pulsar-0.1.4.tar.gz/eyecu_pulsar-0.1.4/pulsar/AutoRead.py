import cv2
from threading import Thread
from time import sleep


class AutoRead:

    def __init__(self,stream_uri:str):
        self.stream_uri = stream_uri
        self.cap = cv2.VideoCapture(stream_uri)
        self.frame = None
        self.on_read_event = None

        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        
        if int(major_ver)  < 3 :
            self.frame_rate = self.cap.get(cv2.CV_CAP_PROP_FPS) or 1
        else :
            self.frame_rate = self.cap.get(cv2.CAP_PROP_FPS) or 1


        t = Thread(target=self._background_fetch,daemon=True)
        t.start()

    def _background_fetch(self):


        while True:
            read,frame = self.cap.read()
            if read:
                self.frame = frame
                if self.on_read_event != None:
                    self.on_read_event(frame)

            sleep(1 / self.frame_rate * .7 )
    
    def get_uri(self):
        return self.stream_uri

    def on_read(self,func):
        self.on_read_event = func

    def read(self):

        return self.frame

