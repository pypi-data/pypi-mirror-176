

from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMainWindow, QAction
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QFileInfo

import argparse, os, sys
from stdcomMenu.stdmenu import *
from stdcomMenu.config import *
from stdcomMenu.stdcOperator import *
import subprocess


class ExeAction(QAction) :
    data = None
    signalClick = pyqtSignal(list)

    def __init__(self, data : list = None, parent = None):
        super().__init__( parent)
        self.data = data
        self.triggered.connect(self.selected)

        decode = DecodeData()
        label = decode.getLabel(self.data)
        label = "action_" + label.replace('&','')
        self.setObjectName(label )

    @pyqtSlot()
    def selected(self):
        self.signalClick.emit(self.data)



class stdcOperatorMenu(QMainWindow):

    menu_Apps = None
    menubar = None
    def __init__(self, projectFile = None):
        self.projectFile = projectFile
        super().__init__()
        self.ui = Ui_MainWindowStdcOperator()
        self.ui.setupUi(self)

        """
        self.menubar = QtWidgets.QMenuBar(MainWindowStdcOperator)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 999, 24))
        self.menubar.setObjectName("menubar")
        """
        self.menubar = self.ui.menubar
        self.statusbar = self.ui.statusbar

        self.show()
        self.buildMenu()

    def buildMenu(self, project = None):
        if project is None :
            menus = MenuConfigue()
        else:
            menus = MenuConfigue(project)

        all = menus.values()

        decode = DecodeData()

        positions = {}
        for da in all :
            position = decode.getPositions(da)
            if position is not None and len(position) > 0 :
                rmposition = position.replace('&','')

                if position not in positions :
                    menu_Other = QtWidgets.QMenu(self.menubar)
                    menu_Other.setObjectName("menu_"+ rmposition )
                    menu_Other.setTitle(position)
                    positions.update( { position : menu_Other })

        for da in all:
            position = decode.getPositions(da)
            label = decode.getLabel(da)
            if label is not None and len(position) > 0 and label is not None and len(label) > 0 :
                menuItm = positions.get(position)

                action_item = ExeAction(da, self)
                action_item.setText(label)
                menuItm.addAction(action_item)
                action_item.signalClick.connect(self.selectedAction)

        for position in positions.keys() :
            itm = positions.get(position)

            self.menubar.addAction(itm.menuAction())

    @pyqtSlot(list)
    def selectedAction(self, data):
        print(data)
        decode = DecodeData()
        fileName = decode.getHelp(data)
        if fileName is not  None and len(fileName) > 0 :
            f = open(fileName, 'r')
            with f:
                text = f.read()
                self.ui.textBrowserHelp.setText(text)
        else:
            self.ui.textBrowserHelp.clear()

        cmd = decode.getApp(data)
        args = decode.getParameters(data)
        if args is not None and len(args) > 0 :
            cmd = cmd + " " + args
        os.system(cmd)


if __name__ == "__main__":


    app = QApplication(sys.argv)

    window = stdcOperatorMenu()
    window.setWindowTitle("Stec Multiverse Menu")

    if '--hide' in sys.argv:
        print("Hidden Display")
        window.hide()
    else:
        window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec_()
