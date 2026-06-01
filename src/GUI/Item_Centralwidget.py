#-----------------------------------------------------------------------------------------
# Purpouse: This file is built to create the central widget of the chat window
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-11-23 
#----------------------------------------------------------------------------------------- 


import sys  # Import system-specific parameters and functions
import os
import webbrowser

from pathlib import Path


#-----------------------------------------------------------------------------------------
# Import PyQt5 widgets for UI elements
from PySide6.QtWidgets import ( 
    QApplication, 
    QMainWindow, QTextEdit, QToolBar, QDockWidget, QListWidget, QFileDialog, QGraphicsDropShadowEffect,
    QLabel, QTextEdit, QFileDialog, QAbstractButton, QWidget, QStackedWidget, QStackedLayout,    
    QLineEdit, QSplitter, QScrollArea, QFrame,
    QPushButton, QRadioButton, QButtonGroup, QWidgetAction,
    QVBoxLayout, QHBoxLayout, QSizePolicy, QTreeWidget, QTreeWidgetItem, QCheckBox,
    QFormLayout, QGridLayout, QDialog, QDialogButtonBox, QComboBox,
    QMenu
)
from PySide6.QtGui import QPixmap, QPainter, QIcon, QAction, QMovie, QColor, QTextCursor, QTextImageFormat   # Import classes for images, fonts, and icons
from PySide6.QtCore import Qt, QSize, QDateTime, Signal, QTimer, QRect, QEvent          # Import Qt core functionalities such as alignment
#-----------------------------------------------------------------------------------------




# Add the parent directory to the Python path for debugging (independent execution)
# ***Sometimes, the Vscode will load wrong python interpreter, if the code doesn't run, try to change the interpreter.
if __name__ == "__main__": 

    print("Debug mode!")   

    # Get project root folder
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if project_root not in sys.path: sys.path.insert(0, project_root)





#-----------------------------------------------------------------------------------------
# Impot the class from the local python files
from Utils.Utils import utils

from Operation.Operation_Bubble_Message import BubbleMessage
#-----------------------------------------------------------------------------------------


class AspectRatioLabel(QLabel):
<<<<<<< HEAD
    """
    Custom Label: Solves GIF looping jitter and implements CSS Cover (fill) effect.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Ignore layout size constraints
=======
    def __init__(self, parent=None):
        super().__init__(parent)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setScaledContents(False)
        self.m_pixmap = None
        self.m_movie = None

    def setPixmap(self, pixmap):
        if self.m_movie:
            self.m_movie.stop()
            self.m_movie = None
        self.m_pixmap = pixmap
        self.update()

    def setMovie(self, movie):
        if self.m_movie:
            self.m_movie.stop()
        self.m_movie = movie
        self.m_pixmap = None
        self.m_movie.frameChanged.connect(self.repaint)
        self.m_movie.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        current_pix = None
        if self.m_movie:
            current_pix = self.m_movie.currentPixmap()
        elif self.m_pixmap:
            current_pix = self.m_pixmap

        if current_pix and not current_pix.isNull():
            win_w = self.width()
            win_h = self.height()
            img_w = current_pix.width()
            img_h = current_pix.height()
<<<<<<< HEAD
            if img_w == 0 or img_h == 0: return

            # Cover algorithm: take the maximum scaling ratio
            ratio = max(win_w / img_w, win_h / img_h)
            new_w = int(img_w * ratio)
            new_h = int(img_h * ratio)
            
            # Draw centered
=======
            if img_w == 0 or img_h == 0:
                return

            ratio = max(win_w / img_w, win_h / img_h)
            new_w = int(img_w * ratio)
            new_h = int(img_h * ratio)

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            x = (win_w - new_w) // 2
            y = (win_h - new_h) // 2
            target_rect = QRect(x, y, new_w, new_h)
            painter.drawPixmap(target_rect, current_pix)





#===============================================================================
class Chat_Central_Widget(QWidget):

    # Define a custom signal
    send_message_signal = Signal(str, list)  # text, images
    show_setting_page_requested_from_chatwindow = Signal()
    new_chat_requested_from_chatwindow          = Signal()
    new_folder_requested_from_chatwindow        = Signal()

    def __init__(self, parent=None):

<<<<<<< HEAD

        super().__init__(parent)

        # Last send timestamp for debounce
        self._last_send_time = 0
        self._send_debounce_ms = 300  # Minimum 300 ms between consecutive sends

        # Get the main window from the parent
        self.main_window = parent

        # self.setAttribute(Qt.WA_StyledBackground, True)
=======
        super().__init__(parent)

        self._last_send_time = 0
        self._send_debounce_ms = 300

        self.main_window = parent

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.setStyleSheet("background-color: #F5F5F5;")

        self.pending_images = []

<<<<<<< HEAD

        #-------------------------------------------------------------------------
        # Initialize the main layout
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

<<<<<<< HEAD
        # ============================================================
        # [Core Modification] Create a stacked layout container
        # Used to stack the "background image layer" and the "message scrolling layer" together
        # ============================================================
        self.stack_container = QWidget()
        self.stack_layout = QStackedLayout(self.stack_container)
        self.stack_layout.setStackingMode(QStackedLayout.StackAll) # Key: Allow transparency, displaying both layers simultaneously

        # ---------------- Layer 1: Background Layer (Bottom) ----------------
        self.background_label = QLabel()
        self.background_label = AspectRatioLabel()
        self.background_label.setAlignment(Qt.AlignCenter)
        self.background_label.setStyleSheet("background-color: #f5f5f5;") 
        
        # Disable automatic label content scaling (we need to manually control the QMovie dimensions)
        self.background_label.setScaledContents(False)

        # Set minimum size to 1x1
        # Tell the layout manager: this widget can shrink this small, do not limit window shrinking
        self.background_label.setMinimumSize(1, 1)

        # [Key Fix 2] Set size policy to Ignored
        # Tell the layout manager: ignore the image's native size, completely follow layout instructions
        self.background_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.stack_layout.insertWidget(0, self.background_label)
        
        # Track current background state
        self.current_background_image_path = None
        self.current_background_is_gif = False

        # Memory cache to avoid repeated disk reads
        self.cached_bg_pixmap = None

        # Debounce timer for high-definition rendering after window resize stops
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.setInterval(100) # 100ms delay
        self.resize_timer.timeout.connect(self._perform_high_quality_scale)

        # ---------------- Layer 2: Message Scrolling Layer (Top) ----------------
        # 1. 初始化 Scroll Area
=======
        self.stack_container = QWidget()
        self.stack_layout = QStackedLayout(self.stack_container)
        self.stack_layout.setStackingMode(QStackedLayout.StackAll)

        self.background_label = QLabel()
        self.background_label = AspectRatioLabel()
        self.background_label.setAlignment(Qt.AlignCenter)
        self.background_label.setStyleSheet("background-color: #f5f5f5;")
        self.background_label.setScaledContents(False)
        self.background_label.setMinimumSize(1, 1)
        self.background_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.stack_layout.insertWidget(0, self.background_label)

        self.current_background_image_path = None
        self.current_background_is_gif = False

        self.cached_bg_pixmap = None

        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.setInterval(100)
        self.resize_timer.timeout.connect(self._perform_high_quality_scale)

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumWidth(800)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.viewport().setStyleSheet("background: transparent;")

<<<<<<< HEAD
        # 2. [Key] Set fully transparent styling
        # We must make scroll-area, viewport, and widget transparent for the background image to show through
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent; /* Transparent */
                border: none;
            }
            /* Set viewport transparent (ViewPort) */
            QScrollArea > QWidget > QWidget { 
                background: transparent; 
            }
            
            /* Scrollbar styling (keep original) */
=======
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollArea > QWidget > QWidget { 
                background: transparent; 
            }
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            QScrollBar:vertical {
                background: transparent;
                width: 10px;
                margin: 4px 2px 4px 2px;
                border-radius: 8px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0,0,0,0.25);
                min-height: 30px;
                border-radius: 8px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0,0,0,0.45);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
        """)

