from persistencia.Counter import Counter
from persistencia.InfoSaver import InfoSaver
from persistencia.Round import Round
from stress_test.StressTest import StressTest
import random 
import time
from pygame import mixer  # Load the popular external library
import datetime
import os
from queue import Queue
from PyQt5.QtGui import QPixmap 
from pynput import keyboard
from pynput.keyboard import Key, Listener

class NBack(StressTest):
    def __init__(self, label_matrix, label_letter, label_nback_title):
        super().__init__()
        self.__timer = Counter()
        self.__infoSaver = InfoSaver()
        self.__infoDict = {'wrong':[], 'correct':[], 'no response':[]}
        self.__label_matrix = label_matrix
        self.__label_letter = label_letter
        self.__label_nback_title = label_nback_title
        self.__n = 1
        self.__matrixQueue = None
        self.userNumber = -1
        self.__KEY_RESPONSE = Key.shift_r
        self.__correctKey = False
        mixer.init()

    def __initDirSave(self):
        nameDir =  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        path = '../usr/pasat_information/' + nameDir + '/'
        self.setPath(path)
        if not os.path.exists(self.getPath()): 
            os.makedirs(self.getPath())

    def __keyboardListener(self, key):
        if key == self.__KEY_RESPONSE:
            self.__correctKey = True
            
    def stop(self):
        self.__stopFlag = True

    def start(self, testing=False):
        print('Nback started')
        self.__stopFlag = False
        self.__infoSaver.setInformationDict(self.__infoDict)
        self.__infoSaver.restartTime()
        # with Listener(on_press = self.__keyboardListener) as listener:   
        #     listener.join()

        listener = keyboard.Listener(
            on_press=self.__keyboardListener)
        listener.start()

        if self.isTestingMode():
            self.__initDirSave()
            self.startRecording()

        for indx, round in enumerate(self.getRounds()):
            if self.__runRound(round):
                return 
            
        #     time.sleep(2)
        #     self.__label_operation.setText('')
        #     self.__label_wrong.setText("Fin del round " + str(indx+1))
        #     time.sleep(1)

        # self.__finishTest()
        # if self.isTestingMode():
        #     self.stopRecording()
        #     self.__infoSaver.save(self.getPath())



    def __runRound(self, round):
        if self.__stopFlag:
            self.__finishTest()
            return True
        
        self.__timer.seconds = round.seconds
        self.__label_nback_title.setText("{}-Back".format(round.n))
        # self.__label_wrong.setText("")
        # oldNumber = 0
        # self.__playNumber(0)
        # time.sleep(round.seconds)
        self.__test1(round.sums)
        # for _ in range(round.sums):
        #     oldNumber = self.__runSums(oldNumber)
        #     if oldNumber == -1:
        #         return True
            
    def __test1(self, qNumber):
        self.__initQueue()
        # print('NUmber of questions:', str(qNumber))
        for _ in range(1,qNumber+1):
            # print('Call run qestion')
            response = self.__runQuestion()
            # print('Return run qestion')

            # n_coordinate = self.__matrixQueue.get()
            # current_coordinate = self.__matrixQueue.queue[-1]
            # if current_coordinate == n_coordinate:
            #     if response == 1:
            #         #Say correct
            #         pass
            #     else:
            #         #Say incorrect
            #         pass
            
            # else:
            #     if response == 0:
            #         #Say correct
            #         pass
            #     else:
            #         #Say incorrect
            #         pass


    
    def __initQueue(self):
        self.__matrixQueue = Queue(maxsize = self.__n + 2)
        for _ in range(self.__n):
            self.__matrixQueue.put((-1,-1))
        #Get shift key
            

    def __runQuestion(self):
        """
        Number representation:
            -1: Cancel or error
            0: Not equals
            1: equals
        """
        if self.__stopFlag:
            self.__finishTest()
            return -1
        
        coordinate = self.__getRandomCoordinate()
        # self.__matrixQueue.put(coordinate)
        self.__showImage(coordinate)
        self.__timer()
        self.__correctKey = False
        print('New question')

        while self.__timer.status:
            if self.__stopFlag:
                self.__finishTest()
                return -1
            
            # if keyboard.is_pressed('q'):
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            if self.__correctKey:
                print('Key pressed!!!')
                self.__timer.cancel()
                return 1

        self.__timer.cancel()

        return 0 

                
    def __finishTest(self):
        self.stopRecording()
        self.__label_wrong.setText("Prueba finalizada")
        self.__label_operation.setText('')
    
    def __getRandomCoordinate(self):
        return (random.randint(0,2), random.randint(0,2))

    def __getRandomLetter(self):
        self.__lettersDict = {0:'c',
                              1:'h',
                              2:'k',
                              3:'n',
                              4:'r',
                              5:'w',
                              6:'x',
                              7:'y'
                              }
        
        return self.__lettersDict[random.randint(0,7)]
    
    def __showImage(self, coordinate):
        imageName = "media/images/{}{}.png".format(coordinate[0], coordinate[1])
        self.__label_matrix.setPixmap(QPixmap(imageName))
    
    def __displayNumber(self, number):
        if self.isVisual():
            self.__label_operation.setText('{}'.format(number))

    def __playNumber(self, number):
        if self.isAudio():
            mixer.music.load("media/audios/{}.mp3".format(number))
            mixer.music.play()
            while mixer.music.get_busy():  # wait for music to finish playing
                time.sleep(1)
        # p = vlc.MediaPlayer("/audios/{}.mp3".format(number))
        # p.play()

    def setN(self, n):
        self.__n = n


    def __questionTransition(self, seconds=1):
        imageName = "media/images/blank.png"
        self.__label_matrix.setPixmap(QPixmap(imageName))
        time.sleep(seconds)
