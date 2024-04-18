from pasat_ui import *
from PyQt5.QtWidgets import*
from Pasat import Pasat
from Round import Round
import threading

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        #Event connection
        self.pushButton_start.clicked.connect(self.__start)
        self.pushButton_1.clicked.connect(self.button1)
        self.pushButton_2.clicked.connect(self.button2)
        self.pushButton_3.clicked.connect(self.button3)
        self.pushButton_4.clicked.connect(self.button4)
        self.pushButton_5.clicked.connect(self.button5)
        self.pushButton_6.clicked.connect(self.button6)
        self.pushButton_7.clicked.connect(self.button7)
        self.pushButton_8.clicked.connect(self.button8)
        self.pushButton_9.clicked.connect(self.button9)
        self.pushButton_10.clicked.connect(self.button10)
        self.pushButton_11.clicked.connect(self.button11)
        self.pushButton_12.clicked.connect(self.button12)
        self.pushButton_13.clicked.connect(self.button13)
        self.pushButton_14.clicked.connect(self.button14)
        self.pushButton_15.clicked.connect(self.button15)
        self.pushButton_16.clicked.connect(self.button16)
        self.pushButton_17.clicked.connect(self.button17)
        self.pushButton_18.clicked.connect(self.button18)
        self.pushButton_19.clicked.connect(self.button19)
        self.pushButton_20.clicked.connect(self.button20)
        self.spinBoxRounds.valueChanged.connect(self.roundsValueChange)


        #Pasat test
        self.__pasat = Pasat(self.label_operation, self.label_wrong)

    def __start(self):
        rounds = []
        for i in range(self.spinBoxRounds.value()):
            sums = int(self.tableDatos.item(i, 0).text())
            seconds = int(self.tableDatos.item(i, 1).text())
            r = Round(sums=sums, seconds=seconds)
            rounds.append(r)

        self.__pasat.rounds = rounds
        self.__pasat.visual = self.checkBox_visual.isChecked()
        self.__pasat.audio = self.checkBox_auditivo.isChecked()

        x = threading.Thread(target=self.__pasat.start)
        x.start()
        
    def __del__(self):
        pass

    def roundsValueChange(self):
        #Se dan el numero de filas solicitadas
        self.tableDatos.setRowCount(self.spinBoxRounds.value())
        #Se agregan los nombres a las filas
        rowsNames = []
        for i in range(self.spinBoxRounds.value()):
            rowsNames.append('Round ' + str(i + 1))

        self.tableDatos.setVerticalHeaderLabels(rowsNames)
        self.rellenarTabla()

    def rellenarTabla(self):
        for i in range(self.spinBoxRounds.value()):#Rows
            # for j in range(self.spinBoxNumeroClases.value() * self.spinBoxDimensionPatron.value()):#Coulumns
            for j in range(2):#Coulumns
            
                item = self.tableDatos.takeItem(i, j)
                if item is None:  
                    self.tableDatos.setItem(i, j, QTableWidgetItem(''))
                else: 
                    self.tableDatos.setItem(i, j, item)


    def button1(self):
        self.__pasat.userNumber = 1 

    def button2(self):
        self.__pasat.userNumber = 2 

    def button3(self):
        self.__pasat.userNumber = 3 

    def button4(self):
        self.__pasat.userNumber = 4 

    def button5(self):
        self.__pasat.userNumber = 5 

    def button6(self):
        self.__pasat.userNumber = 6 

    def button7(self):
        self.__pasat.userNumber = 7 

    def button8(self):
        self.__pasat.userNumber = 8

    def button9(self):
        self.__pasat.userNumber = 9 

    def button10(self):
        self.__pasat.userNumber = 10

    def button11(self):
        self.__pasat.userNumber = 11 

    def button12(self):
        self.__pasat.userNumber = 12

    def button13(self):
        self.__pasat.userNumber = 13 

    def button14(self):
        self.__pasat.userNumber = 14 

    def button15(self):
        self.__pasat.userNumber = 15 

    def button16(self):
        self.__pasat.userNumber = 16

    def button17(self):
        self.__pasat.userNumber = 17 

    def button18(self):
        self.__pasat.userNumber = 18 

    def button19(self):
        self.__pasat.userNumber = 19 

    def button20(self):
        self.__pasat.userNumber = 20

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