<<<<<<< HEAD
        # 3. 初始化内容容器
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.result_container = QWidget()
        self.result_container.setStyleSheet("background: transparent;")
        
        self.result_layout = QVBoxLayout(self.result_container)
        self.result_layout.setAlignment(Qt.AlignTop)
        self.result_layout.setSpacing(10)

<<<<<<< HEAD
        # 底部缓冲
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.bottom_buffer = QWidget()
        self.bottom_buffer.setFixedHeight(150)
        self.bottom_buffer.setStyleSheet("background: transparent;")
        self.result_layout.addWidget(self.bottom_buffer)
        self.result_layout.addStretch()

<<<<<<< HEAD
        # 装载控件
        self.scroll_area.setWidget(self.result_container)
        
        # [Enforce] Insert at index 1 (above the background layer)
        self.stack_layout.insertWidget(1, self.scroll_area)
        
        # [Double Insurance] Force the message layer to the front
        self.scroll_area.raise_()

        # ============================================================
        
        # 最后把这个堆叠容器加入主布局
        main_layout.addWidget(self.stack_container)
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Floating window for input container, it is a rounded QFrame
        # The image, text input and send button will be put in this container
=======
        self.scroll_area.setWidget(self.result_container)
        
        self.stack_layout.insertWidget(1, self.scroll_area)
        self.scroll_area.raise_()

        main_layout.addWidget(self.stack_container)

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.input_container = QFrame(self)
        self.input_container.setObjectName("Chat_Input_Container")
        self.input_container.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 12px;
<<<<<<< HEAD
                padding: 6px 3px 6px 6px;  /* top right bottom left */
=======
                padding: 6px 3px 6px 6px;
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        self.input_min_height = 40
        self.input_max_height = 120

<<<<<<< HEAD
        # Adjust the minimum and maximum height of the input container
        self.input_container.setMinimumHeight(self.input_min_height)
        self.input_container.setMaximumHeight(self.input_max_height)

        input_container_layout = QVBoxLayout(self.input_container)  # Connect vertical layout to the input container
        input_container_layout.setContentsMargins(0, 0, 0, 0)
        input_container_layout.setContentsMargins(0, 0, 0, 6)       # left, top, right, bottom

        # The text input
