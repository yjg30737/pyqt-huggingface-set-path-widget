import os
import subprocess
import sys

# Get the absolute path of the current script file
from PyQt5.QtGui import QGuiApplication, QFont

script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from transformers import TRANSFORMERS_CACHE

from PyQt5.QtCore import Qt, QSettings, QCoreApplication
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QMenu, QAction, QApplication
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog, QLabel

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support
# qt version should be above 5.14
QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

QApplication.setFont(QFont('Arial', 12))


class FindPathLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setMouseTracking(True)
        self.setReadOnly(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__prepareMenu)

    def mouseMoveEvent(self, e):
        self.__showToolTip()
        return super().mouseMoveEvent(e)

    def __showToolTip(self):
        text = self.text()
        text_width = self.fontMetrics().boundingRect(text).width()

        if text_width > self.width():
            self.setToolTip(text)
        else:
            self.setToolTip('')

    def __prepareMenu(self, pos):
        menu = QMenu(self)
        openDirAction = QAction('Open Path')
        openDirAction.setEnabled(self.text().strip() != '')
        openDirAction.triggered.connect(self.__openPath)
        menu.addAction(openDirAction)
        menu.exec(self.mapToGlobal(pos))

    def __openPath(self):
        filename = self.text()
        path = filename.replace('/', '\\')
        subprocess.Popen(r'explorer /select,"' + path + '"')


class FindPathWidget(QWidget):
    findClicked = pyqtSignal()
    onCacheDirSet = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__ext_of_files = ''
        self.__directory = False

        self.__settings_struct = QSettings('hf.ini', QSettings.IniFormat)
        if self.__settings_struct.contains('CACHE_DIR'):
            pass
        # set the cache_dir if ini file is initially made
        else:
            self.__settings_struct.setValue('CACHE_DIR', os.path.normpath(TRANSFORMERS_CACHE))
        self.onCacheDirSet.emit(self.__settings_struct.value('CACHE_DIR'))

    def __initUi(self):
        self.__pathLineEdit = FindPathLineEdit()
        self.__pathLineEdit.setText(self.__settings_struct.value('CACHE_DIR'))

        self.__pathFindBtn = QPushButton('Find...')

        self.__pathFindBtn.clicked.connect(self.__find)

        self.__pathLineEdit.setMaximumHeight(self.__pathFindBtn.sizeHint().height())

        lay = QHBoxLayout()
        lay.addWidget(self.__pathLineEdit)
        lay.addWidget(self.__pathFindBtn)

        self.setLayout(lay)

    def __customFind(self):
        self.findClicked.emit()

    def __find(self):
        dirname = QFileDialog.getExistingDirectory(None, 'Set Path', '', QFileDialog.ShowDirsOnly)
        if dirname:
            self.__cache_dir = dirname
            self.__handleSettingCacheDir()

    def resetCacheDir(self):
        self.__cache_dir = TRANSFORMERS_CACHE
        self.__handleSettingCacheDir()

    def __handleSettingCacheDir(self):
        self.__pathLineEdit.setText(self.__cache_dir)
        self.__settings_struct.setValue('CACHE_DIR', os.path.normpath(self.__cache_dir))
        self.onCacheDirSet.emit(self.__settings_struct.value('CACHE_DIR'))

    def getCacheDirectory(self):
        return self.__pathLineEdit.text()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = FindPathWidget()
    w.show()
    sys.exit(app.exec())
