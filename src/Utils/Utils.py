#-----------------------------------------------------------------------------------------
# Purpouse: This file contains various utility functions for file path handling,
#           text formatting, and filename sanitization.
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-11-23 
#----------------------------------------------------------------------------------------- 

import sys
import re
from pathlib import Path

class utils:

    #--------------------------------------------------------------
    # For static file
    @staticmethod
    def resource_path(relative_path):
        """
        Return an absolute resource path that works both during development
        and when bundled by PyInstaller (uses sys._MEIPASS).
        """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = Path(sys._MEIPASS)
        except AttributeError:
            # base path is the project folder
            base_path = Path(__file__).parent.parent.parent.resolve()
        
        return str(base_path / relative_path)
    #--------------------------------------------------------------

    #--------------------------------------------------------------
    # For dynamic file, such as input/output result file
    @staticmethod
    def get_usr_dir():
        if getattr(sys, 'frozen', False):
            # PyInstaller mode
            base_dir = Path(sys.executable).parent
        else:
            # debug mode
            base_dir = Path(__file__).resolve().parent.parent.parent  

        usr_dir = base_dir / "usr"
        usr_dir.mkdir(exist_ok=True)
        return usr_dir
    #--------------------------------------------------------------

    #--------------------------------------------------------------
    @staticmethod
    def convert_sub_and_superscript(text):
        """
        Convert unit text with ^ (superscript) and _ (subscript) to HTML format.

        Args:
            unit_text (str): The unit text (e.g., "m^2" or "m_3").

        Returns:
            str: HTML-formatted unit (e.g., "m<sup>2</sup>" or "m<sub>3</sub>").
        """
        # Transfer the unicode
        def replace_unicode(match):
            code = match.group(1)
            return chr(int(code, 16))
        
        text = re.sub(r'\\u([0-9A-Fa-f]{4})', replace_unicode, text)
        text = re.sub(r'_([^_}]+)', r'<sub>\1</sub>', text)
        text = re.sub(r'\^([^_^}]+)', r'<sup>\1</sup>', text)
        return text
    #--------------------------------------------------------------

    #--------------------------------------------------------------
    @staticmethod
    def sanitize_filename(name: str) -> str:
        """
        Replace invalid characters for Windows file names with '_'.
        """
        return re.sub(r'[<>:"/\\|?*]', "_", name)
    #--------------------------------------------------------------

    #--------------------------------------------------------------
    @staticmethod
    def build_chat_file_path(folder_name: str, chat_title: str, root_dir=None) -> Path:
        """
        Build a valid JSON file path for a chat under the given folder.

        Args:
            folder_name (str): Folder name.
            chat_title (str): Chat title (will be sanitized).
            root_dir (str|Path, optional): Root directory to store chat folders.
                If None, uses `utils.get_usr_dir()/ChatHistory`.

        Returns:
            Path: Full path to chat JSON file.
        """
        if root_dir is None:
            if getattr(sys, 'frozen', False):
                base_dir = Path(sys.executable).parent
            else:
                base_dir = Path(__file__).resolve().parent.parent.parent
        else:
            base_dir = Path(root_dir)

        folder_path = base_dir / "ChatHistory" / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)

        safe_title = utils.sanitize_filename(chat_title)
        return folder_path / f"{safe_title}.json"

    #--------------------------------------------------------------
