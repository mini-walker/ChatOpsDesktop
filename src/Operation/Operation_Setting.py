#-----------------------------------------------------------------------
# Purpouse: The operation controller for the setting page
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-10-27
#-----------------------------------------------------------------------

import sys
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
from Utils.Utils import utils
from Operation.Operation_Mainwindow import Operation_Mainwindow_Controller
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
class Operation_Setting_Controller(QObject):

    def __init__(self, parent = None):
        self.main_window  = parent
        self.setting_page = parent.setting_page
        self.tool_bar     = parent.tool_bar
        self.side_panel   = parent.side_panel
        self.chat_window  = parent.chat_window

        self.operation_mainwindow  = Operation_Mainwindow_Controller(self.main_window) 
        
        usr_folder = utils.get_usr_dir()
        self.settings_file_path = usr_folder / "settings.ini"

    #-----------------------------------------------------------------------
    def apply_new_settings(self):
        settings = QSettings(str(self.settings_file_path), QSettings.Format.IniFormat)

        font_type = settings.value("Font/type", "Times New Roman")
        font_size = int(settings.value("Font/size", "10"))
        app_font = QFont(font_type, font_size)
        QApplication.instance().setFont(app_font)

        Total_windows = [self.main_window, self.setting_page, self.side_panel, self.chat_window, self.tool_bar]
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

        appearance_mode = settings.value("Appearance/theme", "Light")
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
        light_qss = "" 

        target_qss = light_qss
        if appearance_mode.lower() == "dark":
            target_qss = dark_qss
        elif appearance_mode.lower() == "blue":
            target_qss = blue_qss

        if self.main_window:
            self.main_window.setStyleSheet(target_qss)
        if self.setting_page:
            self.setting_page.setStyleSheet(target_qss)
        QApplication.instance().setStyleSheet(target_qss)

        background_path = settings.value("Appearance/chat_background", "")
        if hasattr(self.main_window, "chat_window"):
            self.main_window.chat_window.set_chat_background(background_path)

        show_toolbar_icons = settings.value("Appearance/toolbar_icons", True, type=bool)
        if hasattr(self.main_window, "tool_bar"):
            self.tool_bar.setVisible(show_toolbar_icons)

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

        use_baidu  = settings.value("Search/Baidu", True, type=bool)
        use_google = settings.value("Search/Google", False, type=bool)
        try:
            self.tool_bar.search_requested.disconnect()
        except (TypeError, RuntimeError):
            pass
        if use_baidu and not use_google:
            self.tool_bar.search_requested.connect(self.operation_mainwindow.perform_baidu_search)
        elif use_google and not use_baidu:
            self.tool_bar.search_requested.connect(self.operation_mainwindow.perform_google_search)
        else:
            self.tool_bar.search_requested.connect(self.operation_mainwindow.perform_baidu_search)

        if hasattr(self.main_window, "chat_controller"):
            current_model = self.tool_bar.get_current_AI_model()
            self.main_window.chat_controller.update_model_for_chat_controller(current_model, None)

        if hasattr(self.setting_page, "controls") and "AI" in self.setting_page.controls:
            ai_ctrls = self.setting_page.controls["AI"]

            if "base_url" in ai_ctrls:
                default_url = "https://openrouter.ai/api/v1/chat/completions"
                saved_url = settings.value("AI/base_url", default_url)
                ai_ctrls["base_url"].setText(saved_url)

            if "system_prompt" in ai_ctrls:
                default_prompt = "You are a helpful assistant."
                saved_prompt = settings.value("AI/system_prompt", default_prompt)
                ai_ctrls["system_prompt"].setPlainText(saved_prompt)

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
    #-----------------------------------------------------------------------
