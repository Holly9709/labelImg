# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # ´´½¨tableºÍmodel
        table = QtGui.QTableView(parent=self)
        self.model = QtGui.QStandardItemModel(parent=self)
        self.model.setHorizontalHeaderLabels(('Name', 'Age'))
        table.setModel(self.model)

        # ´´½¨Ìí¼Ó°´Å¥
        button = QtGui.QPushButton('Add', parent=self)

        # Ìí¼ÓÐÅºÅ²Û
        button.clicked.connect(self.add)
        #button.clicked.connect(self.info)

        # ´´½¨Ò»¸ö´¹Ö±²¼¾Ö£¬ÓÃÓÚ·ÀÖ¹±í¸ñºÍ°´Å¥
        layout = QtGui.QVBoxLayout()
        layout.addWidget(table)
        layout.addWidget(button)

        self.setLayout(layout)

    def add(self):
        dialog = AskDialog(parent=self)
        #dialog = infoDialog(parent=self)
        #if dialog.exec_():
        #    self.model.appendRow((
        #        QtGui.QStandardItem(dialog.name()),
        #        QtGui.QStandardItem(str(dialog.age())),
        #        ))
        dialog.exec_()
        print("name=%s,age=%s"%(dialog.name(),str(dialog.age())))

        dialog.destroy()
    def info(self): 
        infostr='info need to show'
        dialog = InfoDialog(infostr,parent=self)
        dialog.exec_()
class AskDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.resize(240, 200)

        # ±í¸ñ²¼¾Ö£¬ÓÃÀ´²¼¾ÖQLabelºÍQLineEdit¼°QSpinBox
        grid = QtGui.QGridLayout()

        grid.addWidget(QtGui.QLabel('ProjectName', parent=self), 0, 0, 1, 1)

        self.leName = QtGui.QLineEdit(parent=self)
        grid.addWidget(self.leName, 0, 1, 1, 1)

        #grid.addWidget(QtGui.QLabel('Age', parent=self), 1, 0, 1, 1)

        #self.sbAge = QtGui.QSpinBox(parent=self)
        #grid.addWidget(self.sbAge, 1, 1, 1, 1)

        # ´´½¨ButtonBox£¬ÓÃ»§È·¶¨ºÍÈ¡Ïû
        buttonBox = QtGui.QDialogButtonBox(parent=self)
        buttonBox.setOrientation(QtCore.Qt.Horizontal) # ÉèÖÃÎªË®Æ½·½Ïò
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok) # È·¶¨ºÍÈ¡ÏûÁ½¸ö°´Å¥
        # Á¬½ÓÐÅºÅºÍ²Û
        buttonBox.accepted.connect(self.accept) # È·¶¨
        buttonBox.rejected.connect(self.reject) # È¡Ïû

        # ´¹Ö±²¼¾Ö£¬²¼¾Ö±í¸ñ¼°°´Å¥
        layout = QtGui.QVBoxLayout()

        # ¼ÓÈëÇ°Ãæ´´½¨µÄ±í¸ñ²¼¾Ö
        layout.addLayout(grid)

        # ·ÅÒ»¸ö¼ä¸ô¶ÔÏóÃÀ»¯²¼¾Ö
        spacerItem = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        layout.addItem(spacerItem)

        # ButtonBox
        layout.addWidget(buttonBox)

        self.setLayout(layout)

    def name(self):
        return self.leName.text()

    #def age(self):
    #    return self.sbAge.value()

class InfoDialog(QtGui.QDialog):
    def __init__(self, infostr,parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.resize(240, 200)

        # ±í¸ñ²¼¾Ö£¬ÓÃÀ´²¼¾ÖQLabelºÍQLineEdit¼°QSpinBox
        grid = QtGui.QGridLayout()

        grid.addWidget(QtGui.QLabel(infostr, parent=self), 0, 0, 1, 1)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
