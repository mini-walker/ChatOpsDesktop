#-----------------------------------------------------------------------------------------
# File: Tool_Bar.py
# Purpose: Define the top toolbar UI for AIChatCombo
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-11-13
#-----------------------------------------------------------------------------------------


import sys  # Import system-specific parameters and functions
import os
import json

from PySide6.QtWidgets import (
<<<<<<< HEAD
    QWidget, QHBoxLayout, QComboBox, QLineEdit, QToolButton, QFrame, QToolBar, QSizePolicy, QMessageBox, QStyle, QLabel
=======
    QWidget, QHBoxLayout, QComboBox, QLineEdit, QToolButton, QFrame, QToolBar, QSizePolicy, QMessageBox, QStyle
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QAction


# Add the parent directory to the Python path for debugging (independent execution)
if __name__ == "__main__": 

    # Get project root folder
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if project_root not in sys.path: sys.path.insert(0, project_root)


from Utils.Utils import utils


# Create a custom toolbar widget
# This class is used to create the top toolbar widget
# If the class is the QToolBar, you just need to add the items
# You don't need to create the horizontal or vertical layout agqin.
class Tool_Bar(QToolBar):

    """Custom toolbar widget"""

    # Signals
    search_requested            = Signal()
    model_changed_signal        = Signal(str, QIcon)  # Send the new model name
    show_side_panel_requested   = Signal()
    show_setting_page_requested = Signal()
<<<<<<< HEAD
    connection_test_signal      = Signal(bool, str)  # (success, message)
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6



    def __init__(self, parent=None):

        super().__init__(parent)

        self.parent = parent

        self.setWindowTitle("Toolbar")              # The window title
        self.setObjectName("Tool_Bar")              # The object name

<<<<<<< HEAD
=======

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.init_toolbar_ui()

    # ------------------------------------------------------------------
    def init_toolbar_ui(self):

<<<<<<< HEAD
        # Adjust spacing between toolbar widgets
        layout = self.layout()
        if layout is not None:
            layout.setSpacing(12)  # increase inter-widget spacing
            layout.setContentsMargins(5, 5, 5, 5)  # add slight margins around toolbar

=======
        # The default toolbar layout is horizontal,
        # If you want to create a vertical toolbar, you need to set the orientation to Qt.Vertical
        # self.setOrientation(Qt.Vertical)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Set the tool button for side panel
        self.btn_sidepanel = QToolButton()
        self.btn_sidepanel.setIcon(QIcon(utils.resource_path("images/WIN11-Icons/icons8-menu-100.png")))
<<<<<<< HEAD
        self.btn_sidepanel.setObjectName("Side_Panel_Button_Toolbar")
        self.btn_sidepanel.setIconSize(QSize(24, 24))
        self.btn_sidepanel.setToolTip("Toggle Side Panel")
=======
        self.btn_sidepanel.setIconSize(QSize(24, 24))
        self.btn_sidepanel.setToolTip("Show/Hide Side Panel")

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        # Connect the button clicked signal to the corresponding slot
        if self.parent is not None:
            self.btn_sidepanel.clicked.connect(self._on_sidepanel_clicked)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
<<<<<<< HEAD
        # Load all configs from usr/account.json
        usr_dir = utils.get_usr_dir()
        account_file = usr_dir / "account.json"
        self.all_providers = self.load_all_AI_configs(account_file)
        
        # Load settings to get current provider/model selection
        from PySide6.QtCore import QSettings
        setting_file_path = utils.get_usr_dir() / "settings.ini"
        settings = QSettings(str(setting_file_path), QSettings.Format.IniFormat)
        saved_provider = settings.value("AI/provider", "")

        # ComboBox: Provider selection
        self.provider_box = QComboBox()
        for prov in self.all_providers:
            self.provider_box.addItem(prov["Provider"])
            
        matched_prov_idx = 0
        for i, prov in enumerate(self.all_providers):
            p_name = prov["Provider"]
            if saved_provider and (p_name in saved_provider or saved_provider in p_name):
                matched_prov_idx = i
                break
        
        self.provider_box.setCurrentIndex(matched_prov_idx)
        
        active_provider = self.all_providers[matched_prov_idx]
        self.AI_provider = active_provider["Provider"]
        self.base_url = active_provider["base_url"]
        self.api_key = active_provider["API-Key"]
        self.models = active_provider["models"]

        # ComboBox: AI Engine selection
        self.AI_engine_box = QComboBox()
        self.model_icons = []  # Store model icons for future use
        
        # Labels for combo boxes
        self.lbl_provider = QLabel("Provider:")
        self.lbl_model = QLabel("LLM Model:")

        # Connect signals
        self.provider_box.currentIndexChanged.connect(self.emit_provider_changed)
        self.AI_engine_box.currentIndexChanged.connect(self.emit_model_changed)

        # Style sheet setup
        arrow_path = utils.resource_path("images/WIN11-Icons/icons8-expand-arrow-100.png")
        print(f"[DEBUG] Loading arrow from: {arrow_path}")
        arrow_path = arrow_path.replace("\\", "/")

        provider_qss = f"""
            QComboBox {{
                border: 1px solid #aaaaaa;
                border-radius: 8px;
                padding: 4px 28px 4px 8px;
                min-width: 8em;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border: none;
                background: transparent;
            }}
            QComboBox::down-arrow {{
                image: url("{arrow_path}");
                width: 16px;
                height: 16px;
            }}
            QComboBox::item:hover {{
                background-color: #F0F0F0;
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid #aaaaaa;
                border-radius: 6px;
                selection-background-color: #d0f0c0;
            }}
            QComboBox QAbstractItemView::item:hover {{
                background-color: #F0F0F0;
                border-radius: 6px;
                color: black;
            }}
        """
        self.provider_box.setStyleSheet(provider_qss)

=======
        # ComboBox: AI Engine selection
        self.AI_engine_box = QComboBox()

        # Get the AI engine list from usr/account.josn file
        usr_dir = utils.get_usr_dir()
        account_file = usr_dir / "account.json"
        self.AI_provider, self.base_url, self.api_key, self.models = self.load_AI_config(account_file)
        if self.api_key and self.models:
            print("[INFO] API Key:", self.api_key)
            print("[INFO] Models:", self.models)
        else:
            print("[ERROR] Failed to load OpenRouter configuration.")


        self.model_icons = []  # Store model icons for future use

        for full_model_name in self.models:
            
            if "/" in full_model_name:
                print(f"[WARNING] Your model format is 'provider/model_name', such as those in OpenRouter and Groq.")
                AI_engine = full_model_name.split("/")[1]
            else:
                print(f"[WARNING] Your model format is 'model_name', such as those in DeepSeek or Qwen.")
                AI_engine = full_model_name

            fname_lower = full_model_name.lower()
            if any(k in fname_lower for k in ["openai", "gpt"]):
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-chatgpt-100-2.png"))
            elif "openrouter" in fname_lower:
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-openrouter-100.png"))
            elif "tngtech" in fname_lower:
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-tngtech-100.png"))
            elif "deepseek" in fname_lower:
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-deepseek-100.png"))
            elif "qwen" in fname_lower:
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-qwen-100.png"))
            elif any(k in fname_lower for k in ["google", "gemma", "gemini"]):
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-Gemma-100.png"))
            elif any(k in fname_lower for k in ["meta", "llama"]):
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-meta-100.png"))
            elif "kwaipilot" in fname_lower:
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-meta-100.png"))
            elif any(k in fname_lower for k in ["x-ai", "grok"]):
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-grok-100.png"))
            else:
                icon = QIcon()  # default blank icon

            # Add the model to the combobox
            self.AI_engine_box.addItem(icon, AI_engine)
            self.model_icons.append(icon)




        # Connect the combobox selection change signal to the corresponding slot
        self.AI_engine_box.currentIndexChanged.connect(self.emit_model_changed)

        # Set style for the combobox
        arrow_path = utils.resource_path("images/WIN11-Icons/icons8-expand-arrow-100.png")

        print(f"[DEBUG] Loading arrow from: {arrow_path}")

        arrow_path = arrow_path.replace("\\", "/")
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.AI_engine_box.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid #aaaaaa;
                border-radius: 8px;
                padding: 4px 28px 4px 8px;
                min-width: 6em;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border: none;
                background: transparent;
            }}
            QComboBox::down-arrow {{
                image: url("{arrow_path}");
                width: 16px;
                height: 16px;
            }}
            QComboBox::item:hover {{
                background-color: #F0F0F0;  /* Hover color */
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid #aaaaaa;
                border-radius: 6px;
                selection-background-color: #d0f0c0;
            }}
            QComboBox QAbstractItemView::item:hover {{
                background-color: #F0F0F0;      /* Hover color: very light gray */
                border-radius: 6px;              /* Keep rounded corners */
                color: black;                   /* Hover text color */
            }}
        """)
<<<<<<< HEAD

        # Populate model items initially
        self.update_models_list(self.models)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Test Connection Button
        test_connection_container = QWidget()
        test_connection_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        test_connection_layout = QHBoxLayout(test_connection_container)
        test_connection_layout.setContentsMargins(0, 0, 0, 0)
        test_connection_layout.setSpacing(8)

        self.btn_test_connection = QToolButton()
        self.btn_test_connection.setIcon(QIcon(utils.resource_path("images/WIN11-Icons/icons8-rdp-connection-100.png")))
        self.btn_test_connection.setObjectName("Test_API_Connection_Button_Toolbar")
        self.btn_test_connection.setIconSize(QSize(24, 24))
        self.btn_test_connection.setToolTip("Test API Connection")

        # Connect the button clicked signal to the corresponding slot
        if self.parent is not None:
            self.btn_test_connection.clicked.connect(self._on_test_connection_clicked)

        self.lbl_toolbar_connection_status = QLabel("")
        self.lbl_toolbar_connection_status.setStyleSheet("color: gray; font-size: 12px;")
        self.lbl_toolbar_connection_status.setMinimumWidth(120)

        # Put button first, then status label on the right
        test_connection_layout.addWidget(self.btn_test_connection)
        test_connection_layout.addSpacing(6)
        test_connection_layout.addWidget(self.lbl_toolbar_connection_status)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




=======
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Google Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Google search...")
        self.search_input.setFixedHeight(28)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 2px 5px 2px 5px;        /* Space for text, order is top right bottom left */
                padding-left: 10px;              /* Space for the left button */
                padding-right: 10px;             /* Space for the right button */
                border: 1.2px solid grey;
                border-radius: 8px;
                font-size: 13px;
                width: 200px;
            }
            QLineEdit:focus {
                border: 1.0px solid #0078D7;    /* #0078D7 --- Microsoft Blue */
            }
        """)

        # create an icon for google
