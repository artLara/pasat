from persistencia.Round import Round

class StressTest:
    def __ini__(self):
        self.__rounds = [Round(sums=10, seconds=3)]
        self.__stopFlag = False
        self.__audio = False
        self.__visual = True
        self.__testingMode = False #This refers a stress test

    
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
