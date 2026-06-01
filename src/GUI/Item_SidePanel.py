#-----------------------------------------------------------------------------------------
<<<<<<< HEAD
# Purpose : Implements the chat history side panel, including folder management,
#           chat persistence helpers, and UI translations.
# Author  : Shanqin Jin
# Email   : sjin@mun.ca
# Updated : 2025-11-23
=======
# Purpouse: This file is used to create the side panel for chat history management
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-11-23 
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
#----------------------------------------------------------------------------------------- 


from pathlib import Path
import json
import time
from datetime import datetime
import shutil  # For file operations like delete
import re

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem,
    QLineEdit, QFrame, QMenu, QSizePolicy
)
from PySide6.QtCore import Qt, QSize, Signal, QEvent
from PySide6.QtGui import QIcon
from Utils.Utils import utils


# ============================================================================
# Utility helpers (filename sanitization and small helpers)
# These functions are placed near file-operation functions for easier maintenance.
# ============================================================================

<<<<<<< HEAD
# ----------------------------------------------------------------------------
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
def sanitize_filename(name: str, max_len: int = 200) -> str:
    """
    Produce a filesystem-safe filename stem from an arbitrary title.
    - Removes characters not allowed on typical filesystems: / \\ : * ? " < > |.
    - Trims length and strips trailing dots/spaces.
    - This preserves human readable titles but ensures files are safe to create.
    NOTE: This is used only for filenames; UI labels remain unchanged.
    """
    if not isinstance(name, str):
        name = str(name)

    # Replace known forbidden characters with underscore
    cleaned = re.sub(r'[\/\\\:\*\?\"\<\>\|]', '_', name)

    # Collapse whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    # Trim to max_len
    if len(cleaned) > max_len:
        cleaned = cleaned[:max_len].rstrip()

    # Remove trailing dots/spaces (Windows quirk)
    cleaned = cleaned.rstrip(' .')

    # If empty after cleaning, fallback to timestamp
    if not cleaned:
        cleaned = datetime.now().strftime("Chat_%Y-%m-%d_%H-%M-%S")

    return cleaned


# ============================================================================
# Chat Item Widget
# ----------------------------------------------------------------------------
# A single row representing a chat inside the history list.
# Supports inline renaming (Enter or focus out commits) and uses the parent
# side-panel to synchronize rename on disk.
# ============================================================================

class ChatItemWidget(QWidget):
    """
    A QWidget representing a single chat item in the history list.
    Supports inline renaming like folders:
    - Click outside or lose focus finishes editing
    - Press Enter finishes editing
    - Transparent background
    """
<<<<<<< HEAD
    # -------------------------------------------------------------------------
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    def __init__(self, chat_title, icon_path, parent_listwidget_item, folder_name, history_list, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.parent_item = parent_listwidget_item
        self.folder_name = folder_name
        self.history_list = history_list
        self.editor = None

        self.setStyleSheet("background-color: transparent;")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 0, 0, 0)
        layout.setSpacing(6)

        # Icon
        self.icon = QLabel()
        self.icon.setPixmap(QIcon(icon_path).pixmap(16, 16))
        self.icon.setStyleSheet("background-color: transparent;")
        layout.addWidget(self.icon)

        # Title label
        self.label = QLabel(chat_title)
        self.label.setStyleSheet("color:#333; background-color: transparent;")
        layout.addWidget(self.label)
        layout.addStretch()

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    # Inline rename workflow
    # -------------------------------------------------------------------------
    def start_rename(self):
        """
        Replace the static chat title label with a `QLineEdit` so the user can
        rename the chat inline. This method only creates the editor if it is not
        already active, configures styling, and wires up the confirmation hooks.
        """
