# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/levpleshkov/Documents/Курс QGIS & Python/snippets/плагин/selector/selector_dockwidget_base.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SelectorDockWidgetBase(object):
    def setupUi(self, SelectorDockWidgetBase):
        SelectorDockWidgetBase.setObjectName("SelectorDockWidgetBase")
        SelectorDockWidgetBase.resize(672, 317)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.comboBox = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btnPlaceLot = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnPlaceLot.setObjectName("btnPlaceLot")
        self.verticalLayout_2.addWidget(self.btnPlaceLot)
        self.btnCheckPlacement = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnCheckPlacement.setObjectName("btnCheckPlacement")
        self.verticalLayout_2.addWidget(self.btnCheckPlacement)
        self.btnLoadProject = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnLoadProject.setObjectName("btnLoadProject")
        self.verticalLayout_2.addWidget(self.btnLoadProject)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        SelectorDockWidgetBase.setWidget(self.dockWidgetContents)

        self.retranslateUi(SelectorDockWidgetBase)
        QtCore.QMetaObject.connectSlotsByName(SelectorDockWidgetBase)

    def retranslateUi(self, SelectorDockWidgetBase):
        _translate = QtCore.QCoreApplication.translate
        SelectorDockWidgetBase.setWindowTitle(_translate("SelectorDockWidgetBase", "Selector"))
        self.pushButton.setText(_translate("SelectorDockWidgetBase", "PushButton"))
        self.btnPlaceLot.setText(_translate("SelectorDockWidgetBase", "Разместить участок"))
        self.btnCheckPlacement.setText(_translate("SelectorDockWidgetBase", "Проверить положение"))
        self.btnLoadProject.setText(_translate("SelectorDockWidgetBase", "Загрузить проект"))
