#-----------------------------------------------------------------------------------------
<<<<<<< HEAD
<<<<<<< HEAD
# Purpose: This file is used to create the main window of the application
=======
# Purpouse: This file is used to create the main window of the application
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
# Purpouse: This file is used to create the main window of the application
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-11-23 
#----------------------------------------------------------------------------------------- 

import sys
import os

<<<<<<< HEAD
<<<<<<< HEAD
#-----------------------------------------------------------------------------------------
# Import PyQt5 widgets for UI elements
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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
<<<<<<< HEAD
<<<<<<< HEAD
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Add the parent directory to the Python path for debugging (independent execution)
# Note: Sometimes, VSCode may load the wrong Python interpreter. If the code doesn't run, try changing the interpreter.
if __name__ == "__main__": 

    print("Debug mode!")   

    # Get project root folder
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if project_root not in sys.path: sys.path.insert(0, project_root)

#-----------------------------------------------------------------------------------------

=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

if __name__ == "__main__": 
    print("Debug mode!")   
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path: sys.path.insert(0, project_root)

<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
from Utils.Utils import utils
from GUI.Item_Toolbar import Tool_Bar
from GUI.Item_SettingPage import Setting_Window
from GUI.Item_Centralwidget import Chat_Central_Widget
from GUI.Item_SidePanel import Slide_Side_Panel
from GUI.Language_Manager import Language_Manager

from Operation.Operation_Mainwindow import Operation_Mainwindow_Controller
from Operation.Operation_Setting import Operation_Setting_Controller
from Operation.Operation_Chat_Controller import Operation_Chat_Controller

<<<<<<< HEAD
<<<<<<< HEAD
#-----------------------------------------------------------------------------------------
# Initialize the main application class
#-----------------------------------------------------------------------------------------
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
class AI_Chat_App(QMainWindow):

    def __init__(self):

        super().__init__()

<<<<<<< HEAD
<<<<<<< HEAD
        # ========================== Initialize Managers =============================
        # Initialize the language manager and settings
        self.language_manager = Language_Manager()
        self.settings = None
        # ============================================================================

        # ========================== Initialize UI ===================================
        # Create the main window
        # Only functions defined in the present class can use self.function_name()
        self.init_styles()
        self.init_main_ui()
        # ============================================================================

        # ========================= Initialize Functional Modules ====================
        # Initialize other pages and modules
        # Pass self as a parent so that the modules can access the main window
        # Save the created setting page in self.setting_page
        # Use self.setting_page.function_name() to access all items in the setting page
        self.setting_page = Setting_Window(self)

        # The operation modules
        self.operation_mainwindow = Operation_Mainwindow_Controller(self)

        # The setting controller should be initialized before loading settings
        # As load_settings_on_startup() will trigger apply_new_settings() to apply the settings to UI
        self.operation_setting = Operation_Setting_Controller(self)
        # ============================================================================

        # ========================= Load & Apply Settings ============================
        # Load the settings from the configuration file
        self.load_settings_on_startup()
        # ============================================================================

        # ======================== Initialize operation modules ======================
        # Initialize operation modules after loading settings so that the chat controller can access them
        self.operation_chat = Operation_Chat_Controller(self)

        # ================ Initialize Debounce Timer for Drag ======================
        # Debounce timer to prevent excessive bubble updates during drag
        # 100ms provides good balance: updates frequently enough to feel responsive
        # but not so fast that it causes visible layout thrashing
        self.drag_debounce_timer = QTimer(self)
        self.drag_debounce_timer.setSingleShot(True)
        self.drag_debounce_timer.setInterval(100)  # 100ms debounce
        self.drag_debounce_timer.timeout.connect(self.update_bubbles_after_drag)
        # ============================================================================

        # ========================= Connect Signals ==================================
        # Connect signals for various UI components and modules
        self.connect_signals()
        # ============================================================================

    #---------------------------------------------------------------------------------
    # Load the settings, if they exist
    # Otherwise, create default settings
    def load_settings_on_startup(self):
        """
        Check if settings.ini exists; if yes, load it.
        Otherwise, create one with default values.
        Includes migration logic for old 'Advanced' settings and adds new fields (e.g., background).
        """
        usr_folder = utils.get_usr_dir()
        settings_path = usr_folder / "settings.ini"
        
        # Create QSettings object (even if the file does not exist, Qt will create it upon writing)
        settings = QSettings(str(settings_path), QSettings.Format.IniFormat)

        #---------------------------------------------------------------------------------
        # Helper function: Set default values if a key does not exist
        # This handles both "fresh installations" and "upgrades from older versions" (missing new fields)
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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