=======
        self.input_container.setMinimumHeight(self.input_min_height)
        self.input_container.setMaximumHeight(self.input_max_height)

        input_container_layout = QVBoxLayout(self.input_container)
        input_container_layout.setContentsMargins(0, 0, 0, 0)
        input_container_layout.setContentsMargins(0, 0, 0, 6)

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.chat_line_edit = QTextEdit()
        self.chat_line_edit.setPlaceholderText("Ask anything...")
        self.chat_line_edit.setStyleSheet("QScrollBar { margin: 0px; }")
        self.chat_line_edit.setStyleSheet("""
            QTextEdit {
                border: none;
                background: transparent;
                font-size: 13pt;
                line-height: 1.5;
<<<<<<< HEAD
                padding: 0px 0px 0px 0px;   /* left, top, right, bottom */
=======
                padding: 0px 0px 0px 0px;
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            }
            QTextEdit::viewport {
                background: transparent;
            }
<<<<<<< HEAD
            /* the vertical scroll bar */
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;                    /* the width of the scroll bar */
                margin: 0px 0px 14px 0;   /* top right bottom left */
=======
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
                margin: 0px 0px 14px 0;
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 0, 0, 0.4);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 0, 0, 0.6);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                width: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
<<<<<<< HEAD
            /* the horizontal scroll bar (optional) */
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            QScrollBar:horizontal {
                border: none;
                background: rgba(0, 0, 0, 0.1);
                height: 8px;
                margin: 0 4px 0 4px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(0, 0, 0, 0.4);
                min-width: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal:hover {
                background: rgba(0, 0, 0, 0.6);
            }
        """)

        self.chat_line_edit.setAlignment(Qt.AlignVCenter)
        self.chat_line_edit.setMinimumHeight(self.input_min_height)
        self.chat_line_edit.setMaximumHeight(self.input_max_height)
        self.chat_line_edit.textChanged.connect(self.adjust_input_height)

<<<<<<< HEAD


        # Change enter to shift + enter
        # Enter --- submit message
        # Shift + Enter --- new line
        self.chat_line_edit.installEventFilter(self)

        # Define a custom context menu
        self.chat_line_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        # Connect signal to custom slot function
        self.chat_line_edit.customContextMenuRequested.connect(self.show_context_menu)

        # Put the text input in the input container layout
        input_container_layout.addWidget(self.chat_line_edit)  # 0 no stretch, default stretch is 0



        #++++++++++++++++++++++++++++++++++++++++
        # Floating button toolbar container
        #++++++++++++++++++++++++++++++++++++++++
=======
        self.chat_line_edit.installEventFilter(self)
        self.chat_line_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.chat_line_edit.customContextMenuRequested.connect(self.show_context_menu)

        input_container_layout.addWidget(self.chat_line_edit)

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.floating_toptoolbar = QFrame(self)
        self.floating_toptoolbar.setObjectName("floatingtoptoolbar")
        self.floating_toptoolbar.setStyleSheet("""
            QFrame#floatingtoptoolbar {
<<<<<<< HEAD
                background: transparent;   /* green rgba(0, 255, 0, 0.2) for debug, change to transparent when done */
=======
                background: transparent;
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                border: None;
            }
        """)
        self.floating_toptoolbar.setFixedHeight(40)
        self.floating_toptoolbar.setMinimumWidth(self.result_container.width())

        toptoolbar_layout = QHBoxLayout(self.floating_toptoolbar)
<<<<<<< HEAD
        toptoolbar_layout.setContentsMargins(0, 0, 0, 0) # left, top, right, bottom
        toptoolbar_layout.setSpacing(0)


        # ------------------------------------------------------
        # IMPORTANT: buttons must NOT use parent=self!!!
        # ------------------------------------------------------
        def make_btn(icon, text):
            btn = QPushButton()                # no parent
            btn.setIcon(QIcon(utils.resource_path(icon)))
            btn.setIconSize(QSize(20, 20))
            btn.setText(text)
            btn.setMinimumWidth(100)  # prevent being squeezed
=======
        toptoolbar_layout.setContentsMargins(0, 0, 0, 0)
        toptoolbar_layout.setSpacing(0)

        def make_btn(icon, text):
            btn = QPushButton()
            btn.setIcon(QIcon(utils.resource_path(icon)))
            btn.setIconSize(QSize(20, 20))
            btn.setText(text)
            btn.setMinimumWidth(100)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            btn.setStyleSheet("""
                QPushButton {
                    padding: 4px 8px;
                    background: transparent;
                    border-radius: 6px;
                    border: none;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.15);
                }
            """)
            return btn

<<<<<<< HEAD
        # Buttons
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.btn_new_folder  = make_btn("images/WIN11-Icons/icons8-folder-100.png", "New folder")
        self.btn_new_chat    = make_btn("images/WIN11-Icons/icons8-chat-room-100.png", "New chat")
        self.btn_image       = make_btn("images/WIN11-Icons/icons8-add-image-100.png", "Insert image")
        self.btn_settings    = make_btn("images/WIN11-Icons/icons8-settings-100.png", "Settings")

<<<<<<< HEAD
        # Connect button signals
        self.btn_image.clicked.connect(self.insert_image)

        # Submit the button signals to the main window to call the corresponding functions in side panel
        self.btn_new_chat.clicked.connect(
            self.new_chat_requested_from_chatwindow.emit
        )
        self.btn_new_folder.clicked.connect(
            self.new_folder_requested_from_chatwindow.emit
        )
        self.btn_settings.clicked.connect(
            self.show_setting_page_requested_from_chatwindow.emit
        )

        # Add to layout