=======
    # ---------------- Inline rename ----------------
    def start_rename(self):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if self.editor:
            return

        self.editor = QLineEdit(self.label.text(), self)
        self.editor.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.editor.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: 1px solid #0078D4;
                border-radius: 4px;
                padding-left: 4px;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:focus { border: 1px solid #0078D4; }
        """)
        self.editor.setFixedHeight(self.label.height())
        self.editor.setFixedWidth(max(self.label.width() + 60, 120))
        self.editor.move(self.label.pos())
        self.editor.show()
        self.editor.setFocus()
        self.editor.selectAll()

        self.layout().replaceWidget(self.label, self.editor)
        self.label.hide()

        # Install event filter
        self.editor.installEventFilter(self)

        # Enter pressed
        self.editor.returnPressed.connect(self.finish_rename)

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    # Inline rename commit
    # -------------------------------------------------------------------------
    def finish_rename(self):
        """
        Commit the inline rename by synchronizing the in-memory data, the UI
        label, and—when possible—the backing JSON file on disk.
        Steps performed:
          1. Update `QListWidgetItem` user role metadata.
          2. Update the visual label so the list reflects the new title.
          3. Ask the parent side panel to rename the persisted chat file.
=======
    def finish_rename(self):
        """
        Commit rename action:
        - Update UI label
        - Update QListWidgetItem user role data
        - Ask parent Side Panel to rename underlying .json on disk (if exists)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        """
        if not self.editor:
            return

        old_title = self.label.text()
        new_title = self.editor.text().strip() or old_title

        # Update memory/UI first
        self.parent_item.setData(Qt.UserRole, (self.folder_name, new_title))
        self.label.setText(new_title)

        # Notify Side Panel to rename the file on disk (if applicable).
        # We rely on the QListWidget's parent being the Slide_Side_Panel instance.
        try:
            side_panel = self.history_list.parent()
            # Check attribute presence for safety
            if hasattr(side_panel, "rename_chat"):
                # Use sanitized filename for disk rename, but keep UI label unchanged.
                side_panel.rename_chat(self.parent_item, old_title, new_title)
            else:
                # If the method doesn't exist, just print a warning and continue.
                print("[WARN] slide side panel has no rename_chat method — skipping disk rename.")
        except Exception as e:
            print(f"[WARN] rename_chat call failed: {e}")

        self.editor.deleteLater()
        self.editor = None
        self.label.show()

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    # Event filter for inline editor
    # -------------------------------------------------------------------------
    def eventFilter(self, obj, event):
        """
        Close the inline rename editor whenever focus is lost or when the user
        clicks outside of the editor region.
        """
=======
    # ---------------- Event Filter ----------------
    def eventFilter(self, obj, event):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if obj == self.editor:
            if event.type() == QEvent.FocusOut or \
               (event.type() == QEvent.MouseButtonPress and not self.editor.rect().contains(event.pos())):
                self.finish_rename()
        return super().eventFilter(obj, event)


# ============================================================================
# Collapsible Folder Widget
# ----------------------------------------------------------------------------
# Simple folder header that can be expanded/collapsed and supports inline rename.
# ============================================================================

class CollapsibleFolder(QWidget):
    toggled = Signal(bool)

<<<<<<< HEAD
    # -------------------------------------------------------------------------
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    def __init__(self, name: str, parent=None):

        super().__init__(parent)

        self.setObjectName("CollapsibleFolder")

        self.name = name
        self.is_expanded = True
        self.editor = None

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.setSpacing(12)

        # Icon
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(18, 18)
        layout.addWidget(self.icon_label)

        # Folder name label
        self.name_label = QLabel(name)
        self.name_label.setStyleSheet("font-weight:500; background:transparent;")
        self.name_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        layout.addWidget(self.name_label)
        layout.addStretch()

        # Hover / Press style
        self.setStyleSheet("""
            #CollapsibleFolder {
                background-color: transparent;
                border-radius: 6px;
            }
            #CollapsibleFolder:hover {
                background-color: #e9ecef;
            }
            #CollapsibleFolder:pressed {
                background-color: #d0d0d0;
            }
        """)

        self.update_icon()

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    # Toggle expand / collapse state
    # -------------------------------------------------------------------------
=======
    # ---------------- Toggle expand/collapse ----------------
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_expanded = not self.is_expanded
            self.update_icon()
            self.toggled.emit(self.is_expanded)
        super().mousePressEvent(event)

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    # Refresh folder icon based on state
    # -------------------------------------------------------------------------
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    def update_icon(self):
        closed = utils.resource_path("images/WIN11-Icons/icons8-folder-100.png")
        opened = utils.resource_path("images/WIN11-Icons/icons8-opened-folder-100.png")
        icon_path = opened if self.is_expanded else closed
        self.icon_label.setPixmap(QIcon(icon_path).pixmap(18, 18))

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    # Inline rename workflow
    # -------------------------------------------------------------------------
    def start_rename(self):
        """
        Allow the folder header to be renamed inline by temporarily swapping the
        `QLabel` for a styled `QLineEdit`.
        """
=======
    # ---------------- Inline rename ----------------
    def start_rename(self):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if self.editor:
            return
        self.editor = QLineEdit(self.name_label.text(), self)
        self.editor.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.editor.setFixedHeight(20)
        self.editor.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #0078D4;
                border-radius: 4px;
                padding-left: 6px;
                color: #333;
                font-size: 14px;
                font-weight: 500;
            }
            QLineEdit:focus {
                border: none;
                outline: none;
            }
        """)
        min_width = max(self.name_label.width() + 60, 180)
        self.editor.setFixedWidth(min_width)
        self.editor.move(self.name_label.pos())
        self.editor.show()
        self.editor.setFocus()
        self.editor.selectAll()
        self.editor.installEventFilter(self)
        self.editor.returnPressed.connect(self.finish_inline_edit)
        self.name_label.hide()

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    # Inline rename commit
    # -------------------------------------------------------------------------
    def finish_inline_edit(self):
        """
        Persist the inline rename changes by updating both the widget label and
        the cached folder name.
        """
=======
    def finish_inline_edit(self):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if not self.editor:
            return
        new_name = self.editor.text().strip()
        if new_name:
            self.name_label.setText(new_name)
            self.name = new_name
        self.editor.deleteLater()
        self.editor = None
        self.name_label.show()

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    # Event filter for rename editor
    # -------------------------------------------------------------------------
    def eventFilter(self, obj, event):
        """
        Close the rename editor whenever the input loses focus or the user
        clicks outside of the editing rectangle.
        """
=======
    def eventFilter(self, obj, event):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if obj == self.editor:
            if event.type() == QEvent.FocusOut:
                self.finish_inline_edit()
            elif event.type() == QEvent.MouseButtonPress:
                if not self.editor.rect().contains(event.pos()):
                    self.finish_inline_edit()
        return super().eventFilter(obj, event)


# ============================================================================
# Slide Side Panel (Main Class)
# ----------------------------------------------------------------------------
# Responsible for:
# - UI layout of left side panel
# - Loading chat folders and chat items from disk
# - Adding / deleting / renaming chat files (UI + disk sync)
# ============================================================================

class Slide_Side_Panel(QWidget):
<<<<<<< HEAD
    """
    A composite widget that manages the full lifecycle of chat folders and chat
    entries on the left side panel. It keeps UI state, synchronizes with the
    on-disk history directory, and exposes Qt signals for the host window.
    """
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

    chat_clicked = Signal(str, str)
    chat_item_double_clicked = Signal(str, str)
    toggle_requested = Signal()
    new_chat_requested = Signal()
    show_settings_requested = Signal()

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    def __init__(self, parent=None, storage_root: str = "ChatHistory"):
        """
        Initialize the panel, wiring up internal state containers, default UI
        sizing, and eagerly loading any persisted chat history from disk.
        """
=======
    def __init__(self, parent=None, storage_root: str = "ChatHistory"):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

        super().__init__(parent)

        self.side_panel_width = 280
        self.is_visible = True
        self.drag_handle = getattr(parent, 'drag_handle', None)
        self.drag_start_x = 0
        self.start_width = self.side_panel_width
        self.full_width = self.side_panel_width

        # Folder & Chat
        self.chats = {}
        self.folders = {}
        self.chat_counter = 0
        self.folder_counter = 0
        self.active_folder = None  # <-- active folder name (string)

        # storage
        self.storage_root = Path(storage_root)
        self.storage_root.mkdir(parents=True, exist_ok=True)

        self.setStyleSheet("""
            QWidget { background-color: #f8f9fa;}
            QPushButton { background: transparent; border: none; padding: 10px 16px; text-align: left; font-size: 14px; border-radius: 8px; }
            QPushButton:hover { background: #e9ecef; }
            QListWidget { border: none; }
            QListWidget::item { padding: 6px 12px; border-radius: 6px; margin: 1px 0; }
            QListWidget::item:hover { background: #e9ecef; }
            QListWidget::item:selected { background-color: #f0f0f0; color: #333; }
            QLabel#token { color: #666; }
            QFrame#divider { background: #ddd; }
            /* the vertical scroll bar */
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;                    /* the width of the scroll bar */
                margin: 0px 0px 14px 0;   /* top right bottom left */
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 0, 0, 0.4);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 0, 0, 0.6);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                width: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            /* the horizontal scroll bar (optional) */
            QScrollBar:horizontal {
                border: none;
                background: rgba(0, 0, 0, 0.1);
                height: 8px;
                margin: 0 4px 0 4px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(0, 0, 0, 0.4);
                min-width: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal:hover {
                background: rgba(0, 0, 0, 0.6);
            }
        """)

        # ---------------- UI Init ----------------
        self.init_ui()

        # ---------------- Load previous history ----------------
        self.load_chat_history()



<<<<<<< HEAD
    # -------------------------------------------------------------------------
    def init_ui(self):
        """
        Build the full vertical layout for the side panel including toolbar
        buttons, chat history list, and the token statistics section.
        """
        # ---------------- UI Build ----------------
=======
    # ---------------- UI Build ----------------
    def init_ui(self):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # Top Buttons
        top = QWidget()
        top_layout = QVBoxLayout(top)
        top_layout.setContentsMargins(0, 2, 0, 2)
        top_layout.setSpacing(6)

        # ---------------- Create Icon Button ----------------
        def create_icon_button(text, icon_path, object_name, callback):

            btn = QPushButton()
            btn.setObjectName(object_name)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(callback)

            layout_btn = QHBoxLayout(btn)
            layout_btn.setContentsMargins(12,0,12,0)
            layout_btn.setSpacing(10)

            icon_label = QLabel()
            icon_label.setPixmap(QIcon(utils.resource_path(icon_path)).pixmap(20,20))
            icon_label.setAlignment(Qt.AlignVCenter)
            icon_label.setStyleSheet("background: transparent;")
            layout_btn.addWidget(icon_label)

            text_label = QLabel(text)
            text_label.setStyleSheet("color: #333; background: transparent;")
            text_label.setAlignment(Qt.AlignVCenter)
            layout_btn.addWidget(text_label)
            layout_btn.addStretch(1)

            btn.inner_text_label = text_label  # for later text update

            btn.setStyleSheet(f"""
                QPushButton#{object_name} {{
                    border: none;
                    border-radius: 8px;
                    text-align: left;
                    height: 12px;
                }}
            """)
            return btn


        # Create Buttons
        self.btn_new_chat  = create_icon_button(
            "New chat",
            "images/WIN11-Icons/icons8-chat-room-100.png",
            "btn_new_chat",
            self.on_new_chat)
        self.btn_new_folder = create_icon_button(
            "New folder",
            "images/WIN11-Icons/icons8-new-folder-100.png",
            "btn_new_folder",
            self.on_new_folder)
        self.btn_settings = create_icon_button(
            "Settings",
            "images/WIN11-Icons/icons8-settings-100.png",
            "btn_settings",
            lambda: self.show_settings_requested.emit())

        top_layout.addWidget(self.btn_new_folder)
        top_layout.addWidget(self.btn_new_chat)
        top_layout.addWidget(self.btn_settings)
        top_layout.addStretch()
        layout.addWidget(top)

        layout.addWidget(self.create_divider())

        # Chat History Label
        self.history_label = QLabel("Chat History")
        self.history_label.setStyleSheet("font-weight: bold;")
        self.history_label.setObjectName("chat_history_title")
        self.history_label.setFixedHeight(28)
        self.history_label.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        self.history_label.setContentsMargins(16,0,0,0)
        layout.addWidget(self.history_label)

        # Chat History List
        self.history_list = QListWidget()
        self.history_list.setContextMenuPolicy(Qt.CustomContextMenu)
<<<<<<< HEAD
        self.history_list.setSelectionMode(QListWidget.ExtendedSelection)  # Allow Shift/Ctrl multi-select
=======
        self.history_list.setSelectionMode(QListWidget.ExtendedSelection)  # 支持 Shift / Ctrl 多选
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.history_list.customContextMenuRequested.connect(self.show_context_menu)
        self.history_list.itemClicked.connect(self.on_chat_item_clicked)
        self.history_list.itemDoubleClicked.connect(self.on_chat_item_double_clicked)
        layout.addWidget(self.history_list, 1)

        # Check the folder of HistoryChat, if empty, create one default folder
        if not any(self.storage_root.iterdir()):

            # create default folder if none exists
            self.create_folder()  


        layout.addWidget(self.create_divider())

        # Stats Container
        stats = QWidget()
        stats_layout = QVBoxLayout(stats)
        stats_layout.setContentsMargins(16, 12, 16, 12)
        stats_layout.setSpacing(6)

<<<<<<< HEAD
        # Define a compact data structure: (attribute prefix, label text).
        # This lets us auto-create attributes such as self.current_tokens_title.
=======
        # 定义数据结构： (变量前缀, 显示标题)
        # 这样会自动生成: self.current_tokens_title, self.current_tokens_value 等变量
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        stats_metrics = [
            ("current_tokens", "Tokens"),
            ("today_tokens",   "Today"),
            ("total_tokens",   "Total")
        ]

<<<<<<< HEAD
        # Create one row per metric
=======
        # 循环创建 3 行
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        for prefix, title_text in stats_metrics:

            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(0, 0, 0, 0)
            
<<<<<<< HEAD
            # 1. Create title label
=======
            # 1. 创建标题 Label
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            lbl_title = QLabel(f"{title_text}:")
            lbl_title.setStyleSheet("font-weight: bold; color: #666;")
            lbl_title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            
<<<<<<< HEAD
            # 2. Create value label
=======
            # 2. 创建数值 Label
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            lbl_value = QLabel("0")
            lbl_value.setStyleSheet("color: #333;")
            lbl_value.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

<<<<<<< HEAD
            # 3. Attach labels to the row layout
            row_layout.addWidget(lbl_title)
            row_layout.addWidget(lbl_value)
            row_layout.addStretch()  # Keep rows left-aligned

            # 4. Add the row into the stats container
            stats_layout.addLayout(row_layout)

            # 5. Dynamically bind references so translation / updates are easy
            setattr(self, f"{prefix}_title", lbl_title)
            setattr(self, f"{prefix}_value", lbl_value)

        # Add a spacer to push everything upward
=======
            # 3. 添加到行布局
            row_layout.addWidget(lbl_title)
            row_layout.addWidget(lbl_value)
            row_layout.addStretch()  # 靠左对齐

            # 4. 添加行到总布局
            stats_layout.addLayout(row_layout)

            # 5. 【关键】动态绑定变量名，方便后续更新和翻译
            # 相当于执行了: self.current_tokens_title = lbl_title
            # 相当于执行了: self.current_tokens_value = lbl_value
            setattr(self, f"{prefix}_title", lbl_title)
            setattr(self, f"{prefix}_value", lbl_value)

        # 底部弹簧，把内容顶上去
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        stats_layout.addStretch()

        layout.addWidget(stats)

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    def create_divider(self):
        """
        Return a subtle gradient divider frame to visually separate sections
        within the panel layout.
        """
=======


    # ---------------- Divider ----------------
    def create_divider(self):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        line = QFrame()
        line.setObjectName("divider")
        line.setFixedHeight(3)
        line.setStyleSheet("""
            QFrame#divider {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0,0,0,20),
                    stop:0.5 rgba(0,0,0,40),
                    stop:1 rgba(0,0,0,20));
                border-radius:1px;
            }
        """)
        return line

    # =========================================================================
    # Folder / Chat Creation / UI management
    # =========================================================================
<<<<<<< HEAD
    def create_folder(self, name=None):
        """
        Create a folder header row inside the list widget and register internal
        bookkeeping so future chats can be inserted beneath that folder.
        When `name` is omitted, a human-friendly default is generated.
        """
=======

    def create_folder(self, name=None):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if name is None:
            self.folder_counter += 1
            name = f"Default folder" if self.folder_counter==1 else f"New folder {self.folder_counter-1}"

        folder_widget = CollapsibleFolder(name)
        item = QListWidgetItem()
        item.setSizeHint(QSize(0,36))
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item.setData(Qt.UserRole, (name,""))
        self.history_list.addItem(item)
        self.history_list.setItemWidget(item, folder_widget)

        self.folders[name] = {"widget":folder_widget,"item":item,"items":[],"expanded":True}

        folder_widget.toggled.connect(lambda expanded, fw=folder_widget: self.on_folder_toggled(fw, expanded))

        # Set first created folder as active if none
        if not self.active_folder:
            self.active_folder = name

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    def on_folder_toggled(self, folder_widget, expanded):
        """
        Expand or collapse all chat rows under the provided folder widget and
        persist the expanded state for subsequent refreshes.
        """
=======
    def on_folder_toggled(self, folder_widget, expanded):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        folder_name = None
        for k,v in self.folders.items():
            if v["widget"] is folder_widget:
                folder_name = k
                break
        if folder_name is None: return
        folder = self.folders[folder_name]
        folder["expanded"] = expanded
        for chat_item in folder["items"]:
            chat_item.setHidden(not expanded)

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    def on_chat_item_clicked(self,item):
        """
        Handle single-click events on the list widget. Folder rows update the
        active folder selection, while chat rows emit `chat_clicked`.
        """
=======
    # ---------------- Chat / Folder Click ----------------
    def on_chat_item_clicked(self,item):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        data = item.data(Qt.UserRole)
        if not data:
            return
        folder_name, chat_title = data
        if chat_title == "":
            # Clicked a folder → set as active and avoid selecting (no blue highlight)
            self.active_folder = folder_name
            # clear selection so it won't appear as a selected chat
            self.history_list.clearSelection()
        else:
            # Clicked a chat item → emit selection (do not change active folder)
            self.chat_clicked.emit(folder_name, chat_title)


<<<<<<< HEAD
    # -------------------------------------------------------------------------
    def on_chat_item_double_clicked(self, item):
        """
        Emit a stronger signal whenever a chat row is double-clicked so the main
        window can open the conversation immediately.
        """

        folder_name, chat_title = item.data(Qt.UserRole)
        if chat_title:  # Guard against folder headers
            self.chat_item_double_clicked.emit(folder_name, chat_title)


    # -------------------------------------------------------------------------
    def on_new_chat(self):
        """
        Ensure that a folder is active (creating or reusing one when necessary)
        and emit the `new_chat_requested` signal so the host view can reset the
        chat editor area.
        """
=======
    def on_chat_item_double_clicked(self, item):

        folder_name, chat_title = item.data(Qt.UserRole)
        if chat_title:  # 确保不是点击的文件夹
            self.chat_item_double_clicked.emit(folder_name, chat_title)


    # ---------------- New Chat ----------------
    def on_new_chat(self):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        # Ensure there is an active folder; if not, choose the last folder
        if not self.active_folder:
            if self.folders:
                # choose the last folder in insertion order
                self.active_folder = list(self.folders.keys())[-1]
            else:
                # create a default folder
                self.create_folder()

        # Notify main window to clear current chat UI and reset state
        self.new_chat_requested.emit()


    # =========================================================================
    # Save / Add Chat UI + Disk (save_json flag controls whether to write file)
    # =========================================================================
    def save_chat_to_folder(self, folder_name, title=None, save_json=True):
        """
