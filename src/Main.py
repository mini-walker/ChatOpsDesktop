#-----------------------------------------------------------------------------------------
# Purpouse: This file is used to contain the main execution block of the application
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-11-15 
#----------------------------------------------------------------------------------------- 

<<<<<<< HEAD

import sys  # Import system-specific parameters and functions
=======
import sys
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
import os

from pathlib import Path

<<<<<<< HEAD
#-----------------------------------------------------------------------------------------
# Import PySide6 widgets for UI elements
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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
<<<<<<< HEAD
from PySide6.QtGui import QPixmap, QFont, QIcon                     # Import classes for images, fonts, and icons
from PySide6.QtCore import Qt, QSize, QSettings                     # Import Qt core functionalities such as alignment
#-----------------------------------------------------------------------------------------

from GUI.GUI_Chat_Combo import AI_Chat_App  # Import the AI_Chat_App class from the GUI_Chat_Combo module


#-----------------------------------------------------------------------------------------
# Main execution block
if __name__ == '__main__':  # Ensure this code runs only when the file is executed directly
    
    app = QApplication(sys.argv)    # Create the application object
    window = AI_Chat_App()          # Create an instance of the LoginWindow class in the "GUI_Login module"
    window.show()                   # Display the login window
    sys.exit(app.exec())            # Start the application's event loop
#-----------------------------------------------------------------------------------------
=======
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt, QSize, QSettings

from GUI.GUI_Chat_Combo import AI_Chat_App

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = AI_Chat_App()
    window.show()
    sys.exit(app.exec())
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
