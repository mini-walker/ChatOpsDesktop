#-----------------------------------------------------------------------------------------
<<<<<<< HEAD
<<<<<<< HEAD
# Purpose: This file contains the BubbleMessage class for chat messages
=======
# Purpouse: This file contains the BubbleMessage class for chat messages
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
# Purpouse: This file contains the BubbleMessage class for chat messages
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-11-23 
#----------------------------------------------------------------------------------------- 

<<<<<<< HEAD
<<<<<<< HEAD
#-----------------------------------------------------------------------------------------
# Import necessary modules for the BubbleMessage class
#-----------------------------------------------------------------------------------------
import sys
import re
import base64
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
import sys
import re
import io
import base64
import matplotlib
import matplotlib.pyplot as plt
import latex2mathml.converter 
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
import markdown

from PySide6.QtWidgets import (
    QWidget, QLabel, QTextBrowser, QHBoxLayout, QVBoxLayout, 
    QFrame, QSizePolicy, QPushButton, QApplication, QMenu
)
from PySide6.QtGui import (
    QPixmap, QFont, QTextOption, QTextTable, QTextCursor, 
<<<<<<< HEAD
<<<<<<< HEAD
    QAction, QIcon, QPainter, QColor, QResizeEvent
)
from PySide6.QtCore import Qt, QTimer, Signal, QSize, QByteArray, QMimeData
from Utils.Utils import utils, latex_signals_instance

# Import rendering utilities from Utils
latex_to_base64_block = utils.latex_to_base64_block
latex_to_mathml_inline = utils.latex_to_mathml_inline
wrap_code_with_table = utils.wrap_code_with_table
unicode_to_latex = utils.unicode_to_latex
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    QIcon
)
from PySide6.QtCore import Qt, QTimer, Signal, QSize, QByteArray, QMimeData
from Utils.Utils import utils
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

# ==================================================================================
# SECTION 1: CONFIGURATION & HELPER FUNCTIONS
# ==================================================================================

<<<<<<< HEAD
<<<<<<< HEAD
#-----------------------------------------------------------------------------------------
# Markdown Configuration
# Initialize the Markdown converter with specific extensions for rendering
#-----------------------------------------------------------------------------------------
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
md_converter = markdown.Markdown(extensions=[
    'fenced_code', 'tables', 'nl2br', 'codehilite'
], extension_configs={
    'codehilite': {'css_class': 'codehilite', 'noclasses': False, 'use_pygments': True}
})

<<<<<<< HEAD
<<<<<<< HEAD
#-----------------------------------------------------------------------------------------
# SVG Icon Generator
# Generate a copy icon using a resource path
#-----------------------------------------------------------------------------------------
def get_copy_icon():
    return QIcon(utils.resource_path("images/WIN11-Icons/icons8-copy-100.png"))

#-----------------------------------------------------------------------------------------
# Global CSS for rendering HTML content in the QTextBrowser
#-----------------------------------------------------------------------------------------
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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

<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
HTML_WRAPPER = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {{ 
<<<<<<< HEAD
<<<<<<< HEAD
            font-family: 'Times New Roman', 'STFangsong', '华文仿宋', serif; 
=======
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; 
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; 
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            font-size: 15px; line-height: 1.6; color: #24292f;
            margin: 0; padding: 0;
        }}
        p {{ margin: 6px 0; }}
        ul, ol {{ margin: 6px 0 6px 28px; padding: 0; }}
        li {{ margin-bottom: 4px; }}
        pre, code {{ font-family: 'Consolas', 'Monaco', monospace; font-size: 13.5px; }}
        pre {{ margin: 0; padding: 0; background: transparent; border: none; white-space: pre-wrap; }}
        p code, li code {{ background-color: rgba(175, 184, 193, 0.2); padding: 2px 5px; border-radius: 4px; font-size: 0.9em; }}
        