<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        def check_and_set_default(key, default_value):
            if not settings.contains(key):
                settings.setValue(key, default_value)

<<<<<<< HEAD
<<<<<<< HEAD
        #---------------------------------------------------------------------------------
        # Check if this is the first run (settings file does not exist)
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        is_first_run = not settings_path.exists()
        
        if is_first_run:
            print("[INFO] No settings.ini found. Creating default settings...")

<<<<<<< HEAD
<<<<<<< HEAD
        #---------------------------------------------------------------------------------
        # --- Font & Appearance ---
        # Default font supports Chinese to prevent garbled text
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        check_and_set_default("Font/type", "Microsoft YaHei") 
        check_and_set_default("Font/size", 10)
        
        check_and_set_default("Appearance/theme", "Light")
        check_and_set_default("Appearance/toolbar_icons", True)
        
<<<<<<< HEAD
<<<<<<< HEAD
        # Background image path (default is empty)
        check_and_set_default("Appearance/chat_background", "") 

        #---------------------------------------------------------------------------------
        # --- Language ---
        check_and_set_default("Language/type", "English")

        #---------------------------------------------------------------------------------
        # --- Search ---
        check_and_set_default("Search/Baidu", True)
        check_and_set_default("Search/Google", False)

        #---------------------------------------------------------------------------------
        # --- AI Settings & Migration ---
        # 1. Attempt to migrate old data (Advanced -> AI)
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        check_and_set_default("Appearance/chat_background", "") 

        check_and_set_default("Language/type", "English")

        check_and_set_default("Search/Baidu", True)
        check_and_set_default("Search/Google", False)

<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        old_key = settings.value("Advanced/api_key", "")
        if old_key and not settings.contains("AI/api_key"):
            print("[INFO] Migrating old API Key to new AI settings structure...")
            settings.setValue("AI/api_key", old_key)
<<<<<<< HEAD
<<<<<<< HEAD
            settings.remove("Advanced") # Clean up old group
        
        #---------------------------------------------------------------------------------
        # 2. Load provider/model definitions from usr/account.json.
        # account.json is always the source of truth for available AI models.
        usr_dir = utils.get_usr_dir()
        account_file = usr_dir / "account.json"
        
        providers = self.tool_bar.load_all_AI_configs(account_file)
        self.setting_page.update_provider_states(providers)

        def match_account_provider(provider_text):
            provider_text = str(provider_text or "").lower().strip()
            if not provider_text:
                return None
            for provider in providers:
                provider_name = str(provider.get("Provider") or provider.get("provider") or "").lower().strip()
                if provider_name and (provider_name in provider_text or provider_text in provider_name):
                    return provider
            return None

        selected_provider = ""
        matched_provider = None
        if providers:
            saved_provider = settings.value("AI/provider", "")
            matched_provider = match_account_provider(saved_provider)
            provider_missing_or_invalid = not matched_provider
            if provider_missing_or_invalid:
                matched_provider = providers[0]

            account_provider_name = matched_provider.get("Provider") or matched_provider.get("provider") or ""
            found_index = self.setting_page._provider_combo_index_for_account_provider(account_provider_name)
            if found_index != -1:
                self.setting_page.provider_combo.setCurrentIndex(found_index)
                selected_provider = self.setting_page.provider_combo.itemText(found_index)
                print(f"[INFO] Set provider combo box to index {found_index} ({selected_provider})")
            else:
                selected_provider = account_provider_name
                print(f"[WARN] Provider '{account_provider_name}' has no matching settings item.")

            account_models = matched_provider.get("models", [])
            saved_model = settings.value("AI/model", "")
            selected_model = saved_model if saved_model in account_models else (account_models[0] if account_models else "")

            # On first run, initialize AI settings from account.json. On later runs,
            # keep the user's provider/model selection when it still exists in account.json.
            if is_first_run or not settings.contains("AI/provider") or provider_missing_or_invalid:
                print("[INFO] Initializing AI config from account.json...")
                settings.setValue("AI/provider", selected_provider)
            if is_first_run or not settings.contains("AI/base_url") or provider_missing_or_invalid:
                settings.setValue("AI/base_url", matched_provider.get("base_url", ""))
            if is_first_run or not settings.contains("AI/api_key") or provider_missing_or_invalid:
                settings.setValue("AI/api_key", matched_provider.get("API-Key", ""))
            if is_first_run or not settings.contains("AI/model") or saved_model not in account_models:
                settings.setValue("AI/model", selected_model)

            print("[INFO] Provider (GUI):", account_provider_name)
            print("[INFO] Base URL (GUI):", matched_provider.get("base_url", ""))
            print("[INFO] Models (GUI):", account_models)
        else:
            print("[ERROR] (GUI) No valid AI configuration found in account.json.")

        # Then set other AI defaults
        check_and_set_default("AI/system_prompt", "You are a helpful assistant.")
        check_and_set_default("AI/temperature", 0.7)

        #---------------------------------------------------------------------------------
        # Save the settings after all checks
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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

