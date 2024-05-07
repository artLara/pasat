from guis.pasat_ui import *
from PyQt5.QtWidgets import*
from stress_test.Pasat import Pasat
from stress_test.nback.NBack import NBack
from persistencia.Round import Round
import threading
from multiprocessing import Process, Queue
import sys

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        #Event connection
        self.pushButton_start.clicked.connect(self.__start)
        self.pushButton_start_nback.clicked.connect(self.__start)

        self.pushButton_stop.clicked.connect(self.__stop)
        self.pushButton_stop_nback.clicked.connect(self.__stop)

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
        self.spinBoxRounds.valueChanged.connect(self.__dataPasatTrainChangeListening)
        self.spinBoxRounds_prueba.valueChanged.connect(self.__dataPasatTestChangeListening)
        self.spinBoxRounds_nback_training.valueChanged.connect(self.__dataNBackTrainChangeListening)
        self.spinBoxRounds_nback_testing.valueChanged.connect(self.__dataNBackTestChangeListening)

        #Pasat test
        self.__pasat = Pasat(self.label_operation, self.label_wrong)
        self.__nback = NBack(self.label_matrix, self.label_letter, self.label_nback_title, self.label_message_matrix, self.label_message_letter)
        self.__stress_thread = None

    def __start(self):
        currentTest = None
        if self.tabWidget.currentIndex() == 2:
            currentTest = self.__pasat
            currentTest.setTestingMode(self.radioButton_prueba.isChecked())
            currentTest.setVisual(self.checkBox_visual.isChecked()) 
            currentTest.setAudio(self.checkBox_auditivo.isChecked())

        elif self.tabWidget.currentIndex() == 3:
            currentTest = self.__nback
            currentTest.setTestingMode(self.radioButton_prueba_nback.isChecked())
            currentTest.setVisual(self.checkBox_visual_nback.isChecked()) 
            currentTest.setAudio(self.checkBox_auditivo_nback.isChecked())
        
        else:
            print('Something is wrong, Ypu try a test in a different tab')
        
        currentTest.setRounds(self.getData())
        self.__stress_thread = threading.Thread(target=currentTest.start)
        self.__stress_thread.start()

    def __stop(self):
        self.__pasat.stop()
        self.__nback.stop()

    def __getDataSource(self):
        data = self.tableDatos_prueba
        numRounds = self.spinBoxRounds_prueba.value()

        if self.tabWidget.currentIndex() == 2 and self.radioButton_prueba.isChecked():
            data = self.tableDatos_prueba
            numRounds = self.spinBoxRounds_prueba.value()

        elif self.tabWidget.currentIndex() == 2 and self.radioButton_entrenamiento.isChecked():
            data = self.tableDatos
            numRounds = self.spinBoxRounds.value()

        elif self.tabWidget.currentIndex() == 3 and self.radioButton_prueba_nback.isChecked():
            data = self.tableDatos_nback_testing
            numRounds = self.spinBoxRounds_nback_testing.value()    

        elif self.tabWidget.currentIndex() == 3 and self.radioButton_entrenamiento_nback.isChecked():
            data = self.tableDatos_nback_training
            numRounds = self.spinBoxRounds_nback_training.value()
        else:
            print('Something is wrong, Ypu try a test in a different tab')

        return data, numRounds
    
    def getFeaturesFromDataTable(self, data, index):
        sums = int(data.item(index, 0).text())
        seconds = int(data.item(index, 1).text())
        try:
            n = int(data.item(index, 2).text())
            transition = int(data.item(index, 3).text())

        except:
            n = 1
            transition = 0
        return sums, seconds, n, transition
    
    def getData(self):
        rounds = []
        data, numRounds = self.__getDataSource()

        for i in range(numRounds):
            sums, seconds, n, transition = self.getFeaturesFromDataTable(data, i)
            r = Round(sums=sums, seconds=seconds, n=n, transition=transition)
            rounds.append(r)
        
        return rounds
        
    def __del__(self):
        sys.exit()

    # def roundsValueChange(self):
    #     #Se dan el numero de filas solicitadas
    #     self.tableDatos.setRowCount(self.spinBoxRounds.value())
    #     #Se agregan los nombres a las filas
    #     rowsNames = []
    #     for i in range(self.spinBoxRounds.value()):
    #         rowsNames.append('Round ' + str(i + 1))

    #     self.tableDatos.setVerticalHeaderLabels(rowsNames)
    #     self.rellenarTabla()

    # def rellenarTabla(self):
    #     for i in range(self.spinBoxRounds.value()):#Rows
    #         # for j in range(self.spinBoxNumeroClases.value() * self.spinBoxDimensionPatron.value()):#Coulumns
    #         for j in range(2):#Coulumns
            
    #             item = self.tableDatos.takeItem(i, j)
    #             if item is None:  
    #                 self.tableDatos.setItem(i, j, QTableWidgetItem(''))
    #             else: 
    #                 self.tableDatos.setItem(i, j, item)

    # def roundsValueChange_testing(self):
    #     #Se dan el numero de filas solicitadas
    #     self.tableDatos_prueba.setRowCount(self.spinBoxRounds_prueba.value())
    #     #Se agregan los nombres a las filas
    #     rowsNames = []
    #     for i in range(self.spinBoxRounds_prueba.value()):
    #         rowsNames.append('Round ' + str(i + 1))

    #     self.tableDatos_prueba.setVerticalHeaderLabels(rowsNames)
    #     self.rellenarTabla_testing()

    # def rellenarTabla_testing(self):
    #     for i in range(self.spinBoxRounds_prueba.value()):#Rows
    #         # for j in range(self.spinBoxNumeroClases.value() * self.spinBoxDimensionPatron.value()):#Coulumns
    #         for j in range(2):#Coulumns            
    #             item = self.tableDatos_prueba.takeItem(i, j)
    #             if item is None:  
    #                 self.tableDatos_prueba.setItem(i, j, QTableWidgetItem(''))
    #             else: 
    #                 self.tableDatos_prueba.setItem(i, j, item)

    def __roundsValueChange(self, tableData, spin):
        #Se dan el numero de filas solicitadas
        tableData.setRowCount(spin.value())
        #Se agregan los nombres a las filas
        rowsNames = []
        for i in range(spin.value()):
            rowsNames.append('Round ' + str(i + 1))

        tableData.setVerticalHeaderLabels(rowsNames)
        self.__rellenarTabla(tableData, spin)

    def __rellenarTabla(self, tableData, spin):
        for i in range(spin.value()):#Rows
            for j in range(2):#Coulumns
                item = tableData.takeItem(i, j)
                if item is None:  
                    tableData.setItem(i, j, QTableWidgetItem(''))
                else: 
                    tableData.setItem(i, j, item)

    def __dataPasatTrainChangeListening(self):
        self.__roundsValueChange(self.tableDatos, self.spinBoxRounds)

    def __dataPasatTestChangeListening(self):
        self.__roundsValueChange(self.tableDatos_prueba, self.spinBoxRounds_prueba)

    def __dataNBackTrainChangeListening(self):
        self.__roundsValueChange(self.tableDatos_nback_training, self.spinBoxRounds_nback_training)

    def __dataNBackTestChangeListening(self):
        self.__roundsValueChange(self.tableDatos_nback_testing, self.spinBoxRounds_nback_testing)



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
