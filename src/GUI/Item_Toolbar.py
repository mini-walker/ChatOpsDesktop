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
    QWidget, QHBoxLayout, QComboBox, QLineEdit, QToolButton, QFrame, QToolBar, QSizePolicy, QMessageBox, QStyle
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



    def __init__(self, parent=None):

        super().__init__(parent)

        self.parent = parent

        self.setWindowTitle("Toolbar")              # The window title
        self.setObjectName("Tool_Bar")              # The object name


        self.init_toolbar_ui()

    # ------------------------------------------------------------------
    def init_toolbar_ui(self):

        # The default toolbar layout is horizontal,
        # If you want to create a vertical toolbar, you need to set the orientation to Qt.Vertical
        # self.setOrientation(Qt.Vertical)

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Set the tool button for side panel
        self.btn_sidepanel = QToolButton()
        self.btn_sidepanel.setIcon(QIcon(utils.resource_path("images/WIN11-Icons/icons8-menu-100.png")))
        self.btn_sidepanel.setIconSize(QSize(24, 24))
        self.btn_sidepanel.setToolTip("Show/Hide Side Panel")

        # Connect the button clicked signal to the corresponding slot
        if self.parent is not None:
            self.btn_sidepanel.clicked.connect(self._on_sidepanel_clicked)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


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
        google_icon = QIcon(utils.resource_path("images/WIN11-Icons/icons8-google-100.png"))  # 你的logo路径
        action_icon = QAction(google_icon, "Search", self.search_input)

        # add the icon to the line edit
        self.search_input.addAction(action_icon, QLineEdit.LeadingPosition)

        # Send the reset_requested signal
        if self.parent is not None:
            self.search_input.returnPressed.connect(lambda: self.search_requested.emit())
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



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
        self.addWidget(self.AI_engine_box)

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

    def get_current_AI_model(self):
        print("[INFO] Current AI model selected:", self.models[self.AI_engine_box.currentIndex()])
        return self.models[self.AI_engine_box.currentIndex()]
    
    def get_current_AI_model_logo(self):
        return self.model_icons[self.AI_engine_box.currentIndex()]


    def emit_model_changed(self, new_model_index):

        new_model = self.models[new_model_index]
        model_icon = self.model_icons[new_model_index]

        print("[INFO] Tool_Bar: model changed to", new_model)
        self.model_changed_signal.emit(new_model, model_icon)
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
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
    # ------------------------------------------------------------------




    # ------------------------------------------------------------------
    # Update the UI texts fot the tool bar
    def update_ui_texts(self, lang_manager = None):
        
        """Update toolbar texts when language changes."""
        
        print("[INFO] Updating toolbar language...")

        # Search box placeholder
        self.search_input.setPlaceholderText(lang_manager.get_text("Google search..."))

    # ------------------------------------------------------------------