<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        settings.sync()
        self.settings = settings
        
        if is_first_run:
            print("[INFO] Default settings created successfully.")
        else:
            print(f"[INFO] Settings loaded from: {settings_path}")

<<<<<<< HEAD
<<<<<<< HEAD
        #---------------------------------------------------------------------------------
        # Apply settings to the application UI
        if hasattr(self, "operation_setting"):
            self.operation_setting.apply_new_settings()
            
    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    # Connect signals and slots
    def connect_signals(self):

        #---------------------------------------------------------------------------------
        # Signal from the tool bar in the main window
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if hasattr(self, "operation_setting"):
            self.operation_setting.apply_new_settings()

    def connect_signals(self):

<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.tool_bar.show_side_panel_requested.connect(self.toggle_side_panel)
        self.tool_bar.show_setting_page_requested.connect(self.operation_mainwindow.handle_show_setting)
        self.side_panel.show_settings_requested.connect(self.operation_mainwindow.handle_show_setting)

<<<<<<< HEAD
<<<<<<< HEAD
        # Model change signal for both chat controller and worker
        self.tool_bar.model_changed_signal.connect(self.operation_chat.update_model_for_chat_controller)

        #---------------------------------------------------------------------------------
        # --- Connect signals from the side panel ---
        self.side_panel.new_chat_requested.connect(self.operation_chat.handle_new_chat)
        self.side_panel.chat_item_double_clicked.connect(self.operation_chat.handle_open_chat_file)

        #---------------------------------------------------------------------------------
        # Signal from the chat window
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.tool_bar.model_changed_signal.connect(self.operation_chat.worker.update_config)
        self.tool_bar.model_changed_signal.connect(self.operation_chat.update_model_for_chat_controller)

        self.side_panel.new_chat_requested.connect(self.operation_chat.handle_new_chat)
        self.side_panel.chat_item_double_clicked.connect(self.operation_chat.handle_open_chat_file)

<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.chat_window.show_setting_page_requested_from_chatwindow.connect(self.operation_mainwindow.handle_show_setting)
        self.chat_window.new_chat_requested_from_chatwindow.connect(self.side_panel.on_new_chat)
        self.chat_window.new_folder_requested_from_chatwindow.connect(self.side_panel.on_new_folder)

<<<<<<< HEAD
<<<<<<< HEAD
        #---------------------------------------------------------------------------------
        # Get the QSettings file path
        usr_folder = utils.get_usr_dir()    
        settings_file_path = usr_folder / "settings.ini"

        #---------------------------------------------------------------------------------
        # Check the settings
=======
        usr_folder = utils.get_usr_dir()    
        settings_file_path = usr_folder / "settings.ini"

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
        usr_folder = utils.get_usr_dir()    
        settings_file_path = usr_folder / "settings.ini"

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        settings   = QSettings(str(settings_file_path), QSettings.Format.IniFormat)
        use_baidu  = settings.value("Search/Baidu", True, type=bool)
        use_google = settings.value("Search/Google", False, type=bool)

