#-----------------------------------------------------------------------------------------
# Purpose: The language manager
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-10-27
#-----------------------------------------------------------------------------------------

import os
import json
from pathlib import Path
from PySide6.QtCore import QLocale, QSettings
from Utils.Utils import utils


class Language_Manager:
    """
    Manage language loading and translation for UI text.

    Supports:
        - Automatic language detection (system locale or settings.ini)
        - Dynamic switching between English and Chinese
        - Safe fallback for missing keys
    """

    def __init__(self):

        # # Default language
        # self.language = "English"

        #---------------------------------------------------------------------------------
        # Try to read language setting from usr/settings.ini
        #---------------------------------------------------------------------------------
        usr_folder = utils.get_usr_dir()
        settings_path = usr_folder / "settings.ini"

        if settings_path.exists():
            settings = QSettings(str(settings_path), QSettings.IniFormat)
            saved_lang = settings.value("Language/type", "English")

            if saved_lang.startswith("Chinese"):
                self.language = "Chinese"
            else:
                self.language = "English"
        else:
            # If no settings.ini yet, fall back to system language
            system_lang = QLocale.system().name()  # "zh_CN" or "en_US"
            self.language = "Chinese" if "Chinese" in system_lang else "English"

        #---------------------------------------------------------------------------------
        # Load translation file
        #---------------------------------------------------------------------------------
        file_path = utils.resource_path("usr/Translations.json")

        if not os.path.exists(file_path):
            print(f"[WARN] Missing translation file: {file_path}")
            self.translations = {"English": {}, "Chinese": {}}
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load translation file: {e}")
            self.translations = {"English": {}, "Chinese": {}}

    #-------------------------------------------------------------------------------------
    def set_language(self, lang):
        """
        Switch current language manually.
        """
        if lang.startswith("Chinese"):
            self.language = "Chinese"
        else:
            self.language = "English"

    #-------------------------------------------------------------------------------------
    def get_text(self, key):
        """
        Get translated text for given key.
        If missing, return the key itself as fallback.
        """
        print(f"Language: {self.language}, Key: {key}")
        return self.translations.get(self.language, {}).get(key, key)

    #-------------------------------------------------------------------------------------
    def get_current_language(self):
        return self.language
