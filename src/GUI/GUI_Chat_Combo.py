#-----------------------------------------------------------------------------------------
# Purpouse: This file is used to create the main window of the application
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-11-23 
#----------------------------------------------------------------------------------------- 

import sys
import os

from PySide6.QtWidgets import ( 
    QApplication, 
    QMainWindow, QTextEdit, QToolBar, QDockWidget, QListWidget, QFileDialog,
    QLabel, QTextEdit, QFileDialog, QAbstractButton, QWidget, QStackedWidget, QTabWidget,    
    QLineEdit, QSplitter, 
    QPushButton, QButtonGroup,
    QVBoxLayout, QHBoxLayout, QMdiArea, QMdiSubWindow, QSizePolicy, QCheckBox,
    QFormLayout, QGridLayout, QGroupBox, QComboBox,
    QMessageBox
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QPainter
from PySide6.QtCore import Qt, QSize, QTimer, Signal, QSettings, QEvent, QPropertyAnimation

if __name__ == "__main__": 
    print("Debug mode!")   
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path: sys.path.insert(0, project_root)

from Utils.Utils import utils
from GUI.Item_Toolbar import Tool_Bar
from GUI.Item_SettingPage import Setting_Window
from GUI.Item_Centralwidget import Chat_Central_Widget
from GUI.Item_SidePanel import Slide_Side_Panel
from GUI.Language_Manager import Language_Manager

from Operation.Operation_Mainwindow import Operation_Mainwindow_Controller
from Operation.Operation_Setting import Operation_Setting_Controller
from Operation.Operation_Chat_Controller import Operation_Chat_Controller

class AI_Chat_App(QMainWindow):

    def __init__(self):

        super().__init__()

        self.language_manager = Language_Manager()
        self.settings = None

        self.init_styles()
        self.init_main_ui()

        self.setting_page = Setting_Window(self)
        self.operation_mainwindow = Operation_Mainwindow_Controller(self)
        self.operation_setting = Operation_Setting_Controller(self)

        self.load_settings_on_startup()

        self.operation_chat    = Operation_Chat_Controller(self)

        self.connect_signals()

    def load_settings_on_startup(self):

        usr_folder = utils.get_usr_dir()
        settings_path = usr_folder / "settings.ini"
        
        settings = QSettings(str(settings_path), QSettings.Format.IniFormat)

        def check_and_set_default(key, default_value):
            if not settings.contains(key):
                settings.setValue(key, default_value)

        is_first_run = not settings_path.exists()
        
        if is_first_run:
            print("[INFO] No settings.ini found. Creating default settings...")

        check_and_set_default("Font/type", "Microsoft YaHei") 
        check_and_set_default("Font/size", 10)
        
        check_and_set_default("Appearance/theme", "Light")
        check_and_set_default("Appearance/toolbar_icons", True)
        
        check_and_set_default("Appearance/chat_background", "") 

        check_and_set_default("Language/type", "English")

        check_and_set_default("Search/Baidu", True)
        check_and_set_default("Search/Google", False)

        old_key = settings.value("Advanced/api_key", "")
        if old_key and not settings.contains("AI/api_key"):
            print("[INFO] Migrating old API Key to new AI settings structure...")
            settings.setValue("AI/api_key", old_key)
            settings.remove("Advanced")
        
        usr_dir = utils.get_usr_dir()
        account_file = usr_dir / "account.json"
        default_provider, default_base_url, default_key, default_models = self.tool_bar.load_AI_config(account_file)
        if default_provider and default_base_url and default_key and default_models:
            print("[INFO] Provider (GUI):", default_provider)
            print("[INFO] Base URL (GUI):", default_base_url)
            print("[INFO] API Key (GUI):", default_key)
            print("[INFO] Models (GUI):", default_models)
        else:
            print("[ERROR] (GUI) Failed to load OpenRouter configuration.")

        default_provider_lower = default_provider.lower()
        found_index = -1

        for i in range(self.setting_page.provider_combo.count()):
            item_lower = self.setting_page.provider_combo.itemText(i).lower()
            if default_provider_lower in item_lower:
                found_index = i
                break

        if found_index != -1:
            self.setting_page.provider_combo.setCurrentIndex(found_index)
            selected_provider = self.setting_page.provider_combo.itemText(found_index)
            print(f"[INFO] Set provider combo box to index {found_index} ({selected_provider})")
        else:
            custom_index = self.setting_page.provider_combo.findText("Custom")
            self.setting_page.provider_combo.setCurrentIndex(custom_index)
            selected_provider = "Custom"
            print("[INFO] Provider not found in combo box. Setting to 'Custom'")

        if default_provider and default_base_url and default_key:
            print("[INFO] Overwriting settings.ini AI config with account.json values...")

            settings.setValue("AI/provider", selected_provider)
            settings.setValue("AI/base_url", default_base_url)
            settings.setValue("AI/api_key", default_key)
            settings.setValue("AI/model", default_models[0] if default_models else "openai/gpt-oss-120b")

        else:
            print("[WARN] account.json has no valid values. Using settings.ini or defaults.")

        check_and_set_default("AI/system_prompt", "You are a helpful assistant.")
        check_and_set_default("AI/temperature", 0.7)

        settings.sync()
        self.settings = settings
        
        if is_first_run:
            print("[INFO] Default settings created successfully.")
        else:
            print(f"[INFO] Settings loaded from: {settings_path}")

        if hasattr(self, "operation_setting"):
            self.operation_setting.apply_new_settings()

    def connect_signals(self):

        self.tool_bar.show_side_panel_requested.connect(self.toggle_side_panel)
        self.tool_bar.show_setting_page_requested.connect(self.operation_mainwindow.handle_show_setting)
        self.side_panel.show_settings_requested.connect(self.operation_mainwindow.handle_show_setting)

        self.tool_bar.model_changed_signal.connect(self.operation_chat.worker.update_config)
        self.tool_bar.model_changed_signal.connect(self.operation_chat.update_model_for_chat_controller)

        self.side_panel.new_chat_requested.connect(self.operation_chat.handle_new_chat)
        self.side_panel.chat_item_double_clicked.connect(self.operation_chat.handle_open_chat_file)

        self.chat_window.show_setting_page_requested_from_chatwindow.connect(self.operation_mainwindow.handle_show_setting)
        self.chat_window.new_chat_requested_from_chatwindow.connect(self.side_panel.on_new_chat)
        self.chat_window.new_folder_requested_from_chatwindow.connect(self.side_panel.on_new_folder)

        usr_folder = utils.get_usr_dir()    
        settings_file_path = usr_folder / "settings.ini"

        settings   = QSettings(str(settings_file_path), QSettings.Format.IniFormat)
        use_baidu  = settings.value("Search/Baidu", True, type=bool)
        use_google = settings.value("Search/Google", False, type=bool)

        try:
            self.tool_bar.search_requested.disconnect()
        except TypeError:
            pass

        if use_baidu and not use_google:
            self.tool_bar.search_requested.connect(self.operation_mainwindow.perform_baidu_search)
        elif use_google and not use_baidu:
            self.tool_bar.search_requested.connect(self.operation_mainwindow.perform_google_search)
        else:
            self.tool_bar.search_requested.connect(self.operation_mainwindow.perform_baidu_search)

        self.setting_page.apply_settings_signal.connect(self.operation_setting.apply_new_settings)

        self.chat_window.send_message_signal.connect(self.operation_chat.send_message)

    def init_main_ui(self):

        self.setWindowTitle("AiChatCombo")
        self.resize(1300, 800)
        self.setWindowIcon(QIcon(utils.resource_path("images/AIchat_Combo_Logo.jpeg")))

        self.tool_bar = Tool_Bar(self)
        self.tool_bar.setMovable(False)
        self.tool_bar.setMaximumHeight(32)
        self.tool_bar.setIconSize(QSize(24, 24))

        self.addToolBar(self.tool_bar)

        self.chat_window = Chat_Central_Widget()

        self.drag_handle = QWidget()
        self.drag_handle.setFixedWidth(5)
        self.drag_handle.setCursor(Qt.SizeHorCursor)
        self.drag_handle.setStyleSheet("background: #F5F5F5;")

        self.drag_handle.mousePressEvent   = self.handle_mouse_press
        self.drag_handle.mouseMoveEvent    = self.handle_mouse_move
        self.drag_handle.mouseReleaseEvent = self.handle_mouse_release

        self.side_panel = Slide_Side_Panel(self)

        main_widget = QWidget()
        main_widget.setContentsMargins(0, 0, 0, 0)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.side_panel)
        main_layout.addWidget(self.drag_handle)
        main_layout.addWidget(self.chat_window)
        main_layout.setStretch(0, 28)
        main_layout.setStretch(2, 70)

        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

    def toggle_side_panel(self):
        panel = self.side_panel
        currently_visible = panel.is_visible

        if currently_visible:
            panel.full_width = panel.width()
            target_width = 0
        else:
            target_width = panel.full_width if hasattr(panel, "full_width") and panel.full_width > 150 else 280

        anim = QPropertyAnimation(panel, b"maximumWidth")
        anim.setDuration(250)
        anim.setStartValue(panel.width())
        anim.setEndValue(target_width)
        anim.start()

        panel.setMinimumWidth(0)
        panel.is_visible = not currently_visible
        if panel.is_visible:
            panel.setVisible(True)
            self.drag_handle.show()
        else:
            self.drag_handle.hide()
        panel._anim = anim

    def handle_mouse_press(self, event):
        self.drag_start_x = event.globalPosition().x()
        self.start_width = self.side_panel.width()
        event.accept()

    def handle_mouse_move(self, event):

        dx = event.globalPosition().x() - self.drag_start_x
        new_width = self.start_width + dx

        if new_width <= 50:
            self.side_panel.setMaximumWidth(0)
            self.side_panel.setMinimumWidth(0)
            self.side_panel.setVisible(False)
            self.drag_handle.hide()
            self.side_panel.is_visible = False

            self.side_panel.full_width = self.start_width

        else:
            new_width = max(100, new_width)
            self.side_panel.setMaximumWidth(new_width)
            self.side_panel.setMinimumWidth(new_width)
            self.side_panel.setVisible(True)
            self.drag_handle.show()
            self.side_panel.is_visible = True

            self.side_panel.full_width = new_width

        self.chat_window.adjust_input_height()

        if hasattr(self, "operation_chat"):
            self.operation_chat._update_all_bubbles_width()

        event.accept()

    def handle_mouse_release(self, event):
        self.side_panel.panel_width = self.side_panel.width()
        event.accept()

    def resizeEvent(self, event):

        super().resizeEvent(event)

        self.chat_window.adjust_input_height()
        self.chat_window.update_input_container_position()

        if hasattr(self, "operation_chat"):
            QTimer.singleShot(0, self.operation_chat._update_all_bubbles_width)

    def init_styles(self):

        self.setStyleSheet("""
            QMainWindow::separator {
            width: 4px;
            height: 5px;
            background: #F0F0F0;
            }        
            QtoolBar {
                background-color: #F0F0F0;
            }
            QLineEdit {
                padding: 2px 5px 2px 5px;
                padding-left: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
                background-color: #fff;
                font-size: 14px;
                height: 20px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d4;
            }
            QtoolBar::item {
                padding: 3px 15px 3px 15px;
                background: transparent;
                color: black;
                qproperty-alignment: 'AlignCenter';
            }
            QtoolBar::item:selected {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF,
                    stop:1 #FFF0F0
                );
                color: black;
                border-radius: 3px;
            }
            Qtool::item {
                padding: 5px 20px;
                background-color: white;
                color: black;
            }
            Qtool::item:selected {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF,
                    stop:1 #C7ECFF
                );
                color: black;
                border-radius: 4px;
            }            
            QToolButton {
                icon-size: 24px;
                margin-right: 10px;
                margin: 0px 10px;
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
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }           
        """)