<<<<<<< HEAD
<<<<<<< HEAD
        #---------------------------------------------------------------------------------
        # Connect signal from the search button
        try:
            # Disconnect the previous signal
            self.tool_bar.search_requested.disconnect()
        except TypeError:
            # Ignore if the signal is not connected
            pass

        # Connect signal from the search button
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        try:
            self.tool_bar.search_requested.disconnect()
        except TypeError:
            pass

<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if use_baidu and not use_google:
            self.tool_bar.search_requested.connect(self.operation_mainwindow.perform_baidu_search)
        elif use_google and not use_baidu:
            self.tool_bar.search_requested.connect(self.operation_mainwindow.perform_google_search)
        else:
<<<<<<< HEAD
<<<<<<< HEAD
            self.tool_bar.search_requested.connect(self.operation_mainwindow.perform_baidu_search)  # default

        #---------------------------------------------------------------------------------
        # Signal from the setting page
        self.setting_page.apply_settings_signal.connect(self.operation_setting.apply_new_settings) # Connect apply signal
        self.setting_page.models_changed_signal.connect(self.operation_setting.update_toolbar_models)
        # Propagate connection test results between settings page and toolbar
        try:
            self.setting_page.connection_test_signal.connect(self.tool_bar.update_toolbar_connection_status)
        except Exception:
            pass
        try:
            self.tool_bar.connection_test_signal.connect(self.setting_page.update_connection_status)
        except Exception:
            pass

        #---------------------------------------------------------------------------------
        # Chat signal
        self.chat_window.send_message_signal.connect(self.operation_chat.send_message)

    #---------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------
    # Initialize the main UI components
    def init_main_ui(self):

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Initialize the main window 
        # Set the window title and icon
        self.setWindowTitle("AiChatCombo")
        self.resize(1300, 800)
        self.setWindowIcon(QIcon(utils.resource_path("images/AIchat_Combo_Logo.jpeg")))
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Use the external Tool_Bar class to create the tool bar
        self.tool_bar = Tool_Bar(self)                # Initialize the tool bar with the tool bar class
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            self.tool_bar.search_requested.connect(self.operation_mainwindow.perform_baidu_search)

        self.setting_page.apply_settings_signal.connect(self.operation_setting.apply_new_settings)

        self.chat_window.send_message_signal.connect(self.operation_chat.send_message)

    def init_main_ui(self):

        self.setWindowTitle("AiChatCombo")
        self.resize(1300, 800)
        self.setWindowIcon(QIcon(utils.resource_path("images/AIchat_Combo_Logo.jpeg")))

        self.tool_bar = Tool_Bar(self)
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.tool_bar.setMovable(False)
        self.tool_bar.setMaximumHeight(32)
        self.tool_bar.setIconSize(QSize(24, 24))

        self.addToolBar(self.tool_bar)
<<<<<<< HEAD
<<<<<<< HEAD
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Create the center page
        self.chat_window = Chat_Central_Widget()
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Add the drag handle for resizing the side panel
=======

        self.chat_window = Chat_Central_Widget()

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======

        self.chat_window = Chat_Central_Widget()

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.drag_handle = QWidget()
        self.drag_handle.setFixedWidth(5)
        self.drag_handle.setCursor(Qt.SizeHorCursor)
        self.drag_handle.setStyleSheet("background: #F5F5F5;")

<<<<<<< HEAD
<<<<<<< HEAD
        # Connect handle mouse events
        self.drag_handle.mousePressEvent   = self.handle_mouse_press
        self.drag_handle.mouseMoveEvent    = self.handle_mouse_move
        self.drag_handle.mouseReleaseEvent = self.handle_mouse_release
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # ++++++++++++++++++++++++++++++++ Side Panel ++++++++++++++++++++++++++++++++
        # Create the side panel
        self.side_panel = Slide_Side_Panel(self)  # The self is passed as the parent
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Put the Chat widget and side panel in a layout
        # Create a widget to hold the main layout, as central widget only accepts widget type
        main_widget = QWidget()              
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.drag_handle.mousePressEvent   = self.handle_mouse_press
        self.drag_handle.mouseMoveEvent    = self.handle_mouse_move
        self.drag_handle.mouseReleaseEvent = self.handle_mouse_release

        self.side_panel = Slide_Side_Panel(self)

        main_widget = QWidget()
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        main_widget.setContentsMargins(0, 0, 0, 0)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.side_panel)
        main_layout.addWidget(self.drag_handle)
        main_layout.addWidget(self.chat_window)
