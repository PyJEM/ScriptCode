# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 21:51:27 2020

@author: Eiji Okunishi
 Copyright (C) <2021/10/25>  <Eiji Okunishi>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import sys
from PyQt4 import QtCore, QtGui
from PyJEM import TEM3
from PyJEM import detector
from time import sleep


from STEMGUI3 import Ui_AUTOSTEM
 
class Test(QtGui.QDialog):
  def __init__(self,parent=None):
    super(Test, self).__init__(parent)
    self.ui = Ui_AUTOSTEM()
    self.ui.setupUi(self)
    
#PyJEM setting
 
    self.lens = TEM3.Lens3()
    self.alin = TEM3.Def3()
    self.eos = TEM3.EOS3()
    self.ht = TEM3.HT3()
    self.gun = TEM3.GUN3()
    self.det = TEM3.Detector3()
    self.stage = TEM3.Stage3()  
    self.apt = TEM3.Apt3()
    self.detector = detector.function
     
    global clap_index
    global spot_index
    global caml_index

    # default setting

    clap_index = 3
    spot_index = 4
    caml_index = 8

    self.ui.comboBox.setCurrentIndex(clap_index)
    self.ui.comboBox_2.setCurrentIndex(spot_index)
    self.ui.comboBox_3.setCurrentIndex(caml_index)

    global haadfpos1
    global haadfpos2
    global bfpos1
    global Bfpos2
    global sethaadf
    global setbf

    haadfpos1 = self.ui.radioButton.isChecked()
    haadfpos2 = self.ui.radioButton_2.isChecked()
    bfpos1 = self.ui.radioButton_4.isChecked()
    bfpos2 = self.ui.radioButton_3.isChecked()

    if (haadfpos1 == True):
        sethaadf = 0
    elif (haadfpos2 == True):
        sethaadf = 1

    if (bfpos1 == True):
        setbf = 0
    elif (bfpos2 == True):
        setbf = 1

  def clap(self):
    global clap_index
    clap_index = self.ui.comboBox.currentIndex()

  def spot(self):
    global spot_index
    spot_index = self.ui.comboBox_2.currentIndex()

  def caml(self):
    global caml_index
    caml_index = self.ui.comboBox_3.currentIndex()

  def haadfin(self):
    global haadfpos1
    global haadfpos2
    global bfpos1
    global Bfpos2
    global sethaadf
    global setbf

    haadfpos1 = self.ui.radioButton.isChecked()
    haadfpos2 = self.ui.radioButton_2.isChecked()
    bfpos1 = self.ui.radioButton_4.isChecked()
    bfpos2 = self.ui.radioButton_3.isChecked()

    if (haadfpos1 == True):
        sethaadf = 0
    elif (haadfpos2 == True):
        sethaadf = 1
    if (bfpos1 == True):
        setbf = 0
    elif (bfpos2 == True):
        setbf = 1   
    
  def haadfout(self):
    global haadfpos1
    global haadfpos2
    global bfpos1
    global Bfpos2
    global sethaadf
    global setbf

    haadfpos1 = self.ui.radioButton.isChecked()
    haadfpos2 = self.ui.radioButton_2.isChecked()
    bfpos1 = self.ui.radioButton_4.isChecked()
    bfpos2 = self.ui.radioButton_3.isChecked()

    if (haadfpos1 == True):
        sethaadf = 0
    elif (haadfpos2 == True):
        sethaadf = 1
    if (bfpos1 == True):
        setbf = 0
    elif (bfpos2 == True):
        setbf = 1

  def bfin(self):
    global haadfpos1
    global haadfpos2
    global bfpos1
    global Bfpos2
    global sethaadf
    global setbf

    haadfpos1 = self.ui.radioButton.isChecked()
    haadfpos2 = self.ui.radioButton_2.isChecked()
    bfpos1 = self.ui.radioButton_4.isChecked()
    bfpos2 = self.ui.radioButton_3.isChecked()

    if (haadfpos1 == True):
        sethaadf = 0
    elif (haadfpos2 == True):
        sethaadf = 1
    if (bfpos1 == True):
        setbf = 0
    elif (bfpos2 == True):
        setbf = 1

  def bfout(self):
    global haadfpos1
    global haadfpos2
    global bfpos1
    global Bfpos2
    global sethaadf
    global setbf

    haadfpos1 = self.ui.radioButton.isChecked()
    haadfpos2 = self.ui.radioButton_2.isChecked()
    bfpos1 = self.ui.radioButton_4.isChecked()
    bfpos2 = self.ui.radioButton_3.isChecked()

    if (haadfpos1 == True):
        sethaadf = 0
    elif (haadfpos2 == True):
        sethaadf = 1
    if (bfpos1 == True):
        setbf = 0
    elif (bfpos2 == True):
        setbf = 1

  def gotostem(self):
    global clap_index
    global spot_index
    global caml_index

    #Beam Blank
    self.alin.SetBeamBlank(1)

    #sleep(1)

     #change to STEM
    self.eos.SelectTemStem(1)

    #sleep(5)

    #set CL aperture
    self.apt.SelectKind(1)
    self.apt.SetSize(clap_index)

    #set spot size
    self.eos.SelectSpotSize(spot_index)

    #set camera length
    self.eos.SetStemCamSelector(caml_index)  

    #function for HAADF detector
    if (sethaadf == 0):
      self.det.SetPosition(10,1)
      self.detector.Detector("HAADF").livestart()

    else:
      self.detector.Detector("HAADF").livestop()
      self.det.SetPosition(10,0)  

    #function for BF detector
  
    if (setbf == 0):
      self.det.SetPosition(15,1)
      self.detector.Detector("BF").livestart()

    else:
      self.detector.Detector("BF").livestop()
      self.det.SetPosition(15,0)  


    sleep(5)  

    self.alin.SetBeamBlank(0)  



     
if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  window = Test()
  window.show()
  sys.exit(app.exec_())        
     
         