<<<<<<< HEAD
        Insert a chat row under a folder, optionally persisting an empty JSON
        skeleton on disk. Returns the created `QListWidgetItem` so callers can
        trigger additional behavior (e.g., inline rename).

        Args:
            folder_name: Target folder name.
            title: Optional explicit chat title; defaults to timestamp.
            save_json: When True, write a chat JSON file immediately.
=======
        Add a chat entry under folder_name in the side panel list.
        If save_json=True, also save a JSON file on disk.
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        """
        folder = self.folders.get(folder_name)
        if not folder:
            self.create_folder(folder_name)
            folder = self.folders[folder_name]

        self.chat_counter += 1
        now = datetime.now()
        time_str = now.strftime("%Y-%m-%d %H-%M-%S")
        chat_title = title if title else f"Chat {time_str}"

        # ---------------- Add to UI ----------------
        item = QListWidgetItem()
        item.setSizeHint(QSize(0,36))
        item.setData(Qt.UserRole, (folder_name, chat_title))
        chat_widget = ChatItemWidget(
            chat_title=chat_title,
            icon_path=utils.resource_path("images/WIN11-Icons/icons8-chat-100.png"),
            parent_listwidget_item=item,
            folder_name=folder_name,
            history_list=self.history_list
        )
        row = self.history_list.row(folder["item"]) + len(folder["items"]) + 1
        self.history_list.insertItem(row, item)
        self.history_list.setItemWidget(item, chat_widget)
        folder["items"].append(item)
        item.rename_chat_inline = chat_widget.start_rename

        # ---------------- Save JSON to disk ----------------
        if save_json:
            folder_path = self.storage_root / folder_name
            folder_path.mkdir(exist_ok=True)
            # Use sanitized filename for disk safety
            safe_stem = sanitize_filename(chat_title)
            chat_file = folder_path / f"{safe_stem}.json"
            chat_data = {"title": chat_title, "messages": []}
            try:
                with open(chat_file, "w", encoding="utf-8") as f:
                    json.dump(chat_data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Failed to save chat {chat_title}: {e}")

        self.update_tokens(self.chat_counter*100, self.chat_counter*0.002, 0.002)
        return item


<<<<<<< HEAD
    # -------------------------------------------------------------------------
    # Right-click menu actions: Rename, Delete, New chat, New folder, Settings
    # -------------------------------------------------------------------------
    def show_context_menu(self, pos):
        """
        Build a contextual menu based on the current selection (single folder,
        single chat, or multi-selection) and wire up the relevant actions.
        """
=======
    # ---------------- Folder / Chat Menu ----------------
    # Riggt click menu actions: Rename, Delete, New chat, New folder, Settings
    def show_context_menu(self, pos):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        
        selected_items = self.get_selected_items()
        if not selected_items:
            return

        menu = QMenu()
        menu.setContentsMargins(0,4,0,4)  # Left, Top, Right, Bottom

        # Style: white background, hover light gray, rounded corners
        menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;      /* white background */
                color: #333333;                 /* dark text */
                border: 1px solid #cccccc;      /* light border */
                border-radius: 8px;             /* rounded corners */
                padding: 4px;
            }
            QMenu::item {
                background-color: transparent;
                padding: 6px 24px 6px 24px;     /* Adjust padding for comfort */
                border-radius: 6px;
                margin: 2px 4px;                /* Add margin for rounded look */
            }
            /* This controls the hover color */
            QMenu::item:selected {
                background-color: #f0f0f0;      /* hover light gray */
                color: #000000;
            }
            QMenu::separator {
                height: 1px;
                background: #dddddd;
                margin: 4px 0;
            }
        """)
        