<<<<<<< HEAD
<<<<<<< HEAD
        main_layout.setStretch(0, 28)  # side panel 28%
        main_layout.setStretch(2, 70)  # central widget 70%

        main_widget.setLayout(main_layout)   # Set the layout to the widget

        # Set the main layout
        self.setCentralWidget(main_widget)
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    #---------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------
    # Function to toggle the visibility of the side panel
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        main_layout.setStretch(0, 28)
        main_layout.setStretch(2, 70)

        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    def toggle_side_panel(self):
        panel = self.side_panel
        currently_visible = panel.is_visible

        if currently_visible:
<<<<<<< HEAD
<<<<<<< HEAD
            # Collapse
            panel.full_width = panel.width()
            target_width = 0
        else:
            # Expand to a reasonable width
=======
            panel.full_width = panel.width()
            target_width = 0
        else:
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
            panel.full_width = panel.width()
            target_width = 0
        else:
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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

<<<<<<< HEAD
<<<<<<< HEAD
    # ---------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------
    # Functions to handle dragging of the side panel with the mouse
    def handle_mouse_press(self, event):
        # Record the initial horizontal position of the mouse when pressed
        self.drag_start_x = event.globalPosition().x()
        # Record the current width of the side panel at the start of drag
        self.start_width = self.side_panel.width()
        # Accept the event so it is not propagated further
        event.accept()

    def handle_mouse_move(self, event):
        # Adjust the width of the side panel dynamically during drag
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    def handle_mouse_press(self, event):
        self.drag_start_x = event.globalPosition().x()
        self.start_width = self.side_panel.width()
        event.accept()

    def handle_mouse_move(self, event):

<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        dx = event.globalPosition().x() - self.drag_start_x
        new_width = self.start_width + dx

        if new_width <= 50:
            self.side_panel.setMaximumWidth(0)
            self.side_panel.setMinimumWidth(0)
            self.side_panel.setVisible(False)
            self.drag_handle.hide()
            self.side_panel.is_visible = False

<<<<<<< HEAD
<<<<<<< HEAD
            self.side_panel.full_width = self.start_width  # Save the initial width for next time
=======
            self.side_panel.full_width = self.start_width
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
            self.side_panel.full_width = self.start_width
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

        else:
            new_width = max(100, new_width)
            self.side_panel.setMaximumWidth(new_width)
            self.side_panel.setMinimumWidth(new_width)
            self.side_panel.setVisible(True)
            self.drag_handle.show()
            self.side_panel.is_visible = True

<<<<<<< HEAD
<<<<<<< HEAD
            self.side_panel.full_width = new_width        # Save the new width for next time

        # Debounce: restart timer on each move, update only after 50ms of inactivity
        self.drag_debounce_timer.stop()
        self.drag_debounce_timer.start()
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            self.side_panel.full_width = new_width

        self.chat_window.adjust_input_height()

        if hasattr(self, "operation_chat"):
            self.operation_chat._update_all_bubbles_width()
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

        event.accept()

    def handle_mouse_release(self, event):
<<<<<<< HEAD
<<<<<<< HEAD
        # Stop the debounce timer and force immediate update
        self.drag_debounce_timer.stop()
        
        # Update the side panel's stored width after the drag is completed
        self.side_panel.panel_width = self.side_panel.width()
        
        # Force immediate update of bubble widths after drag completes
        self.update_bubbles_after_drag()
        
        # Accept the event so it is not propagated further
        event.accept()
    # ---------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------
    # Helper function to update bubble widths (called by debounce timer or mouse release)
    def update_bubbles_after_drag(self):
        """Update bubble widths and input container position after sidebar resize."""
        self.chat_window.adjust_input_height()
        if hasattr(self, "operation_chat"):
            self.operation_chat.update_all_bubbles_width()
    # ---------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------
    # Resize event to update bubble widths and input container when the window is resized
    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Adjust the height of the text input and input container
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.side_panel.panel_width = self.side_panel.width()
        event.accept()

    def resizeEvent(self, event):

        super().resizeEvent(event)

