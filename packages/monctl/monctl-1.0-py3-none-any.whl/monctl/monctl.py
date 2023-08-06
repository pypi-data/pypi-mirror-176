from qtpy import QtCore, QtWidgets, QtGui

from .g27q import G27Q
from .ui_monctl import Ui_Form

class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.bslider.valueChanged.connect(self.bvalue.setNum)
        self.cslider.valueChanged.connect(self.cvalue.setNum)
        self.sslider.valueChanged.connect(self.svalue.setNum)
        self.blslider.valueChanged.connect(self.blvalue.setNum)

        self.initValues()
        self.connectChanges()

    def initValues(self):
        with G27Q() as monitor:
            self.bslider.setValue(monitor.get_property("Brightness"))
            self.cslider.setValue(monitor.get_property("Contrast"))
            self.sslider.setValue(monitor.get_property("Sharpness"))
            self.blslider.setValue(monitor.get_property("BlueLight"))

    def connectChanges(self):
        self.bslider.valueChanged.connect(self.set_brightness)
        self.cslider.valueChanged.connect(self.set_contrast)
        self.sslider.valueChanged.connect(self.set_sharpness)
        self.blslider.valueChanged.connect(self.set_blueLight)

    def set_monitorProperty(self, property: str, value: int):
        with G27Q() as monitor:
            monitor.set_property(property,value)

    def set_brightness(self,value):
        self.set_monitorProperty("Brightness", value)
    
    def set_contrast(self,value):
        self.set_monitorProperty("Contrast", value)
    
    def set_sharpness(self,value):
        self.set_monitorProperty("Sharpness", value)
    
    def set_blueLight(self,value):
        self.set_monitorProperty("BlueLight", value)