=======
        self.btn_image.clicked.connect(self.insert_image)
        self.btn_new_chat.clicked.connect(self.new_chat_requested_from_chatwindow.emit)
        self.btn_new_folder.clicked.connect(self.new_folder_requested_from_chatwindow.emit)
        self.btn_settings.clicked.connect(self.show_setting_page_requested_from_chatwindow.emit)

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        toptoolbar_layout.addWidget(self.btn_new_folder)
        toptoolbar_layout.addWidget(self.btn_new_chat)
        toptoolbar_layout.addWidget(self.btn_image)
        toptoolbar_layout.addWidget(self.btn_settings)
<<<<<<< HEAD

        # Send History checkbox (default: unchecked = no history sent)
        from PySide6.QtWidgets import QCheckBox
        self.send_history_cb = QCheckBox("Send History")
        self.send_history_cb.setChecked(False)
        self.send_history_cb.setToolTip("Send previous conversation context to the AI")
        self.send_history_cb.setStyleSheet("""
            QCheckBox:hover {
                color: #333;
                background-color: rgba(0, 0, 0, 0.04);
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1.5px solid #bbb;
                border-radius: 3px;
            }
            QCheckBox::indicator:hover {
                border-color: #888;
            }
            QCheckBox::indicator:checked {
                background-color: #555;
                border-color: #555;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #444;
                border-color: #444;
            }
        """)
        self.send_history_cb.setCursor(Qt.PointingHandCursor)
        toptoolbar_layout.addWidget(self.send_history_cb)

        toptoolbar_layout.addStretch()

        # Style the buttons in the floating toolbar layout (toptoolbar_layout)
        for i in range(toptoolbar_layout.count()):
            btn = toptoolbar_layout.itemAt(i).widget()
            if isinstance(btn, QPushButton):

=======
        toptoolbar_layout.addStretch()

        for i in range(toptoolbar_layout.count()):
            btn = toptoolbar_layout.itemAt(i).widget()
            if isinstance(btn, QPushButton):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                btn.setStyleSheet("""
                    QPushButton {
                        padding: 0px;
                        margin: 0px;
                        border: none;
                        background: transparent;
                    }
                    QPushButton:hover {
                        background: #e9ecef;
                        border-radius: 6px;
                    }
                """)
<<<<<<< HEAD
        #++++++++++++++++++++++++++++++++++++++++

        #++++++++++++++++++++++++++++++++++++++++
        # The floating send button
=======

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.btn_send = QPushButton(self)
        self.btn_send.setIcon(QIcon(utils.resource_path("images/WIN11-Icons/icons8-enter-100.png")))
        self.btn_send.setIconSize(QSize(22, 22))
        self.btn_send.setToolTip("Send message")
<<<<<<< HEAD
        self.btn_send.setFixedSize(30, 30)      # Sometimes the QSS does not work, so set fixed size here
=======
        self.btn_send.setFixedSize(30, 30)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.btn_send.setStyleSheet("""
            QPushButton {
                padding: 0px;
                margin: 0px;
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                background: #e9ecef;
                border-radius: 6px;
            }
        """)

        self.btn_send.clicked.connect(self.on_send_clicked)
<<<<<<< HEAD
        self.btn_send.raise_()       # Move the floating send button to the top of the stack
        #++++++++++++++++++++++++++++++++++++++++



        #++++++++++++++++++++++++++++++++++++++++
        # Add a shadow effect to the input container
=======
        self.btn_send.raise_()

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 3)

        self.input_container.setGraphicsEffect(shadow)

        self.input_container.setParent(self)
        self.input_container.raise_()

<<<<<<< HEAD

        self.messages_count = 0        # Count of total messages
        self.resizeEvent(None)         # Initial positioning
        self.update_input_container_position()
    #-----------------------------------------------------------------------------




    #-----------------------------------------------------------------------------
    def set_chat_background(self, image_path):
        """
        Set chat background (Final Fix Version)
        """
        # 1. Invalid or empty path -> Clear background
        if not image_path or not os.path.exists(image_path):
            print("[INFO] Clearing background image.")
            
            # Stop GIF
            if self.background_label.movie():
                self.background_label.movie().stop()
                self.background_label.setMovie(None)

            # [Key Fix] Use clear() instead of setPixmap(None)
            self.background_label.clear()
            
            # If custom AspectRatioLabel is used, manually reset internal variables to trigger repaint
            if hasattr(self.background_label, "m_pixmap"):
                self.background_label.m_pixmap = None
                self.background_label.update()

            # Restore gray background
            self.background_label.setStyleSheet("background-color: #F5F5F5;")
            
            self.current_background_image_path = None
            self.current_background_is_gif = False
            return

        # 2. Set new background
        self.current_background_image_path = image_path
        is_gif = image_path.lower().endswith(".gif")
        self.current_background_is_gif = is_gif

