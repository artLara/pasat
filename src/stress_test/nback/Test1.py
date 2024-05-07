

class Tests():
    def __init__(self, label_matrix, label_letter, label_nback_title, label_message_matrix):
        super().__init__()
        self.__timer = Counter()
        self.__infoSaver = InfoSaver()
        self.__infoDict = {'wrong':[], 'correct':[], 'no response':[]}
        self.__label_matrix = label_matrix
        self.__label_letter = label_letter
        self.__label_nback_title = label_nback_title
        self.__label_message_matrix = label_message_matrix
        self.__n = 1
        self.__matrixQueue = None
        self.userNumber = -1
        self.__KEY_RESPONSE = Key.shift_r
        self.__correctKey = False
        mixer.init()

    def startTest1(self):
        self.__initQueue(round.n)
        for _ in range(1,round.sums+1):
            self.__questionTransition()
            self.__label_message_matrix.setText('')
            response = self.__runQuestion()
            if response == -1:
                return True
            
            self.__checkAnswer(response)

        time.sleep(1.5)
        self.__label_message_matrix.setText('Fin test 1')
        self.__questionTransition()
        time.sleep(1.5)

    def __runQuestion(self):
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
        self.__correctKey = False
        print('New question')

        while self.__timer.status:
            if self.__stopFlag:
                self.__finishTest()
                return -1
            
            if self.__correctKey:
                print('Key pressed!!!')
                self.__timer.cancel()
                return 1

        self.__timer.cancel()

        return 0 

    def __keyboardListener(self, key):
        if key == self.__KEY_RESPONSE:
            self.__correctKey = True

    