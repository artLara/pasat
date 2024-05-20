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
import threading

class NBack(StressTest):
    def __init__(self, label_matrix, 
                 label_letter, label_nback_title, 
                 label_message_matrix, 
                 label_message_letter):
        super().__init__()
        self.__timer = Counter()
        self.__infoSaver = InfoSaver()
        self.__infoDict = {'incorrect':[], 'correct':[], 'no response':[]}
        self.__label_matrix = label_matrix
        self.__label_letter = label_letter
        self.__label_nback_title = label_nback_title
        self.__label_message_matrix = label_message_matrix
        self.__label_message_letter = label_message_letter
        
        self.__n = 1
        self.__matrixQueue = None
        self.userNumber = -1
        self.__shiftR = False
        self.__shiftL = False

        mixer.init()

    def __initDirSave(self):
        nameDir =  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        path = '../usr/nback_information/' + str(self.getId()) + '/'
        self.setPath(path)
        if not os.path.exists(self.getPath()): 
            os.makedirs(self.getPath())

    def __initQueue(self, n, testNumber):
        self.__matrixQueue = Queue()
        for _ in range(n):
            self.__matrixQueue.put(None)
            if testNumber == 3:
                self.__matrixQueue.put(None)


    def __keyboardListener(self, key):
        if key == Key.shift_r:
            self.__shiftR = True

        if key == Key.shift_l:
            self.__shiftL = True
            
    def stop(self):
        self.__stopFlag = True

    def start(self, testing=False):
        self.__stopFlag = False
        listener = keyboard.Listener(
            on_press=self.__keyboardListener)
        listener.start()
        self.__infoSaver.setInformationDict(self.__infoDict)
        self.__infoSaver.restartTime()

        if self.isTestingMode():
            self.__initDirSave()
            self.startRecording()

        for indx, round in enumerate(self.getRounds()):
            if self.__runRound(round):
                return 
        
        time.sleep(1.5)
        self.__finishTest()
        if self.isTestingMode():
            self.stopRecording()
            self.__infoSaver.save(self.getPath())

    def __runRound(self, round):
        if self.__stopFlag:
            self.__finishTest()
            return True
        
        self.__timer.seconds = round.seconds
        self.__label_nback_title.setText("{}-Back".format(round.n))
        if self.__runTest(round, self.__runQuestion1, 1, self.__label_message_matrix):
            return True

        if self.__runTest(round, self.__runQuestion2, 2, self.__label_message_letter):
            return True
        
        if self.__runTest(round, self.__runQuestion3, 3):
            return True
        
        
    def __checkAnswer3(self, response, duration=1):
        lastLetter = self.__matrixQueue.queue[-2]
        firstLetter = self.__matrixQueue.get()
        lastCoord = self.__matrixQueue.queue[-1]
        firstCoord = self.__matrixQueue.get()

        if response == 0:
            self.__label_message_letter.setText('')
            self.__label_message_matrix.setText('')
            self.__infoSaver.saveAnswer('no response', self.getCurrentFrame())
            print('Sin respuesta')

        if response == 1 and lastLetter == firstLetter and self.isShowCorrect():
            self.__label_message_letter.setText('Correcto')
            self.__infoSaver.saveAnswer('correct', self.getCurrentFrame())
        
        if response == 1 and lastLetter != firstLetter and self.isShowIncorrect():
            self.__label_message_letter.setText('Incorrecto')
            self.__infoSaver.saveAnswer('incorrect', self.getCurrentFrame())

        if response == 2 and lastCoord == firstCoord and self.isShowCorrect():
            self.__label_message_matrix.setText('Correcto')
            self.__infoSaver.saveAnswer('correct', self.getCurrentFrame())
        
        if response == 2 and lastCoord != firstCoord and self.isShowIncorrect():
            self.__label_message_matrix.setText('Incorrecto')
            self.__infoSaver.saveAnswer('incorrect', self.getCurrentFrame())

        if response == 3 and lastCoord == firstCoord and self.isShowCorrect():
            self.__label_message_matrix.setText('Correcto')
            self.__infoSaver.saveAnswer('correct', self.getCurrentFrame())
        
        if response == 3 and lastCoord != firstCoord and self.isShowIncorrect():
            self.__label_message_matrix.setText('Incorrecto')
            self.__infoSaver.saveAnswer('incorrect', self.getCurrentFrame())

        if response == 3 and lastLetter == firstLetter and self.isShowCorrect():
            self.__label_message_letter.setText('Correcto')
            self.__infoSaver.saveAnswer('correct', self.getCurrentFrame())
        
        if response == 3 and lastLetter != firstLetter and self.isShowIncorrect():
            self.__label_message_letter.setText('Incorrecto')
            self.__infoSaver.saveAnswer('incorrect', self.getCurrentFrame())

        time.sleep(duration)

    def __checkAnswer(self, response, testNmuber, label_message=None, duration=1):
        if testNmuber == 3:
            self.__checkAnswer3(response=response,
                                duration=duration)
            
            return

        lastElement = self.__matrixQueue.queue[-1]
        firstElement = self.__matrixQueue.get()

        if response == 1 and lastElement == firstElement and self.isShowCorrect():
            label_message.setText('Correcto')
            self.__infoSaver.saveAnswer('correct', self.getCurrentFrame())
        
        if response == 1 and lastElement != firstElement and self.isShowIncorrect():
            label_message.setText('Incorrecto')
            self.__infoSaver.saveAnswer('incorrect', self.getCurrentFrame())

        if response == 0:
            label_message.setText('')
            self.__infoSaver.saveAnswer('no response', self.getCurrentFrame())
            print('Sin respuesta')
        time.sleep(duration)

    def __finishTest(self):
        self.stopRecording()
        self.__label_nback_title.setText("Prueba finalizada")
        self.__label_matrix.clear()
        self.__label_letter.setText('')
        self.__label_message_matrix.setText('')
        self.__label_message_letter.setText('')
        self.__infoDict = {'incorrect':[], 'correct':[], 'no response':[]}

    
    def __getRandomCoordinate(self):
        return (random.randint(0,1), random.randint(0,1))

    def __getRandomLetter(self):
        self.__lettersDict = {0:'C',
                              1:'H',
                              2:'K',
                              3:'N',
                              4:'R',
                              5:'W',
                              6:'X',
                              7:'Y'
                              }
        
        return self.__lettersDict[random.randint(0,7)]
    
    def __showImage(self, coordinate):
        imageName = "media/images/{}{}.png".format(coordinate[0], coordinate[1])
        self.__label_matrix.setPixmap(QPixmap(imageName))
    
    def __displayLetter(self, letter):
        if self.isVisual():
            self.__label_letter.setText('{}'.format(letter))

    def __playLetter(self, letter):
        if self.isAudio():
            mixer.music.load("media/audios/letters/{}.mp3".format(letter))
            mixer.music.play()
            while mixer.music.get_busy():  # wait for music to finish playing
                time.sleep(1)

    def __questionTransition(self, testNumber, seconds=0):
        imageName = "media/images/blank.png"
        if testNumber == 1 or testNumber == 3:
            self.__label_matrix.setPixmap(QPixmap(imageName))

        if testNumber == 2:
            self.__label_matrix.clear()
        
        self.__label_letter.setText('')
        self.__label_message_matrix.setText('')
        self.__label_message_letter.setText('')
        time.sleep(seconds)
    
    def __runTest(self, round, questionFuntion, testNumber, label_message=None):
        self.__label_nback_title.setText('Inicia test {}'.format(testNumber))
        self.__initQueue(round.n, testNumber)
        for _ in range(round.sums):
            response = questionFuntion()
            if response == -1:
                return True
            self.__checkAnswer(response, testNumber, label_message)
            self.__questionTransition(testNumber, round.transition)            

        time.sleep(1)
        self.__label_nback_title.setText('Fin test {}'.format(testNumber))
        self.__questionTransition(testNumber, round.transition)
        self.__label_matrix.clear()        
        time.sleep(1.5)

    def __runQuestion1(self):
        """
        Number representation:
            -1: Cancel or error
            0: Shift did not press
            1: shift pressed
        """
        if self.__stopFlag:
            self.__finishTest()
            return -1
        
        coordinate = self.__getRandomCoordinate()
        self.__matrixQueue.put(coordinate)
        self.__showImage(coordinate)
        self.__timer()
        self.__shiftR = False

        while self.__timer.status:
            if self.__stopFlag:
                self.__finishTest()
                return -1
            
            if self.__shiftR:
                self.__timer.cancel()
                return 1

        self.__timer.cancel()
        return 0 

    def __runQuestion2(self):
        """
        Number representation:
            -1: Cancel or error
            0: Shift did not press
            1: shift pressed
        """
        if self.__stopFlag:
            self.__finishTest()
            return -1
        
        letter = self.__getRandomLetter()
        self.__matrixQueue.put(letter)
        self.__displayLetter(letter)
        self.__audioLetter_thread = threading.Thread(target=self.__playLetter, kwargs={'letter':letter})
        self.__audioLetter_thread.start()
        # self.__playLetter(letter)
        self.__timer()
        self.__shiftL = False
        while self.__timer.status:
            if self.__stopFlag:
                self.__finishTest()
                return -1
            
            if self.__shiftL:
                self.__timer.cancel()
                return 1

        self.__timer.cancel()
        return 0 
    
    def __runQuestion3(self):
        """
        Number representation:
            -1: Cancel or error
            0: Shift did not press
            1: shift pressed
        """
        if self.__stopFlag:
            self.__finishTest()
            return -1
        
        letter = self.__getRandomLetter()
        coordinate = self.__getRandomCoordinate()
        self.__displayLetter(letter)
        self.__showImage(coordinate)
        self.__audioLetter_thread = threading.Thread(target=self.__playLetter, kwargs={'letter':letter})
        self.__audioLetter_thread.start()
        self.__matrixQueue.put(letter)
        self.__matrixQueue.put(coordinate)
        self.__timer()
        self.__shiftL = False
        self.__shiftR = False
        response = [0,0]
        while self.__timer.status:
            if self.__stopFlag:
                self.__finishTest()
                return -1
            
            if self.__shiftL:
                self.__shiftL = False
                response[0] = 1 
            
            if self.__shiftR:
                self.__shiftR = False
                response[1] = 2 
                
            
        self.__timer.cancel()
        return response[0] + response[1] 
    