<<<<<<< HEAD
        google_icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-google-100.png"))  # the logo path
=======
        google_icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-google-100.png"))  # 你的logo路径
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        action_icon = QAction(google_icon, "Search", self.search_input)

        # add the icon to the line edit
        self.search_input.addAction(action_icon, QLineEdit.LeadingPosition)

        # Send the reset_requested signal
        if self.parent is not None:
            self.search_input.returnPressed.connect(lambda: self.search_requested.emit())
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

<<<<<<< HEAD
=======


>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Tool Buttons
        self.btn_settings = QToolButton()
        self.btn_settings.setIcon(QIcon(utils.resource_path("images/WIN11-Icons/icons8-gears-100.png")))
        self.btn_settings.setIconSize(QSize(24, 24))
        self.btn_settings.setToolTip("Settings")

        # Connect the button clicked signal to the corresponding slot
        if self.parent is not None:
            self.btn_settings.clicked.connect(self._on_settings_clicked)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Add widgets
        self.addWidget(self.btn_sidepanel)
<<<<<<< HEAD
        # Provider label and combo
        self.addWidget(self.lbl_provider)
        self.addSeparator()
        self.addWidget(self.provider_box)
        self.addSeparator()
        # Model label and combo
        self.addWidget(self.lbl_model)
        self.addSeparator()
        self.addWidget(self.AI_engine_box)
        self.addSeparator()
        self.addWidget(test_connection_container)
