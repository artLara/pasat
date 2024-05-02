import cv2
import os

class VideoRecorder:
    def __init__(self):
        self.__path = 'video/'
        self.__frames = []
        self.stopRecording = False
        self.__currentFrame = 0
        
    def start(self):
        self.__frames = []
        self.__currentFrame = 0
        self.stopRecording = False
        vid = cv2.VideoCapture(0)
        success, frame = vid.read()
        while success and not self.stopRecording: 
            self.__frames.append(frame)
            success, frame = vid.read()
            self.__currentFrame += 1

    def stop(self):
        self.stopRecording = True

    def getCurrentFrame(self):
        return self.__currentFrame

    def save(self, path):
        path_images = path+'images/'
        if not os.path.exists(path_images): 
            os.makedirs(path_images)

        for ind, frame in enumerate(self.__frames):
            cv2.imwrite(path_images + str(ind) + ".jpg", frame)
        