=======
        self.messages_count = 0
        self.resizeEvent(None)
        self.update_input_container_position()

    #-----------------------------------------------------------------------------


    #-----------------------------------------------------------------------------
    def set_chat_background(self, image_path):
        if not image_path or not os.path.exists(image_path):
            if self.background_label.movie():
                self.background_label.movie().stop()
                self.background_label.setMovie(None)
            self.background_label.clear()
            if hasattr(self.background_label, "m_pixmap"):
                self.background_label.m_pixmap = None
                self.background_label.update()
            self.background_label.setStyleSheet("background-color: #F5F5F5;")
            self.current_background_image_path = None
            self.current_background_is_gif = False
            return
        self.current_background_image_path = image_path
        is_gif = image_path.lower().endswith(".gif")
        self.current_background_is_gif = is_gif
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if is_gif:
            movie = QMovie(image_path)
            movie.setCacheMode(QMovie.CacheAll)
            self.background_label.setMovie(movie)
        else:
            pix = QPixmap(image_path)
            self.background_label.setPixmap(pix)
<<<<<<< HEAD
            
        # Set transparent background to avoid blocking
        self.background_label.setStyleSheet("background-color: transparent;")
        print(f"[INFO] Background set to: {image_path}")
    #-----------------------------------------------------------------------------





    #-----------------------------------------------------------------------------
    # Riggt click menu style for chat input box
    def show_context_menu(self, pos):
        
        menu = self.chat_line_edit.createStandardContextMenu()

        menu.setContentsMargins(0,4,0,4)  # Left, Top, Right, Bottom

        # Style: white background, hover light gray, rounded corners
        menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;      /* white background */
                color: #333333;                 /* dark text */
                border: 1px solid #cccccc;      /* light border */
                border-radius: 8px;             /* rounded corners */
