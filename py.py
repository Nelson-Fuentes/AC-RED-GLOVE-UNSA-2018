import cv2
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic
import random
import ctypes

class Ventana(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.camara = True
        uic.loadUi("ui.ui", self)
        self.show()
        self.arr = [self.b1, self.b2, self.b5, self.b3, self.b4, self.b6]
        self.img = ['starform.png', 'triangleform.png', 'pentagonform.png', 'cuadreform.png', 'moonform.png', 'circleform.png', '']
        a = random.randint(0,5)
        self.mov.setStyleSheet("background: url('"+self.img[a]+"');")
        self.x = self.arr[a].pos().x()
        self.y = self.arr[a].pos().y()
        self.score = 0
        string = str(self.score)
        self.score_ui.setText(string)
        self.run = True

    def empezar(self):
        cam = cv2.VideoCapture(0)
        kernel = np.ones((5, 5), np.uint8)
        widthcam = cam.get(3)
        heigthcam = cam.get(4)
        puntox = 0
        puntoy = 0
        distmin = 3
        catch = False
        area = 0
        posxo = self.mov.pos().x()
        posyo = self.mov.pos().y()
        surrenderx = self.surrender.pos().x()
        surrenderxw = surrenderx + self.surrender.width()
        surrendery = self.surrender.pos().y()
        surrenderyh = surrendery + self.surrender.height()
        while (self.run):
            ret, frame = cam.read()
            rangomax = np.array([220, 60, 255]) #30 30 255
            rangomin = np.array([25, 20, 100]) #10 10 80
            mascara = cv2.inRange(frame, rangomin, rangomax)
            opening = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
            x, y, w, h = cv2.boundingRect(opening)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
            mediox = round(x + w / 2)
            medioy = round(y + h / 2)
            cv2.circle(frame, (mediox, medioy), 6, (0, 0, 100), -1)
            if abs(mediox - puntox) > distmin and abs(medioy - puntoy) >= distmin:
                xframe = self.frameSize().width() - ((self.frameSize().width() * mediox) / widthcam)
                yframe = (800 * medioy) / (heigthcam) - 100  # self.frameSize().height()
                puntox = mediox
                puntoy = medioy
                if h*w - area < -area*1/5 and not catch:
                    if posxo+25 < xframe < posxo+175 and posyo + 25 < yframe < posyo + 175 and not catch:
                        catch=True

                    elif surrenderx < xframe < surrenderxw and surrendery < yframe < surrenderyh:
                        resultado = QMessageBox.question(self, "¡Rendirse!", "¿Estas seguro de querer rendirte?", QMessageBox.Yes | QMessageBox.No)
                        if resultado == QMessageBox.Yes:
                            break

                elif area - h * w < -area*1/2 and catch:
                    catch=False
                    if self.x < xframe < self.x+200 and self.y - 100 < yframe < self.y + 100:
                        self.score = self.score+100
                        string = str(self.score)
                        self.score_ui.setText(string)
                        a = random.randint(0, 5)
                        self.mov.setStyleSheet("background: url('" + self.img[a] + "');")
                        self.x = self.arr[a].pos().x()
                        self.y = self.arr[a].pos().y()
                        self.globos.setMaximumSize(self.score, 40)
                        self.globos.setMinimumSize(self.score,40)
                        if self.width ()<= self.globos.width():
                            resultado = QMessageBox.question(self, "¡GANASTE!", "¿Deseas volver a jugar?", QMessageBox.Yes | QMessageBox.No)
                            if resultado == QMessageBox.Yes:
                                self.score =0
                                string = str(self.score)
                                self.score_ui.setText(string)
                                self.globos.setMaximumSize(0, 00)
                                self.globos.setMinimumSize(0, 00)
                            else:
                                break

                else:
                    self.cs.move(xframe, yframe)
                area = h * w
                if (catch):
                    self.mov.move(xframe-50, yframe-50)
                else:
                    self.mov.move(posxo, posyo)



            cv2.imshow('camara', frame)
            k = cv2.waitKey(1) & 0xFF
            if k == 13:
                break

            # g =None
        #self.hide()

myappid = u'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
app = QApplication(sys.argv)
ventana = Ventana()
ventana.empezar()
app.exec_()
