#-----------------------------------------------------------------------------------------
# Purpouse: This file contains the BubbleMessage class for chat messages
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-11-23 
#----------------------------------------------------------------------------------------- 

import sys
import re
import io
import base64
import matplotlib
import matplotlib.pyplot as plt
import latex2mathml.converter 
import markdown

from PySide6.QtWidgets import (
    QWidget, QLabel, QTextBrowser, QHBoxLayout, QVBoxLayout, 
    QFrame, QSizePolicy, QPushButton, QApplication, QMenu
)
from PySide6.QtGui import (
    QPixmap, QFont, QTextOption, QTextTable, QTextCursor, 
    QIcon
)
from PySide6.QtCore import Qt, QTimer, Signal, QSize, QByteArray, QMimeData
from Utils.Utils import utils

# ==================================================================================
# SECTION 1: CONFIGURATION & HELPER FUNCTIONS
# ==================================================================================

md_converter = markdown.Markdown(extensions=[
    'fenced_code', 'tables', 'nl2br', 'codehilite'
], extension_configs={
    'codehilite': {'css_class': 'codehilite', 'noclasses': False, 'use_pygments': True}
})

def get_copy_icon():
    return QIcon(utils.resource_path("images/WIN11-Icons/icons8-copy-100.png"))

def latex_to_base64_block(latex_str, font_size=12, dpi=110, max_width_px=800):
    clean_latex = f"${latex_str}$"
    safe_width_px = max(max_width_px, 100)
    temp_fig = plt.figure(figsize=(10, 1), dpi=dpi) 
    temp_ax = temp_fig.add_axes([0, 0, 1, 1]); temp_ax.set_axis_off()
    temp_text = temp_ax.text(0, 0, clean_latex, fontsize=font_size, color='black')
    try:
        temp_fig.canvas.draw()
        bbox = temp_text.get_window_extent(temp_fig.canvas.get_renderer())
        w_in, h_in = bbox.width / dpi, bbox.height / dpi
    except: w_in, h_in = 4, 0.5
    finally: plt.close(temp_fig)

    final_w = max(min(w_in, safe_width_px / dpi), 0.1)
    final_h = max(h_in, 0.1)
    fig = plt.figure(figsize=(final_w, final_h), dpi=dpi)
    fig.text(0.5, 0.5, clean_latex, fontsize=font_size, color='black', ha='center', va='center')
    try:
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=dpi, transparent=True, bbox_inches='tight', pad_inches=0.02)
        plt.close(fig); buf.seek(0)
        img = base64.b64encode(buf.read()).decode('utf-8')
        return (f'<div style="text-align: center; margin: 8px 0;">'
                f'<img src="data:image/png;base64,{img}" style="max-width: 100%; height: auto; vertical-align: middle;" /></div>')
    except: 
        plt.close(fig)
        return "[Error]"

def latex_to_mathml_inline(latex_str):
    try: return latex2mathml.converter.convert(latex_str)
    except: return "[Error]"

def wrap_code_with_table(html):
    table_start = (
        '<table width="100%" bgcolor="#f6f8fa" border="0" cellspacing="0" cellpadding="0" '
        'style="margin: 10px 0; border: 1px solid #d0d7de; border-collapse: separate;">'
        '<tr><td style="padding: 12px; color: #24292f;">'
    )
    table_end = '</td></tr></table>'
    pattern = r'<div class="codehilite">(.*?)</div>'
    return re.sub(pattern, lambda m: f"{table_start}{m.group(1)}{table_end}", html, flags=re.DOTALL)

