import time
import json

class InfoSaver:
    def __init__(self):
        self.__timeStart = time.time()
        self.__information = None
    
    def setInformationDict(self, info):
        self.__information = info

    def restartTime(self):
        self.__timeStart = time.time()

    def saveAnswer(self, answer, frame=-1):
        current_time = time.time()
        self.__information[answer].append((current_time-self.__timeStart, frame))
        # self.__wrongList.append((answer, current_time-self.__timeStart, frame))

    def displayInfo(self):
        print('Wrong moments:')
        for i in self.__information:
            print(i)

    def save(self, path):
        with open(path + "info.json", "w") as outfile: 
            json.dump(self.__information, outfile)