<<<<<<< HEAD
        # Only allow delete when multiple items are selected
=======
        # 多选时只允许删除，不允许重命名（或只重命名第一个）
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if len(selected_items) == 1:
            item = selected_items[0]
            folder_name, chat_title = item.data(Qt.UserRole)
            if chat_title == "":
                menu.addAction("Rename", lambda: self.rename_folder_inline(item))
                menu.addAction("Delete", lambda: self.delete_folder(item))
            else:
                menu.addAction("Rename", lambda: item.rename_chat_inline())
                menu.addAction("Delete", lambda: self.delete_chat(item))
        else:
<<<<<<< HEAD
=======
            # 多选删除
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            menu.addAction("Delete", lambda: self.delete_selected_items(selected_items))

        menu.addSeparator()
        menu.addAction("New chat", self.on_new_chat)
        menu.addAction("New folder", self.on_new_folder)
        menu.addAction("Settings", self.show_settings_requested.emit)
        menu.exec(self.history_list.mapToGlobal(pos))



<<<<<<< HEAD
    # -------------------------------------------------------------------------
    def get_selected_items(self):
        """
        Convenience helper to fetch the currently selected list widget items.
        """
        return self.history_list.selectedItems()


    # -------------------------------------------------------------------------
    def delete_selected_items(self, items):
        """
        Iterate through a collection of selected items and dispatch to the
        specific folder/chat delete handlers.
        """
