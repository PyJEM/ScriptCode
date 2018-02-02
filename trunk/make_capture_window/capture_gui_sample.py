# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 19:10:18 2017

@author: dmaekawa
"""

#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
#import datetime 

import sys
import os
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
#from PyJEM.offline import detector

_status = 0     # online

try:
    from PyJEM import  detector
    
except(ImportError):
    from PyJEM.offline import detector
    _status = 1     # offline


#class Example(QMainWindow):
#    def __init__(self):
#        super(Example, self).__init__()
#        self.initUI()
#        
#    def initUI(self):               
#        self.setGeometry(300, 300, 250, 150)
#        self.setWindowTitle('[TEST]PyJEM')    
#        self.show()
#
#        timer = QTimer(self)
#        timer.timeout.connect(self.time_draw)
#        timer.start(1000) #msec       
#       
#
#    def time_draw(self):
#        d = datetime.datetime.today()
#        daystr=d.strftime("%Y-%m-%d %H:%M:%S")
#        self.statusBar().showMessage(daystr)
#
#def main():
#
#    app = QApplication(sys.argv)
#    ex = Example()
#    sys.exit(app.exec_())
#    
#if __name__ == '__main__':
#    main()


class MainMenu(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        self.setWindowTitle('PyJEM Sample')    
        self.setGeometry(10,10,40,300)
        button = QtGui.QPushButton('Capture',self)
        self.Label = QtGui.QLabel(self)
        self.Label.setGeometry(20,20,512,512)
#        self.connect(button,QtCore.SIGNAL('clicked()'),self.show_image)
        if (_status == 1):
            self.connect(button,QtCore.SIGNAL('clicked()'),self.show_image_offline)
        elif (_status == 0):
            self.connect(button,QtCore.SIGNAL('clicked()'),self.show_image_online)

    def get_detectorname(self):
        data = detector.get_attached_detector()
        self.Label.setText(data[0])
        
    def show_image_online(self, extention="jpg"):
        det = detector.Detector(detector.detectors[0])
        data = det.snapshot(extention, filename="snapshot",save=True)
#        file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "\\image\\snapshot." + extention
        file = detector.base.imagefilepath + "\\snapshot." + extention
        self.pixmap = QtGui.QPixmap(file)
        self.Label.setPixmap(QtGui.QPixmap(file))

    def show_image_offline(self, extention="jpg"):
        file = r"C:\Users\dmaekawa\Desktop\python\PyJEM\Src\PyJEM\PyJEM\offline\resource" + "\SnapShot" + "." + extention
        self.pixmap = QtGui.QPixmap(file)
        self.Label.setPixmap(QtGui.QPixmap(file))
        
    def changeText(self):
        self.Label.setText("abcd")

if __name__ == '__main__':
        
    application = QtGui.QApplication(sys.argv)
    
    main = MainMenu()
    main_window =QtGui.QMainWindow()
    main_window.setCentralWidget(main)
    main_window.show()
    
    application.exec_()
 
 