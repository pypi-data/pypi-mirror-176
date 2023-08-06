# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'monctlHRvwHx.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from qtpy.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from qtpy.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QSlider, QToolButton, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(318, 331)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.brightness = QWidget(Form)
        self.brightness.setObjectName(u"brightness")
        self.gridLayout = QGridLayout(self.brightness)
        self.gridLayout.setObjectName(u"gridLayout")
        self.bslider = QSlider(self.brightness)
        self.bslider.setObjectName(u"bslider")
        self.bslider.setMaximum(100)
        self.bslider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.bslider, 2, 0, 1, 2)

        self.btitle = QLabel(self.brightness)
        self.btitle.setObjectName(u"btitle")

        self.gridLayout.addWidget(self.btitle, 0, 0, 1, 1)

        self.bvalue = QLabel(self.brightness)
        self.bvalue.setObjectName(u"bvalue")
        self.bvalue.setLayoutDirection(Qt.LeftToRight)
        self.bvalue.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.bvalue, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.brightness)

        self.contrast = QWidget(Form)
        self.contrast.setObjectName(u"contrast")
        self.gridLayout_2 = QGridLayout(self.contrast)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.cslider = QSlider(self.contrast)
        self.cslider.setObjectName(u"cslider")
        self.cslider.setMaximum(100)
        self.cslider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.cslider, 2, 0, 1, 2)

        self.ctitle = QLabel(self.contrast)
        self.ctitle.setObjectName(u"ctitle")

        self.gridLayout_2.addWidget(self.ctitle, 0, 0, 1, 1)

        self.cvalue = QLabel(self.contrast)
        self.cvalue.setObjectName(u"cvalue")
        self.cvalue.setLayoutDirection(Qt.LeftToRight)
        self.cvalue.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.cvalue, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.contrast)

        self.sharpness = QWidget(Form)
        self.sharpness.setObjectName(u"sharpness")
        self.gridLayout_3 = QGridLayout(self.sharpness)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.sslider = QSlider(self.sharpness)
        self.sslider.setObjectName(u"sslider")
        self.sslider.setMaximum(10)
        self.sslider.setPageStep(2)
        self.sslider.setOrientation(Qt.Horizontal)

        self.gridLayout_3.addWidget(self.sslider, 2, 0, 1, 2)

        self.stitle = QLabel(self.sharpness)
        self.stitle.setObjectName(u"stitle")

        self.gridLayout_3.addWidget(self.stitle, 0, 0, 1, 1)

        self.svalue = QLabel(self.sharpness)
        self.svalue.setObjectName(u"svalue")
        self.svalue.setLayoutDirection(Qt.LeftToRight)
        self.svalue.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.svalue, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.sharpness)

        self.bluelight = QWidget(Form)
        self.bluelight.setObjectName(u"bluelight")
        self.gridLayout_4 = QGridLayout(self.bluelight)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.blslider = QSlider(self.bluelight)
        self.blslider.setObjectName(u"blslider")
        self.blslider.setMaximum(10)
        self.blslider.setPageStep(2)
        self.blslider.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.blslider, 2, 0, 1, 2)

        self.bltitle = QLabel(self.bluelight)
        self.bltitle.setObjectName(u"bltitle")

        self.gridLayout_4.addWidget(self.bltitle, 0, 0, 1, 1)

        self.blvalue = QLabel(self.bluelight)
        self.blvalue.setObjectName(u"blvalue")
        self.blvalue.setLayoutDirection(Qt.LeftToRight)
        self.blvalue.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.blvalue, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.bluelight)

        self.colortemp = QWidget(Form)
        self.colortemp.setObjectName(u"colortemp")
        self.verticalLayout_2 = QVBoxLayout(self.colortemp)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.cttitle = QLabel(self.colortemp)
        self.cttitle.setObjectName(u"cttitle")

        self.verticalLayout_2.addWidget(self.cttitle)

        self.toolButton = QToolButton(self.colortemp)
        self.toolButton.setObjectName(u"toolButton")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton.sizePolicy().hasHeightForWidth())
        self.toolButton.setSizePolicy(sizePolicy)
        self.toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.toolButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.toolButton.setAutoRaise(False)
        self.toolButton.setArrowType(Qt.NoArrow)

        self.verticalLayout_2.addWidget(self.toolButton)


        self.verticalLayout.addWidget(self.colortemp)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Monitor Control", None))
        self.btitle.setText(QCoreApplication.translate("Form", u"Brightness", None))
        self.bvalue.setText(QCoreApplication.translate("Form", u"0", None))
        self.ctitle.setText(QCoreApplication.translate("Form", u"Contrast", None))
        self.cvalue.setText(QCoreApplication.translate("Form", u"0", None))
        self.stitle.setText(QCoreApplication.translate("Form", u"Sharpness", None))
        self.svalue.setText(QCoreApplication.translate("Form", u"0", None))
        self.bltitle.setText(QCoreApplication.translate("Form", u"BlueLight", None))
        self.blvalue.setText(QCoreApplication.translate("Form", u"0", None))
        self.cttitle.setText(QCoreApplication.translate("Form", u"COLOR TEMPERATURE", None))
        self.toolButton.setText(QCoreApplication.translate("Form", u"PROFILE", None))
    # retranslateUi

