from persistencia.Counter import Counter
from persistencia.InfoSaver import InfoSaver
from persistencia.Round import Round

from stress_test.StressTest import StressTest
import random 
import time
from pygame import mixer  # Load the popular external library
import datetime
import os

class Pasat(StressTest):
    def __init__(self, label_operation, label_wrong):
        super().__init__()
        self.__timer = Counter()
        self.__infoSaver = InfoSaver()
        self.__infoDict = {'wrong':[], 'correct':[], 'no response':[]}
        self.__label_operation = label_operation
        self.__label_wrong = label_wrong
        self.userNumber = -1

        mixer.init()

    def __initDirSave(self):
        nameDir =  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        path = '../usr/pasat_information/' + str(self.getId()) + '/'
        self.setPath(path)
        print('ruta de pasat class'+ self.getPath())
        if not os.path.exists(self.getPath()): 
            print("crea dir pasat clase pasat")
            os.makedirs(self.getPath())

    def stop(self):
        self.__stopFlag = True

    def start(self, testing=False):
        self.__stopFlag = False
        self.__label_wrong.setText("")
        self.__infoSaver.setInformationDict(self.__infoDict)
        self.__infoSaver.restartTime()
        if self.isTestingMode():
            #Start video recording
            self.__currentFrame = 0
            self.__initDirSave()
            # self.__pasat_thread = threading.Thread(target=self.__videoRecorder.start, kwargs={'currentFrame':self.__currentFrame})
            self.startRecording(path = '../usr/pasat_information/'+str(self.getId())+'/')

        for indx, round in enumerate(self.getRounds()):
            if self.__runRound(round):
                return 
            
            time.sleep(2)
            self.__label_operation.setText('')
            self.__label_wrong.setText("Fin del round " + str(indx+1))
            time.sleep(1)

        self.__finishTest()
        if self.isTestingMode():
            self.stopRecording()
            self.__infoSaver.save(self.getPath())
            self.__infoDict = {'wrong':[], 'correct':[], 'no response':[]}




    def __runRound(self, round):
        if self.__stopFlag:
            self.__finishTest()
            return True
        
        self.__timer.seconds = round.seconds
        self.__label_wrong.setText("")
        oldNumber = 0
        self.__displayNumber(0)
        self.__playNumber(0)
        time.sleep(round.seconds)
        for _ in range(round.sums):
            oldNumber = self.__runSums(oldNumber)
            if oldNumber == -1:
                return True

    def __runSums(self, oldNumber):
        if self.__stopFlag:
            self.__finishTest()
            return -1
        
        number1 = self.__getRandomNumber()
        self.userNumber = 0
        self.__displayNumber(number1)
        self.__playNumber(number1)
        self.__timer()
        responseFlag = True
        
        while self.__timer.status:
            if self.__stopFlag:
                self.__finishTest()
                return -1
            
            if self.userNumber != 0 and responseFlag:
                responseFlag = False
                if (number1+oldNumber) != self.userNumber:
                    self.__label_wrong.setText('Incorrecto')
                    self.__infoSaver.saveAnswer('wrong', self.getCurrentFrame())
                    # break
                else:
                    self.__label_wrong.setText('Correcto')
                    self.__infoSaver.saveAnswer('correct', self.getCurrentFrame())

        self.__timer.cancel()
        if self.userNumber == 0:
            self.__label_wrong.setText("Sin respuesta")
            self.__infoSaver.saveAnswer('no response', self.getCurrentFrame())

        return number1

                
    def __finishTest(self):
        self.stopRecording()
        self.__label_wrong.setText("Prueba finalizada")
        self.__label_operation.setText('')
    
    def __getRandomNumber(self):
        return random.randint(1,10) 
    
    def __displayNumber(self, number):
        if self.isVisual():
            self.__label_operation.setText('{}'.format(number))

    def __playNumber(self, number):
        if self.isAudio():
            mixer.music.load("media/audios/numbers/{}.mp3".format(number))
            mixer.music.play()
            while mixer.music.get_busy():  # wait for music to finish playing
                time.sleep(1)
        # p = vlc.MediaPlayer("/audios/{}.mp3".format(number))
        # p.play()



