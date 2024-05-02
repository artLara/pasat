import time
import json
import datetime

class InfoSaver:
    def __init__(self):
        self.__timeStart = time.time()
        self.__information = {'wrong':[], 'correct':[], 'no response':[]}
        self.__path = 'information/'
    
    def restart(self):
        self.__information = {'wrong':[], 'correct':[], 'no response':[]}

    def saveAnswer(self, answer, frame=-1):
        current_time = time.time()
        self.__information[answer].append((current_time-self.__timeStart, frame))
        # self.__wrongList.append((answer, current_time-self.__timeStart, frame))

    def displayInfo(self):
        print('Wrong moments:')
        for i in self.__information:
            print(i)

    def save(self, name):
        with open(name + "info.json", "w") as outfile: 
            json.dump(self.__information, outfile)
