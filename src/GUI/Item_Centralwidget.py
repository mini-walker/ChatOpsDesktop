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
    def __init__(self, parent=None):
        super().__init__(parent)
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
            if img_w == 0 or img_h == 0:
                return

            ratio = max(win_w / img_w, win_h / img_h)
            new_w = int(img_w * ratio)
            new_h = int(img_h * ratio)

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

        super().__init__(parent)

        self._last_send_time = 0
        self._send_debounce_ms = 300

        self.main_window = parent

        self.setStyleSheet("background-color: #F5F5F5;")

        self.pending_images = []

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

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

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumWidth(800)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.viewport().setStyleSheet("background: transparent;")

        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollArea > QWidget > QWidget { 
                background: transparent; 
            }
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

        self.result_container = QWidget()
        self.result_container.setStyleSheet("background: transparent;")
        
        self.result_layout = QVBoxLayout(self.result_container)
        self.result_layout.setAlignment(Qt.AlignTop)
        self.result_layout.setSpacing(10)

        self.bottom_buffer = QWidget()
        self.bottom_buffer.setFixedHeight(150)
        self.bottom_buffer.setStyleSheet("background: transparent;")
        self.result_layout.addWidget(self.bottom_buffer)
        self.result_layout.addStretch()

        self.scroll_area.setWidget(self.result_container)
        
        self.stack_layout.insertWidget(1, self.scroll_area)
        self.scroll_area.raise_()

        main_layout.addWidget(self.stack_container)

        self.input_container = QFrame(self)
        self.input_container.setObjectName("Chat_Input_Container")
        self.input_container.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 12px;
                padding: 6px 3px 6px 6px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        self.input_min_height = 40
        self.input_max_height = 120

        self.input_container.setMinimumHeight(self.input_min_height)
        self.input_container.setMaximumHeight(self.input_max_height)

        input_container_layout = QVBoxLayout(self.input_container)
        input_container_layout.setContentsMargins(0, 0, 0, 0)
        input_container_layout.setContentsMargins(0, 0, 0, 6)

        self.chat_line_edit = QTextEdit()
        self.chat_line_edit.setPlaceholderText("Ask anything...")
        self.chat_line_edit.setStyleSheet("QScrollBar { margin: 0px; }")
        self.chat_line_edit.setStyleSheet("""
            QTextEdit {
                border: none;
                background: transparent;
                font-size: 13pt;
                line-height: 1.5;
                padding: 0px 0px 0px 0px;
            }
            QTextEdit::viewport {
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
                margin: 0px 0px 14px 0;
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

        self.chat_line_edit.installEventFilter(self)
        self.chat_line_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.chat_line_edit.customContextMenuRequested.connect(self.show_context_menu)

        input_container_layout.addWidget(self.chat_line_edit)

        self.floating_toptoolbar = QFrame(self)
        self.floating_toptoolbar.setObjectName("floatingtoptoolbar")
        self.floating_toptoolbar.setStyleSheet("""
            QFrame#floatingtoptoolbar {
                background: transparent;
                border: None;
            }
        """)
        self.floating_toptoolbar.setFixedHeight(40)
        self.floating_toptoolbar.setMinimumWidth(self.result_container.width())

        toptoolbar_layout = QHBoxLayout(self.floating_toptoolbar)
        toptoolbar_layout.setContentsMargins(0, 0, 0, 0)
        toptoolbar_layout.setSpacing(0)

        def make_btn(icon, text):
            btn = QPushButton()
            btn.setIcon(QIcon(utils.resource_path(icon)))
            btn.setIconSize(QSize(20, 20))
            btn.setText(text)
            btn.setMinimumWidth(100)
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

        self.btn_new_folder  = make_btn("images/WIN11-Icons/icons8-folder-100.png", "New folder")
        self.btn_new_chat    = make_btn("images/WIN11-Icons/icons8-chat-room-100.png", "New chat")
        self.btn_image       = make_btn("images/WIN11-Icons/icons8-add-image-100.png", "Insert image")
        self.btn_settings    = make_btn("images/WIN11-Icons/icons8-settings-100.png", "Settings")

        self.btn_image.clicked.connect(self.insert_image)
        self.btn_new_chat.clicked.connect(self.new_chat_requested_from_chatwindow.emit)
        self.btn_new_folder.clicked.connect(self.new_folder_requested_from_chatwindow.emit)
        self.btn_settings.clicked.connect(self.show_setting_page_requested_from_chatwindow.emit)

        toptoolbar_layout.addWidget(self.btn_new_folder)
        toptoolbar_layout.addWidget(self.btn_new_chat)
        toptoolbar_layout.addWidget(self.btn_image)
        toptoolbar_layout.addWidget(self.btn_settings)
        toptoolbar_layout.addStretch()

        for i in range(toptoolbar_layout.count()):
            btn = toptoolbar_layout.itemAt(i).widget()
            if isinstance(btn, QPushButton):
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

        self.btn_send = QPushButton(self)
        self.btn_send.setIcon(QIcon(utils.resource_path("images/WIN11-Icons/icons8-enter-100.png")))
        self.btn_send.setIconSize(QSize(22, 22))
        self.btn_send.setToolTip("Send message")
        self.btn_send.setFixedSize(30, 30)
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
        self.btn_send.raise_()

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 3)

        self.input_container.setGraphicsEffect(shadow)

        self.input_container.setParent(self)
        self.input_container.raise_()

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
        if is_gif:
            movie = QMovie(image_path)
            movie.setCacheMode(QMovie.CacheAll)
            self.background_label.setMovie(movie)
        else:
            pix = QPixmap(image_path)
            self.background_label.setPixmap(pix)
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
                padding: 4px;
            }
            QMenu::item {
                background-color: transparent;
                padding: 2px 8px 2px 8px;
                border-radius: 6px;
                margin: 2px 4px;
            }
            QMenu::item:selected {
                background-color: #f0f0f0;
                color: #000000;
            }
            QMenu::separator {
                height: 1px;
                background: #dddddd;
                margin: 4px 0;
            }
        """)
        menu.exec(self.chat_line_edit.mapToGlobal(pos))

    def on_send_clicked(self):
        text = self.chat_line_edit.toPlainText().strip()
        if not text and not self.pending_images:
            return
        images = self.pending_images.copy()
        self.send_message_signal.emit(text, images)
        self.chat_line_edit.clear()
        self.pending_images.clear()
        self.messages_count += 1
        self.adjust_input_height()
        self.update_input_container_position()
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def eventFilter(self, obj, event):
        if obj == self.chat_line_edit and event.type() == QEvent.KeyPress:
            key_event = event
            if key_event.key() in (Qt.Key_Enter, Qt.Key_Return):
                if key_event.modifiers() & Qt.ShiftModifier:
                    self.chat_line_edit.insertPlainText("\n")
                    return True
                else:
                    current_time = QDateTime.currentMSecsSinceEpoch()
                    if current_time - self._last_send_time >= self._send_debounce_ms:
                        self.on_send_clicked()
                        self._last_send_time = current_time
                    else:
                        print("Send ignored due to debounce")
                    return True
        return super().eventFilter(obj, event)

    def insert_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_name:
            self.selected_image = file_name
            print("Image selected:", file_name)
            self.pending_images.append(file_name)
            cursor = self.chat_line_edit.textCursor()
            cursor.movePosition(QTextCursor.End)
            img_format = QTextImageFormat()
            img_format.setName(file_name)
            img_format.setWidth(80)
            img_format.setHeight(80)
            cursor.insertImage(img_format)
            cursor.insertText(" ")

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
        if scaled_pix.width() > win_w or scaled_pix.height() > win_h:
            x = (scaled_pix.width() - win_w) // 2
            y = (scaled_pix.height() - win_h) // 2
            scaled_pix = scaled_pix.copy(x, y, win_w, win_h)
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
        if scaled_pix.width() > win_w or scaled_pix.height() > win_h:
            x = (scaled_pix.width() - win_w) // 2
            y = (scaled_pix.height() - win_h) // 2
            scaled_pix = scaled_pix.copy(x, y, win_w, win_h)
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
        while layout.count() > 2:
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def update_ui_texts(self, lang_manager):
        if not lang_manager: return
        self.btn_new_folder.setText(lang_manager.get_text("New folder"))
        self.btn_new_chat.setText(lang_manager.get_text("New chat"))
        self.btn_image.setText(lang_manager.get_text("Insert image"))
        self.btn_settings.setText(lang_manager.get_text("Settings"))
        self.btn_send.setToolTip(lang_manager.get_text("Send message"))
        self.chat_line_edit.setPlaceholderText(lang_manager.get_text("Ask anything..."))