<<<<<<< HEAD
<<<<<<< HEAD
        /* Table Styles */
        table {{ border-collapse: collapse; margin: 10px 0; width: 100%; border: 1px solid #d0d7de; }}
        th, td {{ border: 1px solid #d0d7de; padding: 8px 12px; text-align: left; }}
        th {{ background-color: #f6f8fa; font-weight: bold; }}
        tr:nth-child(even) {{ background-color: #f6f8fa; }}
        
        /* Syntax Highlighting Colors */
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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
<<<<<<< HEAD
<<<<<<< HEAD

#-----------------------------------------------------------------------------------------
# BubbleMessage Class
# This class represents a chat bubble for displaying user or AI messages
#-----------------------------------------------------------------------------------------
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
class BubbleMessage(QWidget):
    content_updated = Signal()

    def __init__(self, text=None, images=None, is_user=True, user_name="User",
                 ai_logo=None, model_name=None, parent_width=800):
        super().__init__()
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) 

<<<<<<< HEAD
<<<<<<< HEAD
        # Initialize instance variables
        self.is_user = is_user
        self.text = text or ""
        
        # [CRITICAL FIX] Remove <think> tags from AI messages during initialization
        # This ensures that internal reasoning content is not displayed to the user
        if not self.is_user and self.text != "Thinking...":
            original_text = self.text
            self.text = re.sub(r'<think>.*?</think>\s*', '', self.text, flags=re.DOTALL)
            if '<think>' in original_text:
                print(f"[DEBUG BubbleMessage.__init__] Removed <think> tags, original length: {len(original_text)}, cleaned length: {len(self.text)}")
        
=======
        self.is_user = is_user
        self.text = text or ""
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
        self.is_user = is_user
        self.text = text or ""
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.images = images or []
        self.user_name = user_name
        self.ai_logo = ai_logo
        self.model_name = model_name or "AI"
        self.available_width = max(parent_width, 100)
        self.fixed_ratio = 0.85 if not self.is_user else 0.7
        self.bubble_width = int(self.available_width * self.fixed_ratio)
        self.image_labels = []
        self.text_edit = None
<<<<<<< HEAD
<<<<<<< HEAD
        self.overlay_buttons = [] # Store overlay buttons to manage memory

        # Layout Setup
=======
        self.overlay_buttons = []

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
        self.overlay_buttons = []

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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
        
<<<<<<< HEAD
<<<<<<< HEAD
        # Build UI Components
        self.addHeader()
        self.addText()
        self.addImages()

        self.main_stack.addWidget(self.bubble_widget)
        self.applyAlignment()
        self.applyStylesheet()
        
        QTimer.singleShot(0, self.calculateAndSetSize)
        
        self._latex_listener_connected = False
        self._ensure_latex_listener()

    # ------------------------------------------------------------------------------
    # Async LaTeX Rendering Methods
    # ------------------------------------------------------------------------------
    def _ensure_latex_listener(self):
        """Connect latex_ready once the bubble has real AI text (not Thinking...)."""
        if self.is_user or not self.text or self.text == "Thinking...":
            return
        if self._latex_listener_connected:
            return
        latex_signals_instance.latex_ready.connect(
            self._on_latex_ready, Qt.ConnectionType.QueuedConnection
        )
        self._latex_listener_connected = True

    def _on_latex_ready(self, latex_str: str):
        """
        Slot called when a background LaTeX fetch thread completes.
        Refreshes the bubble when it may contain the finished formula.
        """
        if not self.text_edit or self.is_user or self.text == "Thinking...":
            return
        # Exact match, or any complex environment (whitespace in $$ blocks may differ)
        if latex_str in self.text or '\\begin{' in self.text:
            QTimer.singleShot(0, self._refresh_html)

    def _refresh_html(self):
        """Re-render the bubble content now that the cache has the real image."""
        if self.text_edit and not self.is_user:
            self.text_edit.setHtml(self.renderLocal(self.text))
            self.calculateAndSetSize()
            QTimer.singleShot(50, self.updateOverlayButtons)

    # ------------------------------------------------------------------------------
    # UI Construction Methods
    # ------------------------------------------------------------------------------
    def addHeader(self):
        """Adds the user/model name and the main Copy button."""
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self._add_header()
        self._add_text()
        self._add_images()

        self.main_stack.addWidget(self.bubble_widget)
        self._apply_alignment()
        self._apply_stylesheet()
        
        QTimer.singleShot(0, self._calculate_and_set_size)

    def _add_header(self):
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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

<<<<<<< HEAD
<<<<<<< HEAD
        # --- Main Copy Button (Global) ---
        # [FIXED]: Added Icon and adjusted size
        copy_btn = QPushButton("Copy")
        copy_btn.setIcon(get_copy_icon())
        copy_btn.setIconSize(QSize(12, 12))
        copy_btn.setFixedSize(60, 22) # Slightly wider to fit Icon + Text
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        copy_btn = QPushButton("Copy")
        copy_btn.setIcon(get_copy_icon())
        copy_btn.setIconSize(QSize(12, 12))
        copy_btn.setFixedSize(60, 22)
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        copy_btn.setCursor(Qt.PointingHandCursor)
        copy_btn.setStyleSheet("""
            QPushButton { 
                background: #F0F0F0; border-radius: 6px; border: none; 
                padding: 0; font-size: 10px; color: #444; text-align: center;
            }
            QPushButton:hover { background: #E0E0E0; }
        """)
<<<<<<< HEAD
<<<<<<< HEAD
        copy_btn.clicked.connect(self.smartCopy)
=======
        copy_btn.clicked.connect(self._smart_copy)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
        copy_btn.clicked.connect(self._smart_copy)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        header.addWidget(copy_btn)

        self.main_stack.addLayout(header)

<<<<<<< HEAD
<<<<<<< HEAD
    #-----------------------------------------------------------------------------
    # Copy Functionality
    #-----------------------------------------------------------------------------
    def smartCopy(self):
        """
        Smart copy functionality: Constructs rich text (HTML) and places it in the clipboard.
        Includes both text content and embedded Base64 images for complete message copying.
        """
        clipboard = QApplication.clipboard()
        mime_data = QMimeData()

        # 1. Get plain text (as a fallback)
=======
    def _smart_copy(self):
        clipboard = QApplication.clipboard()
        mime_data = QMimeData()
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
    def _smart_copy(self):
        clipboard = QApplication.clipboard()
        mime_data = QMimeData()
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        plain_text = self.text
        if self.text == "Thinking..." and self.text_edit:
             plain_text = self.text_edit.toPlainText()
        
<<<<<<< HEAD
<<<<<<< HEAD
        # 2. Construct HTML content (text + images)
        html_content = f"<div>{plain_text.replace(chr(10), '<br>')}</div>"

        # If there are images, append them as Base64 <img> tags to the HTML
        if self.images:
            html_content += "<br><hr><br>" # Add a separator line
            for img_data in self.images:
                # Ensure the format is Data URI
                src = img_data
                if isinstance(img_data, str) and not img_data.startswith("data:"):
                    src = f"data:image/png;base64,{img_data}"
                
                # Append image tag
                html_content += f'<img src="{src}" width="400"><br>'

        # 3. Set MimeData
        mime_data.setText(plain_text)  # Set plain text (for apps that don't support rich text)
        mime_data.setHtml(html_content) # Set HTML (for apps that support rich text)

        # 4. Write to clipboard
        clipboard.setMimeData(mime_data)
        
        # Step 5: Notify user with visual feedback
        if self.images:
            self.flashCopyBtn("Copied All")
        else:
            self.flashCopyBtn("Copied")

    def flashCopyBtn(self, text):
        """
        Provide visual feedback by temporarily changing button text.
        Restores original button appearance after 1 second.
        
        Args:
            text: The text to display temporarily on the button
        """
        sender = self.sender()
        if sender:
            # Temporarily remove icon to show text cleanly, then restore
            orig_text = sender.text()
            orig_icon = sender.icon()
            
            sender.setText(text)
            sender.setIcon(QIcon()) # Hide icon
            
            def restore():
                sender.setText(orig_text)
                sender.setIcon(orig_icon)

            QTimer.singleShot(1000, restore)

    def renderLocal(self, raw_text):
        """
        Handles LaTeX and Markdown rendering for AI messages.
        Processes mathematical expressions, code blocks, and markdown formatting.
        """
        # [NEW] Remove <think> tags and their content
        # This prevents internal reasoning from being displayed in the rendered output
        text = re.sub(r'<think>.*?</think>\s*', '', raw_text, flags=re.DOTALL)
        
        # [CRITICAL FIX] Convert Unicode mathematical symbols to LaTeX first
        # This ensures proper rendering of mathematical notation
        text = unicode_to_latex(text)
        
        # Format list items and numbered lists for better markdown rendering
        text = re.sub(r'([^\n])\n\s*-\s+', r'\1\n\n- ', text)
        text = re.sub(r'(?m)^(\s*)(\d+)\.\s+(.*)', r'\1**\2.** \3', text)
        
        # Placeholder map for LaTeX expressions (block and inline)
        ph_map = {}
        ctr = 0
        
        def rep_blk(m):
            """Replace block LaTeX expressions ($$...$$) with Base64 image placeholders."""
            nonlocal ctr
            k = f"MB{ctr}P"
            ctr += 1
            latex_code = m.group(1) or m.group(2)
            ph_map[k] = latex_to_base64_block(latex_code.strip(), max_width_px=self.bubble_width*0.9)
            return k
        
        def rep_inl(m):
            """Replace inline LaTeX expressions ($...$) with MathML or Base64 image placeholders."""
            nonlocal ctr
            k = f"MI{ctr}P"
            ctr += 1
            latex_code = m.group(1) or m.group(2)
            latex_code = latex_code.strip()
            
            # [CRITICAL FIX] If the expression contains superscripts (_) or subscripts (^), use image rendering
            # This is because QTextBrowser cannot correctly display MathML's <msup> and <msub> elements
            if '_' in latex_code or '^' in latex_code or '\\begin{matrix}' in latex_code or '\\begin{pmatrix}' in latex_code:
                # inline=True: Use inline style to align with text
                ph_map[k] = latex_to_base64_block(latex_code, font_size=11, dpi=120, max_width_px=400, inline=True)
            else:
                ph_map[k] = latex_to_mathml_inline(latex_code)
            return k
        
        # Replace block LaTeX ($$...$$ and \[...\]) and inline LaTeX ($...$ and \(...\)) with placeholders
        text = re.sub(r'(?:\$\$([\s\S]*?)\$\$)|(?:\\\[([\s\S]*?)\\\])', rep_blk, text)
        text = re.sub(r'(?:(?<!\\)\$([^$]+?)(?<!\\)\$)|(?:\\\([\s\S]*?\\\))', rep_inl, text)
        
        # Convert markdown to HTML
        md_converter.reset()
        html = md_converter.convert(text)
        html = wrap_code_with_table(html)  # Wrap code blocks in tables for better styling
        
        # Replace placeholders with actual LaTeX renderings
        for k, v in ph_map.items():
            html = html.replace(k, v)
        
        return HTML_WRAPPER.format(content=html)
    
    #-----------------------------------------------------------------------------


    #-----------------------------------------------------------------------------
    # Context Menu for Text Bubble
    #-----------------------------------------------------------------------------
    def show_context_menu_for_bubble(self, pos):
        """
        Display a custom right-click context menu for the text bubble.
        Provides standard text editing options with custom styling.
        """
        
        menu = self.text_edit.createStandardContextMenu()

        menu.setContentsMargins(0,4,0,4)  # Left, Top, Right, Bottom

        # Style: white background, hover light gray, rounded corners
        menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;      /* white background */
                color: #333333;                 /* dark text */
                border: 1px solid #cccccc;      /* light border */
                border-radius: 8px;             /* rounded corners */
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                padding: 4px;
            }
            QMenu::item {
                background-color: transparent;
<<<<<<< HEAD
<<<<<<< HEAD
                padding: 2px 8px 2px 8px;     /* Adjust padding for comfort */
                border-radius: 6px;
                margin: 2px 4px;                /* Add margin for rounded look */
            }
            /* This controls the hover color */
            QMenu::item:selected {
                background-color: #f0f0f0;      /* hover light gray */
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                padding: 2px 8px 2px 8px;
                border-radius: 6px;
                margin: 2px 4px;
            }
            QMenu::item:selected {
                background-color: #f0f0f0;
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                color: #000000;
            }
            QMenu::separator {
                height: 1px;
                background: #dddddd;
                margin: 4px 0;
            }
        """)
<<<<<<< HEAD
<<<<<<< HEAD

        # Show the menu at the cursor position
        menu.exec(self.text_edit.mapToGlobal(pos))
    
    #-----------------------------------------------------------------------------



    #-----------------------------------------------------------------------------
    # Add Text Component
    #-----------------------------------------------------------------------------
    def addText(self):
        """
        Create and configure the text display component for the bubble message.
        Handles both user messages (simple markdown) and AI messages (LaTeX + Markdown).
        """
=======
        menu.exec(self.text_edit.mapToGlobal(pos))

    def _add_text(self):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
        menu.exec(self.text_edit.mapToGlobal(pos))

    def _add_text(self):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.text_edit = QTextBrowser()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFrameStyle(QFrame.NoFrame)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
<<<<<<< HEAD
<<<<<<< HEAD
        
        # Set font: Times New Roman (English), STFangsong (Chinese)
        # This provides good readability for both English and Chinese text
        font = QFont()
        font.setFamilies(["Times New Roman", "STFangsong", "华文仿宋", "serif"])
        font.setPointSize(11)
        self.text_edit.setFont(font)
        
        self.text_edit.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.text_edit.setOpenExternalLinks(True)

        # Configure custom context menu for right-click functionality
        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.show_context_menu_for_bubble)

        # Render content based on message type
        if self.is_user:
            # User messages: simple markdown conversion
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.text_edit.setFont(QFont("Segoe UI", 11))
        self.text_edit.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.text_edit.setOpenExternalLinks(True)
        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.show_context_menu_for_bubble)

        if self.is_user:
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            md_converter.reset()
            html = md_converter.convert(self.text)
            self.text_edit.setHtml(f"<style>p{{margin:0;}}</style>{html}")
        elif self.text == "Thinking...":
<<<<<<< HEAD
<<<<<<< HEAD
            # Special case: show plain text for "Thinking..." state
            self.text_edit.setPlainText(self.text)
        else:
            # AI messages: full LaTeX and Markdown rendering
            self.text_edit.setHtml(self.renderLocal(self.text))

        # Apply transparent styling to blend with bubble background
        self.text_edit.setStyleSheet("QTextBrowser {background: transparent; border: none; padding: 0;}")
        self.bubble_layout.addWidget(self.text_edit)

        # Install overlay button listeners for code block copy functionality
        self.installOverlayUpdate()
    
    #-----------------------------------------------------------------------------

    #-----------------------------------------------------------------------------
    # Add Image Components
    #-----------------------------------------------------------------------------
    def addImages(self):
        """
        Process and display images in the bubble message.
        Supports QPixmap objects, file paths, and Base64 encoded images.
        """
        self.image_labels = []
        for img in self.images:
            pix = QPixmap()
            
            # Case 1: The input is already a QPixmap object
            if isinstance(img, QPixmap):
                pix = img
            
            # Case 2: The input is a string (could be a file path or Base64)
            elif isinstance(img, str):
                # A. Try loading as a regular file path first (e.g., "C:/images/photo.png")
                if not pix.load(img):
                    # B. If loading as a path fails, it might be a Base64 string
                    try:
                        # 1. Clean the data: remove any data URI prefix (e.g., "data:image/png;base64,")
                        base64_str = img
                        if "base64," in base64_str:
                            base64_str = base64_str.split("base64,")[1]
                        
                        # 2. Decode Base64 string to binary data
                        img_data = base64.b64decode(base64_str)
                        
                        # 3. Load the image from memory data
                        pix.loadFromData(QByteArray(img_data))
                    except Exception as e:
                        print(f"[Error] Failed to load image from Base64: {e}")

            # Check if the image is valid, skip if not
            if pix.isNull(): 
                print("[Warn] Image is null, skipping.")
                continue

            # Create label to display the image
            lbl = QLabel()
            lbl.setProperty("original_pixmap", pix)  # Store original for copying
            lbl.setAlignment(Qt.AlignCenter)

            # Apply transparent background with padding for better visual appearance
            lbl.setStyleSheet("background: transparent; padding: 4px;")

            # Enable right-click context menu support for images
            lbl.setContextMenuPolicy(Qt.CustomContextMenu)
            # Use lambda to pass the current label to the slot function
            lbl.customContextMenuRequested.connect(
                lambda pos, l=lbl: self.showImageContextMenu(pos, l)
            )
            
            self.bubble_layout.addWidget(lbl)
            self.image_labels.append(lbl)
    
    #-----------------------------------------------------------------------------

    #-----------------------------------------------------------------------------
    # Image Context Menu
    #-----------------------------------------------------------------------------
    def showImageContextMenu(self, pos, label):
        """
        Display a right-click context menu for images.
        Provides a 'Copy Image' option to copy the image to clipboard.
        """
        menu = QMenu(self)
        
        # Add copy action
        copy_action = menu.addAction(QIcon(), "Copy Image")
        
        # Style the menu (consistent with your previous menu style)
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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
<<<<<<< HEAD
<<<<<<< HEAD
        
        # Show the menu at the cursor position
        action = menu.exec(label.mapToGlobal(pos))
        
        # Handle copy action if user clicked "Copy Image"
=======
        action = menu.exec(label.mapToGlobal(pos))
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
        action = menu.exec(label.mapToGlobal(pos))
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if action == copy_action:
            pixmap = label.property("original_pixmap")
            if pixmap and not pixmap.isNull():
                QApplication.clipboard().setPixmap(pixmap)
<<<<<<< HEAD
<<<<<<< HEAD
                self.flashCopyBtn("Image Copied!")  # Reuse the button's feedback effect
    
    #-----------------------------------------------------------------------------





    # ------------------------------------------------------------------------------
    # Styling & Sizing Methods
    # ------------------------------------------------------------------------------
    def applyAlignment(self):
        """
        Apply horizontal alignment based on message type.
        User messages align to the right, AI messages align to the left.
        """
        if self.is_user: 
            self.outer_layout.addStretch()
            self.outer_layout.addLayout(self.main_stack)
        else: 
            self.outer_layout.addLayout(self.main_stack)
            self.outer_layout.addStretch()

    def applyStylesheet(self):
        """
        Apply visual styling to the bubble widget.
        User messages have a green background, AI messages have a white background.
        """
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                self._flash_copy_btn("Image Copied!")

    def _apply_alignment(self):
        if self.is_user: 
            self.outer_layout.addStretch(); self.outer_layout.addLayout(self.main_stack)
        else: 
            self.outer_layout.addLayout(self.main_stack); self.outer_layout.addStretch()

    def _apply_stylesheet(self):
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        bg = "#DCF8C6" if self.is_user else "#FFFFFF"
        border = "#E5E5E5"
        self.bubble_widget.setObjectName("bubble_widget")
        self.bubble_widget.setStyleSheet(
            f"#bubble_widget {{ background-color: {bg}; border-radius: 12px; border: 1px solid {border}; }}"
        )

<<<<<<< HEAD
<<<<<<< HEAD
    def calculateAndSetSize(self):
        """
        Calculate and set the optimal size for the bubble and its contents.
        Scales images and adjusts text width to fit within the bubble.
        """
        # Set bubble width
        self.bubble_widget.setFixedWidth(self.bubble_width)
        
        # Calculate content width (bubble width minus margins)
        cw = self.bubble_width - (self.bubble_layout.contentsMargins().left() + self.bubble_layout.contentsMargins().right())
        
        if cw > 0:
            # Scale images to fit within content width
            for lbl in self.image_labels:
                pix = lbl.property("original_pixmap")
                if pix:
                    lbl.setPixmap(pix.scaled(cw, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            
            # Adjust text width and height
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    def _calculate_and_set_size(self):
        self.bubble_widget.setFixedWidth(self.bubble_width)
        cw = self.bubble_width - (self.bubble_layout.contentsMargins().left() + self.bubble_layout.contentsMargins().right())
        if cw > 0:
            for lbl in self.image_labels:
                pix = lbl.property("original_pixmap")
                if pix: lbl.setPixmap(pix.scaled(cw, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            if self.text_edit:
                self.text_edit.document().setTextWidth(cw)
                h = int(self.text_edit.document().size().height()) + 5
                self.text_edit.setFixedHeight(h)
<<<<<<< HEAD
<<<<<<< HEAD
        
        # Update widget geometry and emit signal
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.adjustSize()
        self.updateGeometry()
        self.content_updated.emit()

<<<<<<< HEAD
<<<<<<< HEAD
    # ------------------------------------------------------------------------------
    # Public Methods for Controller
    # ------------------------------------------------------------------------------
    def set_content(self, raw_text):
        """
        Standard method to update content from AI.
        Re-renders the message with new text content.
        
        Args:
            raw_text: The new text content to display
        """
        self.text = raw_text
        self._ensure_latex_listener()
        if self.text_edit:
            if self.is_user:
                # User messages: simple markdown conversion
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    def set_content(self, raw_text):
        self.text = raw_text
        if self.text_edit:
            if self.is_user:
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                md_converter.reset()
                html = md_converter.convert(self.text)
                self.text_edit.setHtml(f"<style>p{{margin:0;}}</style>{html}")
            else:
<<<<<<< HEAD
<<<<<<< HEAD
                # AI messages: full LaTeX and Markdown rendering
                self.text_edit.setHtml(self.renderLocal(self.text))
            
            self.calculateAndSetSize()
            QTimer.singleShot(50, self.updateOverlayButtons)

    def update_max_width(self, w):
        """
        Update the maximum available width for the bubble.
        Recalculates bubble width and adjusts all content accordingly.
        
        Args:
            w: The new maximum width in pixels
        """
        self.available_width = max(w, 100)
        self.bubble_width = int(self.available_width * self.fixed_ratio)
        self.bubble_widget.setFixedWidth(self.bubble_width)
        self.calculateAndSetSize()

    def set_pre_rendered_content(self, html_content, raw_text=None):
        """
        Legacy: set pre-built HTML. Prefer set_content(raw_text) so LaTeX async works.
        
        Args:
            html_content: Pre-rendered HTML string to display
            raw_text: Original markdown/LaTeX source (required for async formula refresh)
        """
        if not self.text_edit:
            return
        if raw_text is not None:
            self.text = raw_text
        self.text_edit.setHtml(html_content)
        if raw_text is None:
            self.text = self.text_edit.toPlainText()
        self._ensure_latex_listener()
        self.calculateAndSetSize()
        QTimer.singleShot(50, self.updateOverlayButtons)
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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

<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

    # ==============================================================================
    # SECTION 3: OVERLAY COPY BUTTONS LOGIC (Advanced)
    # ==============================================================================
    def resizeEvent(self, event):
        """
<<<<<<< HEAD
<<<<<<< HEAD
        Handle widget resize events.
        
        CRITICAL: When the window/bubble is resized, the code blocks move.
        We must trigger a re-calculation of the overlay button positions.
        
        Args:
            event: The resize event
        """
        super().resizeEvent(event)
        QTimer.singleShot(10, self.updateOverlayButtons)

    def installOverlayUpdate(self):
        """
        Install event listeners to update overlay button positions.
        Updates buttons when content changes, scrolls, or resizes.
        """
        if not self.text_edit:
            return
        
        # Connect signals to update overlay buttons on various events
        # Update on scroll
        self.text_edit.verticalScrollBar().valueChanged.connect(self.updateOverlayButtons)
        # Update on content change (with slight delay to ensure rendering is complete)
        self.text_edit.document().contentsChanged.connect(lambda: QTimer.singleShot(50, self.updateOverlayButtons))

        # Initial triggers to ensure buttons appear after initial render
        QTimer.singleShot(100, self.updateOverlayButtons)
        QTimer.singleShot(500, self.updateOverlayButtons)



    def updateOverlayButtons(self):
        """
        Scan the QTextDocument for tables (code blocks) and place 'Copy' buttons
        at their exact top-right visual coordinates.
        
        This method dynamically positions overlay buttons for each code block
        in the message, updating their positions when content changes or scrolls.
        """
        if not self.text_edit:
            return

        # Step 1: Cleanup old buttons to prevent memory leaks
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        for b in self.overlay_buttons:
            b.deleteLater()
        self.overlay_buttons.clear()

<<<<<<< HEAD
<<<<<<< HEAD
        # Get document layout information
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        doc = self.text_edit.document()
        layout = doc.documentLayout()
        root = doc.rootFrame()
        scroll_y = self.text_edit.verticalScrollBar().value()
        viewport_width = self.text_edit.viewport().width()

<<<<<<< HEAD
<<<<<<< HEAD
        # Step 2: Iterate over frames to find code blocks (rendered as tables)
        for frame in root.childFrames():
            if isinstance(frame, QTextTable):  # Our code blocks are rendered as tables
                
                # Get geometry relative to the document
                rect = layout.frameBoundingRect(frame)
                
                # Calculate Y position relative to the viewport
                y_pos = rect.top() - scroll_y
                
                # Optimization: Skip buttons for off-screen code blocks
                if y_pos > self.text_edit.height() or (y_pos + rect.height()) < 0:
                    continue

                # Step 3: Create button with copy icon
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        for frame in root.childFrames():
            if isinstance(frame, QTextTable):  # Identify code blocks
                rect = layout.frameBoundingRect(frame)
                y_pos = rect.top() - scroll_y

                # Skip off-screen tables
                if y_pos > self.text_edit.height() or (y_pos + rect.height()) < 0:
                    continue

                # Create button
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                btn = QPushButton(self.text_edit)
                btn.setCursor(Qt.PointingHandCursor)
                btn.setIcon(get_copy_icon())
                btn.setIconSize(QSize(14, 14))
                btn.setToolTip("Copy code")
<<<<<<< HEAD
<<<<<<< HEAD
                
                # Style: Transparent background, visible on hover
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent; border: none;
                        border-radius: 4px; padding: 4px;
                    }
                    QPushButton:hover { background-color: rgba(0, 0, 0, 0.08); }
                    QPushButton:pressed { background-color: rgba(0, 0, 0, 0.15); }
                """)
                btn.adjustSize()

<<<<<<< HEAD
<<<<<<< HEAD
                # Step 4: Calculate top-right position for the button
                # X = Right edge of table - button width - margin
                x_pos = rect.right() - btn.width() - 10
                
                # Ensure button doesn't overflow viewport (e.g. if table is wider than view)
                if x_pos > viewport_width - btn.width():
                    x_pos = viewport_width - btn.width() - 5

                # Position button slightly above the code block (Y - 15px padding)
                btn.move(int(x_pos), int(y_pos - 15))
                btn.show()
                
                # Connect click handler to copy code from this frame
                btn.clicked.connect(lambda c=False, f=frame: self.copyCodeFromFrame(f))
                self.overlay_buttons.append(btn)

    def copyCodeFromFrame(self, frame):
        """
        Extract text from the table frame (code block) and copy it to clipboard.
        Updates button UI to provide visual feedback to the user.
        
        Args:
            frame: The QTextTable frame containing the code block
        """
        try:
            # Extract text from the first cell of the table (code blocks use single-cell tables)
            cell = frame.cellAt(0, 0)
            cursor = cell.firstCursorPosition()
            cursor.setPosition(cell.lastCursorPosition().position(), QTextCursor.KeepAnchor)
            
            # Clean up Qt paragraph separators and normalize line breaks
            code = cursor.selectedText().replace("\u2029", "\n").replace("\u2028", "\n").strip()
            QApplication.clipboard().setText(code)
            
            # Visual Feedback: Temporarily change button icon to "Copied!" text
            sender = self.sender()
            if sender:
                original_icon = sender.icon()
                sender.setIcon(QIcon())  # Remove icon
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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
<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                sender.setText("Copied!")
                sender.setStyleSheet("""
                    QPushButton {
                        background-color: #E6FFFA; color: #008000;
                        border: 1px solid #008000; border-radius: 4px;
                        font-size: 10px; padding: 2px 6px;
                    }
                """)
                sender.adjustSize()
<<<<<<< HEAD
<<<<<<< HEAD
                
                # Re-align slightly to keep right-alignment visual
                curr_pos = sender.pos()
                sender.move(curr_pos.x() - 20, curr_pos.y() + 5)

                # Restore original button appearance after 1.5 seconds
                def restore():
                    if not sender:
                        return
                    sender.setText("")
                    sender.setIcon(original_icon)
                    sender.setStyleSheet("""
                        QPushButton { background-color: transparent; border: none; border-radius: 4px; padding: 4px; }
                        QPushButton:hover { background-color: rgba(0, 0, 0, 0.08); }
                    """)
                    sender.adjustSize()
                    # The exact position will be fixed by the next resize/scroll event
                    # or we can try to restore roughly:
                    sender.move(curr_pos.x(), curr_pos.y())

                QTimer.singleShot(1500, restore)
                
        except Exception as e:
            print(f"Copy failed: {e}")
=======
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

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

<<<<<<< HEAD
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
