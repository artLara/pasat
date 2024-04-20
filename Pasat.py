from Counter import Counter
from InfoSaver import InfoSaver
from VideoRecorder import VideoRecorder
from AudioRecorder import AudioRecorder
import random 
from Round import Round
import time
import threading
from pygame import mixer  # Load the popular external library
import datetime
import os

class Pasat:
    def __init__(self, label_operation, label_wrong):
        self.__seconds = 3
        self.__timer = Counter()
        self.__infoSaver = InfoSaver()
        self.__videoRecorder = VideoRecorder()
        self.__audioRecorder = AudioRecorder()
        self.__label_operation = label_operation
        self.__label_wrong = label_wrong
        self.__TIMES = 10
        self.audio = False
        self.visual = True
        self.userNumber = -1
        self.rounds = [Round(sums=10, seconds=3)]
        self.testingMode = False #This refers a PASAT test
        self.stop = False
        self.__currentFrame = 0
        self.__path =  ''

        mixer.init()

    def __initDirSave(self):
        nameDir =  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        self.__path = 'information/' + nameDir + '/'
        if not os.path.exists(self.__path): 
            os.makedirs(self.__path)


    def start(self, testing=False):
        self.stop = False
        self.__initDirSave()
        self.__infoSaver.restart()
        self.__label_wrong.setText("")
        self.__infoSaver = InfoSaver()
        if self.testingMode:
            #Start video recording
            self.__currentFrame = 0
            # self.__pasat_thread = threading.Thread(target=self.__videoRecorder.start, kwargs={'currentFrame':self.__currentFrame})
            self.__pasat_thread = threading.Thread(target=self.__videoRecorder.start)
            self.__pasat_thread.start()
            self.__audioRecorder = AudioRecorder()
            self.__pasat_thread_audio = threading.Thread(target=self.__audioRecorder.start)
            self.__pasat_thread_audio.start()

        for indx, round in enumerate(self.rounds):
            if self.__runRound(round):
                return 
            
            time.sleep(1)
            self.__label_operation.setText('')
            self.__label_wrong.setText("Fin del round " + str(indx+1))
            time.sleep(2)

        self.__stop()
        self.__videoRecorder.save(self.__path)
        self.__audioRecorder.save(self.__path)
        self.__infoSaver.save(self.__path)



    def __runRound(self, round):
        if self.stop:
            self.__stop()
            return True
        
        self.__timer.seconds = round.seconds
        self.__label_wrong.setText("")
        oldNumber = 0
        for _ in range(round.sums):
            oldNumber = self.__runSums(oldNumber)
            if oldNumber == -1:
                return True

    def __runSums(self, oldNumber):
        if self.stop:
            self.__stop()
            return -1
        
        number1 = self.getRandomNumber()
        self.userNumber = 0
        self.displayNumber(number1)
        self.playNumber(number1)
        self.__timer()
        while self.__timer.status:
            if self.stop:
                self.__stop()
                return -1
            
            if self.userNumber != 0:
                if (number1+oldNumber) != self.userNumber:
                    self.__label_wrong.setText('Wrong!!!')
                    self.__infoSaver.saveAnswer('wrong', self.__videoRecorder.getCurrentFrame())
                    break
                self.__label_wrong.setText('Correct!!!')
                self.__infoSaver.saveAnswer('correct', self.__videoRecorder.getCurrentFrame())

                break

        self.__timer.cancel()
        if self.userNumber == 0:
            self.__label_wrong.setText("Sin respuesta")
            self.__infoSaver.saveAnswer('no response', self.__videoRecorder.getCurrentFrame())

        return number1

                
    def __stop(self):
        self.__videoRecorder.stop()
        self.__audioRecorder.stop()
        self.__label_wrong.setText("Prueba finalizada")
        self.__label_operation.setText('')
    
    def getRandomNumber(self):
        return random.randint(1,10) 
    
    def displayNumber(self, number):
        if self.visual:
            self.__label_operation.setText('{}'.format(number))

    def playNumber(self, number):
        if self.audio:
            mixer.music.load("audios/{}.mp3".format(number))
            mixer.music.play()
            while mixer.music.get_busy():  # wait for music to finish playing
                time.sleep(1)
        # p = vlc.MediaPlayer("/audios/{}.mp3".format(number))
        # p.play()



