import sys
import serial

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QSlider, QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QLineEdit, QMessageBox




class DragButton(QtWidgets.QLabel):


    def mousePressEvent(self, event):


        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos

            #print (diff)

            movex = 0;
            movey = 0;
            mdis = (self.__mouseMovePos.x()-175)**2 + (self.__mouseMovePos.y()-165)**2
            if mdis>5625:
                x = self.__mouseMovePos.x()-175
                y =self.__mouseMovePos.y()-165

                


            newPos = self.mapFromGlobal(currPos + diff)
            # print("Qpoint")
            # print(newPos.x())
            # print(newPos.y())

            #print (type(newPos))
            dis = (newPos.x()-175)**2 + (newPos.y()-165)**2
            if dis<=5625:
                self.move(newPos)
                self.__mouseMovePos = globalPos

                movex = (newPos.x()-175);
                movey = (newPos.y()-165);
                print((newPos.x()-175),(newPos.y()-165))
            else:
                newPos.setX((newPos.x()-175)/(dis**0.5)*75+175)
                newPos.setY((newPos.y()-165)/(dis**0.5)*75+165)




                movex = ((newPos.x()-175)/(dis**0.5)*75);
                movey = ((newPos.y()-165)/(dis**0.5)*75);
                print( ((newPos.x()-175)/(dis**0.5)*75),((newPos.y()-165)/(dis**0.5)*75)  )

                self.move(newPos)
                self.__mouseMovePos = globalPos
                #make the interpolation here

            direction = 1;
            if movex<0:
                movex = movex*-1;
                direction = 0;
            # out = [chr(51) +chr(10)+ chr(1)+ chr(int(direction))+ chr(int(movex))];

            # outs = ''.join(out)

            # ser.write(outs.encode())
            # self.move(newPos)

            # self.__mouseMovePos = globalPos

        super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos
            backPos = self.mapToGlobal(self.pos())
            backPos.setX(175)
            backPos.setY(165)
            self.move(backPos)

            if moved.manhattanLength() > 3:
                event.ignore()
                return

        super(DragButton, self).mouseReleaseEvent(event)

def clicked():
    print ("click as normal!")

if __name__ == "__main__":


    ser = serial.Serial('/dev/tty.lpss-serial1')
    print(ser.name)

    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(800,600)



    l1 = QtWidgets.QLabel(w)
    l1.setPixmap(QtGui.QPixmap('bg.png'))
    l1.move(100,90)


    s1 = QSlider(Qt.Horizontal, w) 
    s1.setMinimum(1)
    s1.setMaximum(100)
    s1.setValue(25)
    s1.setTickInterval(20)
    s1.setTickPosition(QSlider.TicksBelow)
    # v_box = QVBoxLayout(w)
    # v_box.addwigit(s1)



    button = DragButton(w)
    button.setPixmap(QtGui.QPixmap('thumb.png'))
    button.move(100+75,90+75)


    #button.clicked.connect(clicked)

    w.show()
    app.exec_()