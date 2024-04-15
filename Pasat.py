from Counter import Counter
import random 
 

class Pasat:
    def __init__(self, label_operation, label_wrong):
        self.__seconds = 3
        self.__timer = Counter()
        self.__label_operation = label_operation
        self.__label_wrong = label_wrong
        self.__TIMES = 10
        self.userNumber = -1

    def start(self, testing=False):
        if not testing:
            #Start video recording
            pass

        oldNumber = 0
        self.__label_wrong.setText("")

        for _ in range(self.__TIMES):
            number1 = self.getRandomNumber()
            self.userNumber = -1
            self.__label_operation.setText('{}'.format(number1))
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

        self.__label_wrong.setText("Finish")
                

    def getRandomNumber(self):
        return random.randint(1,10) 