=======
        self.addWidget(self.AI_engine_box)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

        # Add a spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer)

        self.addWidget(self.search_input)
        # self.addWidget(self.btn_settings)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



    # ------------------------------------------------------------------
    # Slots for signals
    def _on_sidepanel_clicked(self):
        print("Toolbar: emit show side panel signal")
        self.show_side_panel_requested.emit()

    def _on_search_clicked(self):
        print("Toolbar: emit search signal")
        self.search_requested.emit()

    def _on_settings_clicked(self):
        print("Toolbar: emit show setting dialog signal")
        self.show_setting_page_requested.emit()

<<<<<<< HEAD
    def _on_test_connection_clicked(self):
        """Handle test connection button click from toolbar"""
        import requests
        from threading import Thread
        
        # Get current configuration
        api_key = ""
        base_url = ""
        model = self.get_current_AI_model()
        
        # Try to get config from parent main window settings
        if self.parent is not None and hasattr(self.parent, 'setting_page'):
            setting_page = self.parent.setting_page
            if hasattr(setting_page, 'controls'):
                ai_controls = setting_page.controls.get("AI", {})
                api_key = ai_controls.get("api_key").text().strip() if "api_key" in ai_controls else ""
                base_url = ai_controls.get("base_url").text().strip() if "base_url" in ai_controls else ""
        
        # Validate inputs
        if not api_key or not base_url or not model:
            self.lbl_toolbar_connection_status.setText("⚠️ Please configure API Key, Base URL, and Model in Settings first.")
            self.lbl_toolbar_connection_status.setStyleSheet("color: #ffaa00; font-size: 12px; font-weight: bold;")
            return
        
        # Show testing status in toolbar label
        self.btn_test_connection.setEnabled(False)
        self.lbl_toolbar_connection_status.setText("🔄 Testing...")
        self.lbl_toolbar_connection_status.setStyleSheet("color: #0099ff; font-size: 12px; font-weight: bold;")
        
        # Run test in background thread
        def test_connection():
            try:
                response = requests.post(
                    base_url,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": "test"}],
                        "max_tokens": 10
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.lbl_toolbar_connection_status.setText("✅ Connection successful!")
                    self.lbl_toolbar_connection_status.setStyleSheet("color: #00aa00; font-size: 12px; font-weight: bold;")
                    self.connection_test_signal.emit(True, "Connection successful")
                else:
                    error_msg = f"Connection failed (HTTP {response.status_code})"
                    try:
                        error_data = response.json()
                        if "error" in error_data:
                            error_msg = error_data['error'].get('message', error_msg)
                    except:
                        pass
                    self.lbl_toolbar_connection_status.setText(f"❌ {error_msg}")
                    self.lbl_toolbar_connection_status.setStyleSheet("color: #ff4444; font-size: 12px; font-weight: bold;")
                    self.connection_test_signal.emit(False, error_msg)
            except requests.exceptions.Timeout:
                self.lbl_toolbar_connection_status.setText("❌ Connection timeout")
                self.lbl_toolbar_connection_status.setStyleSheet("color: #ff4444; font-size: 12px; font-weight: bold;")
                self.connection_test_signal.emit(False, "Connection timeout")
            except requests.exceptions.ConnectionError:
                self.lbl_toolbar_connection_status.setText("❌ Connection error")
                self.lbl_toolbar_connection_status.setStyleSheet("color: #ff4444; font-size: 12px; font-weight: bold;")
                self.connection_test_signal.emit(False, "Connection error")
            except Exception as e:
                self.lbl_toolbar_connection_status.setText(f"❌ {str(e)}")
                self.lbl_toolbar_connection_status.setStyleSheet("color: #ff4444; font-size: 12px; font-weight: bold;")
                self.connection_test_signal.emit(False, str(e))
            finally:
                self.btn_test_connection.setEnabled(True)
        
        thread = Thread(target=test_connection, daemon=True)
        thread.start()

    def get_current_AI_model(self):
        idx = self.AI_engine_box.currentIndex()
        if idx < 0 or idx >= len(self.models):
            print("[WARNING] get_current_AI_model: index out of bounds or empty models list.")
            return ""
        print("[INFO] Current AI model selected:", self.models[idx])
        return self.models[idx]
    
    def get_current_AI_model_logo(self):
        idx = self.AI_engine_box.currentIndex()
        if idx < 0 or idx >= len(self.model_icons):
            return QIcon()
        return self.model_icons[idx]

    def update_toolbar_connection_status(self, success, message):
        """Update the toolbar status label from external sources (e.g., settings page)."""
        try:
            if success is True:
                self.lbl_toolbar_connection_status.setText(message or "✅ Connection successful!")
                self.lbl_toolbar_connection_status.setStyleSheet("color: #00aa00; font-size: 12px; font-weight: bold;")
            elif success is False:
                self.lbl_toolbar_connection_status.setText(message or "❌ Connection failed")
                self.lbl_toolbar_connection_status.setStyleSheet("color: #ff4444; font-size: 12px; font-weight: bold;")
            else:
                self.lbl_toolbar_connection_status.setText(message or "🔄 Testing...")
                self.lbl_toolbar_connection_status.setStyleSheet("color: #0099ff; font-size: 12px; font-weight: bold;")
        except Exception:
            pass


    def emit_model_changed(self, new_model_index):
        if new_model_index < 0 or new_model_index >= len(self.models):
            print("[WARNING] emit_model_changed: index out of bounds.")
            return
=======
    def get_current_AI_model(self):
        print("[INFO] Current AI model selected:", self.models[self.AI_engine_box.currentIndex()])
        return self.models[self.AI_engine_box.currentIndex()]
    
    def get_current_AI_model_logo(self):
        return self.model_icons[self.AI_engine_box.currentIndex()]


    def emit_model_changed(self, new_model_index):

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        new_model = self.models[new_model_index]
        model_icon = self.model_icons[new_model_index]

        print("[INFO] Tool_Bar: model changed to", new_model)
        self.model_changed_signal.emit(new_model, model_icon)
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
<<<<<<< HEAD
    def emit_provider_changed(self, new_provider_index):
        """
        Called when the user selects a different provider in the provider combo box.
        Updates credentials/models and persists the selection to settings.ini.
        """
        if not self.all_providers or new_provider_index < 0 or new_provider_index >= len(self.all_providers):
            print("[WARNING] emit_provider_changed: index out of bounds.")
            return

        selected = self.all_providers[new_provider_index]
        self.AI_provider = selected["Provider"]
        self.base_url    = selected["base_url"]
        self.api_key     = selected["API-Key"]
        self.models      = selected["models"]

        print(f"[INFO] Tool_Bar: provider changed to {self.AI_provider}")

        # Refresh model dropdown for the new provider (restore saved model if possible)
        self.update_models_list(self.models)

        # Persist provider/credentials to settings.ini
        from PySide6.QtCore import QSettings
        setting_file_path = utils.get_usr_dir() / "settings.ini"
        settings = QSettings(str(setting_file_path), QSettings.Format.IniFormat)
        settings.setValue("AI/provider", self.AI_provider)
        settings.setValue("AI/base_url", self.base_url)
        settings.setValue("AI/api_key",  self.api_key)
        if self.models:
            settings.setValue("AI/model", self.models[0])
        settings.sync()

        # Propagate new config to chat controller and settings page via parent
        if self.parent is not None:
            # Sync the provider combo in the settings dialog
            if hasattr(self.parent, "setting_page"):
                sp = self.parent.setting_page
                if hasattr(sp, "_provider_combo_index_for_account_provider"):
                    idx = sp._provider_combo_index_for_account_provider(self.AI_provider)
                    if idx != -1:
                        sp.provider_combo.blockSignals(True)
                        sp.provider_combo.setCurrentIndex(idx)
                        sp.provider_combo.blockSignals(False)
                # Sync the API key / base URL fields in settings dialog
                if hasattr(sp, "controls") and "AI" in sp.controls:
                    ai_ctrls = sp.controls["AI"]
                    if "base_url" in ai_ctrls:
                        ai_ctrls["base_url"].setText(self.base_url)
                    if "api_key"  in ai_ctrls:
                        ai_ctrls["api_key"].setText(self.api_key)

            # Notify the chat controller of new credentials
            if hasattr(self.parent, "operation_chat"):
                chat = self.parent.operation_chat
                current_model = self.get_current_AI_model()
                if hasattr(chat, "update_model_for_chat_controller"):
                    chat.update_model_for_chat_controller(current_model, None)
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    def select_provider_in_toolbar(self, provider_name):
        """
        Programmatically select the provider dropdown by name (used by Operation_Setting).
        Blocks signals to avoid a recursive update loop.
        """
        if not provider_name:
            return
        for i in range(self.provider_box.count()):
            if self.provider_box.itemText(i).lower().strip() == provider_name.lower().strip():
                if self.provider_box.currentIndex() != i:
                    self.provider_box.blockSignals(True)
                    self.provider_box.setCurrentIndex(i)
                    self.provider_box.blockSignals(False)
                return
        print(f"[WARN] select_provider_in_toolbar: '{provider_name}' not found in provider_box.")
    # ------------------------------------------------------------------


    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    def load_all_AI_configs(self, config_path):
        """
        Load all provider configurations from account.json.
        Supports both single-provider object and multi-provider array/dictionary formats.
        """
        import json
        if not os.path.exists(config_path):
            return []
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load account file: {e}")
            return []

        providers = []
        
        def parse_single(item):
            if not isinstance(item, dict):
                return None
            prov = item.get("Provider") or item.get("provider")
            base = item.get("base_url") or item.get("baseUrl")
            key = item.get("API-Key") or item.get("api_key") or item.get("apiKey")
            models = item.get("models")
            if prov and models is not None:
                if isinstance(models, list):
                    model_list = list(models)
                elif isinstance(models, (tuple, set)):
                    model_list = list(models)
                else:
                    model_list = [str(models)]
                return {
                    "Provider": str(prov),
                    "base_url": str(base or ""),
                    "API-Key": str(key or ""),
                    "models": model_list
                }
            return None

        if isinstance(data, list):
            for item in data:
                parsed = parse_single(item)
                if parsed:
                    providers.append(parsed)
        elif isinstance(data, dict):
            # Check if it is a single provider at root
            parsed = parse_single(data)
            if parsed:
                providers.append(parsed)
            else:
                # Multi-provider dictionary format: {"Groq": {...}, "OpenRouter": {...}}
                for key, val in data.items():
                    if isinstance(val, dict):
                        item = val.copy()
                        if "Provider" not in item and "provider" not in item:
                            item["Provider"] = key
                        parsed = parse_single(item)
                        if parsed:
                            providers.append(parsed)
        return providers

    def load_AI_config(self, config_path):
        """
        Load OpenRouter configuration from a JSON file.
        Uses load_all_AI_configs and returns the first loaded provider.
        """
        providers = self.load_all_AI_configs(config_path)
        if not providers:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(None, "Error", "No valid AI configuration found in account file!")
            return None, None, None, None
        
        first = providers[0]
        return first["Provider"], first["base_url"], first["API-Key"], first["models"]

    def update_models_list(self, new_models, preferred_model=None):
        """Update the toolbar's models dropdown list dynamically."""
        self.models = list(new_models)
        
        # Block signals temporarily to prevent firing model change signals during repopulation
        self.AI_engine_box.blockSignals(True)
        self.AI_engine_box.clear()
        self.model_icons = []

        for full_model_name in self.models:
            if "/" in full_model_name:
                AI_engine = full_model_name.split("/")[1]
            else:
                AI_engine = full_model_name

            fname_lower = full_model_name.lower()
            if any(k in fname_lower for k in ["openai", "gpt"]):
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-chatgpt-100-2.png"))
            elif "openrouter" in fname_lower:
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-openrouter-100.png"))
            elif "tngtech" in fname_lower:
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-tngtech-100.png"))
            elif "deepseek" in fname_lower:
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-deepseek-100.png"))
            elif "qwen" in fname_lower:
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-qwen-100.png"))
            elif any(k in fname_lower for k in ["google", "gemma", "gemini"]):
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-Gemma-100.png"))
            elif any(k in fname_lower for k in ["meta", "llama"]):
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-meta-100.png"))
            elif "kwaipilot" in fname_lower:
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-meta-100.png"))
            elif any(k in fname_lower for k in ["x-ai", "grok"]):
                icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-grok-100.png"))
            else:
                icon = QIcon()  # default blank icon

            self.AI_engine_box.addItem(icon, AI_engine)
            self.model_icons.append(icon)

        self.AI_engine_box.blockSignals(False)
        # Select the preferred/saved model in the new list if found, otherwise select the first model
        saved_index = 0
        selected_model = preferred_model
        if selected_model is None:
            from PySide6.QtCore import QSettings
            setting_file_path = utils.get_usr_dir() / "settings.ini"
            settings = QSettings(str(setting_file_path), QSettings.Format.IniFormat)
            selected_model = settings.value("AI/model", "")
        if selected_model in self.models:
            saved_index = self.models.index(selected_model)

        if self.AI_engine_box.count() > 0:
            self.AI_engine_box.setCurrentIndex(saved_index)
            self.emit_model_changed(saved_index)
        else:
            self.model_changed_signal.emit("", QIcon())
=======
    def load_AI_config(self, config_path):
        """
        Load OpenRouter configuration from a JSON file.
        Shows error message boxes if any required fields are missing.
        
        Returns:
            tuple: (api_key: str, models: list) or (None, None) if error occurs
        """
        import json
        from PySide6.QtWidgets import QMessageBox

        # -------------------------------
        # Load JSON file
        # -------------------------------
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load account file:\n{e}")
            return None, None

        # -------------------------------
        # Check Provider
        # -------------------------------
        AI_provider = config.get("Provider")
        if not AI_provider:
            QMessageBox.critical(None, "Error", "Missing 'Provider' in account file!")
            return None, None
        
        # -------------------------------
        # Check OpenRouter config
        # -------------------------------
        base_url = config.get("base_url")
        if not base_url:
            QMessageBox.critical(None, "Error", "Missing or invalid 'base_url' in account file!")
            return None, None

        # -------------------------------
        # Check API Key
        # -------------------------------
        api_key = config.get("API-Key")
        if not api_key:
            QMessageBox.critical(None, "Error", "Missing 'API-Key' in account file!")
            return None, None

        # -------------------------------
        # Check models list
        # -------------------------------
        models = config.get("models")
        if not models or not isinstance(models, (list, set)):
            QMessageBox.critical(None, "Error", "Missing or invalid 'models' list in account file!")
            return None, None

        return AI_provider, base_url, api_key, list(models)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    # ------------------------------------------------------------------




    # ------------------------------------------------------------------
    # Update the UI texts fot the tool bar
    def update_ui_texts(self, lang_manager = None):
        
        """Update toolbar texts when language changes."""
        
        print("[INFO] Updating toolbar language...")

        # Search box placeholder
        self.search_input.setPlaceholderText(lang_manager.get_text("Google search..."))

    # ------------------------------------------------------------------