=======
    def get_selected_items(self):
        """Return list of currently selected QListWidgetItems."""
        return self.history_list.selectedItems()


    def delete_selected_items(self, items):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        for item in items:
            folder_name, chat_title = item.data(Qt.UserRole)
            if chat_title == "":
                self.delete_folder(item)
            else:
                self.delete_chat(item)

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    # Folder Rename
    # -------------------------------------------------------------------------
    def rename_folder_inline(self,item):
        """
        Kick off the inline rename workflow for a folder header and ensure the
        resulting name change propagates back through `update_folder_name`.
        """
=======
    # ---------------- Folder Rename ----------------
    def rename_folder_inline(self,item):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        folder_name,_ = item.data(Qt.UserRole)
        folder_widget = self.folders[folder_name]["widget"]
        folder_widget.start_rename()
        if folder_widget.editor:
            # when editingFinished fires, folder_widget.name has been updated in finish_inline_edit
            folder_widget.editor.editingFinished.connect(lambda fw=folder_widget,it=item,old=folder_name: self.update_folder_name(it, old, fw.name))

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    # Stats
    # -------------------------------------------------------------------------
    def format_number(self, num):
        """
        Humanize large numeric values using k/M suffixes for compact display.
        """
=======
    # ---------------- Stats ----------------
    def format_number(self, num):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}k"
        return str(num)


