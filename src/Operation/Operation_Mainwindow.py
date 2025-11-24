#-----------------------------------------------------------------------
# Purpouse: The operation controller for the user interface
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-10-27  
#-----------------------------------------------------------------------


import sys  # Import system-specific parameters and functions
import os
import webbrowser
import logging
import subprocess
import time
import json
import pandas as pd
import difflib

from pathlib import Path
from urllib.parse import quote_plus

#-----------------------------------------------------------------------
# Import PyQt5 widgets for UI elements
from PySide6.QtWidgets import ( 
    QApplication, 
    QMainWindow, QTextEdit, QToolBar, QDockWidget, QListWidget, QFileDialog,
    QLabel, QFileDialog, QAbstractButton, QWidget, QStackedWidget, QTabWidget,    
    QLineEdit, QSplitter, 
    QPushButton, QRadioButton, QButtonGroup, QWidgetAction,
    QVBoxLayout, QHBoxLayout, QSizePolicy, QTreeWidget, QTreeWidgetItem, QCheckBox,
    QFormLayout, QGridLayout, QDialog, QDialogButtonBox, QComboBox,
    QMessageBox
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QAction, QPainter                              # Import classes for images, fonts, and icons
from PySide6.QtCore import Qt, QSize, QDateTime, Signal, QSettings, QObject, Slot, QThread      # Import Qt core functionalities such as alignment
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# Impot the class from the local python files
from Utils.Utils import utils
# from GUI.Virtual_Keyboard import CalculatorKeyboard
# from GUI.Page_Log import LogWidget, QTextEditHandler
# from GUI.Operation_Computing import Compute_Thread
#-----------------------------------------------------------------------




#-----------------------------------------------------------------------
class Operation_Mainwindow_Controller(QObject):

    def __init__(self, parent=None): 

        super().__init__(parent) 

        # Get the main window from the parent
        self.main_window = parent

        # Get the language manager from the main window
        self.lang_manager = getattr(self.main_window, "language_manager", None) 

    # ----------------------- Signal Handlers ------------------------


    # ----------------------------------------------------------------
    # Show the perference setting dialog
    def handle_show_setting(self):

        print("Toolbar: Show setting")

        # Show the setting dialog
        self.main_window.setting_page.show()

    # ----------------------------------------------------------------



    # ----------------------------------------------------------------
    # The function to perform Baidu search
    def perform_baidu_search(self):
            
        query = self.main_window.tool_bar.search_input.text().strip()
        if query:
            encoded_query = quote_plus(query)
            url = f"https://www.baidu.com/s?wd={encoded_query}"
        else:
            url = "https://www.baidu.com"

        webbrowser.open(url)

        # self.main_window.close()  # Close dialog after search
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # The function to perform google search
    def perform_google_search(self):
        query = self.main_window.tool_bar.search_input.text().strip()
        if query:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        else:
            url = "https://www.google.com"

        webbrowser.open(url)


        # Close the window after search
        # self.main_window.close()
    # ----------------------------------------------------------------





