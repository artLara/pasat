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
from numpy import random as randomNP

class NBack(StressTest):
    def __init__(self, label_matrix, label_letter, label_nback_title, label_message_matrix, label_message_letter):
        super().__init__()
        self.__timer = Counter()
        self.__infoSaver = InfoSaver()
        self.__infoDict = {'incorrect':[], 'correct':[], 'no response':[]}
        self.__label_matrix = label_matrix
        self.__label_letter = label_letter
        self.__label_nback_title = label_nback_title
        self.__label_message_matrix = label_message_matrix
        self.__label_message_letter = label_message_letter
        self.__MAX_QUESTIONS = 0
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
            # self.startRecording()
            self.startRecording(path = '../usr/nback_information/'+str(self.getId())+'/')

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
        time.sleep(2)
        if self.__runTest(round, self.__runQuestion2, 2, self.__label_message_letter):
            return True

        if self.__runTest(round, self.__runQuestion1, 1, self.__label_message_matrix):
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

    # def __getRandomLetter(self):
    #     self.__lettersDict = {0:'C',
    #                           1:'H',
    #                           2:'K',
    #                           3:'N',
    #                           4:'R',
    #                           5:'W',
    #                           6:'X',
    #                           7:'Y'
    #                           }
        
    #     return self.__lettersDict[random.randint(0,7)]
    
    def __getRandomLetter(self):
        self.__lettersDict = {0:'c',
                              1:'h',
                              2:'r',
                              3:'w',
                              4:'x',
                              }
        
        return self.__lettersDict[random.randint(0,4)]

    ##
    def __initSequenceCoord(self,testNumber, size):
        if testNumber == 1:
            seed = 44
        if testNumber == 3:
            seed = 46

        # N = 22
        # R = 1
        
        random.seed(seed) #42

        generate_tuples = lambda N, R: [(random.randint(0, 1), random.randint(0, 1)) for _ in range(size)]

        self.__rand_coord = generate_tuples(size, 1)  
        print(self.__rand_coord)  


    def __initSequence(self, testNumber, size):
        if testNumber == 2:
            seed = 44

        if testNumber == 3:
            seed = 46
        
        randomNP.seed(seed)
        self.__rand_list = randomNP.choice(['x', 'w', 'r', 'h','c'], p=[0.2, 0.2, 0.2, 0.2,0.2], size=(size)).tolist()

    def __getRandomCoord(self):
        return self.__rand_coord.pop()

    def __getRandomSequence(self):
        return self.__rand_list.pop()
    
    def __showImage(self, coordinate):
        imageName = "media/images/{}{}.png".format(coordinate[0], coordinate[1])
        self.__label_matrix.setPixmap(QPixmap(imageName))
    
    def __displayLetter(self, letter):
        if self.isVisual():
            self.__label_letter.setText('{}'.format(letter.upper()))

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
        tipo_test=["visual","auditivo","dual"]
        self.__label_nback_title.setText('Test {}'.format(tipo_test[testNumber-1]))
        self.__initQueue(round.n, testNumber)
        if testNumber != 1:
            self.__initSequence(testNumber, round.sums)
        
        ###
        if testNumber != 2:
            self.__initSequenceCoord(testNumber,round.sums)
        
        for _ in range(round.sums): #num de preguntas
            response = questionFuntion(testNumber, label_message)
            if response == -1:
                return True
            self.__questionTransition(testNumber, round.transition)  
                      

        time.sleep(1)
        self.__label_nback_title.setText('Fin test {}'.format(tipo_test[testNumber-1]))
        self.__questionTransition(testNumber, round.transition)
        self.__label_matrix.clear()        
        time.sleep(1.5)

    def __runQuestion1(self, testNumber, label_message):
        """
        Number representation:
            -1: Cancel or error
            0: Shift did not press
            1: shift pressed
        """
        if self.__stopFlag:
            self.__finishTest()
            return -1
        
        # coordinate = self.__getRandomCoordinate()
        coordinate = self.__getRandomCoord()
        print(coordinate)
        self.__matrixQueue.put(coordinate)
        self.__showImage(coordinate)
        self.__timer()
        self.__shiftR = False
        response = 0
        checkAnswerFlag = True


        while self.__timer.status:
            if self.__stopFlag:
                self.__finishTest()
                response = -1
                break
            
            if self.__shiftR:
                response=1
                self.__shiftR = False
                print('Shift-R pressed')
                if not self.isWaitTimeResponse():
                    self.__timer.cancel()
                    break 

            if response == 1 and checkAnswerFlag:
                checkAnswerFlag = False
                self.__checkAnswer(response, testNumber, label_message)

        self.__timer.cancel()
        return response

    def __runQuestion2(self, testNumber, label_message):
        """
        Number representation:
            -1: Cancel or error
            0: Shift did not press
            1: shift pressed
        """
        if self.__stopFlag:
            self.__finishTest()
            return -1
        

        # letter = self.__getRandomLetter()
        letter = self.__getRandomSequence()
        self.__matrixQueue.put(letter)
        self.__displayLetter(letter)
        self.__audioLetter_thread = threading.Thread(target=self.__playLetter, kwargs={'letter':letter})
        self.__audioLetter_thread.start()
        #self.__playLetter(letter)
        self.__timer()
        self.__shiftL = False
        response = 0
        checkAnswerFlag = True

        while self.__timer.status:
            if self.__stopFlag:
                self.__finishTest()
                response = -1
                break
                # return -1
            
            if self.__shiftL :#and response != 1:
                response = 1
                self.__shiftL = False
                print('Shift-L pressed')
                if not self.isWaitTimeResponse():
                    self.__timer.cancel()
                    self.__checkAnswer(response, testNumber, label_message)
                    break 
                # return 1
            if response == 1 and checkAnswerFlag:
                checkAnswerFlag = False
                self.__checkAnswer(response, testNumber, label_message)

        self.__timer.cancel()
        return response
    
    def __runQuestion3(self, testNumber, label_message):
        """
        Number representation:
            -1: Cancel or error
            0: Shift did not press
            1: shift pressed
        """
        if self.__stopFlag:
            self.__finishTest()
            return -1
        
        letter = self.__getRandomSequence()
        # coordinate = self.__getRandomCoordinate()
        coordinate = self.__getRandomCoord()
        print(coordinate)
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
        checkAnswerFlag1 = True
        checkAnswerFlag2 = True


        while self.__timer.status:
            if self.__stopFlag:
                self.__finishTest()
                return -1
            
            if self.__shiftL:
                self.__shiftL = False
                print('Shift-L pressed')
                response[0] = 1 
            
            if self.__shiftR:
                self.__shiftR = False
                print('Shift-R pressed')
                response[1] = 2 
                
            
        self.__timer.cancel()
        self.__checkAnswer(response[0] + response[1], testNumber, label_message)
        return response[0] + response[1] 
    