<<<<<<< HEAD
    # -------------------------------------------------------------------------
    def update_tokens(self, tokens, total, today):
        """
        Refresh the token statistics labels with the provided numeric values.
        """
=======
    def update_tokens(self, tokens, total, today):
        # Update token stats
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.current_tokens_value.setText(f"{tokens}")
        self.total_tokens_value.setText(f"{self.format_number(total)}")
        self.today_tokens_value.setText(f"{self.format_number(today)}")


<<<<<<< HEAD
    # -------------------------------------------------------------------------
    def refresh_chat_list(self):
        """
        Iterate through folders/chats and trigger lightweight repaints so custom
        widgets pick up any style or icon changes.
=======
    def refresh_chat_list(self):
        """
        Refresh the chat history UI.
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        """
        for folder_name, folder in self.folders.items():

            folder["widget"].update_icon()  # update folder icon
            for chat_item in folder["items"]:
                widget = self.history_list.itemWidget(chat_item)
                if widget:
<<<<<<< HEAD
                    widget.repaint()  # Use repaint() to force immediate refresh
=======
                    widget.repaint()  # <-- 用 repaint() 而不是 update()
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6



    # =========================================================================
    # Load Chat History from disk into the Side Panel
    # - supports old-format (list) and new-format (dict with 'title' + 'messages')
    # =========================================================================
    def load_chat_history(self):
        """
        Load all folders and chats from ChatHistory directory.
        Supports both old-style JSON (list of messages) and new-style (dict with title + messages).
        """
        for folder_path in sorted(self.storage_root.iterdir()):
            if not folder_path.is_dir():
                continue
            folder_name = folder_path.name
            self.create_folder(folder_name)
            folder = self.folders[folder_name]

            for chat_file in sorted(folder_path.glob("*.json")):
                try:
                    with open(chat_file, "r", encoding="utf-8") as f:
                        chat_data = json.load(f)

                    # ---------------- Detect format ----------------
                    if isinstance(chat_data, dict):
                        chat_title = chat_data.get("title", chat_file.stem)
                        messages = chat_data.get("messages", [])
                    elif isinstance(chat_data, list):
                        # old format: list of messages
                        chat_title = chat_file.stem
                        messages = chat_data
                        # wrap into dict for compatibility
                        chat_data = {"title": chat_title, "messages": messages}
                    else:
                        print(f"[WARN] Unknown chat file format: {chat_file}")
                        continue

                    # ---------------- Add to side panel ----------------
                    item = self.save_chat_to_folder(folder_name, title=chat_title, save_json=False)
                    # optionally attach loaded messages to the item for later display
                    item.chat_messages = messages
                    print(f"[INFO] Loaded chat: {chat_title} ({len(messages)} messages)")

                except Exception as e:
                    print(f"[ERROR] Failed to load {chat_file}: {e}")


    # =========================================================================
    # Disk rename helper — main fix point
    # - This method performs a safe rename of the underlying JSON file when a chat
    #   is renamed in the UI. It attempts to find the existing file (old_title)
    #   and rename it to new_title (sanitized for filename safety).
    # =========================================================================
    def rename_chat(self, listwidget_item: QListWidgetItem, old_title: str, new_title: str):
        """
        Attempt to rename the underlying JSON file for this chat.
        - listwidget_item: the QListWidgetItem representing this chat row.
        - old_title: previous visible title (UI)
        - new_title: new visible title (UI)
        This function tries a few heuristics:
         1. Exact match: {old_title}.json
         2. Sanitized match: sanitize_filename(old_title) + .json
         3. Case-insensitive / normalized search inside folder for closest stem
        """
        try:
            folder_name, _ = listwidget_item.data(Qt.UserRole)
            folder_path = self.storage_root / folder_name
            if not folder_path.exists():
                # No folder on disk — nothing to rename
                return

            # Candidate file names to check (exact UI string and sanitized)
            candidates = []
            candidates.append(folder_path / f"{old_title}.json")
            candidates.append(folder_path / f"{sanitize_filename(old_title)}.json")

            # Add also possible JSON files in folder (fallback search)
            all_jsons = list(folder_path.glob("*.json"))

            # Try exact or sanitized matches first
            chosen = None
            for c in candidates:
                if c.exists():
                    chosen = c
                    break

            # If none found, attempt reasonable fallback: case-insensitive / normalized matching
            if chosen is None:
                norm_new = sanitize_filename(new_title).lower()
                for p in all_jsons:
                    stem_norm = sanitize_filename(p.stem).lower()
                    if stem_norm == norm_new or stem_norm == sanitize_filename(old_title).lower():
                        chosen = p
                        break

            # Final fallback: try match by title inside JSON 'title' field
            if chosen is None:
                for p in all_jsons:
                    try:
                        with open(p, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            if isinstance(data, dict) and data.get("title", "") == old_title:
                                chosen = p
                                break
                    except Exception:
                        continue

            if chosen:
                # Compose new filename using sanitized stem
                new_stem = sanitize_filename(new_title)
                target = folder_path / f"{new_stem}.json"

                # If target already exists and it's the same as chosen, nothing to do
                if target.exists() and target.samefile(chosen):
                    return

                # If target exists but is different, we choose a safe fallback by appending timestamp
                if target.exists() and not target.samefile(chosen):
                    ts = datetime.now().strftime("%Y%m%d%H%M%S")
                    target = folder_path / f"{new_stem}_{ts}.json"

                try:
                    chosen.rename(target)
                    print(f"[INFO] Renamed chat file: {chosen} -> {target}")
                except Exception as e:
                    print(f"[ERROR] Failed to rename chat file {chosen} -> {target}: {e}")
            else:
                # No file found to rename — this is OK (maybe it was never saved to disk)
                print(f"[INFO] No underlying chat file found for rename: '{old_title}' in folder '{folder_name}'")
        except Exception as e:
            print(f"[ERR] rename_chat general failure: {e}")


    # =========================================================================
    # Delete Folder / Chat operations
    # =========================================================================

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    def on_new_folder(self):
        """
        Create a brand-new folder both in the UI list and on disk, then mark it
        as the active folder for immediate use.
        """
=======
    def on_new_folder(self):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.folder_counter += 1
        folder_name = f"New folder {self.folder_counter}"
        self.create_folder(folder_name)
        self.active_folder = folder_name

        # Create folder on disk
        folder_path = self.storage_root / folder_name
        folder_path.mkdir(exist_ok=True)

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    # Update Folder Name
    # -------------------------------------------------------------------------
    def update_folder_name(self,item,old_name,new_name):
        """
        Apply a folder rename by updating in-memory dictionaries, list widget
        items, and the on-disk directory if it exists.
        """
=======
    # ---------------- Update Folder Name ----------------
    def update_folder_name(self,item,old_name,new_name):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if not new_name or new_name==old_name: return
        if new_name in self.folders: return

        # Rename folder in memory
        self.folders[new_name] = self.folders.pop(old_name)
        self.folders[new_name]["item"].setData(Qt.UserRole,(new_name,""))
        for chat_item in self.folders[new_name]["items"]:
            fn, title = chat_item.data(Qt.UserRole)
            chat_item.setData(Qt.UserRole, (new_name, title))
        if self.active_folder == old_name:
            self.active_folder = new_name

        # Rename folder on disk
        old_path = self.storage_root / old_name
        new_path = self.storage_root / new_name
        if old_path.exists():
            try:
                old_path.rename(new_path)
            except Exception as e:
                print(f"Failed to rename folder {old_name} -> {new_name}: {e}")

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    # Delete Folder
    # -------------------------------------------------------------------------
    def delete_folder(self, item):
        """
        Remove a folder header, all of its child chats, and the corresponding
        directory on disk. Also keeps the active folder pointer in sync.
        """
=======
    # ---------------- Delete Folder ----------------
    def delete_folder(self, item):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        folder_name, _ = item.data(Qt.UserRole)
        if folder_name not in self.folders:
            return
        folder = self.folders.pop(folder_name)

        # remove all chat items under the folder
        for chat_item in folder["items"]:
            self.history_list.takeItem(self.history_list.row(chat_item))
        # remove folder header
        self.history_list.takeItem(self.history_list.row(folder["item"]))

        # Delete folder on disk
        folder_path = self.storage_root / folder_name
        if folder_path.exists():
            import shutil
            try:
                shutil.rmtree(folder_path)
            except Exception as e:
                print(f"Failed to delete folder {folder_name}: {e}")

        # Update active folder
        if self.active_folder == folder_name:
            self.active_folder = list(self.folders.keys())[-1] if self.folders else None

<<<<<<< HEAD
    # -------------------------------------------------------------------------
    # Delete Chat
    # -------------------------------------------------------------------------
    def delete_chat(self, item):
        """
        Remove a single chat row and delete its persisted JSON file if present.
        """
=======
    # ---------------- Delete Chat ----------------
    def delete_chat(self, item):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        folder_name, chat_title = item.data(Qt.UserRole)
        folder = self.folders.get(folder_name)
        if not folder or item not in folder["items"]:
            return
        folder["items"].remove(item)
        self.history_list.takeItem(self.history_list.row(item))

        # Delete JSON file on disk
        chat_file = self.storage_root / folder_name / f"{chat_title}.json"
        # Try sanitized filename deletion as well (safer)
        chat_file_alt = self.storage_root / folder_name / f"{sanitize_filename(chat_title)}.json"
        try:
            if chat_file.exists():
                chat_file.unlink()
            elif chat_file_alt.exists():
                chat_file_alt.unlink()
        except Exception as e:
            print(f"Failed to delete chat {chat_title}: {e}")


    #-----------------------------------------------------------------------------
    # Update UI texts for localization
<<<<<<< HEAD
    #-----------------------------------------------------------------------------
    def update_ui_texts(self, lang_manager):
        """
        Refresh every translatable label or tooltip on the side panel using the
        provided language manager.
