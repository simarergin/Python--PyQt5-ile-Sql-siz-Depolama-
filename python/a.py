import datetime
from itertools import product
import sys
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
from tablewidget import Ui_MainWindow
from typing_extensions import Self
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from SayfaUi import *
import time
from datetime import datetime as dt, timedelta as td
from openpyxl import workbook
import openpyxl
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import xlsxwriter
from calendar import c 
import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication
from tkinter import messagebox

fileNames = []
Uygulama = QApplication(sys.argv)
penAna = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(penAna)
penAna.show()

class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.UI()
        self.ui.setupUi(self)

def getValues():
    
    tarih1 = ui.calendarWidget.selectedDate().toString(QtCore.Qt.ISODate)
    tarih2 = ui.calendarWidget_2.selectedDate().toString(QtCore.Qt.ISODate)
    isim = ui.lineEdit.text().upper()
    tip = ui.comboBox.currentText()
    ip = ui.lineEdit_3.text()
    url = ui.lineEdit_4.text()   
    trh = ui.chkTarih.isChecked()

    bul(isim,tip,ip,url,tarih1,tarih2, trh)

def loadProducts():
    table = ui.tableWidget.text()
    print(table)

ui.pushButton_2.clicked.connect(getValues)

sonuc = []

selectedFolder = [""]

def bul(isim, tip, ip, url,tarih1, tarih2, trh):

    t1 = time.time()
    count = 0
    fileNames = os.listdir(selectedFolder[0])

    secilenDosyalar = [] 

    for a in fileNames:
        b = dt.strptime(a[0:10], '%Y-%m-%d')
        tarih1_ = dt.strptime(tarih1[0:10], '%Y-%m-%d')
        tarih2_ = dt.strptime(tarih2[0:10], '%Y-%m-%d')

        if(b < tarih2_ and b > tarih1_):
            secilenDosyalar.append(a)
    print(secilenDosyalar)

    if(trh == False):
        secilenDosyalar = fileNames
    for fileName in secilenDosyalar:

        with open(selectedFolder[0] +  "/" + fileName, encoding="utf8") as file:
            for idx, line in enumerate(file, 0):
                columns = line.split("|")    

                if len(columns) == 5 and ("GET" in columns[2]  or  "PUT" in columns[2] or  "POST" in columns[2] or  "DELETE" in columns[2]): 
                    count += 1
                    if len(isim) > 0 and isim in columns[1]:
                        print(line)
                        sonuc.append(line)
                    elif len(tip) > 0 and tip in columns[2]:
                        print(line)
                        sonuc.append(line)
                    elif len(ip) > 0 and ip in columns[3]:
                        print(line)
                        sonuc.append(line)
                    elif len(url) > 0 and url in columns[4]:
                        print(line)
                        sonuc.append(line)

                    if(trh):
                        if len(tarih1) > 0 and len(tarih2) > 0:
                            date_string = columns[0][0:10]
                            lineDate =  dt.strptime(date_string, '%Y-%m-%d')
                            tarih1_ = dt.strptime(tarih1[0:10], '%Y-%m-%d')
                            tarih2_ = dt.strptime(tarih2[0:10], '%Y-%m-%d')
                        if(lineDate < tarih2_ and lineDate > tarih1_):
                            sonuc.append(line)    

            print("Okunan veri sayısı: "+str(count))               

    for idx, satir in enumerate(sonuc, 0):
        columns = satir.split("|")
        ui.tableWidget.setHorizontalHeaderLabels(('Tarih','İsim','Tip','Ip','Url'))
        ui.tableWidget.setItem(idx,0,QTableWidgetItem(columns[0]))
        ui.tableWidget.setItem(idx,1,QTableWidgetItem(columns[1]))
        ui.tableWidget.setItem(idx,2,QTableWidgetItem(columns[2]))
        ui.tableWidget.setItem(idx,3,QTableWidgetItem(columns[3]))
        ui.tableWidget.setItem(idx,4,QTableWidgetItem(columns[4]))


    t2 = time.time()

    print("elapsed time: "+ str(t2-t1))

def DOSYASEC():
    print(selectedFolder[0])
    fileName = QFileDialog.getExistingDirectory(ui.pushButton_4 , "Open Directory",
                                            "/home",
                                            QFileDialog.ShowDirsOnly
                                            | QFileDialog.DontResolveSymlinks)
    print(fileName)
    if fileName:
        selectedFolder[0] = fileName
        print(selectedFolder[0])


def initUi(self):
    self.openFileNameDialog()
    self.saveFileDialog()
    self.show()
     
def openFileNameDialog(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
    if fileName:
        print(fileName)
    
def saveFileDialog(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
    if fileName:
        print(fileName)

ui.pushButton_4.clicked.connect(DOSYASEC)  

def ARA():
    ui.pushButton_2.clicked.connect(ARA)   

    son_mesaj = ""
    cevap=QMessageBox.question(penAna,"ARA","Aranıyor..",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        return
    ui.tblwÇalışanlar.clear()

def EXCEL():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    print(timestr)
    workbook = xlsxwriter.Workbook(timestr+'.xlsx')
    worksheet = workbook.add_worksheet()

    cevap=QMessageBox.question(penAna,"EXCEL","Excel...",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        for idx, satir in enumerate(sonuc, 0):
            columns = satir.split("|")                

            worksheet.write('A'+str(idx+1), columns[0])
            worksheet.write('B'+str(idx+1), columns[1])
            worksheet.write('C'+str(idx+1), columns[2])
            worksheet.write('D'+str(idx+1), columns[3])
            worksheet.write('E'+str(idx+1), columns[4])

        workbook.close()
                
    else:
        cevap==QMessageBox.No

        sys.exit(Uygulama.exec_())
ui.pushButton_3.clicked.connect(EXCEL)

def CIKIS():
    cevap=QMessageBox.question(penAna,"ÇIKIŞ","Programdan çıkmak istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        sys.exit(Uygulama.exec_())
ui.pushButton.clicked.connect(CIKIS)

sys.exit(Uygulama.exec_())
