from Counter import Counter
import random 
from Round import Round
import time
from pygame import mixer  # Load the popular external library


class Pasat:
    def __init__(self, label_operation, label_wrong):
        self.__seconds = 3
        self.__timer = Counter()
        self.__label_operation = label_operation
        self.__label_wrong = label_wrong
        self.__TIMES = 10
        self.audio = False
        self.visual = True
        self.userNumber = -1
        self.rounds = [Round(sums=10, seconds=3)]
        mixer.init()



    def start(self, testing=False):
        if not testing:
            #Start video recording
            pass

        oldNumber = 0
        self.__label_wrong.setText("")

        for indx, round in enumerate(self.rounds):
            self.__timer.seconds = round.seconds
            self.__label_wrong.setText("")
            oldNumber = 0

            for _ in range(round.sums):
                number1 = self.getRandomNumber()
                self.userNumber = -1
                self.displayNumber(number1)
                self.playNumber(number1)
                self.__timer()
                while self.__timer.status:
                    # print('Waiting...')
                    if self.userNumber != -1:
                        if (number1+oldNumber) != self.userNumber:
                            self.__label_wrong.setText('Wrong!!!')
                            break
                        self.__label_wrong.setText('Correct!!!')
                        break
                self.__timer.cancel()
                oldNumber = number1

                if self.userNumber == -1:
                    self.__label_wrong.setText("Sin respuesta")
            self.__label_operation.setText('')
            self.__label_wrong.setText("Fin del round" + str(indx+1))
            time.sleep(2)

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
        # p = vlc.MediaPlayer("/audios/{}.mp3".format(number))
        # p.play()



