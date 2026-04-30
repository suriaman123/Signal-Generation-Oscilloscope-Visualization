# Assignment 6: by Aman and Vikas

import pyvisa
import time
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from assignment6_gui import assignment6_ui

import numpy as np


class assignment6(QMainWindow):    
                 
    
    def __init__(self):         

        super().__init__()       
        self.ui = assignment6_ui()                          
        self.ui.setupUi(self)   

        self.canvas = FigureCanvas(Figure())
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.ui.graphbox.addWidget(self.canvas)                           
        
        self.ui.pb.clicked.connect(self.showme)


    def showme(self):

        rm = pyvisa.ResourceManager()
        rm.list_resources()

        function_generator = 'USB0::0x0957::0x2507::MY52101242::INSTR'
        self.fg = rm.open_resource(function_generator) 
        oscilloscope = 'USB0::0x0957::0x179B::MY51361672::INSTR'
        self.os = rm.open_resource(oscilloscope) 
        self.fg.write("*RST")                              
        self.os.write("*RST")

        waveform = self.ui.dd_waveform.currentText()
        frequency = self.ui.doubleSpinBox_frequency.value()
        amplitude = self.ui.spinBox_amplitude.value()
        offset = self.ui.spinBox_offset.value()

        self.fg.write(f"APPLy:{waveform} {float(frequency)},{float(amplitude)},{float(offset)}")
        print(f"Function generator set to output a {frequency} kHz {waveform} wave with {amplitude} Vpp and {offset} VDC.")
        self.os.write("AUTOSCALE")   

        time.sleep(5)                                  # give some time to oscilloscope to adjust

        self.os.write("WAV:POIN 500") 
        self.os.write("WAV:FORM ASC") 
        oscilloscope_data = self.os.query('WAV:DATA?')

        # removing the intial garbage value
        os_data = oscilloscope_data
        os_data = os_data.strip()
        a = os_data.find('-')
        os_data = os_data[a + 1:]
        os_list = os_data.split(',')
        y_data = [float(num.strip()) for num in os_list] 

        y =  np.array(y_data)
        t = np.linspace(0, len(y), len(y))           # np.linspace(start, stop, num)

       # self.canvas.set_window_title("Yo YO YO")
        self.canvas.axes.plot(t,y,c='blue')
        self.canvas.axes.set_xlabel('time')
        self.canvas.axes.set_ylabel('amplitude')

        self.canvas.draw() 


      


app = QApplication([])
window = assignment6()
window.show()
app.exec_()