=======
    def update_ui_texts(self, lang_manager):
        """
        更新侧边栏按钮的文字
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        """
        if not lang_manager:
            return

<<<<<<< HEAD
        # 1. Update the "New Chat" button label and tooltip
=======
        # 1. 更新 "New Chat" 按钮
        # 注意：这里使用的是我们在 create_icon_button 里绑定的 inner_text_label
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if hasattr(self.btn_new_chat, "inner_text_label"):
            self.btn_new_chat.inner_text_label.setText(lang_manager.get_text("New chat"))
            self.btn_new_chat.setToolTip(lang_manager.get_text("Start a new chat"))

<<<<<<< HEAD
        # 2. Update the "New Folder" button label and tooltip
=======
        # 2. 更新 "New Folder" 按钮
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if hasattr(self.btn_new_folder, "inner_text_label"):
            self.btn_new_folder.inner_text_label.setText(lang_manager.get_text("New folder"))
            self.btn_new_folder.setToolTip(lang_manager.get_text("Create a new folder"))

<<<<<<< HEAD
        # 3. Update the "Settings" button label and tooltip
=======
        # 3. 更新 "Settings" 按钮
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if hasattr(self.btn_settings, "inner_text_label"):
            self.btn_settings.inner_text_label.setText(lang_manager.get_text("Settings"))
            self.btn_settings.setToolTip(lang_manager.get_text("Open settings"))
            
<<<<<<< HEAD
        # 4. Update remaining labels such as the chat history section title
=======
        # 4. 如果你还有其他的 label (比如 "Chat History" 的标题)，也在这里更新
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.history_label.setText(lang_manager.get_text("Chat History"))

        # 5. Token stats labels
        self.current_tokens_title.setText(f"{lang_manager.get_text('Tokens')}:")
        self.total_tokens_title.setText(f"{lang_manager.get_text('Total')}:")
        self.today_tokens_title.setText(f"{lang_manager.get_text('Today')}:")