=======
        self.background_label.setStyleSheet("background-color: transparent;")
        print(f"[INFO] Background set to: {image_path}")

    def show_context_menu(self, pos):
        menu = self.chat_line_edit.createStandardContextMenu()
        menu.setContentsMargins(0,4,0,4)
        menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 8px;
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                padding: 4px;
            }
            QMenu::item {
                background-color: transparent;
<<<<<<< HEAD
                padding: 2px 8px 2px 8px;     /* Adjust padding for comfort */
                border-radius: 6px;
                margin: 2px 4px;                /* Add margin for rounded look */
            }
            /* This controls the hover color */
            QMenu::item:selected {
                background-color: #f0f0f0;      /* hover light gray */
=======
                padding: 2px 8px 2px 8px;
                border-radius: 6px;
                margin: 2px 4px;
            }
            QMenu::item:selected {
                background-color: #f0f0f0;
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                color: #000000;
            }
            QMenu::separator {
                height: 1px;
                background: #dddddd;
                margin: 4px 0;
            }
        """)
<<<<<<< HEAD

        # Show the menu at the cursor position
        menu.exec(self.chat_line_edit.mapToGlobal(pos))
    #-----------------------------------------------------------------------------










    #-----------------------------------------------------------------------------
    # The send button
    def on_send_clicked(self):

        """
        Handles sending a message from the chat input area.
        
        Steps:
        1. Retrieves the text and pending images.
        2. Skips sending if both are empty.
        3. Emits the custom signal with text and images.
        4. Clears the input and pending image list.
        """

        text = self.chat_line_edit.toPlainText().strip()
        if not text and not self.pending_images:
            return  # Do not send empty messages

        # Copy images to avoid mutation during async send
        images = self.pending_images.copy()
        
        # Emit the signal for the main chat handler
        self.send_message_signal.emit(text, images)

        # Clear input box and temporary images after sending
        self.chat_line_edit.clear()
        self.pending_images.clear()

        # Update the position of the input container
=======
        menu.exec(self.chat_line_edit.mapToGlobal(pos))

    def on_send_clicked(self):
        text = self.chat_line_edit.toPlainText().strip()
        if not text and not self.pending_images:
            return
        images = self.pending_images.copy()
        self.send_message_signal.emit(text, images)
        self.chat_line_edit.clear()
        self.pending_images.clear()
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.messages_count += 1
        self.adjust_input_height()
        self.update_input_container_position()
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
<<<<<<< HEAD
    #-----------------------------------------------------------------------------



    #-----------------------------------------------------------------------------
    # The event filter
    def eventFilter(self, obj, event):
        """
        Custom event filter for the chat_line_edit widget to handle key press events.

        Behaviors:
        - Shift+Enter: insert a new line.
        - Enter: send the message, but prevent rapid double sends using debounce.
        """
=======

    def eventFilter(self, obj, event):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if obj == self.chat_line_edit and event.type() == QEvent.KeyPress:
            key_event = event
            if key_event.key() in (Qt.Key_Enter, Qt.Key_Return):
                if key_event.modifiers() & Qt.ShiftModifier:
<<<<<<< HEAD
                    # User wants a newline, insert '\n' without sending
                    self.chat_line_edit.insertPlainText("\n")
                    return True
                else:
                    # User wants to send the message
=======
                    self.chat_line_edit.insertPlainText("\n")
                    return True
                else:
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                    current_time = QDateTime.currentMSecsSinceEpoch()
                    if current_time - self._last_send_time >= self._send_debounce_ms:
                        self.on_send_clicked()
                        self._last_send_time = current_time
                    else:
<<<<<<< HEAD
                        # Ignore rapid repeat Enter
                        print("Send ignored due to debounce")
                    return True
        return super().eventFilter(obj, event)
    #-----------------------------------------------------------------------------



    #-----------------------------------------------------------------------------
    # The local operations
    # Function for inserting image
=======
                        print("Send ignored due to debounce")
                    return True
        return super().eventFilter(obj, event)

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    def insert_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_name:
<<<<<<< HEAD

=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            self.selected_image = file_name
            print("Image selected:", file_name)
            self.pending_images.append(file_name)
            cursor = self.chat_line_edit.textCursor()
            cursor.movePosition(QTextCursor.End)
<<<<<<< HEAD

=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            img_format = QTextImageFormat()
            img_format.setName(file_name)
            img_format.setWidth(80)
            img_format.setHeight(80)
            cursor.insertImage(img_format)
            cursor.insertText(" ")
<<<<<<< HEAD
    #-----------------------------------------------------------------------------


    #-----------------------------------------------------------------------------
    # The local operations
    def update_input_container_position(self):

        """
        Update the position of the input container and floating buttons.
        - No messages: float in the middle
        - Has messages: float at bottom
        Ensures buttons do not overlap with other interactive widgets.
        """

        # Container vertical position
        h = self.scroll_area.height()
        box_h = self.input_container.height()

        if self.messages_count == 0:
            y = int(h * 0.40)
        else:
            margin = 30   # Margin from bottom
            y = h - box_h - margin

        # Horizontal center
        x = int((self.width() - self.input_container.width()) / 2)
        self.input_container.move(x, y)
        self.input_container.raise_()

        # Floating buttons positioning
        # Put them just above the container, with small offsets
        top_btn_offset_y    = 28      # 8 px below input container
        bottom_btn_offset_y = box_h - 35      # 5 px above input container
        btn_spacing = 5      # horizontal spacing between buttons

        # ======= Position the floating toolbar =======
        toolbar_y = y - self.floating_toptoolbar.height() - 2   # above the input box
        toolbar_x = x + 5    # 5 px from left edge of input box

        # float the toolbar to the top-left of the input container
        self.floating_toptoolbar.move(toolbar_x, toolbar_y)

        # Send button on the bottom right
        fixed_btn_width = 30 
        right_margin = 8       # Desired margin in pixels from the right border

        btn_x = x + self.input_container.width() - fixed_btn_width - right_margin
        btn_y = y + box_h - 35 # Keep original Y-axis logic (35px from bottom)
        self.btn_send.move(btn_x, btn_y)

        # Raise buttons to top to receive events
        self.btn_image.raise_()
        self.btn_send.raise_()
    #-----------------------------------------------------------------------------


    #-----------------------------------------------------------------------------
    # Add this function to the ChatWindow class
    def showEvent(self, event):
        """
        Triggered when the window is shown.
        Uses 0ms delay to ensure the layout is fully calculated before programmatically correcting the input box position.
        """
        super().showEvent(event)
        
        # If the input box size wasn't calculated correctly either, adjust its height now (It should be done first)
        if hasattr(self, 'adjust_input_height'):
             QTimer.singleShot(0, self.adjust_input_height)

        # Execute position update with a 0ms delay
        # This allows Qt to render the window and fix the size first, then move the input box
        QTimer.singleShot(0, self.update_input_container_position)

    #-----------------------------------------------------------------------------

    #-----------------------------------------------------------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Update the input container height first
        if hasattr(self, 'adjust_input_height'):
            self.adjust_input_height()

        # Then update its width and its position
        self.update_input_container_position()
        
        # 1. If it's a GIF, do nothing (QMovie will handle it) or perform a simple resize
        if self.current_background_is_gif:
            self._update_background_size()
            return

        # 2. If it's a static image, for smoothness:
        # Perform a fast scale (FastTransformation) first to ensure the background moves dynamically without lag
        if self.cached_bg_pixmap:
            self._perform_fast_scale()
        
        # 3. Start timer, wait 100ms after the user stops resizing to perform high-definition rendering
        self.resize_timer.start()
    #-----------------------------------------------------------------------------

    #-----------------------------------------------------------------------------
    def _perform_fast_scale(self):
        """Fast scale: called while resizing to prioritize smoothness"""
        if not self.cached_bg_pixmap: return
        
        win_w = self.stack_container.width()
        win_h = self.stack_container.height()
        if win_w <= 0 or win_h <= 0: return

        # [Key] Use Qt.FastTransformation (fast speed, average quality)
        scaled_pix = self.cached_bg_pixmap.scaled(
            win_w, win_h,
            Qt.KeepAspectRatioByExpanding, 
            Qt.FastTransformation          
        )
        
        # Simple crop (centered)
=======

    def update_input_container_position(self):
        h = self.scroll_area.height()
        box_h = self.input_container.height()
        if self.messages_count == 0:
            y = int(h * 0.40)
        else:
            margin = 30
            y = h - box_h - margin
        x = int((self.width() - self.input_container.width()) / 2)
        self.input_container.move(x, y)
        self.input_container.raise_()
        top_btn_offset_y = 28
        bottom_btn_offset_y = box_h - 35
        btn_spacing = 5
        toolbar_y = y - self.floating_toptoolbar.height() - 2
        toolbar_x = x + 5
        self.floating_toptoolbar.move(toolbar_x, toolbar_y)
        fixed_btn_width = 30
        right_margin = 8
        btn_x = x + self.input_container.width() - fixed_btn_width - right_margin
        btn_y = y + box_h - 35
        self.btn_send.move(btn_x, btn_y)
        self.btn_image.raise_()
        self.btn_send.raise_()

    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, 'adjust_input_height'):
            QTimer.singleShot(0, self.adjust_input_height)
        QTimer.singleShot(0, self.update_input_container_position)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'adjust_input_height'):
            self.adjust_input_height()
        self.update_input_container_position()
        if self.current_background_is_gif:
            self._update_background_size()
            return
        if self.cached_bg_pixmap:
            self._perform_fast_scale()
        self.resize_timer.start()

    def _perform_fast_scale(self):
        if not self.cached_bg_pixmap: return
        win_w = self.stack_container.width()
        win_h = self.stack_container.height()
        if win_w <= 0 or win_h <= 0: return
        scaled_pix = self.cached_bg_pixmap.scaled(
            win_w, win_h,
            Qt.KeepAspectRatioByExpanding, 
            Qt.FastTransformation
        )
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if scaled_pix.width() > win_w or scaled_pix.height() > win_h:
            x = (scaled_pix.width() - win_w) // 2
            y = (scaled_pix.height() - win_h) // 2
            scaled_pix = scaled_pix.copy(x, y, win_w, win_h)
<<<<<<< HEAD

        self.background_label.setPixmap(scaled_pix)

    #-----------------------------------------------------------------------------
    def _perform_high_quality_scale(self):
        """High-quality scale: called when static to guarantee image quality"""
        if not self.cached_bg_pixmap: return
        
        win_w = self.stack_container.width()
        win_h = self.stack_container.height()
        if win_w <= 0 or win_h <= 0: return

        # [Key] Use Qt.SmoothTransformation (slower speed, excellent quality)
        scaled_pix = self.cached_bg_pixmap.scaled(
            win_w, win_h,
            Qt.KeepAspectRatioByExpanding, 
            Qt.SmoothTransformation        
        )

=======
        self.background_label.setPixmap(scaled_pix)

    def _perform_high_quality_scale(self):
        if not self.cached_bg_pixmap: return
        win_w = self.stack_container.width()
        win_h = self.stack_container.height()
        if win_w <= 0 or win_h <= 0: return
        scaled_pix = self.cached_bg_pixmap.scaled(
            win_w, win_h,
            Qt.KeepAspectRatioByExpanding, 
            Qt.SmoothTransformation
        )
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if scaled_pix.width() > win_w or scaled_pix.height() > win_h:
            x = (scaled_pix.width() - win_w) // 2
            y = (scaled_pix.height() - win_h) // 2
            scaled_pix = scaled_pix.copy(x, y, win_w, win_h)
<<<<<<< HEAD

        self.background_label.setPixmap(scaled_pix)

    #-----------------------------------------------------------------------------
    def _update_background_size(self):
        """
        Dedicated size update logic for GIFs.
        Implements CSS Cover (fill) effect and prevents jitter/flicker.
        """
        # 1. Only process GIFs
        if not self.current_background_is_gif:
            return

        movie = self.background_label.movie()
        if not movie or not movie.isValid():
            return

        # 2. Retrieve size
        win_w = self.stack_container.width()
        win_h = self.stack_container.height()
        
        # Try to retrieve original size if not already cached
        if not hasattr(self, 'gif_orig_size') or self.gif_orig_size.isEmpty():
            self.gif_orig_size = movie.currentImage().size()
            if self.gif_orig_size.isEmpty(): return # Abort if still empty

        img_w = self.gif_orig_size.width()
        img_h = self.gif_orig_size.height()

        if img_w == 0 or img_h == 0: return

        # 3. [Core Algorithm] Calculate the minimum scaling ratio required to fill the container
        # Similar to CSS object-fit: cover
        ratio_w = win_w / img_w
        ratio_h = win_h / img_h
        scale_ratio = max(ratio_w, ratio_h) # Take the larger value to ensure it fills

        # 4. Calculate target dimensions
        new_w = int(img_w * scale_ratio)
        new_h = int(img_h * scale_ratio)

        # 5. [Anti-jitter] Apply only when size change exceeds a certain threshold
        # Resizing QMovie is resource-heavy; ignore minor adjustments
        current_movie_size = movie.scaledSize()
        if abs(current_movie_size.width() - new_w) > 2 or abs(current_movie_size.height() - new_h) > 2:
            movie.setScaledSize(QSize(new_w, new_h))
    #-----------------------------------------------------------------------------

    #-----------------------------------------------------------------------------
    # Adjust the height of the text input and input container
    def adjust_input_height(self):
        """
        Adjust the height of the text input and the container based on content.
        Uses atomic setGeometry to ensure the input box grows UPWARDS.
        """
        
        # 1. Calculate the ideal height based on content
        doc_height = self.chat_line_edit.document().size().height() + 10
        new_height = int(max(self.input_min_height, min(self.input_max_height, doc_height)))
        
        curr_height = self.input_container.height()


        # Update width (from your original logic)
        if self.messages_count == 0:
            new_width = int(0.75 * self.scroll_area.width()) # match your init logic
        else:
            new_width = int(0.95 * self.scroll_area.width())
        
        self.input_container.setFixedWidth(new_width)

        
        # Only update if height actually changed
        if new_height != curr_height:
            
            # 2. Get current geometry
            geo = self.input_container.geometry()
            current_bottom_y = geo.y() + geo.height()
            
            # 3. Handle the "Center" mode vs "Bottom" mode logic
            h = self.scroll_area.height()
            
            if self.messages_count == 0:
                # [Case A] Initial State (Floating in Middle)
                # Keep the TOP fixed, let it grow down (standard behavior for center box)
                # Or if you prefer it to grow symmetrically, you need complex logic.
                # Usually growing down in the center is fine. 
                # BUT if you want to strictly fix this, we recalculate Y based on the center logic:
                new_y = int(h * 0.40) # Keep Y fixed as defined in update_input_container_position
                
                # If you prefer Center-Grows-Up behavior, uncomment below:
                # new_y = geo.y() - (new_height - curr_height) 
            else:
                # [Case B] Chat Mode (Anchored at Bottom) - The specific problem you faced
                # Logic: New Y = (Screen Height) - (New Height) - (Bottom Margin)
                margin = 30
                new_y = h - new_height - margin

            # 4. Atomic Update: Set Position (Y) and Size (Height) together
            # This prevents the visual "jump" or "growing down" artifact
            self.input_container.setGeometry(
                geo.x(),        # Keep X
                new_y,          # New Y (calculated to grow up)
                geo.width(),    # Keep Width
                new_height      # New Height
            )
            
            # 5. Sync the inner TextEdit height
            self.chat_line_edit.setFixedHeight(new_height)




            
            # 7. Update floating buttons (Send button, Toolbar) to follow the new Y
            self.update_input_container_position()
    #-----------------------------------------------------------------------------


    #-----------------------------------------------------------------------------
    # Clear all messages    
    def clear_all_messages(self):
        """
        Clear only the chat bubbles inside result_layout but keep bottom buffer and stretch.
        """
        layout = self.result_layout

        # layout.count() contains bottom_buffer and stretch
        # we want to keep the bottom buffer, so only delete the message bubbles in front
=======
        self.background_label.setPixmap(scaled_pix)

    def _update_background_size(self):
        if not self.current_background_is_gif:
            return
        movie = self.background_label.movie()
        if not movie or not movie.isValid():
            return
        win_w = self.stack_container.width()
        win_h = self.stack_container.height()
        if not hasattr(self, 'gif_orig_size') or self.gif_orig_size.isEmpty():
            self.gif_orig_size = movie.currentImage().size()
            if self.gif_orig_size.isEmpty(): return
        img_w = self.gif_orig_size.width()
        img_h = self.gif_orig_size.height()
        if img_w == 0 or img_h == 0: return
        ratio_w = win_w / img_w
        ratio_h = win_h / img_h
        scale_ratio = max(ratio_w, ratio_h)
        new_w = int(img_w * scale_ratio)
        new_h = int(img_h * scale_ratio)
        current_movie_size = movie.scaledSize()
        if abs(current_movie_size.width() - new_w) > 2 or abs(current_movie_size.height() - new_h) > 2:
            movie.setScaledSize(QSize(new_w, new_h))

    def adjust_input_height(self):
        doc_height = self.chat_line_edit.document().size().height() + 10
        new_height = int(max(self.input_min_height, min(self.input_max_height, doc_height)))
        curr_height = self.input_container.height()
        if self.messages_count == 0:
            new_width = int(0.75 * self.scroll_area.width())
        else:
            new_width = int(0.95 * self.scroll_area.width())
        self.input_container.setFixedWidth(new_width)
        if new_height != curr_height:
            geo = self.input_container.geometry()
            current_bottom_y = geo.y() + geo.height()
            h = self.scroll_area.height()
            if self.messages_count == 0:
                new_y = int(h * 0.40)
            else:
                margin = 30
                new_y = h - new_height - margin
            self.input_container.setGeometry(
                geo.x(),
                new_y,
                geo.width(),
                new_height
            )
            self.chat_line_edit.setFixedHeight(new_height)
            self.update_input_container_position()

    def clear_all_messages(self):
        layout = self.result_layout
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        while layout.count() > 2:
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
<<<<<<< HEAD
    #-----------------------------------------------------------------------------

    #-----------------------------------------------------------------------------
    # Update UI texts for localization
    def update_ui_texts(self, lang_manager):
        """
        Refresh interface text based on current language selection.
        """
        if not lang_manager: return

        # 1. Update floating toolbar buttons
=======

    def update_ui_texts(self, lang_manager):
        if not lang_manager: return
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.btn_new_folder.setText(lang_manager.get_text("New folder"))
        self.btn_new_chat.setText(lang_manager.get_text("New chat"))
        self.btn_image.setText(lang_manager.get_text("Insert image"))
        self.btn_settings.setText(lang_manager.get_text("Settings"))
<<<<<<< HEAD

        # 2. Update tooltips (Tooltips)
        self.btn_send.setToolTip(lang_manager.get_text("Send message"))


        # 3. Update input box placeholder
        self.chat_line_edit.setPlaceholderText(lang_manager.get_text("Ask anything..."))
    #-----------------------------------------------------------------------------


#===============================================================================






#--------------------------------------------------------------------------------
# For testing
if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Chat_Central_Widget()
    window.resize(600, 500)
    window.show()
    sys.exit(app.exec())
#--------------------------------------------------------------------------------

=======
        self.btn_send.setToolTip(lang_manager.get_text("Send message"))
        self.chat_line_edit.setPlaceholderText(lang_manager.get_text("Ask anything..."))
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