<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.chat_window.adjust_input_height()
        self.chat_window.update_input_container_position()

        if hasattr(self, "operation_chat"):
<<<<<<< HEAD
<<<<<<< HEAD
            QTimer.singleShot(0, self.operation_chat.update_all_bubbles_width)
    # ---------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # Initialize global QSS styles for the app
    def init_styles(self):
        """Initialize global QSS styles for the app."""
        self.setStyleSheet("""
            /* Main window separator */
            QMainWindow::separator {
            width: 4px;
            height: 5px;
            background: #F0F0F0;   /* Light gray or white */
            }        
            QtoolBar {
                background-color: #F0F0F0;   /* Light gray or white */
            }
            QLineEdit {
                padding: 2px 5px 2px 5px;   /* Space for text, order is top right bottom left */
                padding-left: 5px;     /* Space for magnifying glass icon */
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                border: 1px solid #ccc;
                border-radius: 3px;
                background-color: #fff;
                font-size: 14px;
                height: 20px;
            }
            QLineEdit:focus {
<<<<<<< HEAD
<<<<<<< HEAD
                border: 1px solid #0078d4; /* VS Code blue highlight */
            }
            QtoolBar::item {
                padding: 3px 15px 3px 15px;             /* Spacing around tool items, padding order: up right down left */
                background: transparent;                /* Keep it transparent when not hovered */
                color: black;                           /* Text color */
                qproperty-alignment: 'AlignCenter';     /* Center the text */
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                border: 1px solid #0078d4;
            }
            QtoolBar::item {
                padding: 3px 15px 3px 15px;
                background: transparent;
                color: black;
                qproperty-alignment: 'AlignCenter';
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            }
            QtoolBar::item:selected {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
<<<<<<< HEAD
<<<<<<< HEAD
                    stop:0 #FFFFFF,     /* top white */
                    stop:1 #FFF0F0      /* bottom pale cyan --- #C7ECFF; grey --- #C0C0C0 */
                );
                color: black;           /* text color on selection */
                border-radius: 3px;     /* rounded corners */
            }
            /* Drop-down tools */
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                    stop:0 #FFFFFF,
                    stop:1 #FFF0F0
                );
                color: black;
                border-radius: 3px;
            }
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            Qtool::item {
                padding: 5px 20px;
                background-color: white;
                color: black;
            }
<<<<<<< HEAD
<<<<<<< HEAD
            /* Hover effect for tool items */
            Qtool::item:selected {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF,     /* top white */
                    stop:1 #C7ECFF      /* bottom pale cyan */
                );
                color: black;           /* text color on selection */
                border-radius: 4px;     /* rounded corners */
            }            
            /* Toolbar styling */
            QToolButton {
                icon-size: 24px;
                margin-right: 10px;
                margin: 0px 10px;                           /* Spacing around tool items, padding order: up right down left */
            }
            /* ---- 2. Vertical scroll bar (thin & modern) ---- */
            QScrollBar:vertical {
                background: transparent;
                width: 10px;                /* thickness */
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                margin: 4px 2px 4px 2px;
                border-radius: 8px;
            }
            QScrollBar::handle:vertical {
<<<<<<< HEAD
<<<<<<< HEAD
                background: rgba(0,0,0,0.25);   /* subtle gray */
=======
                background: rgba(0,0,0,0.25);
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
                background: rgba(0,0,0,0.25);
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                min-height: 30px;
                border-radius: 8px;
            }
            QScrollBar::handle:vertical:hover {
<<<<<<< HEAD
<<<<<<< HEAD
                background: rgba(0,0,0,0.45);   /* darker on hover */
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;   /* hide arrows */
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                background: rgba(0,0,0,0.45);
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }           
        """)
<<<<<<< HEAD
<<<<<<< HEAD
    # ------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------
# Run the application for testing
# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     win = AI_Chat_App()
#     win.show()
#     app.exec()
#-----------------------------------------------------------------------------------
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
