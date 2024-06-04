import cv2
import os

class VideoRecorder:
    def __init__(self):
        self.__path = ''
        self.__frames = []
        self.__stopRecording = False
        self.__currentFrame = 0
        self.__id = 0
        self.__listFlag = False

    def setPath(self, path):
        self.__path = path

    def setListFlag(self, flag):
        self.__listFlag = True
        
        
    def start(self):
        path_images = self.__path + 'images/'
        if not os.path.exists(path_images): 
            os.makedirs(path_images)

        self.__frames = []
        self.__currentFrame = 0
        self.__stopRecording = False
        vid = cv2.VideoCapture(0)
        success, frame = vid.read()
        while success and not self.__stopRecording: 
            if self.__listFlag:
                self.__frames.append(frame)
            
            else:
                cv2.imwrite(path_images + str(self.__currentFrame) + ".jpg", frame)
            
            success, frame = vid.read()
            self.__currentFrame += 1


    def stop(self):
        self.__stopRecording = True

    def getCurrentFrame(self):
        return self.__currentFrame
    
    def saveBatchImage(self):
        path_images = path+'images/'
        if not os.path.exists(path_images): 
            os.makedirs(path_images)

        for ind, frame in enumerate(self.__frames):
            cv2.imwrite(path_images + str(ind) + ".jpg", frame)

    def initDir(self):
        path_images = +'images/'
        if not os.path.exists(path_images): 
            os.makedirs(path_images)

    def save(self, path):
        path_images = path+'images/'
        if not os.path.exists(path_images): 
            os.makedirs(path_images)

        for ind, frame in enumerate(self.__frames):
            cv2.imwrite(path_images + str(ind) + ".jpg", frame)
    
    def saveRelax1(self, path,index):
        if index == 1:
            path_images = path+'relax/'
        elif index == 2:
            path_images = path+'Instrucciones/'
        
        if not os.path.exists(path_images): 
            os.makedirs(path_images)

        for ind, frame in enumerate(self.__frames):
            cv2.imwrite(path_images + str(ind) + ".jpg", frame)
        