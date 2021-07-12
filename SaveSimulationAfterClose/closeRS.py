from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QTextBrowser, QCheckBox, QPushButton, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtGui import  QIcon
from PyQt5.QtCore import QRect, pyqtSlot
from pywinauto.application import Application
from playsound import playsound
import os
import time
import sys

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Save RobotStudio simulation'
        self.left = 100
        self.top = 100
        self.width = 300
        self.height = 170
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon(App.resource_path("RS.png")))
        
        self.textBrowserLoadName = QLineEdit(self)
        self.textBrowserLoadName.setGeometry(QRect(10, 10, 280, 30))
        self.textBrowserLoadName.setPlaceholderText("directory and exe name")
        
        self.groupBoxActivity= QGroupBox(self)
        self.groupBoxActivity.setGeometry(QRect(10, 50, 280, 60))
        self.groupBoxActivity.setTitle("Action after saving:")

        self.checkBoxTurnOff = QCheckBox(self.groupBoxActivity)
        self.checkBoxTurnOff.setGeometry(QRect(10, 30, 170, 20))
        self.checkBoxTurnOff.setText("Turn off computer")

        self.checkBoxPlaySound = QCheckBox(self.groupBoxActivity)
        self.checkBoxPlaySound.setGeometry(QRect(180, 30, 170, 20))
        self.checkBoxPlaySound.setText("Play sound")

        self.pushButtonStart = QPushButton(self)
        self.pushButtonStart.setGeometry(QRect(10, 125, 280, 30))
        self.pushButtonStart.setText("start")
        self.pushButtonStart.clicked.connect(self.saveAsDialogMaintenance)

        self.show()
        
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def saveAsDialogMaintenance(self):
        saved = False
        self.hide()
        while (saved==False):
            try:
                directory = self.textBrowserLoadName.text()
                app = Application().connect(title_re="Save As")
                app.SaveAs.edit1.set_text(directory)
                ftptool = app.SaveAs.Save.click()
                try:
                    ftptooly = app.ConfirmSaveAs.Yes.click()
                except:
                    pass
                saved = True
            except:
                time.sleep(10)
        
        time.sleep(60)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Saving finished")
        msg.setWindowTitle("Saving finished")

        if self.checkBoxPlaySound.isChecked():
            playsound('end.wav')
        if self.checkBoxTurnOff.isChecked():
            os.system("shutdown /s /t 1")
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = App()
    sys.exit(app.exec_())
