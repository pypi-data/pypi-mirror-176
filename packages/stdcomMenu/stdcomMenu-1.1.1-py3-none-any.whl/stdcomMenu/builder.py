
from stdcomQt.stdcomutilitywidgets import StecTreeMorph
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QFileDialog
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QFileInfo

import argparse, os, sys
from stdcomMenu.stdmenu import *
from stdcomMenu.config import *

class Builder(QWidget):

    ui =  None
    Tree = None
    Setupdata = None
    def __init__(self, parent=None):
        super().__init__(parent )
        self.ui = Ui_menuBuilder()
        self.ui.setupUi(self )
        self.show()
        self.setWindowTitle("Stec Menu Apps Editor")
        self.ui.pushButtonAdd.clicked.connect(self.openFileNameDialog)
        self.ui.pushButtonSave.clicked.connect(self.Save)
        self.Tree = StecTreeMorph(self.ui.treeWidgetMenuItems,[""])
        self.Tree.newTextUserSignal.connect(self.TreeClicked)
        self.ui.pushButtonHelp.clicked.connect(self.HelpClicked)
        self.ui.pushButtonDelete.clicked.connect(self.Delete)
        self.Setupdata =  MenuConfigue()

        keys = self.Setupdata.keys()
        for each in keys :
            if keys is not None:
                data = self.Setupdata.getFromKey(each)
                if data is not None and len(data):
                    label = data[0]
                    app = data[1]
                    args = data[2]
                    position = data[3]
                    self.Tree.AddName(app)
                    self.Tree.AddDesc(app,label)
                    self.Tree.AddUserData(app,data)

    @pyqtSlot()
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.ui.lineEditApp.setText(fileName)
            base = QFileInfo(fileName)
            baseName = base.baseName()
            self.ui.lineEditName.setText(baseName)
    @pyqtSlot()
    def Save(self):
        print("Save")
        textLabel = self.ui.lineEditName.text()
        textApp = self.ui.lineEditApp.text()
        parmeters: str = self.ui.plainTextEditParameters.toPlainText()
        menuItem = self.ui.lineEditMenuGroup.text()
        helpFile = self.ui.lineEditHelp.text()

        if len(textLabel) >= 1 and len(textApp) >= 1 :
            userData = [textLabel, textApp, parmeters, menuItem, helpFile]
            self.Tree.DeleteKey(textApp)
            self.Tree.AddName(textApp)
            self.Tree.AddDesc(textApp, textLabel)
            self.Tree.AddUserData(textApp, userData)
            self.Setupdata.addKey(textLabel, userData )

        self.ui.lineEditName.clear()
        self.ui.lineEditApp.clear()
        self.ui.plainTextEditParameters.clear()

    @pyqtSlot()
    def Delete(self):
        textLabel = self.ui.lineEditName.text()
        textApp = self.ui.lineEditApp.text()

        if textApp is not None and len(textApp) > 0 and textLabel is not None and len(textLabel) > 0:
            self.Tree.DeleteSelected()
            self.Setupdata.deleteKey(textLabel)
            self.ui.lineEditName.clear()
            self.ui.lineEditApp.clear()
            self.ui.plainTextEditParameters.clear()




    @pyqtSlot(str,str,list)
    def TreeClicked(self,name,desc,data):
        print(name,desc,data)
        if len(data) >= 5 :
            text = data[2]
            self.ui.plainTextEditParameters.clear()
            self.ui.plainTextEditParameters.appendPlainText(text)
            menuItem = data[3]
            self.ui.lineEditApp.setText(name)
            self.ui.lineEditName.setText(desc)
            self.ui.lineEditMenuGroup.setText(menuItem)

            helpFile = data[4]
            self.ui.lineEditHelp.setText(helpFile)

        else:
            self.ui.plainTextEditParameters.clear()
            self.ui.lineEditApp.clear()
            self.ui.lineEditName.clear()
            self.ui.lineEditMenuGroup.clear()


    @pyqtSlot()
    def HelpClicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*.HTML);;HTML Help Files (*.html)", options=options)
        if fileName:
            self.ui.lineEditHelp.setText(fileName)


if __name__=="__main__":
    my_parser = argparse.ArgumentParser(description="Version :" + stdcomQt.stdcomQtVersion + " Stec Menu Program")
    current = os.path.dirname(os.path.realpath(__file__))

    # Getting the parent directory name
    # where the current directory is present.
    parent = os.path.dirname(current)

    # adding the parent directory to
    # the sys.path.

    app = QApplication(sys.argv)
    w = Builder()
    w.show()

    sys.exit(app.exec_())
