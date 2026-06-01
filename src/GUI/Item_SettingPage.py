#-----------------------------------------------------------------------------------------
<<<<<<< HEAD
# Purpose: This file is used to create the Settings Window with multi-language support
=======
# Purpouse: This file is used to create the Settings Window with multi-language support
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-11-23 
#----------------------------------------------------------------------------------------- 

import sys
import os
from pathlib import Path

#-----------------------------------------------------------------------------------------
<<<<<<< HEAD
# Import PySide6 widgets for creating the UI components
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
from PySide6.QtWidgets import ( 
    QFileDialog, QDialog, QHBoxLayout, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
    QStackedWidget, QDialogButtonBox, QLineEdit, QLabel, QComboBox, QCheckBox, 
    QMessageBox, QPushButton, QWidget, QGroupBox, QFormLayout, QSlider, QTextEdit,
<<<<<<< HEAD
    QRadioButton, QButtonGroup, QStyledItemDelegate, QStyle, QStyleOptionViewItem,
    QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QSettings, QRect, QPoint, QEvent
from PySide6.QtGui import QColor, QFont, QIcon
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Import utility functions from the Utils module
# If the module is not found, define a fallback class for debugging
=======
    QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt, Signal, QSettings
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
try:
    from Utils.Utils import utils
except ImportError:
    class Utils:
        def get_usr_dir(self): return Path("usr")
    utils = Utils()
#-----------------------------------------------------------------------------------------

<<<<<<< HEAD
#-----------------------------------------------------------------------------------------
class QComboBoxDeleteDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, delete_callback=None):
        super().__init__(parent)
        self.delete_callback = delete_callback

    def paint(self, painter, option, index):
        # Draw the item with space reserved for the delete affordance.
        item_option = QStyleOptionViewItem(option)
        item_option.rect = option.rect.adjusted(0, 0, -34, 0)
        super().paint(painter, item_option, index)

        painter.save()
        rect = option.rect
        btn_width = 24
        btn_height = 20
        # Position button 5px from the right edge
        btn_rect = QRect(rect.right() - btn_width - 5, rect.top() + (rect.height() - btn_height) // 2, btn_width, btn_height)

        painter.setRenderHint(painter.RenderHint.Antialiasing)
        if option.state & QStyle.State_Selected:
            painter.setPen(QColor("#FF4D4D")) # Soft red
        else:
            painter.setPen(QColor("#888888")) # Soft gray
            
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(btn_rect, Qt.AlignmentFlag.AlignCenter, "×")
        painter.restore()

    def editorEvent(self, event, model, option, index):
        if event.type() in (QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonRelease):
            rect = option.rect
            btn_width = 24
            btn_height = 20
            btn_rect = QRect(rect.right() - btn_width - 5, rect.top() + (rect.height() - btn_height) // 2, btn_width, btn_height)
            
            pos = event.position().toPoint() if hasattr(event, "position") else event.pos()
            if btn_rect.contains(pos):
                if event.type() == QEvent.Type.MouseButtonRelease:
                    if self.delete_callback:
                        self.delete_callback(index.row())
                return True
        return super().editorEvent(event, model, option, index)

#-----------------------------------------------------------------------------------------
# Define the Setting_Window class for the Preferences Dialog
class Setting_Window(QDialog):
    """
    Preferences Dialog with Multi-language Support.
    """

    settings_page_operation_signal = Signal(str)
    apply_settings_signal = Signal()
    models_changed_signal = Signal(list, str)
    connection_test_signal = Signal(bool, str)  # (success, message)
=======
class Setting_Window(QDialog):

    settings_page_operation_signal = Signal(str)
    apply_settings_signal = Signal()
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Preferences")
<<<<<<< HEAD
        self.resize(780, 600) 
        self.setMinimumSize(720, 540)

        self.account_providers = []
        self.custom_account_provider = None

        #---------------------------------------------------------------------------------
        # Setup Settings File
        # Create the user folder if it doesn't exist
        # Initialize QSettings to manage application settings
=======
        self.resize(700, 550) 

        #---------------------------------------------------------------------------------
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        usr_folder = utils.get_usr_dir()
        os.makedirs(usr_folder, exist_ok = True)
        setting_file_path = usr_folder / "settings.ini"
        self.settings = QSettings(str(setting_file_path), QSettings.Format.IniFormat)
        #---------------------------------------------------------------------------------

        #---------------------------------------------------------------------------------
<<<<<<< HEAD
        # Main Layout
        # Create a horizontal layout with a navigation tree on the left
        # and a stacked widget for pages on the right
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(16)

        # Left: Navigation Tree
        self.preference_tree = QTreeWidget()
        self.preference_tree.setObjectName("settingsNav")
        self.preference_tree.setHeaderHidden(True)
        self.preference_tree.setFixedWidth(190)
        main_layout.addWidget(self.preference_tree)

        #---------------------------------------------------------------------------------
        # Define navigation tree items for different settings categories
=======
        main_layout = QHBoxLayout()

        self.preference_tree = QTreeWidget()
        self.preference_tree.setHeaderHidden(True)
        self.preference_tree.setFixedWidth(160)
        main_layout.addWidget(self.preference_tree)

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.item_ai = QTreeWidgetItem(["AI Configuration"]) 
        self.item_appearance = QTreeWidgetItem(["Appearance"])
        self.item_font = QTreeWidgetItem(["Font Settings"])
        self.item_language = QTreeWidgetItem(["Language Settings"])
        self.item_search = QTreeWidgetItem(["Search"])
        
        self.preference_tree.addTopLevelItems([
            self.item_ai, 
            self.item_appearance, 
            self.item_font, 
            self.item_language, 
            self.item_search
        ])
        self.preference_tree.setIndentation(0)
<<<<<<< HEAD
        self.preference_tree.setRootIsDecorated(False)
        self.preference_tree.setUniformRowHeights(True)

        # Right: Pages
        self.stack = QStackedWidget()
        self.stack.setObjectName("settingsStack")
=======

        self.preference_tree.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #D3D3D3;
                border-radius: 8px;
                padding: 0px;
            }
            QTreeWidget::item { padding: 8px; color: #333333; }
            QTreeWidget::item:hover { background-color: #E8E8E8; }
            QTreeWidget::item:selected { background-color: #DCDCDC; color: #333333; }
        """)

        self.stack = QStackedWidget()
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        main_layout.addWidget(self.stack)

        self.controls = {
            "AI": {}, "Font": {}, "Search": {}, "Language": {}, "Appearance": {}
        }

<<<<<<< HEAD
        #---------------------------------------------------------------------------------
        # Create pages for each settings category and add them to the stacked widget
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.ai_page = self.create_ai_page_in_setting()
        self.appearance_page = self.create_appearance_page_in_setting()
        self.font_page = self.create_font_page_in_setting()
        self.language_page = self.create_language_page_in_setting()
        self.search_page = self.create_search_page_in_setting()

        self.stack.addWidget(self.ai_page)
        self.stack.addWidget(self.appearance_page)
        self.stack.addWidget(self.font_page)
        self.stack.addWidget(self.language_page)
        self.stack.addWidget(self.search_page)

<<<<<<< HEAD
        #---------------------------------------------------------------------------------
        # Connect the navigation tree to the stacked widget to switch pages
        self.preference_tree.currentItemChanged.connect(self.change_page)
        self.preference_tree.setCurrentItem(self.item_ai)

        #---------------------------------------------------------------------------------
        # Add dialog buttons for saving or canceling changes
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.setObjectName("settingsButtons")
        self.button_box.button(QDialogButtonBox.Ok).setObjectName("primaryButton")
        self.button_box.button(QDialogButtonBox.Cancel).setObjectName("secondaryButton")
=======
        self.preference_tree.currentItemChanged.connect(self.change_page)
        self.preference_tree.setCurrentItem(self.item_ai)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
<<<<<<< HEAD
        layout.setContentsMargins(18, 18, 18, 14)
        layout.setSpacing(14)
        layout.addLayout(main_layout)
        layout.addWidget(self.button_box)
        self.apply_theme_style(self.settings.value("Appearance/theme", "Light"))


    def _setup_form_layout(self, form_layout):
        form_layout.setContentsMargins(16, 20, 16, 16)
        form_layout.setHorizontalSpacing(16)
        form_layout.setVerticalSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

    def _provider_matches_display(self, provider_name, display_text):
        provider = str(provider_name or "").lower().strip()
        display = str(display_text or "").lower().strip()
        return bool(provider and display and (provider in display or display in provider))

    def _is_custom_provider_display(self, display_text):
        return str(display_text or "").lower().strip() == "custom"

    def _provider_name(self, provider):
        if not isinstance(provider, dict):
            return ""
        return str(provider.get("Provider") or provider.get("provider") or "").lower().strip()

    def _find_custom_account_provider(self):
        explicit_custom = None
        unmatched_provider = None
        known_items = [
            self.provider_combo.itemText(i)
            for i in range(self.provider_combo.count())
            if self.provider_combo.itemText(i).lower().strip() != "custom"
        ]

        for provider in self.account_providers:
            provider_name = self._provider_name(provider)
            if provider_name == "custom":
                explicit_custom = provider
                break
            if provider_name and not any(self._provider_matches_display(provider_name, item) for item in known_items):
                unmatched_provider = unmatched_provider or provider

        return explicit_custom or unmatched_provider

    def _account_provider_for_display(self, display_text):
        if self._is_custom_provider_display(display_text):
            if self.custom_account_provider is None:
                self.custom_account_provider = self._find_custom_account_provider()
            return self.custom_account_provider

        for provider in self.account_providers:
            provider_name = provider.get("Provider") or provider.get("provider") or ""
            if self._provider_matches_display(provider_name, display_text):
                return provider
        return None

    def _provider_combo_index_for_account_provider(self, provider_name):
        for i in range(self.provider_combo.count()):
            item_text = self.provider_combo.itemText(i)
            if item_text.lower().strip() == "custom":
                continue
            if self._provider_matches_display(provider_name, item_text):
                return i
        return self.provider_combo.findText("Custom") if self.custom_account_provider else -1

    def _account_provider_name_for_display(self, display_text):
        matched_provider = self._account_provider_for_display(display_text)
        if matched_provider:
            return (matched_provider.get("Provider") or matched_provider.get("provider") or "").lower().strip()
        if self._is_custom_provider_display(display_text):
            return "custom"
        return str(display_text or "").lower().strip()

    def _style_interactive_children(self):
        for widget_type in (QLineEdit, QComboBox):
            for widget in self.findChildren(widget_type):
                widget.setMinimumHeight(34)
        for text_edit in self.findChildren(QTextEdit):
            text_edit.setMinimumHeight(72)
        for button in self.findChildren(QPushButton):
            if button.objectName() != "iconButton":
                button.setMinimumHeight(34)

    def apply_theme_style(self, appearance_mode="Light"):
        self._style_interactive_children()
        mode = str(appearance_mode or "Light").lower()
        is_dark = mode == "dark"

        if is_dark:
            bg = "#25272d"
            panel = "#30333a"
            field = "#25282e"
            border = "#4a4f58"
            text = "#f3f4f6"
            muted = "#c4c7cf"
            nav_hover = "#3a3f47"
            accent = "#5aa0ff"
            accent_hover = "#75b2ff"
            selection = "#344b70"
        else:
            bg = "#f5f7fb"
            panel = "#ffffff"
            field = "#ffffff"
            border = "#d9dee8"
            text = "#20242c"
            muted = "#5d6676"
            nav_hover = "#edf2f8"
            accent = "#2563eb"
            accent_hover = "#1d4ed8"
            selection = "#e8f0ff"

        self.setStyleSheet(f"""
            QDialog {{
                background: {bg};
                color: {text};
            }}
            QTreeWidget#settingsNav {{
                background: {panel};
                border: 1px solid {border};
                border-radius: 8px;
                padding: 8px;
                outline: 0;
            }}
            QTreeWidget#settingsNav::item {{
                min-height: 34px;
                padding: 7px 10px;
                border-radius: 6px;
                color: {muted};
            }}
            QTreeWidget#settingsNav::item:hover {{
                background: {nav_hover};
                color: {text};
            }}
            QTreeWidget#settingsNav::item:selected {{
                background: {selection};
                color: {accent};
                font-weight: 600;
            }}
            QStackedWidget#settingsStack {{
                background: transparent;
            }}
            QWidget#settingsPage {{
                background: transparent;
            }}
            QGroupBox {{
                background: {panel};
                border: 1px solid {border};
                border-radius: 8px;
                margin-top: 16px;
                color: {text};
                font-weight: 600;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 14px;
                padding: 0 6px;
                color: {text};
                background: {bg};
            }}
            QLabel {{
                color: {muted};
            }}
            QLineEdit, QComboBox, QTextEdit {{
                background: {field};
                color: {text};
                border: 1px solid {border};
                border-radius: 6px;
                padding: 6px 9px;
                selection-background-color: {selection};
            }}
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {{
                border: 1px solid {accent};
            }}
            QComboBox::drop-down {{
                border: 0;
                width: 28px;
            }}
            QComboBox QAbstractItemView {{
                background: {panel};
                color: {text};
                border: 1px solid {border};
                border-radius: 6px;
                padding: 4px;
                selection-background-color: {selection};
            }}
            QComboBox QAbstractItemView::item {{
                min-height: 28px;
                padding: 4px 28px 4px 8px;
            }}
            QSlider::groove:horizontal {{
                height: 6px;
                background: {border};
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
                background: {accent};
            }}
            QPushButton {{
                background: {panel};
                color: {text};
                border: 1px solid {border};
                border-radius: 6px;
                padding: 6px 14px;
            }}
            QPushButton:hover {{
                border-color: {accent};
                background: {nav_hover};
            }}
            QPushButton#iconButton {{
                padding: 0;
                font-weight: 700;
            }}
            QPushButton#secondaryButton {{
                color: {accent};
            }}
            QPushButton#primaryButton {{
                background: {accent};
                border-color: {accent};
                color: white;
                font-weight: 600;
            }}
            QPushButton#primaryButton:hover {{
                background: {accent_hover};
                border-color: {accent_hover};
            }}
            QDialogButtonBox QPushButton {{
                min-width: 84px;
            }}
            QDialogButtonBox QPushButton:hover {{
                border-color: {accent_hover};
            }}
            QCheckBox, QRadioButton {{
                color: {text};
                spacing: 8px;
            }}
        """)


    #-------------------------------------------------------------------------------------
    # Create the AI Settings Page
    def create_ai_page_in_setting(self):
        page = QWidget()
        page.setObjectName("settingsPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)
        
        # --- Group 1: API Connection ---
        # Create input fields for AI provider, base URL, and API key
        self.group_ai_api = QGroupBox("API Connection") 
        api_layout = QFormLayout()
        self._setup_form_layout(api_layout)

        # 1. Provider
=======
        layout.addLayout(main_layout)
        layout.addWidget(self.button_box)

    #-------------------------------------------------------------------------------------
    def create_ai_page_in_setting(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        self.group_ai_api = QGroupBox("API Connection") 
        api_layout = QFormLayout()

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.lbl_provider = QLabel("Provider:")
        self.provider_combo = QComboBox()
        self.provider_combo.addItems([
            "OpenRouter (Recommended)", 
            "OpenAI (Official)",
            "Alibaba Qwen (DashScope)", 
            "DeepSeek (Official)", 
            "X.AI (Grok)", 
            "Groq (Meta Llama/Mixtral)",
            "Google Gemini (via OpenRouter)",
            "SiliconFlow (硅基流动)", 
            "Ollama (Localhost)",
            "Arli", 
            "Custom" 
        ])
        
        saved_provider = self.settings.value("AI/provider", "OpenRouter (Recommended)")
        self.provider_combo.setCurrentText(saved_provider)
<<<<<<< HEAD
        self.provider_combo.currentTextChanged.connect(self.on_provider_changed)
        self.controls["AI"]["provider"] = self.provider_combo
        self.provider_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # 2. Model selector
        self.lbl_model = QLabel("Model:")
        
        model_container = QWidget()
        model_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        model_layout = QHBoxLayout(model_container)
        model_layout.setContentsMargins(0, 0, 0, 0)
        model_layout.setSpacing(5)
        
        self.models_combo = QComboBox()
        self.models_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.models_delegate = QComboBoxDeleteDelegate(self.models_combo.view(), delete_callback=self.delete_model_callback)
        self.models_combo.view().setItemDelegate(self.models_delegate)
        self.models_combo.view().setMouseTracking(True)
        self.models_combo.view().viewport().installEventFilter(self)
        self.models_combo.currentTextChanged.connect(lambda _text: self._emit_models_changed())
        self.controls["AI"]["models"] = self.models_combo
        
        self.btn_add_model = QPushButton("+")
        self.btn_add_model.setObjectName("iconButton")
        self.btn_add_model.setFixedSize(34, 34)
        self.btn_add_model.setToolTip("Add Custom Model")
        self.btn_add_model.clicked.connect(self.add_custom_model_dialog)
        
        model_layout.addWidget(self.models_combo, 1)
        model_layout.addWidget(self.btn_add_model)
        
        # Populate models for the current provider
        current_provider = self.provider_combo.currentText()
        self._populate_models_for_provider(current_provider)
        # Restore saved model selection
        saved_model = self.settings.value("AI/model", "")
        if saved_model:
            idx = self.models_combo.findText(saved_model)
            if idx != -1:
                self.models_combo.setCurrentIndex(idx)
        
        # The combo boxes will naturally expand to fill the layout width, matching other inputs.

        # 2. Base URL
        self.lbl_base_url = QLabel("Base URL:")
        base_url_input = QLineEdit()
        base_url_input.setPlaceholderText("https://...")
        default_url = "https://api.deepseek.com/chat/completions"
        base_url_input.setText(self.settings.value("AI/base_url", default_url))
        self.controls["AI"]["base_url"] = base_url_input

        # 3. API Key
        self.lbl_api_key = QLabel("API Key:")
        
        api_key_container = QWidget()
        api_key_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        api_key_layout = QHBoxLayout(api_key_container)
        api_key_layout.setContentsMargins(0, 0, 0, 0)
        api_key_layout.setSpacing(5)
        
        api_input = QLineEdit()
        api_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
=======
        self.provider_combo.currentTextChanged.connect(self._on_provider_changed)
        self.controls["AI"]["provider"] = self.provider_combo

        self.lbl_base_url = QLabel("Base URL:")
        base_url_input = QLineEdit()
        base_url_input.setPlaceholderText("https://...")
        default_url = "https://openrouter.ai/api/v1/chat/completions"
        base_url_input.setText(self.settings.value("AI/base_url", default_url))
        self.controls["AI"]["base_url"] = base_url_input

        self.lbl_api_key = QLabel("API Key:")
        api_input = QLineEdit()
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        api_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_input.setPlaceholderText("sk-...")
        api_input.setText(self.settings.value("AI/api_key", ""))
        self.controls["AI"]["api_key"] = api_input
<<<<<<< HEAD
        
        self.btn_toggle_key = QPushButton("👁️")
        self.btn_toggle_key.setObjectName("iconButton")
        self.btn_toggle_key.setFixedSize(34, 34)
        self.btn_toggle_key.setToolTip("Show/Hide API Key")
        self.btn_toggle_key.clicked.connect(self.toggle_api_key_visibility)
        
        api_key_layout.addWidget(api_input, 1)
        api_key_layout.addWidget(self.btn_toggle_key)

        api_layout.addRow(self.lbl_provider, self.provider_combo)
        api_layout.addRow(self.lbl_base_url, base_url_input)
        api_layout.addRow(self.lbl_model, model_container)
        api_layout.addRow(self.lbl_api_key, api_key_container)
        
        # Test Connection Button - Horizontal layout (similar to API Key layout)
        test_connection_container = QWidget()
        test_connection_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        test_connection_layout = QHBoxLayout(test_connection_container)
        test_connection_layout.setContentsMargins(0, 0, 0, 0)
        test_connection_layout.setSpacing(5)
        
        self.btn_test_connection = QPushButton()
        self.btn_test_connection.setIcon(QIcon(utils.resource_path("images/WIN11-Icons/icons8-rdp-connection-100.png")))
        self.btn_test_connection.setObjectName("Test_API_Connection_Button")
        self.btn_test_connection.setFixedSize(34, 34)
        self.btn_test_connection.setToolTip("Test API Connection")
        self.btn_test_connection.clicked.connect(self.on_test_connection_clicked)
        self.controls["AI"]["test_connection_btn"] = self.btn_test_connection
        

        self.lbl_connection_status = QLabel("")
        self.lbl_connection_status.setStyleSheet("color: gray; font-size: 13px;")
        
        test_connection_layout.addStretch()
        test_connection_layout.addWidget(self.lbl_connection_status)
        test_connection_layout.addSpacing(10)
        test_connection_layout.addWidget(self.btn_test_connection)
        
        api_layout.addRow("", test_connection_container)
        
        self.group_ai_api.setLayout(api_layout)
        layout.addWidget(self.group_ai_api)

        # --- Group 2: Behavior ---
        # Create input fields for system prompt and temperature
        self.group_ai_behavior = QGroupBox("Behavior")
        behavior_layout = QFormLayout()
        self._setup_form_layout(behavior_layout)

        # 4. System Prompt
=======

        api_layout.addRow(self.lbl_provider, self.provider_combo)
        api_layout.addRow(self.lbl_base_url, base_url_input)
        api_layout.addRow(self.lbl_api_key, api_input)
        self.group_ai_api.setLayout(api_layout)
        layout.addWidget(self.group_ai_api)

        self.group_ai_behavior = QGroupBox("Behavior")
        behavior_layout = QFormLayout()

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.lbl_sys_prompt = QLabel("System Prompt:")
        sys_prompt = QTextEdit()
        sys_prompt.setPlaceholderText("You are a helpful assistant...")
        sys_prompt.setMaximumHeight(60)
        sys_prompt.setPlainText(self.settings.value("AI/system_prompt", "You are a helpful assistant."))
        self.controls["AI"]["system_prompt"] = sys_prompt

<<<<<<< HEAD
        # 5. Temperature
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.lbl_temperature = QLabel("Temperature:")
        temp_container = QWidget()
        temp_h = QHBoxLayout(temp_container)
        temp_h.setContentsMargins(0,0,0,0)
        
        temp_slider = QSlider(Qt.Orientation.Horizontal)
        temp_slider.setRange(0, 20) 
        saved_temp = int(float(self.settings.value("AI/temperature", 0.7)) * 10)
        temp_slider.setValue(saved_temp)
        
        temp_label = QLabel(str(saved_temp / 10.0))
        temp_label.setFixedWidth(30)
        temp_slider.valueChanged.connect(lambda v: temp_label.setText(str(v/10.0)))
        
        temp_h.addWidget(temp_slider)
        temp_h.addWidget(temp_label)
        self.controls["AI"]["temperature"] = temp_slider

        behavior_layout.addRow(self.lbl_sys_prompt, sys_prompt)
        behavior_layout.addRow(self.lbl_temperature, temp_container)
        self.group_ai_behavior.setLayout(behavior_layout)
        layout.addWidget(self.group_ai_behavior)

<<<<<<< HEAD
        # --- Reset Button ---
        # Add a button to reset AI settings to default values
        self.btn_reset_ai = QPushButton("Reset AI Settings")
        self.btn_reset_ai.setObjectName("secondaryButton")
        self.btn_reset_ai.setFixedHeight(34)
        self.btn_reset_ai.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
=======
        self.btn_reset_ai = QPushButton("Reset AI Settings")
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.btn_reset_ai.clicked.connect(self.reset_preferences)
        layout.addWidget(self.btn_reset_ai)

        layout.addStretch()
        return page

<<<<<<< HEAD
    def update_provider_states(self, providers):
        """
        Enable/disable provider combobox items based on account.json definition.
        Defined providers are shown as black and selectable.
        Others are shown as gray and unselectable.
        """
        self.account_providers = providers
        self.custom_account_provider = self._find_custom_account_provider()
        
        is_dark = str(self.settings.value("Appearance/theme", "Light")).lower() == "dark"
        enabled_color = QColor("#f3f4f6" if is_dark else "#20242c")
        disabled_color = QColor("#777b84" if is_dark else "#9ca3af")

        model = self.provider_combo.model()
        for i in range(self.provider_combo.count()):
            item_text = self.provider_combo.itemText(i)
            is_custom = self._is_custom_provider_display(item_text)
            is_enabled = is_custom or self._account_provider_for_display(item_text) is not None
            
            item = model.item(i, 0)
            if item:
                item.setEnabled(is_enabled)
                item.setForeground(enabled_color if is_enabled else disabled_color)
                item.setToolTip("" if is_enabled else "Not configured in account.json")

        if providers:
            first_provider_name = providers[0].get("Provider") or providers[0].get("provider") or ""
            default_index = self._provider_combo_index_for_account_provider(first_provider_name)
            if default_index != -1:
                self.provider_combo.setCurrentIndex(default_index)

        # Trigger model load for the selected provider on startup.
        self.on_provider_changed(self.provider_combo.currentText())

    def _model_delete_button_rect(self, item_rect):
        btn_width = 24
        btn_height = 20
        return QRect(
            item_rect.right() - btn_width - 5,
            item_rect.top() + (item_rect.height() - btn_height) // 2,
            btn_width,
            btn_height
        )

    def eventFilter(self, watched, event):
        if watched == self.models_combo.view().viewport():
            if event.type() in (QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonRelease):
                pos = event.position().toPoint() if hasattr(event, "position") else event.pos()
                index = self.models_combo.view().indexAt(pos)
                if index.isValid():
                    item_rect = self.models_combo.view().visualRect(index)
                    if self._model_delete_button_rect(item_rect).contains(pos):
                        if event.type() == QEvent.Type.MouseButtonRelease:
                            self.delete_model_callback(index.row())
                        return True
        return super().eventFilter(watched, event)

    def add_custom_model_dialog(self):
        from PySide6.QtWidgets import QInputDialog
        provider_name = self.provider_combo.currentText()
        
        # Show input dialog to prompt for the custom model name
        model_name, ok = QInputDialog.getText(
            self, 
            "Add Custom Model", 
            f"Enter custom model name for {provider_name}:"
        )
        if ok and model_name.strip():
            model_name = model_name.strip()
            
            # Check if model already exists in the combo box
            if self.models_combo.findText(model_name) != -1:
                QMessageBox.warning(self, "Warning", "This model name already exists!")
                return
            
            # Add to combo box and select it
            self.models_combo.addItem(model_name)
            self.models_combo.setCurrentText(model_name)
            
            # Update local account_providers and write back to account.json
            self.save_new_model_to_account_json(provider_name, model_name)
            self._emit_models_changed()
            
            QMessageBox.information(self, "Success", f"Model '{model_name}' has been added successfully!")

    def save_new_model_to_account_json(self, provider_name, new_model):
        """
        Save the new model back to account.json for the matching provider.
        """
        import json
        usr_folder = utils.get_usr_dir()
        account_file = usr_folder / "account.json"
        if not account_file.exists():
            if self._is_custom_provider_display(provider_name):
                self._create_custom_provider_in_account_json(new_model)
                return
            print(f"[WARN] account.json does not exist at: {account_file}")
            return

        try:
            with open(account_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load account.json to save model: {e}")
            return

        provider_name_lower = self._account_provider_name_for_display(provider_name)
        updated = False

        def update_item(item):
            nonlocal updated
            prov_def = item.get("Provider") or item.get("provider") or ""
            if prov_def.lower().strip() in provider_name_lower or provider_name_lower in prov_def.lower().strip():
                if "models" not in item:
                    item["models"] = []
                if new_model not in item["models"]:
                    item["models"].append(new_model)
                    updated = True

        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    update_item(item)
        elif isinstance(data, dict):
            if "Provider" in data or "models" in data:
                update_item(data)
            else:
                for key, val in data.items():
                    if isinstance(val, dict):
                        prov_def = val.get("Provider") or val.get("provider") or key
                        if prov_def.lower().strip() in provider_name_lower or provider_name_lower in prov_def.lower().strip():
                            if "models" not in val:
                                val["models"] = []
                            if new_model not in val["models"]:
                                val["models"].append(new_model)
                                updated = True

        if updated:
            try:
                with open(account_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"[INFO] Settings: Successfully added model '{new_model}' for provider '{provider_name}' in account.json")
                
                # Also update our local cached copy of account_providers
                self._set_account_provider_cache(data)
            except Exception as e:
                print(f"[ERROR] Failed to save updated account.json with new model: {e}")
        elif self._is_custom_provider_display(provider_name):
            self._create_custom_provider_in_account_json(new_model)

    def delete_model_callback(self, row):
        model_name = self.models_combo.itemText(row)
        if not model_name:
            return
            
        provider_name = self.provider_combo.currentText()
        
        # Confirm deletion
        confirm = QMessageBox.question(
            self, 
            "Delete Model", 
            f"Are you sure you want to delete the model '{model_name}' for provider '{provider_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            # Delete from account.json
            self.remove_model_from_account_json(provider_name, model_name)
            
            # Remove from UI combo box
            self.models_combo.removeItem(row)
            
            # Keep dropdown open
            self.models_combo.showPopup()
            
            # If the deleted model was the currently saved model, update the settings
            saved_model = self.settings.value("AI/model", "")
            if saved_model == model_name:
                # Find a new selected model or set it to empty
                new_model = self.models_combo.currentText()
                self.settings.setValue("AI/model", new_model)
                self.settings.sync()
            
            self._emit_models_changed()

    def remove_model_from_account_json(self, provider_name, model_to_delete):
        """
        Delete the model from account.json for the matching provider.
        """
        import json
        usr_folder = utils.get_usr_dir()
        account_file = usr_folder / "account.json"
        if not account_file.exists():
            print(f"[WARN] account.json does not exist at: {account_file}")
            return

        try:
            with open(account_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load account.json to delete model: {e}")
            return

        provider_name_lower = self._account_provider_name_for_display(provider_name)
        updated = False

        def update_item(item):
            nonlocal updated
            prov_def = item.get("Provider") or item.get("provider") or ""
            if prov_def.lower().strip() in provider_name_lower or provider_name_lower in prov_def.lower().strip():
                if "models" in item and model_to_delete in item["models"]:
                    item["models"].remove(model_to_delete)
                    updated = True

        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    update_item(item)
        elif isinstance(data, dict):
            if "Provider" in data or "models" in data:
                update_item(data)
            else:
                for key, val in data.items():
                    if isinstance(val, dict):
                        prov_def = val.get("Provider") or val.get("provider") or key
                        if prov_def.lower().strip() in provider_name_lower or provider_name_lower in prov_def.lower().strip():
                            if "models" in val and model_to_delete in val["models"]:
                                val["models"].remove(model_to_delete)
                                updated = True

        if updated:
            try:
                with open(account_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"[INFO] Settings: Successfully deleted model '{model_to_delete}' for provider '{provider_name}' in account.json")
                
                # Also update our local cached copy of account_providers
                self._set_account_provider_cache(data)
            except Exception as e:
                print(f"[ERROR] Failed to save updated account.json with model deletion: {e}")

    def _populate_models_for_provider(self, provider_name):
        """Load model list for the given provider from account.json and populate the combo."""
        self.models_combo.blockSignals(True)
        self.models_combo.clear()
        matched = self._account_provider_for_display(provider_name)
        if matched:
            models = matched.get("models", [])
            for m in models:
                self.models_combo.addItem(m)
        self.models_combo.blockSignals(False)

    def _current_models(self):
        return [self.models_combo.itemText(i) for i in range(self.models_combo.count())]

    def _emit_models_changed(self):
        self.models_changed_signal.emit(self._current_models(), self.models_combo.currentText())

    def _set_account_provider_cache(self, data):
        if isinstance(data, list):
            self.account_providers = [item for item in data if isinstance(item, dict)]
        elif isinstance(data, dict):
            if "Provider" in data or "provider" in data:
                self.account_providers = [data]
            else:
                providers = []
                for key, val in data.items():
                    if isinstance(val, dict):
                        item = val.copy()
                        if "Provider" not in item and "provider" not in item:
                            item["Provider"] = key
                        providers.append(item)
                self.account_providers = providers
        else:
            self.account_providers = []
        self.custom_account_provider = self._find_custom_account_provider()

    def _custom_provider_payload(self, initial_model=None):
        models = []
        if initial_model:
            models.append(initial_model)
        return {
            "Provider": "Custom",
            "base_url": self.controls["AI"].get("base_url").text().strip() if "base_url" in self.controls["AI"] else "",
            "API-Key": self.controls["AI"].get("api_key").text().strip() if "api_key" in self.controls["AI"] else "",
            "models": models
        }

    def _create_custom_provider_in_account_json(self, initial_model=None):
        import json
        usr_folder = utils.get_usr_dir()
        account_file = usr_folder / "account.json"

        data = []
        if account_file.exists():
            try:
                with open(account_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"[ERROR] Failed to load account.json to create Custom provider: {e}")
                return

        custom_payload = self._custom_provider_payload(initial_model)
        if isinstance(data, list):
            data.append(custom_payload)
        elif isinstance(data, dict):
            if "Provider" in data or "provider" in data:
                data = [data, custom_payload]
            else:
                data["Custom"] = custom_payload
        else:
            data = [custom_payload]

        try:
            with open(account_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("[INFO] Settings: Created Custom provider in account.json")
            self._set_account_provider_cache(data)
        except Exception as e:
            print(f"[ERROR] Failed to save Custom provider to account.json: {e}")

    def on_provider_changed(self, provider_name):
        """Handle provider change: update base URL, API key and models list."""
        matched_provider = self._account_provider_for_display(provider_name)
        
        if matched_provider:
            # Update base_url and api_key
            if "base_url" in self.controls["AI"]:
                self.controls["AI"]["base_url"].setText(matched_provider.get("base_url", ""))
            if "api_key" in self.controls["AI"]:
                self.controls["AI"]["api_key"].setText(matched_provider.get("API-Key", ""))
            # Populate models for this provider
            self._populate_models_for_provider(provider_name)
            # Try to restore previously saved model selection
            saved_model = self.settings.value("AI/model", "")
            if saved_model:
                idx = self.models_combo.findText(saved_model)
                if idx != -1:
                    self.models_combo.setCurrentIndex(idx)
            print(f"[INFO] Settings Page: loaded config for matched provider '{provider_name}' from account.json")
            self._emit_models_changed()
            return

        # Fallback to hardcoded URL map
=======
    def _on_provider_changed(self, provider_name):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        url_map = {
            "OpenRouter (Recommended)": "https://openrouter.ai/api/v1/chat/completions",
            "OpenAI (Official)": "https://api.openai.com/v1/chat/completions",
            "Alibaba Qwen (DashScope)": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            "DeepSeek (Official)": "https://api.deepseek.com/chat/completions",
            "X.AI (Grok)": "https://api.x.ai/v1/chat/completions",
            "Groq (Meta Llama/Mixtral)": "https://api.groq.com/openai/v1/chat/completions",
            "Google Gemini (via OpenRouter)": "https://openrouter.ai/api/v1/chat/completions",
            "SiliconFlow (硅基流动)": "https://api.siliconflow.cn/v1/chat/completions",
            "Ollama (Localhost)": "http://localhost:11434/v1/chat/completions",
            "Arli": "https://api.arliai.com/v1/chat/completions"
        }
        if provider_name in url_map:
            self.controls["AI"]["base_url"].setText(url_map[provider_name])
<<<<<<< HEAD
        elif self._is_custom_provider_display(provider_name):
            if "base_url" in self.controls["AI"]:
                self.controls["AI"]["base_url"].clear()
            if "api_key" in self.controls["AI"]:
                self.controls["AI"]["api_key"].clear()
        self.models_combo.clear()
        self._emit_models_changed()

    def toggle_api_key_visibility(self):
        api_input = self.controls["AI"]["api_key"]
        if api_input.echoMode() == QLineEdit.EchoMode.Password:
            api_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_toggle_key.setText("🔒")
        else:
            api_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_toggle_key.setText("👁️")

    def save_api_key_to_account_json(self, provider_name, new_key, new_base_url=None):
        """
        Save the new API key back to account.json for the matching provider.
        """
        import json
        usr_folder = utils.get_usr_dir()
        account_file = usr_folder / "account.json"
        if not account_file.exists():
            if self._is_custom_provider_display(provider_name):
                self._create_custom_provider_in_account_json(self.models_combo.currentText())
                return
            print(f"[WARN] account.json does not exist at: {account_file}")
            return

        try:
            with open(account_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load account.json to save key: {e}")
            return

        provider_name_lower = self._account_provider_name_for_display(provider_name)
        updated = False

        def update_item(item):
            nonlocal updated
            prov_def = item.get("Provider") or item.get("provider") or ""
            if prov_def.lower().strip() in provider_name_lower:
                if new_base_url is not None and item.get("base_url", "") != new_base_url:
                    item["base_url"] = new_base_url
                    updated = True
                for k in ["API-Key", "api_key", "API_Key", "apiKey"]:
                    if k in item:
                        if item[k] != new_key:
                            item[k] = new_key
                            updated = True
                        break
                else:
                    item["API-Key"] = new_key
                    updated = True

        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    update_item(item)
        elif isinstance(data, dict):
            if "Provider" in data or "API-Key" in data:
                update_item(data)
            else:
                for key, val in data.items():
                    if isinstance(val, dict):
                        prov_def = val.get("Provider") or val.get("provider") or key
                        if prov_def.lower().strip() in provider_name_lower:
                            if new_base_url is not None and val.get("base_url", "") != new_base_url:
                                val["base_url"] = new_base_url
                                updated = True
                            for k in ["API-Key", "api_key", "API_Key", "apiKey"]:
                                if k in val:
                                    if val[k] != new_key:
                                        val[k] = new_key
                                        updated = True
                                    break
                            else:
                                val["API-Key"] = new_key
                                updated = True

        if updated:
            try:
                with open(account_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"[INFO] Settings: Successfully updated API-Key for provider '{provider_name}' in account.json")
                self._set_account_provider_cache(data)
            except Exception as e:
                print(f"[ERROR] Failed to save updated account.json: {e}")
        elif self._is_custom_provider_display(provider_name):
            self._create_custom_provider_in_account_json(self.models_combo.currentText())
    #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------
    # Create the Appearance Settings Page
    def create_appearance_page_in_setting(self):
        page = QWidget()
        page.setObjectName("settingsPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        # --- Group 1: Theme ---
        # Create input fields for theme mode and toolbar icon visibility
        self.group_theme = QGroupBox("Theme & UI")
        form = QFormLayout(self.group_theme)
        self._setup_form_layout(form)
=======

    #-------------------------------------------------------------------------------------
    def create_appearance_page_in_setting(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0,0,0,0)

        self.group_theme = QGroupBox("Theme & UI")
        form = QFormLayout(self.group_theme)
        form.setVerticalSpacing(15)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

        self.lbl_theme_mode = QLabel("Theme mode:")
        mode_combo = QComboBox()
        mode_combo.addItems(["Light"])
        mode_combo.setCurrentText(self.settings.value("Appearance/theme", "Light"))
        self.controls["Appearance"]["theme"] = mode_combo
        
        self.chk_toolbar_icons = QCheckBox("Show toolbar icons")
        self.chk_toolbar_icons.setChecked(self.settings.value("Appearance/toolbar_icons", True, type=bool))
        self.controls["Appearance"]["toolbar_icons"] = self.chk_toolbar_icons

        form.addRow(self.lbl_theme_mode, mode_combo)
        form.addRow("", self.chk_toolbar_icons)
        layout.addWidget(self.group_theme)

<<<<<<< HEAD
        # --- Group 2: Chat Background ---
        # Create input fields for selecting a custom background image
        self.group_bg = QGroupBox("Chat Background")
        bg_layout = QVBoxLayout(self.group_bg)
        bg_layout.setContentsMargins(16, 20, 16, 16)
        bg_layout.setSpacing(12)
        
        self.lbl_bg_instruction = QLabel("Select a custom background image (JPG, PNG, GIF):")
        
        # Read-only line edit
=======
        self.group_bg = QGroupBox("Chat Background")
        bg_layout = QVBoxLayout(self.group_bg)
        
        self.lbl_bg_instruction = QLabel("Select a custom background image (JPG, PNG, GIF):")
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.bg_path_input = QLineEdit()
        self.bg_path_input.setPlaceholderText("No image selected (Default)")
        self.bg_path_input.setReadOnly(True)
        saved_bg = self.settings.value("Appearance/chat_background", "")
        self.bg_path_input.setText(saved_bg)
        self.controls["Appearance"]["chat_background"] = self.bg_path_input

<<<<<<< HEAD
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(10)
=======
        btn_layout = QHBoxLayout()
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.btn_browse_bg = QPushButton("Browse Image...")
        self.btn_browse_bg.clicked.connect(self.browse_background_image)
        
        self.btn_clear_bg = QPushButton("Clear / Reset")
        self.btn_clear_bg.clicked.connect(lambda: self.bg_path_input.setText(""))

        btn_layout.addWidget(self.btn_browse_bg)
        btn_layout.addWidget(self.btn_clear_bg)
        
        bg_layout.addWidget(self.lbl_bg_instruction)
        bg_layout.addWidget(self.bg_path_input)
        bg_layout.addLayout(btn_layout)
        
        layout.addWidget(self.group_bg)
        layout.addStretch()
        return page

    def browse_background_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Background Image", 
            "", 
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self.bg_path_input.setText(file_path)
<<<<<<< HEAD
    #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------
    # Create the Font Settings Page
    def create_font_page_in_setting(self):
        page = QWidget()
        page.setObjectName("settingsPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)
        self.group_font = QGroupBox("Font Settings")
        font_layout = QVBoxLayout(self.group_font)
        font_layout.setContentsMargins(16, 20, 16, 16)
        font_layout.setSpacing(10)

        # --- Font Type ---
        # Create a dropdown for selecting the font type
        self.lbl_font_type = QLabel("Font type:")
        font_combo = QComboBox()
        
=======

    def create_font_page_in_setting(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.group_font = QGroupBox("Font Settings")
        font_layout = QVBoxLayout(self.group_font)

        self.lbl_font_type = QLabel("Font type:")
        font_combo = QComboBox()
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        font_list = [
            "Arial", "Calibri", "Times New Roman", "Courier New", 
            "Microsoft YaHei", "SimHei", "SimSun", 
            "KaiTi", "FangSong", 
            "STHeiti", "STKaiti", "STSong", "STFangsong", "PingFang SC"
        ]
        font_combo.addItems(font_list)
        font_combo.setCurrentText(self.settings.value("Font/type", "Microsoft YaHei"))
        font_layout.addWidget(self.lbl_font_type)
        font_layout.addWidget(font_combo)
        self.controls["Font"]["type"] = font_combo

<<<<<<< HEAD
        # --- Font Size ---
        # Create a dropdown for selecting the font size
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.lbl_font_size = QLabel("Font size:")
        size_combo = QComboBox()
        size_combo.addItems([str(s) for s in range(8, 30)])
        size_combo.setCurrentText(self.settings.value("Font/size", "10"))
        font_layout.addWidget(self.lbl_font_size)
        font_layout.addWidget(size_combo)
        self.controls["Font"]["size"] = size_combo

        layout.addWidget(self.group_font)
        layout.addStretch()
        return page

<<<<<<< HEAD
    #-------------------------------------------------------------------------------------
    # Create the Language Settings Page
    def create_language_page_in_setting(self):
        page = QWidget()
        page.setObjectName("settingsPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)
        self.group_language = QGroupBox("Language Settings")
        lang_layout = QVBoxLayout(self.group_language)
        lang_layout.setContentsMargins(16, 20, 16, 16)
        lang_layout.setSpacing(10)
        
        # --- Language Type ---
        # Create a dropdown for selecting the application language
=======
    def create_language_page_in_setting(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.group_language = QGroupBox("Language Settings")
        lang_layout = QVBoxLayout(self.group_language)
        
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.lbl_lang_type = QLabel("Language type:")
        language_combo = QComboBox()
        language_combo.addItems(["English", "Chinese"])
        language_combo.setCurrentText(self.settings.value("Language/type", "English"))
        lang_layout.addWidget(self.lbl_lang_type)
        lang_layout.addWidget(language_combo)
        self.controls["Language"]["type"] = language_combo
        
        layout.addWidget(self.group_language)
        layout.addStretch()
        return page

<<<<<<< HEAD
    #-------------------------------------------------------------------------------------
    # Create the Search Settings Page
    def create_search_page_in_setting(self):
        page = QWidget()
        page.setObjectName("settingsPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        self.lbl_search_engine = QLabel("Search engine:")
        
        # --- Search Engine ---
        # Create radio buttons for selecting the default search engine
=======
    def create_search_page_in_setting(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.lbl_search_engine = QLabel("Search engine:")
        
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        baidu_radio = QRadioButton("Baidu")
        google_radio = QRadioButton("Google")
        
        if self.settings.value("Search/Google", False, type=bool):
            google_radio.setChecked(True)
        else:
            baidu_radio.setChecked(True)

        bg = QButtonGroup(page)
        bg.addButton(baidu_radio)
        bg.addButton(google_radio)

<<<<<<< HEAD
        self.group_search = QGroupBox("Search Engine")
        search_layout = QVBoxLayout(self.group_search)
        search_layout.setContentsMargins(16, 20, 16, 16)
        search_layout.setSpacing(10)
        search_layout.addWidget(self.lbl_search_engine)
        search_layout.addWidget(baidu_radio)
        search_layout.addWidget(google_radio)

        self.controls["Search"]["Baidu"] = baidu_radio
        self.controls["Search"]["Google"] = google_radio
        layout.addWidget(self.group_search)
        layout.addStretch()
        return page

    #-------------------------------------------------------------------------------------
    # Change the current page in the stacked widget based on the selected tree item
    def change_page(self, current, previous):
        if not current: return
        
        # Map Tree Items to Pages
=======
        layout.addWidget(self.lbl_search_engine)
        layout.addWidget(baidu_radio)
        layout.addWidget(google_radio)

        self.controls["Search"]["Baidu"] = baidu_radio
        self.controls["Search"]["Google"] = google_radio
        layout.addStretch()
        return page

    def change_page(self, current, previous):
        if not current: return
        
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if current == self.item_ai:
            self.stack.setCurrentWidget(self.ai_page)
        elif current == self.item_appearance:
            self.stack.setCurrentWidget(self.appearance_page)
        elif current == self.item_font:
            self.stack.setCurrentWidget(self.font_page)
        elif current == self.item_language:
            self.stack.setCurrentWidget(self.language_page)
        elif current == self.item_search:
            self.stack.setCurrentWidget(self.search_page)

<<<<<<< HEAD
    #-------------------------------------------------------------------------------------
    # Update UI Texts for Translation
    # Refresh all text in the Settings Window based on the current language
    def update_ui_texts(self, lang_manager):
        """
        Refreshes all text in the Settings Window based on the current language.
        """
        if not lang_manager: return
        
        # Window Title
        self.setWindowTitle(lang_manager.get_text("Preferences"))

        # Sidebar Items
=======
    def update_ui_texts(self, lang_manager):
        if not lang_manager: return
        
        self.setWindowTitle(lang_manager.get_text("Preferences"))

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.item_ai.setText(0, lang_manager.get_text("AI Configuration"))
        self.item_appearance.setText(0, lang_manager.get_text("Appearance"))
        self.item_font.setText(0, lang_manager.get_text("Font Settings"))
        self.item_language.setText(0, lang_manager.get_text("Language Settings"))
        self.item_search.setText(0, lang_manager.get_text("Search"))

<<<<<<< HEAD
        # Dialog Buttons
        self.button_box.button(QDialogButtonBox.Ok).setText(lang_manager.get_text("Save"))
        self.button_box.button(QDialogButtonBox.Cancel).setText(lang_manager.get_text("Cancel"))

        # 1. AI Page
        self.group_ai_api.setTitle(lang_manager.get_text("API Connection"))
        self.lbl_provider.setText(lang_manager.get_text("Provider"))
        self.lbl_model.setText(lang_manager.get_text("Model"))
=======
        self.button_box.button(QDialogButtonBox.Ok).setText(lang_manager.get_text("Save"))
        self.button_box.button(QDialogButtonBox.Cancel).setText(lang_manager.get_text("Cancel"))

        self.group_ai_api.setTitle(lang_manager.get_text("API Connection"))
        self.lbl_provider.setText(lang_manager.get_text("Provider"))
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.lbl_base_url.setText(lang_manager.get_text("Base URL"))
        self.lbl_api_key.setText(lang_manager.get_text("API Key"))
        
        self.group_ai_behavior.setTitle(lang_manager.get_text("Behavior"))
        self.lbl_sys_prompt.setText(lang_manager.get_text("System Prompt"))
        self.lbl_temperature.setText(lang_manager.get_text("Temperature"))
        self.btn_reset_ai.setText(lang_manager.get_text("Reset"))

<<<<<<< HEAD
        # 2. Appearance Page
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.group_theme.setTitle(lang_manager.get_text("Theme & UI"))
        self.lbl_theme_mode.setText(lang_manager.get_text("Theme mode:"))
        self.chk_toolbar_icons.setText(lang_manager.get_text("Show toolbar icons"))
        
        self.group_bg.setTitle(lang_manager.get_text("Chat Background"))
        self.lbl_bg_instruction.setText(lang_manager.get_text("Select a custom background image (JPG, PNG, GIF):"))
        self.btn_browse_bg.setText(lang_manager.get_text("Browse Image..."))
        self.btn_clear_bg.setText(lang_manager.get_text("Clear / Reset"))

<<<<<<< HEAD
        # 3. Font Page
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.group_font.setTitle(lang_manager.get_text("Font Settings"))
        self.lbl_font_type.setText(lang_manager.get_text("Font type:"))
        self.lbl_font_size.setText(lang_manager.get_text("Font size:"))

<<<<<<< HEAD
        # 4. Language Page
        self.group_language.setTitle(lang_manager.get_text("Language Settings"))
        self.lbl_lang_type.setText(lang_manager.get_text("Select Language"))

        # 5. Search Page
        self.group_search.setTitle(lang_manager.get_text("Search"))
        self.lbl_search_engine.setText(lang_manager.get_text("Search engine:"))

    #-------------------------------------------------------------------------------------
    # Save all settings to the settings.ini file
    def accept(self):
        """Save all settings"""
        #---------------------------------------------------------------------------------
        # Save AI settings
        ai = self.controls["AI"]
        provider_name = ai["provider"].currentText()
        new_key = ai["api_key"].text().strip()
        selected_model = ai["models"].currentText()

        self.settings.setValue("AI/provider", provider_name)
        self.settings.setValue("AI/base_url", ai["base_url"].text().strip())
        self.settings.setValue("AI/api_key", new_key)
        self.settings.setValue("AI/model", selected_model)
        self.settings.setValue("AI/system_prompt", ai["system_prompt"].toPlainText().strip())
        self.settings.setValue("AI/temperature", ai["temperature"].value() / 10.0)

        # Save to account.json dynamically
        self.save_api_key_to_account_json(provider_name, new_key, ai["base_url"].text().strip())
        
        #---------------------------------------------------------------------------------
        # Save appearance settings
        self.settings.setValue("Appearance/theme", self.controls["Appearance"]["theme"].currentText())
        self.settings.setValue("Appearance/toolbar_icons", self.controls["Appearance"]["toolbar_icons"].isChecked())

        self.settings.setValue("Appearance/chat_background", self.controls["Appearance"]["chat_background"].text())

        #---------------------------------------------------------------------------------
        # Save font settings
        self.settings.setValue("Font/type", self.controls["Font"]["type"].currentText())
        self.settings.setValue("Font/size", self.controls["Font"]["size"].currentText())

        #---------------------------------------------------------------------------------
        # Save language settings
        self.settings.setValue("Language/type", self.controls["Language"]["type"].currentText())

        #---------------------------------------------------------------------------------
        # Save search settings
=======
        self.group_language.setTitle(lang_manager.get_text("Language Settings"))
        self.lbl_lang_type.setText(lang_manager.get_text("Select Language"))

        self.lbl_search_engine.setText(lang_manager.get_text("Search engine:"))

    def accept(self):
        ai = self.controls["AI"]
        self.settings.setValue("AI/provider", ai["provider"].currentText())
        self.settings.setValue("AI/base_url", ai["base_url"].text().strip())
        self.settings.setValue("AI/api_key", ai["api_key"].text().strip())
        self.settings.setValue("AI/system_prompt", ai["system_prompt"].toPlainText().strip())
        self.settings.setValue("AI/temperature", ai["temperature"].value() / 10.0)
        
        self.settings.setValue("Appearance/theme", self.controls["Appearance"]["theme"].currentText())
        self.settings.setValue("Appearance/toolbar_icons", self.controls["Appearance"]["toolbar_icons"].isChecked())
        self.settings.setValue("Appearance/chat_background", self.controls["Appearance"]["chat_background"].text())

        self.settings.setValue("Font/type", self.controls["Font"]["type"].currentText())
        self.settings.setValue("Font/size", self.controls["Font"]["size"].currentText())
        self.settings.setValue("Language/type", self.controls["Language"]["type"].currentText())
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.settings.setValue("Search/Baidu", self.controls["Search"]["Baidu"].isChecked())
        self.settings.setValue("Search/Google", self.controls["Search"]["Google"].isChecked())

        self.settings.sync()
        self.settings_page_operation_signal.emit("Settings saved successfully!")
        self.apply_settings_signal.emit()
        super().accept()

<<<<<<< HEAD
    #-------------------------------------------------------------------------------------
    # Discard changes and close the dialog
    def reject(self):
        self.settings_page_operation_signal.emit("Settings discarded!")
        self.apply_settings_signal.emit()
        super().reject()

    #-------------------------------------------------------------------------------------
    # Reset preferences to default values
    def reset_preferences(self):
        #---------------------------------------------------------------------------------
        # Reset UI elements for model selection as well
        ai = self.controls["AI"]
        ai["models"].clear()
        # after reset, repopulate models for default provider
        default_provider = "OpenRouter (Recommended)"
        self._populate_models_for_provider(default_provider)
        # Set default model to first option if any
        if ai["models"].count() > 0:
            ai["models"].setCurrentIndex(0)
        
=======
    def reject(self):
        self.settings_page_operation_signal.emit("Settings discarded!")
        super().reject()

    def reset_preferences(self):
        ai = self.controls["AI"]
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        ai["provider"].setCurrentText("OpenRouter (Recommended)")
        ai["base_url"].setText("https://openrouter.ai/api/v1/chat/completions")
        ai["api_key"].setText("")
        ai["system_prompt"].setPlainText("You are a helpful assistant.")
        ai["temperature"].setValue(7)
        
        QMessageBox.information(self, "Reset", "AI Settings reset to defaults.")

<<<<<<< HEAD
    #-------------------------------------------------------------------------------------
    # Test Connection to API
    def on_test_connection_clicked(self):
        """Handle test connection button click"""
        import requests
        from threading import Thread
        
        # Get current values
        api_key = self.controls["AI"]["api_key"].text().strip()
        base_url = self.controls["AI"]["base_url"].text().strip()
        model = self.controls["AI"]["models"].currentText().strip()
        
        # Validate inputs
        if not api_key:
            self.update_connection_status(False, "❌ API Key is required")
            return
        if not base_url:
            self.update_connection_status(False, "❌ Base URL is required")
            return
        if not model:
            self.update_connection_status(False, "❌ Model is required")
            return
        
        # Show testing status
        self.btn_test_connection.setEnabled(False)
        self.update_connection_status(None, "🔄 Testing connection...")
        
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
                    self.update_connection_status(True, "✅ Connection successful!")
                    self.connection_test_signal.emit(True, "Connection successful")
                else:
                    error_msg = f"❌ Connection failed (HTTP {response.status_code})"
                    try:
                        error_data = response.json()
                        if "error" in error_data:
                            error_msg += f": {error_data['error'].get('message', 'Unknown error')}"
                    except:
                        pass
                    self.update_connection_status(False, error_msg)
                    self.connection_test_signal.emit(False, error_msg)
            except requests.exceptions.Timeout:
                self.update_connection_status(False, "❌ Connection timeout")
                self.connection_test_signal.emit(False, "Connection timeout")
            except requests.exceptions.ConnectionError:
                self.update_connection_status(False, "❌ Connection error - Check URL and network")
                self.connection_test_signal.emit(False, "Connection error")
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                self.update_connection_status(False, error_msg)
                self.connection_test_signal.emit(False, str(e))
            finally:
                self.btn_test_connection.setEnabled(True)
        
        thread = Thread(target=test_connection, daemon=True)
        thread.start()
    
    def update_connection_status(self, success, message):
        """Update the connection status label"""
        self.lbl_connection_status.setText(message)
        
        if success is True:
            self.lbl_connection_status.setStyleSheet("color: #00aa00; font-size: 14px; font-weight: bold;")
        elif success is False:
            self.lbl_connection_status.setStyleSheet("color: #ff4444; font-size: 14px; font-weight: bold;")
        else:
            self.lbl_connection_status.setStyleSheet("color: #0099ff; font-size: 14px; font-weight: bold;")

    #-------------------------------------------------------------------------------------
    # Getters for retrieving specific settings
    def get_api_key(self):
        """Get the saved API key"""
        return self.settings.value("AI/api_key", "", type=str)

    def get_base_url(self):
        """Get the saved base URL"""
        return self.settings.value("AI/base_url", "", type=str)

    def get_system_prompt(self):
        """Get the saved system prompt"""
=======
    def get_api_key(self):
        return self.settings.value("AI/api_key", "", type=str)

    def get_base_url(self):
        return self.settings.value("AI/base_url", "", type=str)

    def get_system_prompt(self):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        return self.settings.value("AI/system_prompt", "You are a helpful assistant.", type=str)
