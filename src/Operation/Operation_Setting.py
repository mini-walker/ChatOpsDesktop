#-----------------------------------------------------------------------
<<<<<<< HEAD
<<<<<<< HEAD
# Purpose: The operation controller for the setting page
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-10-27  
#-----------------------------------------------------------------------

import sys  # Import system-specific parameters and functions
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
# Purpouse: The operation controller for the setting page
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-10-27
#-----------------------------------------------------------------------

import sys
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
import os
import webbrowser
import logging
import subprocess
import time
import json
import pandas as pd

from pathlib import Path
from urllib.parse import quote_plus

#-----------------------------------------------------------------------
<<<<<<< HEAD
<<<<<<< HEAD
# Import PyQt5 widgets for UI elements
from PySide6.QtWidgets import ( 
    QApplication, 
    QMainWindow, QTextEdit, QToolBar, QDockWidget, QListWidget, QFileDialog,
    QLabel, QFileDialog, QAbstractButton, QWidget, QStackedWidget, QTabWidget, QGroupBox,    
    QLineEdit, QMenu, 
    QPushButton, QRadioButton, QButtonGroup, QWidgetAction,
    QVBoxLayout, QHBoxLayout, QSizePolicy, QTreeWidget, QTreeWidgetItem, QCheckBox,
    QFormLayout, QGridLayout, QDialog, QDialogButtonBox, QComboBox,
    QMessageBox
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QAction, QPainter, QColor                      # Import classes for images, fonts, and icons
from PySide6.QtCore import Qt, QSize, QDateTime, Signal, QSettings, QObject, Slot, QThread      # Import Qt core functionalities such as alignment
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# Import the class from the local python files
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
from PySide6.QtWidgets import (
QApplication,
QMainWindow, QTextEdit, QToolBar, QDockWidget, QListWidget, QFileDialog,
QLabel, QAbstractButton, QWidget, QStackedWidget, QTabWidget, QGroupBox,
QLineEdit, QMenu,
QPushButton, QRadioButton, QButtonGroup, QWidgetAction,
QVBoxLayout, QHBoxLayout, QSizePolicy, QTreeWidget, QTreeWidgetItem, QCheckBox,
QFormLayout, QGridLayout, QDialog, QDialogButtonBox, QComboBox,
QMessageBox
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QAction, QPainter, QColor
from PySide6.QtCore import Qt, QSize, QDateTime, Signal, QSettings, QObject, Slot, QThread
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
from Utils.Utils import utils
from Operation.Operation_Mainwindow import Operation_Mainwindow_Controller
#-----------------------------------------------------------------------

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
#-----------------------------------------------------------------------
class Operation_Setting_Controller(QObject):

    def __init__(self, parent = None):
<<<<<<< HEAD
<<<<<<< HEAD
        """
        Controller for applying settings to the main application UI.

        Args:
            main_window (QMainWindow): The main window instance of the application.
        """

        #-----------------------------------------------------------------------
        # Get the main window, setting page, and tool bar from the parent
        #-----------------------------------------------------------------------
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.main_window  = parent
        self.setting_page = parent.setting_page
        self.tool_bar     = parent.tool_bar
        self.side_panel   = parent.side_panel
        self.chat_window  = parent.chat_window

        self.operation_mainwindow  = Operation_Mainwindow_Controller(self.main_window) 
        
<<<<<<< HEAD
<<<<<<< HEAD
        #-----------------------------------------------------------------------
        # Get the QSettings file path
        #-----------------------------------------------------------------------
        usr_folder = utils.get_usr_dir()
        self.settings_file_path = usr_folder / "settings.ini"

    def update_toolbar_models(self, models, selected_model=""):
        """Synchronize toolbar model choices with the settings dialog immediately."""
        if hasattr(self.main_window, "tool_bar"):
            self.main_window.tool_bar.update_models_list(models, selected_model)
        if hasattr(self.main_window, "operation_chat") and hasattr(self.setting_page, "controls"):
            ai_ctrls = self.setting_page.controls.get("AI", {})
            new_model = self.tool_bar.get_current_AI_model()
            new_key = ai_ctrls.get("api_key").text().strip() if "api_key" in ai_ctrls else ""
            new_url = ai_ctrls.get("base_url").text().strip() if "base_url" in ai_ctrls else ""
            chat = self.main_window.operation_chat
            chat.model = new_model
            chat.api_key = new_key
            chat.base_url = new_url
            chat.model_logo = self.tool_bar.get_current_AI_model_logo()
            if getattr(chat, "worker", None):
                chat.worker.update_config(new_key, new_url, new_model)

    #-----------------------------------------------------------------------
    # Apply new settings from settings.ini to the main application
    #-----------------------------------------------------------------------
    def apply_new_settings(self):
        """
        Apply new settings from settings.ini to the main application.

        This function reads the .ini file and updates:
        - Font (type and size) for text-based widgets only
        - Theme / Appearance
        - Toolbar icon visibility and size
        - Language
        - Search Engine
        - AI Configuration (Provider, URL, Key, Prompt)
        """

        # ---------------- Font Settings ----------------
        # Apply font settings to all specific windows and their children
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        usr_folder = utils.get_usr_dir()
        self.settings_file_path = usr_folder / "settings.ini"

    #-----------------------------------------------------------------------
    def apply_new_settings(self):
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        settings = QSettings(str(self.settings_file_path), QSettings.Format.IniFormat)

        font_type = settings.value("Font/type", "Times New Roman")
        font_size = int(settings.value("Font/size", "10"))
        app_font = QFont(font_type, font_size)
        QApplication.instance().setFont(app_font)

        Total_windows = [self.main_window, self.setting_page, self.side_panel, self.chat_window, self.tool_bar]
<<<<<<< HEAD
<<<<<<< HEAD
        
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        text_widgets = (QTextEdit, QLineEdit, QComboBox, QPushButton, QToolBar,
                        QLabel, QRadioButton, QCheckBox, QDialog, QWidget, QGroupBox, 
                        QGridLayout, QTreeWidget, QTreeWidgetItem, QMenu)
        
        for window in Total_windows:
            if not window: continue
            for cls in text_widgets:
                for widget in window.findChildren(cls):
                    widget.setFont(app_font)
            window.setFont(app_font)

        QApplication.instance().setFont(app_font)

<<<<<<< HEAD
<<<<<<< HEAD
        # ---------------- Appearance / Theme ----------------
        # Define QSS stylesheets for different themes
        appearance_mode = settings.value("Appearance/theme", "Light")  # Light, Dark, Blue
        
=======
        appearance_mode = settings.value("Appearance/theme", "Light")
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
        appearance_mode = settings.value("Appearance/theme", "Light")
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        dark_qss = """
            QWidget { 
                background-color: #2E2E2E; 
                color: #F0F0F0; 
            }
            QLineEdit, QTextEdit, QPlainTextEdit, QTreeWidget, QListWidget {
                background-color: #3E3E3E; 
                color: #FFFFFF; 
                border: 1px solid #555555;
            }
            QComboBox {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #555555;
            }
            QPushButton {
                background-color: #454545;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 4px;
            }
            QPushButton:hover { background-color: #505050; }
            QMenu { background-color: #2E2E2E; color: #FFFFFF; }
            QMenu::item:selected { background-color: #505050; }
        """
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        blue_qss = """
            QWidget { 
                background-color: #DCE6F1; 
                color: #000000; 
            }
            QLineEdit, QTextEdit, QPlainTextEdit, QTreeWidget {
                background-color: #FFFFFF;
                color: #000000;
                border: 1px solid #A0A0A0;
            }
        """
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        light_qss = "" 

        target_qss = light_qss
        if appearance_mode.lower() == "dark":
            target_qss = dark_qss
        elif appearance_mode.lower() == "blue":
            target_qss = blue_qss

        if self.main_window:
            self.main_window.setStyleSheet(target_qss)
<<<<<<< HEAD
<<<<<<< HEAD
        
        if self.setting_page:
            self.setting_page.setStyleSheet(target_qss)

        QApplication.instance().setStyleSheet(target_qss)
        if hasattr(self.setting_page, "apply_theme_style"):
            self.setting_page.apply_theme_style(appearance_mode)

        # ---------------- Chat Background ----------------
        # Apply chat background settings
        background_path = settings.value("Appearance/chat_background", "")
        
        if hasattr(self.main_window, "chat_window"):
            self.main_window.chat_window.set_chat_background(background_path)
            print(f"[INFO] Applied chat background: {background_path}")

        # ---------------- Toolbar Icons ----------------
        # Apply toolbar icon visibility settings
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if self.setting_page:
            self.setting_page.setStyleSheet(target_qss)
        QApplication.instance().setStyleSheet(target_qss)

        background_path = settings.value("Appearance/chat_background", "")
        if hasattr(self.main_window, "chat_window"):
            self.main_window.chat_window.set_chat_background(background_path)

<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        show_toolbar_icons = settings.value("Appearance/toolbar_icons", True, type=bool)
        if hasattr(self.main_window, "tool_bar"):
            self.tool_bar.setVisible(show_toolbar_icons)

<<<<<<< HEAD
<<<<<<< HEAD
        # ---------------- Language Settings ----------------
        # Apply language settings to the application
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        language_type = settings.value("Language/type", "English")
        new_language = "Chinese" if language_type.startswith("Chinese") else "English"
        if hasattr(self.main_window, "language_manager"):
            self.main_window.language_manager.set_language(new_language)

        if hasattr(self.tool_bar, "update_ui_texts"):
            self.tool_bar.update_ui_texts(self.main_window.language_manager)
<<<<<<< HEAD
<<<<<<< HEAD

        if hasattr(self.chat_window, "update_ui_texts"):
            self.chat_window.update_ui_texts(self.main_window.language_manager)

        if hasattr(self.side_panel, "update_ui_texts"):
            self.side_panel.update_ui_texts(self.main_window.language_manager)

        if hasattr(self.setting_page, "update_ui_texts"):
            self.setting_page.update_ui_texts(self.main_window.language_manager)

        # ---------------- Search Settings ----------------
        # Apply search engine settings
        use_baidu  = settings.value("Search/Baidu", True, type=bool)
        use_google = settings.value("Search/Google", False, type=bool)

=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if hasattr(self.chat_window, "update_ui_texts"):
            self.chat_window.update_ui_texts(self.main_window.language_manager)
        if hasattr(self.side_panel, "update_ui_texts"):
            self.side_panel.update_ui_texts(self.main_window.language_manager)
        if hasattr(self.setting_page, "update_ui_texts"):
            self.setting_page.update_ui_texts(self.main_window.language_manager)

        use_baidu  = settings.value("Search/Baidu", True, type=bool)
        use_google = settings.value("Search/Google", False, type=bool)
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        try:
            self.tool_bar.search_requested.disconnect()
        except (TypeError, RuntimeError):
            pass
<<<<<<< HEAD
<<<<<<< HEAD

        if use_baidu and not use_google:
            self.tool_bar.search_requested.connect(self.operation_mainwindow.perform_baidu_search)
        # Apply chat background settings
        background_path = settings.value("Appearance/chat_background", "")
        
        if hasattr(self.main_window, "chat_window"):
            self.main_window.chat_window.set_chat_background(background_path)
            print(f"[INFO] Applied chat background: {background_path}")

        # ---------------- Toolbar Icons ----------------
        # Apply toolbar icon visibility settings
        show_toolbar_icons = settings.value("Appearance/toolbar_icons", True, type=bool)
        if hasattr(self.main_window, "tool_bar"):
            self.tool_bar.setVisible(show_toolbar_icons)

        # ---------------- Language Settings ----------------
        # Apply language settings to the application
        language_type = settings.value("Language/type", "English")
        new_language = "Chinese" if language_type.startswith("Chinese") else "English"
        if hasattr(self.main_window, "language_manager"):
            self.main_window.language_manager.set_language(new_language)

        if hasattr(self.tool_bar, "update_ui_texts"):
            self.tool_bar.update_ui_texts(self.main_window.language_manager)

        if hasattr(self.chat_window, "update_ui_texts"):
            self.chat_window.update_ui_texts(self.main_window.language_manager)

        if hasattr(self.side_panel, "update_ui_texts"):
            self.side_panel.update_ui_texts(self.main_window.language_manager)

        if hasattr(self.setting_page, "update_ui_texts"):
            self.setting_page.update_ui_texts(self.main_window.language_manager)

        # ---------------- Search Settings ----------------
        # Apply search engine settings
        use_baidu  = settings.value("Search/Baidu", True, type=bool)
        use_google = settings.value("Search/Google", False, type=bool)

        try:
            self.tool_bar.search_requested.disconnect()
        except (TypeError, RuntimeError):
            pass

=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if use_baidu and not use_google:
            self.tool_bar.search_requested.connect(self.operation_mainwindow.perform_baidu_search)
        elif use_google and not use_baidu:
            self.tool_bar.search_requested.connect(self.operation_mainwindow.perform_google_search)
        else:
            self.tool_bar.search_requested.connect(self.operation_mainwindow.perform_baidu_search)

<<<<<<< HEAD
<<<<<<< HEAD
        ## ---------------- AI Settings ----------------
        # Apply AI configuration settings
        usr_dir = utils.get_usr_dir()
        account_file = usr_dir / "account.json"

        # Load all configs
        providers = []
        if hasattr(self.main_window, "tool_bar"):
            providers = self.tool_bar.load_all_AI_configs(account_file)

        saved_provider = settings.value("AI/provider", "").lower().strip()
        matched_provider = None
        for p in providers:
            p_name = p.get("Provider", "").lower().strip()
            if saved_provider and (p_name in saved_provider or saved_provider in p_name):
                matched_provider = p
                break
        if not matched_provider and providers:
            matched_provider = providers[0]

        # Prepare UI controls
        if hasattr(self.setting_page, "controls") and "AI" in self.setting_page.controls:
            ai_ctrls = self.setting_page.controls["AI"]
            # Base URL
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if hasattr(self.main_window, "chat_controller"):
            current_model = self.tool_bar.get_current_AI_model()
            self.main_window.chat_controller.update_model_for_chat_controller(current_model, None)

        if hasattr(self.setting_page, "controls") and "AI" in self.setting_page.controls:
            ai_ctrls = self.setting_page.controls["AI"]

<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            if "base_url" in ai_ctrls:
                default_url = "https://openrouter.ai/api/v1/chat/completions"
                saved_url = settings.value("AI/base_url", default_url)
                ai_ctrls["base_url"].setText(saved_url)
<<<<<<< HEAD
<<<<<<< HEAD
            # System Prompt
=======

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            if "system_prompt" in ai_ctrls:
                default_prompt = "You are a helpful assistant."
                saved_prompt = settings.value("AI/system_prompt", default_prompt)
                ai_ctrls["system_prompt"].setPlainText(saved_prompt)
<<<<<<< HEAD
<<<<<<< HEAD
            # Provider combo
            if "provider" in ai_ctrls:
                provider_combo = ai_ctrls["provider"]
                matched_index = -1
                if matched_provider and hasattr(self.setting_page, "_provider_combo_index_for_account_provider"):
                    matched_index = self.setting_page._provider_combo_index_for_account_provider(
                        matched_provider.get("Provider") or matched_provider.get("provider") or ""
                    )
                if matched_index != -1:
                    provider_combo.setCurrentIndex(matched_index)
                    print(f"[INFO] Provider matched: {provider_combo.itemText(matched_index)}")
                else:
                    print("[WARN] Provider not found in account.json-enabled settings items.")
            # API Key
            if "api_key" in ai_ctrls:
                saved_key = settings.value("AI/api_key", "")
                ai_ctrls["api_key"].setText(saved_key)
                print("[INFO] (Apply settings) Loading saved API key into settings UI.")
            # Temperature
            if "temperature" in ai_ctrls:
                saved_temp = float(settings.value("AI/temperature", 0.7))
                ai_ctrls["temperature"].setValue(int(saved_temp * 10))

        # Update toolbar model list and select saved model
        if matched_provider and hasattr(self.main_window, "tool_bar"):
            new_models = matched_provider.get("models", [])
            # Update toolbar models list
            self.main_window.tool_bar.update_models_list(new_models)
            # Ensure a valid saved model
            saved_model = settings.value("AI/model", "")
            if saved_model not in new_models:
                # fallback to first model if available
                if new_models:
                    saved_model = new_models[0]
                    settings.setValue("AI/model", saved_model)
            # Select model in toolbar
            if saved_model in new_models:
                idx = new_models.index(saved_model)
                self.main_window.tool_bar.AI_engine_box.setCurrentIndex(idx)

        # Notify chat controller of new configuration
        if hasattr(self.main_window, "operation_chat"):
            chat = self.main_window.operation_chat
            # Update model, api_key, base_url from settings/UI
            chat.update_model_for_chat_controller(self.main_window.tool_bar.get_current_AI_model(), None)
            print("[INFO] AI Chat Controller settings updated.")
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

            if "provider" in ai_ctrls:
                saved_provider = settings.value("AI/provider", "openrouter").lower().strip()
                provider_combo = ai_ctrls["provider"]
                matched_index = -1
                for i in range(provider_combo.count()):
                    item = provider_combo.itemText(i).lower()
                    if saved_provider in item:
                        matched_index = i
                        break
                if matched_index != -1:
                    provider_combo.setCurrentIndex(matched_index)
                else:
                    custom_index = provider_combo.findText("Custom")
                    provider_combo.setCurrentIndex(custom_index)

            if "api_key" in ai_ctrls:
                saved_key = settings.value("AI/api_key", "")
                ai_ctrls["api_key"].setText(saved_key)

            if "temperature" in ai_ctrls:
                saved_temp = float(settings.value("AI/temperature", 0.7))
                ai_ctrls["temperature"].setValue(int(saved_temp * 10))
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    #-----------------------------------------------------------------------