HTML_WRAPPER = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {{ 
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; 
            font-size: 15px; line-height: 1.6; color: #24292f;
            margin: 0; padding: 0;
        }}
        p {{ margin: 6px 0; }}
        ul, ol {{ margin: 6px 0 6px 28px; padding: 0; }}
        li {{ margin-bottom: 4px; }}
        pre, code {{ font-family: 'Consolas', 'Monaco', monospace; font-size: 13.5px; }}
        pre {{ margin: 0; padding: 0; background: transparent; border: none; white-space: pre-wrap; }}
        p code, li code {{ background-color: rgba(175, 184, 193, 0.2); padding: 2px 5px; border-radius: 4px; font-size: 0.9em; }}
        
        .k, .kd, .kn {{ color: #cf222e; font-weight: bold; }} 
        .s, .sb, .s1, .s2 {{ color: #0a3069; }} 
        .c, .cm, .c1 {{ color: #6e7781; font-style: italic; }} 
        .nf {{ color: #8250df; font-weight: bold; }} 
        .nc {{ color: #953800; font-weight: bold; }} 
        .mi, .mf {{ color: #0550ae; }} 
        .o, .ow {{ color: #24292f; }} 
        .nb {{ color: #953800; }} 

        math {{ font-size: 1.15em; font-family: 'Cambria Math', sans-serif; }}
        img {{ max-width: 100%; height: auto; vertical-align: middle; }}
    </style>
</head>
<body>
    {content}
</body>
</html>
"""

# ==================================================================================
# SECTION 2: BUBBLE MESSAGE CLASS
# ==================================================================================
class BubbleMessage(QWidget):
    content_updated = Signal()

    def __init__(self, text=None, images=None, is_user=True, user_name="User",
                 ai_logo=None, model_name=None, parent_width=800):
        super().__init__()
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) 

        self.is_user = is_user
        self.text = text or ""
        self.images = images or []
        self.user_name = user_name
        self.ai_logo = ai_logo
        self.model_name = model_name or "AI"
        self.available_width = max(parent_width, 100)
        self.fixed_ratio = 0.85 if not self.is_user else 0.7
        self.bubble_width = int(self.available_width * self.fixed_ratio)
        self.image_labels = []
        self.text_edit = None
        self.overlay_buttons = []

        self.outer_layout = QHBoxLayout(self)
        self.outer_layout.setContentsMargins(10, 6, 10, 6)
        self.outer_layout.setSpacing(0)
        
        self.main_stack = QVBoxLayout()
        self.main_stack.setContentsMargins(0, 0, 0, 0)
        self.main_stack.setSpacing(4)
        
        self.bubble_layout = QVBoxLayout()
        self.bubble_layout.setContentsMargins(12, 8, 12, 8)
        self.bubble_layout.setSpacing(4)
        
        self.bubble_widget = QWidget()
        self.bubble_widget.setLayout(self.bubble_layout)
        
        self._add_header()
        self._add_text()
        self._add_images()

        self.main_stack.addWidget(self.bubble_widget)
        self._apply_alignment()
        self._apply_stylesheet()
        
        QTimer.singleShot(0, self._calculate_and_set_size)

    def _add_header(self):
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(6)

        if self.is_user:
            header.addStretch()
            name = QLabel(self.user_name)
            name.setFont(QFont("Segoe UI", 9, QFont.Bold))
            header.addWidget(name)
        else:
            if self.ai_logo:
                logo = QLabel()
                if self.ai_logo and not self.ai_logo.isNull():
                    pix = self.ai_logo.pixmap(18, 18)
                    logo.setPixmap(pix)
                header.addWidget(logo)
            
            model = QLabel(self.model_name.split("/")[1] if "/" in self.model_name else self.model_name)
            model.setFont(QFont("Segoe UI", 9, QFont.Bold))
            header.addWidget(model)
            header.addStretch()

        copy_btn = QPushButton("Copy")
        copy_btn.setIcon(get_copy_icon())
        copy_btn.setIconSize(QSize(12, 12))
        copy_btn.setFixedSize(60, 22)
        copy_btn.setCursor(Qt.PointingHandCursor)
        copy_btn.setStyleSheet("""
            QPushButton { 
                background: #F0F0F0; border-radius: 6px; border: none; 
                padding: 0; font-size: 10px; color: #444; text-align: center;
            }
            QPushButton:hover { background: #E0E0E0; }
        """)
        copy_btn.clicked.connect(self._smart_copy)
        header.addWidget(copy_btn)

        self.main_stack.addLayout(header)

    def _smart_copy(self):
        clipboard = QApplication.clipboard()
        mime_data = QMimeData()
        plain_text = self.text
        if self.text == "Thinking..." and self.text_edit:
             plain_text = self.text_edit.toPlainText()
        
        html_content = f"<div>{plain_text.replace(chr(10), '<br>')}</div>"

        if self.images:
            html_content += "<br><hr><br>"
            for img_data in self.images:
                src = img_data
                if isinstance(img_data, str) and not img_data.startswith("data:"):
                    src = f"data:image/png;base64,{img_data}"
                html_content += f'<img src="{src}" width="400"><br>'

        mime_data.setText(plain_text)
        mime_data.setHtml(html_content)
        clipboard.setMimeData(mime_data)
        
        if self.images:
            self._flash_copy_btn("Copied All")
        else:
            self._flash_copy_btn("Copied")

    def _flash_copy_btn(self, text):
        sender = self.sender()
        if sender:
            orig_text = sender.text()
            orig_icon = sender.icon()
            sender.setText(text)
            sender.setIcon(QIcon())
            def restore():
                sender.setText(orig_text)
                sender.setIcon(orig_icon)
            QTimer.singleShot(1000, restore)

    def _render_local(self, raw_text):
        text = re.sub(r'([^\n])\n\s*-\s+', r'\1\n\n- ', raw_text)
        text = re.sub(r'(?m)^(\s*)(\d+)\.\s+(.*)', r'\1**\2.** \3', text)
        ph_map = {}; ctr = 0
        def rep_blk(m):
            nonlocal ctr; k = f"MB{ctr}P"; ctr+=1
            ph_map[k] = latex_to_base64_block(m.group(1).strip(), max_width_px=self.bubble_width*0.9)
            return k
        def rep_inl(m):
            nonlocal ctr; k = f"MI{ctr}P"; ctr+=1
            ph_map[k] = latex_to_mathml_inline(m.group(1).strip())
            return k
        text = re.sub(r'\$\$([\s\S]*?)\$\$', rep_blk, text)
        text = re.sub(r'(?<!\\)\$([^\$\n]+?)(?<!\\)\$', rep_inl, text)
        
        md_converter.reset()
        html = md_converter.convert(text)
        html = wrap_code_with_table(html)
        for k, v in ph_map.items(): html = html.replace(k, v)
        return HTML_WRAPPER.format(content=html)

    def show_context_menu_for_bubble(self, pos):
        menu = self.text_edit.createStandardContextMenu()
        menu.setContentsMargins(0,4,0,4)
        menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item {
                background-color: transparent;
                padding: 2px 8px 2px 8px;
                border-radius: 6px;
                margin: 2px 4px;
            }
            QMenu::item:selected {
                background-color: #f0f0f0;
                color: #000000;
            }
            QMenu::separator {
                height: 1px;
                background: #dddddd;
                margin: 4px 0;
            }
        """)
        menu.exec(self.text_edit.mapToGlobal(pos))

    def _add_text(self):
        self.text_edit = QTextBrowser()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFrameStyle(QFrame.NoFrame)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.text_edit.setFont(QFont("Segoe UI", 11))
        self.text_edit.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.text_edit.setOpenExternalLinks(True)
        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.show_context_menu_for_bubble)

        if self.is_user:
            md_converter.reset()
            html = md_converter.convert(self.text)
            self.text_edit.setHtml(f"<style>p{{margin:0;}}</style>{html}")
        elif self.text == "Thinking...":
            self.text_edit.setPlainText(self.text)
        else:
            self.text_edit.setHtml(self._render_local(self.text))

        self.text_edit.setStyleSheet("QTextBrowser {background: transparent; border: none; padding: 0;}")
        self.bubble_layout.addWidget(self.text_edit)
        self._install_overlay_update()

    def _add_images(self):
        self.image_labels = []
        for img in self.images:
            pix = QPixmap()
            if isinstance(img, QPixmap):
                pix = img
            elif isinstance(img, str):
                if not pix.load(img):
                    try:
                        base64_str = img
                        if "base64," in base64_str:
                            base64_str = base64_str.split("base64,")[1]
                        img_data = base64.b64decode(base64_str)
                        pix.loadFromData(QByteArray(img_data))
                    except: pass
            if pix.isNull(): continue
            lbl = QLabel()
            lbl.setProperty("original_pixmap", pix)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("background: transparent; padding: 4px;")
            lbl.setContextMenuPolicy(Qt.CustomContextMenu)
            lbl.customContextMenuRequested.connect(
                lambda pos, l=lbl: self._show_image_context_menu(pos, l)
            )
            self.bubble_layout.addWidget(lbl)
            self.image_labels.append(lbl)

    def _show_image_context_menu(self, pos, label):
        menu = QMenu(self)
        copy_action = menu.addAction(QIcon(), "Copy Image")
        menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 4px 12px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #f0f0f0;
                color: black;
            }
        """)
        action = menu.exec(label.mapToGlobal(pos))
        if action == copy_action:
            pixmap = label.property("original_pixmap")
            if pixmap and not pixmap.isNull():
                QApplication.clipboard().setPixmap(pixmap)
                self._flash_copy_btn("Image Copied!")

    def _apply_alignment(self):
        if self.is_user: 
            self.outer_layout.addStretch(); self.outer_layout.addLayout(self.main_stack)
        else: 
            self.outer_layout.addLayout(self.main_stack); self.outer_layout.addStretch()

    def _apply_stylesheet(self):
        bg = "#DCF8C6" if self.is_user else "#FFFFFF"
        border = "#E5E5E5"
        self.bubble_widget.setObjectName("bubble_widget")
        self.bubble_widget.setStyleSheet(
            f"#bubble_widget {{ background-color: {bg}; border-radius: 12px; border: 1px solid {border}; }}"
        )

    def _calculate_and_set_size(self):
        self.bubble_widget.setFixedWidth(self.bubble_width)
        cw = self.bubble_width - (self.bubble_layout.contentsMargins().left() + self.bubble_layout.contentsMargins().right())
        if cw > 0:
            for lbl in self.image_labels:
                pix = lbl.property("original_pixmap")
                if pix: lbl.setPixmap(pix.scaled(cw, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            if self.text_edit:
                self.text_edit.document().setTextWidth(cw)
                h = int(self.text_edit.document().size().height()) + 5
                self.text_edit.setFixedHeight(h)
        self.adjustSize()
        self.updateGeometry()
        self.content_updated.emit()

    def set_content(self, raw_text):
        self.text = raw_text
        if self.text_edit:
            if self.is_user:
                md_converter.reset()
                html = md_converter.convert(self.text)
                self.text_edit.setHtml(f"<style>p{{margin:0;}}</style>{html}")
            else:
                self.text_edit.setHtml(self._render_local(self.text))
            self._calculate_and_set_size()
            QTimer.singleShot(50, self._update_overlay_buttons)

    def update_max_width(self, w):
        self.available_width = max(w, 100)
        self.bubble_width = int(self.available_width * self.fixed_ratio)
        self.bubble_widget.setFixedWidth(self.bubble_width)
        self._calculate_and_set_size()

    def set_pre_rendered_content(self, html_content):
        if not self.text_edit: return
        self.text_edit.setHtml(html_content)
        self.text = self.text_edit.toPlainText()
        self._calculate_and_set_size()
        QTimer.singleShot(50, self._update_overlay_buttons)


    # ==============================================================================
    # SECTION 3: OVERLAY COPY BUTTONS LOGIC (Advanced)
    # ==============================================================================
    def resizeEvent(self, event):
        """
        Triggered when the window/bubble is resized.
        Ensures code block overlay buttons reposition correctly.
        """
        super().resizeEvent(event)
        QTimer.singleShot(10, self._update_overlay_buttons)

    def _install_overlay_update(self):
        """Connect scroll and document changes to overlay button updates."""
        if not self.text_edit: return

        self.text_edit.verticalScrollBar().valueChanged.connect(self._update_overlay_buttons)
        self.text_edit.document().contentsChanged.connect(lambda: QTimer.singleShot(50, self._update_overlay_buttons))

        # Initial triggers to position buttons correctly
        QTimer.singleShot(100, self._update_overlay_buttons)
        QTimer.singleShot(500, self._update_overlay_buttons)

    def _update_overlay_buttons(self):
        """
        Scan QTextDocument for code block tables and place 'Copy' buttons
        at their top-right visual coordinates within the viewport.
        """
        if not self.text_edit: return

        # Remove old buttons
        for b in self.overlay_buttons:
            b.deleteLater()
        self.overlay_buttons.clear()

        doc = self.text_edit.document()
        layout = doc.documentLayout()
        root = doc.rootFrame()
        scroll_y = self.text_edit.verticalScrollBar().value()
        viewport_width = self.text_edit.viewport().width()

        for frame in root.childFrames():
            if isinstance(frame, QTextTable):  # Identify code blocks
                rect = layout.frameBoundingRect(frame)
                y_pos = rect.top() - scroll_y

                # Skip off-screen tables
                if y_pos > self.text_edit.height() or (y_pos + rect.height()) < 0:
                    continue

                # Create button
                btn = QPushButton(self.text_edit)
                btn.setCursor(Qt.PointingHandCursor)
                btn.setIcon(get_copy_icon())
                btn.setIconSize(QSize(14, 14))
                btn.setToolTip("Copy code")
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent; border: none;
                        border-radius: 4px; padding: 4px;
                    }
                    QPushButton:hover { background-color: rgba(0, 0, 0, 0.08); }
                    QPushButton:pressed { background-color: rgba(0, 0, 0, 0.15); }
                """)
                btn.adjustSize()

                # Position top-right with margin
                x_pos = rect.right() - btn.width() - 10
                if x_pos > viewport_width - btn.width():
                    x_pos = viewport_width - btn.width() - 5
                btn.move(int(x_pos), int(y_pos - 15))
                btn.show()

                btn.clicked.connect(lambda c=False, f=frame: self._copy_code_from_frame(f))
                self.overlay_buttons.append(btn)

    def _copy_code_from_frame(self, frame):
        """Copy text from a code block frame and give visual feedback."""
        try:
            cell = frame.cellAt(0, 0)
            cursor = cell.firstCursorPosition()
            cursor.setPosition(cell.lastCursorPosition().position(), QTextCursor.KeepAnchor)

            code = cursor.selectedText().replace("\u2029", "\n").replace("\u2028", "\n").strip()
            QApplication.clipboard().setText(code)

            sender = self.sender()
            if sender:
                original_icon = sender.icon()
                sender.setIcon(QIcon())
                sender.setText("Copied!")
                sender.setStyleSheet("""
                    QPushButton {
                        background-color: #E6FFFA; color: #008000;
                        border: 1px solid #008000; border-radius: 4px;
                        font-size: 10px; padding: 2px 6px;
                    }
                """)
                sender.adjustSize()

                curr_pos = sender.pos()
                sender.move(curr_pos.x() - 20, curr_pos.y() + 5)

                def restore():
                    if not sender: return
                    sender.setText("")
                    sender.setIcon(original_icon)
                    sender.setStyleSheet("""
                        QPushButton {
                            background-color: transparent; border: none;
                            border-radius: 4px; padding: 4px;
                        }
                        QPushButton:hover { background-color: rgba(0, 0, 0, 0.08); }
                    """)
                    sender.adjustSize()
                    sender.move(curr_pos.x(), curr_pos.y())

                QTimer.singleShot(1500, restore)

        except Exception as e:
            print(f"Copy failed: {e}")

