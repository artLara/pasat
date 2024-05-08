from persistencia.Round import Round
from recorder.VideoRecorder import VideoRecorder
from recorder.AudioRecorder import AudioRecorder
import threading
class StressTest:
    def __init__(self):
        self.__rounds = [Round(sums=10, seconds=3)]
        self.__stopFlag = False
        self.__audio = False
        self.__visual = True
        self.__testingMode = False #This refers a stress test
        self.__videoRecorder = VideoRecorder()
        self.__audioRecorder = AudioRecorder()
        self.__path = ''
        self.__id = 0

    
    def start(self):
        pass

    def stop(self):
        pass

    def setTestingMode(self, mode):
        self.__testingMode = mode #This refers a stress test

    def isTestingMode(self):
        return self.__testingMode

    def setRounds(self, rounds):
        self.__rounds = rounds

    def getRounds(self):
        return self.__rounds

    def isAudio(self):
        return self.__audio
    
    def isVisual(self):
        return self.__visual

    def setAudio(self, flag):
        self.__audio = flag

    def setVisual(self, flag):
        self.__visual = flag

    def setPath(self,path):
        self.__path = path

    def getPath(self):
        return self.__path
    
    def setId(self, id):
        self.__id = id

    def getId(self):
        return self.__id


    def startRecording(self):
        self.__video_thread = threading.Thread(target=self.__videoRecorder.start)
        self.__video_thread.start()
        self.__audioRecorder = AudioRecorder()
        self.__audio_thread = threading.Thread(target=self.__audioRecorder.start)
        self.__audio_thread.start()   

    def stopRecording(self):
        self.__videoRecorder.stop()
        self.__audioRecorder.stop()
        self.__videoRecorder.save(self.__path)
        self.__audioRecorder.save(self.__path)

    def getCurrentFrame(self):
        return self.__videoRecorder.getCurrentFrame()
    
