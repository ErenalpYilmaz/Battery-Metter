from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


import sys
import serial
import time

arduino = serial.Serial("COM8",9600)

#gelen veriyi okur utf8 olarak decode eder.
#Sondaki /n leri temizler.

veri=arduino.readline().decode('utf-8').rstrip()  



class BatteryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle("BATTERY SCREEN")
        self.setGeometry(100,100,1280,720)
        
        #Pil yuzdesini Gosteren etiket
        self.battery_Label = QLabel(str("%"+veri),self)
        self.battery_Label.setAlignment(Qt.AlignCenter)
        
        

        #Pil Yuzdesinin ustune yazi ekleyen etiket
        bataryaDurumu = degerHesaplama(int_veri)
        self.status_label = QLabel(bataryaDurumu,self)
        self.status_label.setAlignment(Qt.AlignCenter)
        


        #Font Ayarlari
        battery_font = QFont("Arial",30)
        status_font = QFont("Arial",24)
        
        self.battery_Label.setFont(battery_font)
        self.status_label.setFont(status_font)

        # Layout Olusturulmasi
        main_layout = QVBoxLayout()

        #Pil Yuzdesi icin ust duzen
        pil_yuzdesi_layout = QVBoxLayout()
        pil_yuzdesi_layout.addWidget(self.battery_Label)
        main_layout.addLayout(pil_yuzdesi_layout)


        # Pil Durumu 
        pil_durumu_layout = QHBoxLayout()
        pil_durumu_layout.addWidget(self.status_label)
        main_layout.addLayout(pil_durumu_layout)

        self.setLayout(main_layout)

        


        # QTimer olusturulmasi
        self.timer = QTimer(self)   
        self.timer.timeout.connect(self.update_label)
        self.timer.start(500)

    #arduino daki bilgileri guncellemek icin kullaniyoruz.
    def update_label(self):
            veri =arduino.readline().decode('utf-8').rstrip()  
            int_veri2 = float(veri)
            self.battery_Label.setText(f"%{veri}")
            bataryaDurumu = degerHesaplama(int_veri2)
            self.status_label.setText(bataryaDurumu)

int_veri = float(veri)
def degerHesaplama(a):
    bataryaYuzdesi =""
    if float(a) >= 70 :
        bataryaYuzdesi = "Pil Durumu Iyi"
    if a < 70 and a > 50:
        bataryaYuzdesi = "Pil Durumn Ortalama"
    if a < 50 :
        bataryaYuzdesi = "Pil Durumu Dusuk"
    return bataryaYuzdesi




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BatteryWidget()
    ex.resize(600,300)
    ex.show()
    sys.exit(app.exec_())
