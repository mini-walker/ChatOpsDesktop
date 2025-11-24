#-----------------------------------------------------------------------------------------
# Purpouse: This file is used to contain the main execution block of the application
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-11-15 
#----------------------------------------------------------------------------------------- 

import sys
import os

from pathlib import Path

from PySide6.QtWidgets import ( 
    QApplication, 
    QWidget, 
    QLabel, 
    QLineEdit, 
    QPushButton, QRadioButton, QButtonGroup,
    QVBoxLayout, QHBoxLayout,
    QFormLayout, QGridLayout,
    QMessageBox
)
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt, QSize, QSettings

from GUI.GUI_Chat_Combo import AI_Chat_App

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = AI_Chat_App()
    window.show()
    sys.exit(app.exec())
