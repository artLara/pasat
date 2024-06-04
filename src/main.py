from guis.pasat_ui import *
from PyQt5.QtWidgets import*
from stress_test.Pasat import Pasat
from stress_test.nback.NBack import NBack
from persistencia.Round import Round
import threading
from multiprocessing import Process, Queue
import sys
import json

##
from stress_test.StressTest import StressTest
import os
import datetime

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        #Event connection
        self.pushButton_start.clicked.connect(self.__start)
        self.pushButton_start_nback.clicked.connect(self.__start)

        self.pushButton_stop.clicked.connect(self.__stop)
        self.pushButton_stop_nback.clicked.connect(self.__stop)
        self.pushButton_registrar.clicked.connect(self.__loadId)
        self.pushButton_nback_guardar.clicked.connect(self.__saveFormsNBack)
        self.pushButton_pasat_guardar.clicked.connect(self.__saveFormsPasat)

        ##botones para grabar videos extras pasat
        self.pushButton_grabar_relax1.clicked.connect(self.__grabarRelax1)
        self.pushButton_detener_relax1.clicked.connect(self.__detenerRelax1)
        self.pushButton_grabar_instrucciones_pasat.clicked.connect(self.__grabarRelax1)
        self.pushButton_detener_instrucciones_pasat.clicked.connect(self.__detenerInstrucciones)
        ##botones para grabar extras nback
        self.pushButton_grabar_relax2.clicked.connect(self.__grabarRelax2)
        self.pushButton_detener_relax2.clicked.connect(self.__detenerRelax2)
        self.pushButton_grabar_instrucciones_nback.clicked.connect(self.__grabarRelax2)
        self.pushButton_detener_instrucciones_nback.clicked.connect(self.__detenerInstruccionesNback)

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
        self.__id = 0
        self.__pasat = Pasat(self.label_operation, self.label_wrong)
        self.__nback = NBack(self.label_matrix, self.label_letter, self.label_nback_title, self.label_message_matrix, self.label_message_letter)
        self.__stress_thread = None


    def __start(self):
        currentTest = None
        if self.tabWidget.currentIndex() == 3:
            currentTest = self.__pasat
            currentTest.setTestingMode(self.radioButton_prueba.isChecked())
            currentTest.setVisual(self.checkBox_visual.isChecked()) 
            currentTest.setAudio(self.checkBox_auditivo.isChecked())

        elif self.tabWidget.currentIndex() == 7:
            currentTest = self.__nback
            currentTest.setTestingMode(self.radioButton_prueba_nback.isChecked())
            currentTest.setVisual(self.checkBox_visual_nback.isChecked()) 
            currentTest.setAudio(self.checkBox_auditivo_nback.isChecked())
        
        else:
            print('Something is wrong, Ypu try a test in a different tab')
            print("tab currentIndex "+str(self.tabWidget.currentIndex()))
        
        currentTest.setId(self.__id)
        currentTest.setRounds(self.getData())
        self.__stress_thread = threading.Thread(target=currentTest.start)
        self.__stress_thread.start()

    def __stop(self):
        self.__pasat.stop()
        self.__nback.stop()

    def __loadId(self):
        f = open('id.json')
        data = json.load(f)
        f.close() 
        data['id'] += 1
        self.__id = int(data['id'])
        f = open('id.json', 'w')
        json.dump(data, f, indent = 6) 
        f.close() 
        print('Current ID: {}'.format(self.__id))
        self.label_usuario.setText('Usuario: {}'.format(self.__id))
        self.label_guardado_pasat.setText('')
        self.label_guardado_nback.setText('')

    # def __saveFormsPasat(self):
    #     self.label_guardado_pasat.setText('¡Guardado!')

    # def __saveFormsNBack(self):
    #     self.label_guardado_nback.setText('¡Guardado!')

    ### 
    def __initDirSaveNback(self):
        currentTestNback = self.__nback
        currentTestNback.setId(self.__id)
        nameDir =  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        path = '../usr/nback_information/' + str(self.__nback.getId()) + '/'
        currentTestNback.setPath(path)
        print("ruta de currentTestNback:"+currentTestNback.getPath())
        if not os.path.exists(currentTestNback.getPath()): 
            print("crea dir nback en main")
            os.makedirs(self.__nback.getPath())
    def __grabarRelax2(self):
        self.__initDirSaveNback()
        self.__nback.startRecording(listFlag=True)
    def __detenerRelax2(self):
        print('DetenerRelax2')
        currentTestNback = self.__nback
        currentTestNback.stopRecordingRelax1(1)

    def __detenerInstruccionesNback(self):
        currentTestNback = self.__nback
        currentTestNback.stopRecordingRelax1(2)

    def __initDirSave(self):
        currentTest = self.__pasat
        currentTest.setId(self.__id)
        nameDir =  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        path = '../usr/pasat_information/' + str(self.__pasat.getId()) + '/'
        currentTest.setPath(path)
        print("ruta de currentTest:"+currentTest.getPath())
        # print('ruta objeto pasat main' + self.getPath())
        if not os.path.exists(currentTest.getPath()): 
            print("crea dir pasat en main")
            os.makedirs(self.__pasat.getPath())

        self.__path = '../usr/forms/' + str(self.__id) + '/'
        if not os.path.exists(self.__path): 
            os.makedirs(self.__path)

    def __grabarRelax1(self):
        self.__initDirSave()
        # self.__pasat_thread = threading.Thread(target=self.__videoRecorder.start, kwargs={'currentFrame':self.__currentFrame})
        self.__pasat.startRecording(listFlag=True)

    def __detenerRelax1(self):
        currentTest = self.__pasat
        currentTest.stopRecordingRelax1(1)
    
    def __detenerInstrucciones(self):
        currentTest = self.__pasat
        currentTest.stopRecordingRelax1(2)
    ### aqui termina lo que agregue

    def __getDataSource(self):
        data = self.tableDatos_prueba
        numRounds = self.spinBoxRounds_prueba.value()

        if self.tabWidget.currentIndex() == 3 and self.radioButton_prueba.isChecked():
            data = self.tableDatos_prueba
            numRounds = self.spinBoxRounds_prueba.value()

        elif self.tabWidget.currentIndex() == 3 and self.radioButton_entrenamiento.isChecked():
            data = self.tableDatos
            numRounds = self.spinBoxRounds.value()

        elif self.tabWidget.currentIndex() == 7 and self.radioButton_prueba_nback.isChecked():
            data = self.tableDatos_nback_testing
            numRounds = self.spinBoxRounds_nback_testing.value()    

        elif self.tabWidget.currentIndex() == 7 and self.radioButton_entrenamiento_nback.isChecked():
            data = self.tableDatos_nback_training
            numRounds = self.spinBoxRounds_nback_training.value()
        else:
            print('Something is wrong, Ypu try a test in a different tab')
            print("tab currentIndex en __getDataSource: "+ self.tabWidget.currentIndex())

        return data, numRounds
    
    def getFeaturesFromDataTable(self, data, index):
        sums = int(data.item(index, 0).text())
        seconds = float(data.item(index, 1).text())
        try:
            n = int(data.item(index, 2).text())
            transition = float(data.item(index, 3).text())

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

    def __getOptionEstresPasat(self):
        if self.radioButton_pasat_estresado_nada.isChecked():
            return 'nada'
        
        if self.radioButton_pasat_estresado_poco.isChecked():
            return 'poco'
        
        if self.radioButton_pasat_estresado_moderado.isChecked():
            return 'moderado'
        
        if self.radioButton_pasat_estresado_muy.isChecked():
            return 'mucho'
        
    def __getOptionDificultadPasat(self):
        if self.radioButton_pasat_estresado_dif_ninguna.isChecked():
            return 'nada'
        
        if self.radioButton_pasat_estresado_dif_poco.isChecked():
            return 'poco'
        
        if self.radioButton_pasat_estresado_dif_mod.isChecked():
            return 'moderado'
        
        if self.radioButton_pasat_estresado_dif_mucha.isChecked():
            return 'mucho'
        
    def __saveFormsPasat(self):
        self.__initDirSave()
        info = {}
        info['estres'] = self.__getOptionEstresPasat()
        info['dificultad'] = self.__getOptionDificultadPasat()
        info['q1'] = self.plainTextEdit_pasat_q1.toPlainText()
        info['q2'] = self.plainTextEdit_pasat_q2.toPlainText()
        info['q3'] = self.plainTextEdit_pasat_q3.toPlainText()
        
        with open(self.__path + "pasat.json", "w") as outfile: 
            json.dump(info, outfile)

        self.label_guardado_pasat.setText('¡Guardado!')
        self.plainTextEdit_pasat_q1.clear()
        self.plainTextEdit_pasat_q2.clear()
        self.plainTextEdit_pasat_q3.clear()

    def __getOptionEstresNBack(self):
        if self.radioButton_nback_estresado_nada.isChecked():
            return 'nada'
        
        if self.radioButton_nback_estresado_poco.isChecked():
            return 'poco'
        
        if self.radioButton_nback_estresado_moderado.isChecked():
            return 'moderado'
        
        if self.radioButton_nback_estresado_muy.isChecked():
            return 'mucho'
        
    def __getOptionDificultadNBack(self):
        if self.radioButton_nback_estresado_dif_ninguna.isChecked():
            return 'nada'
        
        if self.radioButton_nback_estresado_dif_poco.isChecked():
            return 'poco'
        
        if self.radioButton_nback_estresado_dif_mod.isChecked():
            return 'moderado'
        
        if self.radioButton_nback_estresado_dif_mucha.isChecked():
            return 'mucho'
        
    def __saveFormsNBack(self):
        self.__initDirSave()
        info = {}
        info['estres'] = self.__getOptionEstresNBack()
        info['dificultad'] = self.__getOptionDificultadNBack()
        info['q1'] = self.plainTextEdit_nback_q1.toPlainText()
        info['q2'] = self.plainTextEdit_nback_q2.toPlainText()
        info['q3'] = self.plainTextEdit_nback_q3.toPlainText()
        
        with open(self.__path + "nback.json", "w") as outfile: 
            json.dump(info, outfile)

        self.label_guardado_nback.setText('¡Guardado!')
        self.plainTextEdit_nback_q1.clear()
        self.plainTextEdit_nback_q2.clear()
        self.plainTextEdit_nback_q3.clear()

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
