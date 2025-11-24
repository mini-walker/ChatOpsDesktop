#-----------------------------------------------------------------------------------------
# Purpouse: This file is used to create the Settings Window with multi-language support
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-11-23 
#----------------------------------------------------------------------------------------- 

import sys
import os
from pathlib import Path

#-----------------------------------------------------------------------------------------
from PySide6.QtWidgets import ( 
    QFileDialog, QDialog, QHBoxLayout, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
    QStackedWidget, QDialogButtonBox, QLineEdit, QLabel, QComboBox, QCheckBox, 
    QMessageBox, QPushButton, QWidget, QGroupBox, QFormLayout, QSlider, QTextEdit,
    QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt, Signal, QSettings
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
try:
    from Utils.Utils import utils
except ImportError:
    class Utils:
        def get_usr_dir(self): return Path("usr")
    utils = Utils()
#-----------------------------------------------------------------------------------------

class Setting_Window(QDialog):

    settings_page_operation_signal = Signal(str)
    apply_settings_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Preferences")
        self.resize(700, 550) 

        #---------------------------------------------------------------------------------
        usr_folder = utils.get_usr_dir()
        os.makedirs(usr_folder, exist_ok = True)
        setting_file_path = usr_folder / "settings.ini"
        self.settings = QSettings(str(setting_file_path), QSettings.Format.IniFormat)
        #---------------------------------------------------------------------------------

        #---------------------------------------------------------------------------------
        main_layout = QHBoxLayout()

        self.preference_tree = QTreeWidget()
        self.preference_tree.setHeaderHidden(True)
        self.preference_tree.setFixedWidth(160)
        main_layout.addWidget(self.preference_tree)

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
        main_layout.addWidget(self.stack)

        self.controls = {
            "AI": {}, "Font": {}, "Search": {}, "Language": {}, "Appearance": {}
        }

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

        self.preference_tree.currentItemChanged.connect(self.change_page)
        self.preference_tree.setCurrentItem(self.item_ai)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(main_layout)
        layout.addWidget(self.button_box)

    #-------------------------------------------------------------------------------------
    def create_ai_page_in_setting(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        self.group_ai_api = QGroupBox("API Connection") 
        api_layout = QFormLayout()

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
        api_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_input.setPlaceholderText("sk-...")
        api_input.setText(self.settings.value("AI/api_key", ""))
        self.controls["AI"]["api_key"] = api_input

        api_layout.addRow(self.lbl_provider, self.provider_combo)
        api_layout.addRow(self.lbl_base_url, base_url_input)
        api_layout.addRow(self.lbl_api_key, api_input)
        self.group_ai_api.setLayout(api_layout)
        layout.addWidget(self.group_ai_api)

        self.group_ai_behavior = QGroupBox("Behavior")
        behavior_layout = QFormLayout()

        self.lbl_sys_prompt = QLabel("System Prompt:")
        sys_prompt = QTextEdit()
        sys_prompt.setPlaceholderText("You are a helpful assistant...")
        sys_prompt.setMaximumHeight(60)
        sys_prompt.setPlainText(self.settings.value("AI/system_prompt", "You are a helpful assistant."))
        self.controls["AI"]["system_prompt"] = sys_prompt

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

        self.btn_reset_ai = QPushButton("Reset AI Settings")
        self.btn_reset_ai.clicked.connect(self.reset_preferences)
        layout.addWidget(self.btn_reset_ai)

        layout.addStretch()
        return page

    def _on_provider_changed(self, provider_name):
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

    #-------------------------------------------------------------------------------------
    def create_appearance_page_in_setting(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0,0,0,0)

        self.group_theme = QGroupBox("Theme & UI")
        form = QFormLayout(self.group_theme)
        form.setVerticalSpacing(15)

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

        self.group_bg = QGroupBox("Chat Background")
        bg_layout = QVBoxLayout(self.group_bg)
        
        self.lbl_bg_instruction = QLabel("Select a custom background image (JPG, PNG, GIF):")
        self.bg_path_input = QLineEdit()
        self.bg_path_input.setPlaceholderText("No image selected (Default)")
        self.bg_path_input.setReadOnly(True)
        saved_bg = self.settings.value("Appearance/chat_background", "")
        self.bg_path_input.setText(saved_bg)
        self.controls["Appearance"]["chat_background"] = self.bg_path_input

        btn_layout = QHBoxLayout()
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

    def create_font_page_in_setting(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.group_font = QGroupBox("Font Settings")
        font_layout = QVBoxLayout(self.group_font)

        self.lbl_font_type = QLabel("Font type:")
        font_combo = QComboBox()
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

    def create_language_page_in_setting(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.group_language = QGroupBox("Language Settings")
        lang_layout = QVBoxLayout(self.group_language)
        
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

    def create_search_page_in_setting(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.lbl_search_engine = QLabel("Search engine:")
        
        baidu_radio = QRadioButton("Baidu")
        google_radio = QRadioButton("Google")
        
        if self.settings.value("Search/Google", False, type=bool):
            google_radio.setChecked(True)
        else:
            baidu_radio.setChecked(True)

        bg = QButtonGroup(page)
        bg.addButton(baidu_radio)
        bg.addButton(google_radio)

        layout.addWidget(self.lbl_search_engine)
        layout.addWidget(baidu_radio)
        layout.addWidget(google_radio)

        self.controls["Search"]["Baidu"] = baidu_radio
        self.controls["Search"]["Google"] = google_radio
        layout.addStretch()
        return page

    def change_page(self, current, previous):
        if not current: return
        
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

    def update_ui_texts(self, lang_manager):
        if not lang_manager: return
        
        self.setWindowTitle(lang_manager.get_text("Preferences"))

        self.item_ai.setText(0, lang_manager.get_text("AI Configuration"))
        self.item_appearance.setText(0, lang_manager.get_text("Appearance"))
        self.item_font.setText(0, lang_manager.get_text("Font Settings"))
        self.item_language.setText(0, lang_manager.get_text("Language Settings"))
        self.item_search.setText(0, lang_manager.get_text("Search"))

        self.button_box.button(QDialogButtonBox.Ok).setText(lang_manager.get_text("Save"))
        self.button_box.button(QDialogButtonBox.Cancel).setText(lang_manager.get_text("Cancel"))

        self.group_ai_api.setTitle(lang_manager.get_text("API Connection"))
        self.lbl_provider.setText(lang_manager.get_text("Provider"))
        self.lbl_base_url.setText(lang_manager.get_text("Base URL"))
        self.lbl_api_key.setText(lang_manager.get_text("API Key"))
        
        self.group_ai_behavior.setTitle(lang_manager.get_text("Behavior"))
        self.lbl_sys_prompt.setText(lang_manager.get_text("System Prompt"))
        self.lbl_temperature.setText(lang_manager.get_text("Temperature"))
        self.btn_reset_ai.setText(lang_manager.get_text("Reset"))

        self.group_theme.setTitle(lang_manager.get_text("Theme & UI"))
        self.lbl_theme_mode.setText(lang_manager.get_text("Theme mode:"))
        self.chk_toolbar_icons.setText(lang_manager.get_text("Show toolbar icons"))
        
        self.group_bg.setTitle(lang_manager.get_text("Chat Background"))
        self.lbl_bg_instruction.setText(lang_manager.get_text("Select a custom background image (JPG, PNG, GIF):"))
        self.btn_browse_bg.setText(lang_manager.get_text("Browse Image..."))
        self.btn_clear_bg.setText(lang_manager.get_text("Clear / Reset"))

        self.group_font.setTitle(lang_manager.get_text("Font Settings"))
        self.lbl_font_type.setText(lang_manager.get_text("Font type:"))
        self.lbl_font_size.setText(lang_manager.get_text("Font size:"))

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
        self.settings.setValue("Search/Baidu", self.controls["Search"]["Baidu"].isChecked())
        self.settings.setValue("Search/Google", self.controls["Search"]["Google"].isChecked())

        self.settings.sync()
        self.settings_page_operation_signal.emit("Settings saved successfully!")
        self.apply_settings_signal.emit()
        super().accept()

    def reject(self):
        self.settings_page_operation_signal.emit("Settings discarded!")
        super().reject()

    def reset_preferences(self):
        ai = self.controls["AI"]
        ai["provider"].setCurrentText("OpenRouter (Recommended)")
        ai["base_url"].setText("https://openrouter.ai/api/v1/chat/completions")
        ai["api_key"].setText("")
        ai["system_prompt"].setPlainText("You are a helpful assistant.")
        ai["temperature"].setValue(7)
        
        QMessageBox.information(self, "Reset", "AI Settings reset to defaults.")

    def get_api_key(self):
        return self.settings.value("AI/api_key", "", type=str)

    def get_base_url(self):
        return self.settings.value("AI/base_url", "", type=str)

    def get_system_prompt(self):
        return self.settings.value("AI/system_prompt", "You are a helpful assistant.", type=str)
