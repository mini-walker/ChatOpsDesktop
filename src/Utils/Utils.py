#-----------------------------------------------------------------------------------------
# Purpouse: This file contains various utility functions for file path handling,
<<<<<<< HEAD
#           text formatting, filename sanitization, and LaTeX/Math rendering.
=======
#           text formatting, and filename sanitization.
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-11-23 
#----------------------------------------------------------------------------------------- 

import sys
import re
<<<<<<< HEAD
import io
import base64
from pathlib import Path

# Lazy imports for rendering (only loaded when needed)
try:
    import matplotlib.pyplot as plt
    import latex2mathml.converter
    RENDERING_AVAILABLE = True
except ImportError:
    RENDERING_AVAILABLE = False

from PySide6.QtCore import QObject, Signal, QThread

# Global signals for asynchronous latex rendering
class LatexSignals(QObject):
    latex_ready = Signal(str)

latex_signals_instance = LatexSignals()

# CodeCogs: no socket timeout — wait until the server responds; retry on transient errors.
CODECOGS_FETCH_TIMEOUT = None
CODECOGS_RETRY_INITIAL_SEC = 2
CODECOGS_RETRY_MAX_SEC = 30

class LatexFetchThread(QThread):
    """Background thread to fetch LaTeX images from CodeCogs without blocking UI."""
    def __init__(self, latex_str, dpi, inline, cache_key, max_width_px):
        super().__init__()
        self.latex_str = latex_str
        self.dpi = dpi
        self.inline = inline
        self.cache_key = cache_key
        self.max_width_px = max_width_px

    def run(self):
        import time
        import urllib.parse
        import urllib.request
        import base64

        url = (
            f"https://latex.codecogs.com/png.image?\\dpi{{{self.dpi}}}\\bg{{white}}"
            + urllib.parse.quote(self.latex_str)
        )
        req = urllib.request.Request(
            url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )

        retry_delay = CODECOGS_RETRY_INITIAL_SEC
        while not self.isInterruptionRequested():
            try:
                with urllib.request.urlopen(req, timeout=CODECOGS_FETCH_TIMEOUT) as response:
                    img_data = response.read()
                if not img_data:
                    raise ValueError("empty image response")

                img = base64.b64encode(img_data).decode('utf-8')
                if self.inline:
                    result = (
                        f'<img src="data:image/png;base64,{img}" '
                        f'style="display: inline; vertical-align: middle; '
                        f'max-height: 3em; width: auto; margin: 0 2px;" />'
                    )
                else:
                    result = (
                        f'<div style="text-align: center; margin: 8px 0; overflow-x: auto;">'
                        f'<img src="data:image/png;base64,{img}" '
                        f'style="max-width: 100%; height: auto; vertical-align: middle;" /></div>'
                    )
                utils._latex_cache[self.cache_key] = result
                latex_signals_instance.latex_ready.emit(self.latex_str)
                return
            except Exception:
                if self.isInterruptionRequested():
                    return
                # Keep "[公式渲染中...]" in cache; do not cache failure (allows retry).
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 1.5, CODECOGS_RETRY_MAX_SEC)


=======
from pathlib import Path

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
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
<<<<<<< HEAD

    # ================================================================
    # SECTION: LaTeX and Math Rendering Utilities
    # ================================================================

    #--------------------------------------------------------------
    # Unicode to LaTeX Converter
    #--------------------------------------------------------------
    @staticmethod
    def unicode_to_latex(text):
        """
        Convert Unicode math symbols to LaTeX commands.
        
        This ensures matplotlib and latex2mathml can properly render 
        mathematical notation.
        
        Args:
            text (str): Input text with Unicode symbols
            
        Returns:
            str: Text with LaTeX commands
        """
        replacements = {
            # Greek letters (lowercase)
            'α': r'\alpha', 'β': r'\beta', 'γ': r'\gamma', 
            'δ': r'\delta', 'ε': r'\epsilon', 'ζ': r'\zeta', 
            'η': r'\eta', 'θ': r'\theta', 'ι': r'\iota', 
            'κ': r'\kappa', 'λ': r'\lambda', 'μ': r'\mu',
            'ν': r'\nu', 'ξ': r'\xi', 'ο': r'o', 'π': r'\pi',
            'ρ': r'\rho', 'ς': r'\varsigma', 'σ': r'\sigma', 
            'τ': r'\tau', 'υ': r'\upsilon', 'φ': r'\phi', 
            'χ': r'\chi', 'ψ': r'\psi', 'ω': r'\omega',
            
            # Greek letters (uppercase)
            'Α': r'A', 'Β': r'B', 'Γ': r'\Gamma', 'Δ': r'\Delta',
            'Ε': r'E', 'Ζ': r'Z', 'Η': r'H', 'Θ': r'\Theta',
            'Ι': r'I', 'Κ': r'K', 'Λ': r'\Lambda', 'Μ': r'M',
            'Ν': r'N', 'Ξ': r'\Xi', 'Ο': r'O', 'Π': r'\Pi',
            'Ρ': r'P', 'Σ': r'\Sigma', 'Τ': r'T', 
            'Υ': r'\Upsilon', 'Φ': r'\Phi', 'Χ': r'X', 
            'Ψ': r'\Psi', 'Ω': r'\Omega',
            
            # Math operators
            '±': r'\pm', '∓': r'\mp', '×': r'\times', '÷': r'\div',
            '≠': r'\neq', '≈': r'\approx', '≡': r'\equiv',
            '≤': r'\leq', '≥': r'\geq', '≪': r'\ll', '≫': r'\gg',
            '∞': r'\infty', '∂': r'\partial', '∇': r'\nabla',
            '∫': r'\int', '∮': r'\oint', '∑': r'\sum', '∏': r'\prod',
            '√': r'\sqrt', '∛': r'\sqrt[3]', '∜': r'\sqrt[4]',
            '∈': r'\in', '∉': r'\notin', '∋': r'\ni', 
            '∌': r'\not\ni', '⊂': r'\subset', '⊃': r'\supset', 
            '⊆': r'\subseteq', '⊇': r'\supseteq',
            '∪': r'\cup', '∩': r'\cap', '∅': r'\emptyset',
            '∀': r'\forall', '∃': r'\exists', '∄': r'\nexists',
            '∧': r'\wedge', '∨': r'\vee', '¬': r'\neg',
            '⇒': r'\Rightarrow', '⇐': r'\Leftarrow', 
            '⇔': r'\Leftrightarrow', '→': r'\rightarrow', 
            '←': r'\leftarrow', '↔': r'\leftrightarrow',
            '℘': r'\wp', 'ℜ': r'\Re', 'ℑ': r'\Im', 'ℵ': r'\aleph',
            '∝': r'\propto', '∠': r'\angle', '⊥': r'\perp', 
            '∥': r'\parallel',
            
            # Superscripts
            '⁰': r'^0', '¹': r'^1', '²': r'^2', '³': r'^3', 
            '⁴': r'^4', '⁵': r'^5', '⁶': r'^6', '⁷': r'^7', 
            '⁸': r'^8', '⁹': r'^9',
            
            # Subscripts
            '₀': r'_0', '₁': r'_1', '₂': r'_2', '₃': r'_3', 
            '₄': r'_4', '₅': r'_5', '₆': r'_6', '₇': r'_7', 
            '₈': r'_8', '₉': r'_9',
            
            # Special
            '°': r'^\circ',
        }
        
        for unicode_char, latex_cmd in replacements.items():
            text = text.replace(unicode_char, latex_cmd)
        
        return text
    #--------------------------------------------------------------

    #--------------------------------------------------------------
    # LaTeX to Base64 Image
    #--------------------------------------------------------------
    # Cache for rendered LaTeX images to avoid redundant API/Matplotlib calls during streaming
    _latex_cache = {}

    @staticmethod
    def latex_to_base64_block(
        latex_str, 
        font_size=12, 
        dpi=110, 
        max_width_px=800, 
        inline=False
    ):
        """
        Render LaTeX to Base64-encoded PNG image using Matplotlib or CodeCogs API.
        Caches results to prevent rate-limiting and UI freezing during streaming.
        """
        if not RENDERING_AVAILABLE:
            return "[LaTeX rendering unavailable]"
            
        # Check cache first
        cache_key = (latex_str, font_size, dpi, max_width_px, inline)
        if cache_key in utils._latex_cache:
            return utils._latex_cache[cache_key]
            
        clean_latex = f"${latex_str}$"
        safe_width_px = max(max_width_px, 100)
        
        # [CRITICAL FIX] Matplotlib's mathtext does NOT support environments like \begin{pmatrix} or \begin{cases}
        # For complex environments, use the CodeCogs LaTeX rendering API asynchronously
        if '\\begin{' in latex_str:
            # Mark cache as loading so we don't spawn 100 threads for the same matrix
            utils._latex_cache[cache_key] = f'<div style="text-align: center; margin: 8px 0; color: #888;">[公式渲染中...]</div>'
            
            # Start background thread to fetch image
            thread = LatexFetchThread(latex_str, dpi, inline, cache_key, max_width_px)
            # Store thread reference to prevent garbage collection
            if not hasattr(utils, '_active_latex_threads'):
                utils._active_latex_threads = []
            # Clean up dead threads
            utils._active_latex_threads = [t for t in utils._active_latex_threads if t.isRunning()]
            utils._active_latex_threads.append(thread)
            thread.start()
            
            return utils._latex_cache[cache_key]
        
        # Measure text size (for simple formulas supported by Matplotlib)
        temp_fig = plt.figure(figsize=(10, 1), dpi=dpi)
        temp_ax = temp_fig.add_axes([0, 0, 1, 1])
        temp_ax.set_axis_off()
        temp_text = temp_ax.text(
            0, 0, clean_latex, 
            fontsize=font_size, 
            color='black'
        )
        
        try:
            temp_fig.canvas.draw()
            bbox = temp_text.get_window_extent(
                temp_fig.canvas.get_renderer()
            )
            w_in, h_in = bbox.width / dpi, bbox.height / dpi
        except:
            w_in, h_in = 4, 0.5
        finally:
            plt.close(temp_fig)

        final_w = max(min(w_in, safe_width_px / dpi), 0.1)
        final_h = max(h_in, 0.1)
        
        # Render final image
        fig = plt.figure(figsize=(final_w, final_h), dpi=dpi)
        fig.text(
            0.5, 0.5, clean_latex, 
            fontsize=font_size, 
            color='black', 
            ha='center', 
            va='center'
        )
        
        try:
            import io, base64
            buf = io.BytesIO()
            fig.savefig(
                buf, 
                format='png', 
                dpi=dpi, 
                transparent=True, 
                bbox_inches='tight', 
                pad_inches=0.02
            )
            plt.close(fig)
            buf.seek(0)
            img = base64.b64encode(buf.read()).decode('utf-8')
            
            # Return appropriate HTML based on inline/block mode
            if inline:
                result = (
                    f'<img src="data:image/png;base64,{img}" '
                    f'style="display: inline; '
                    f'vertical-align: middle; '
                    f'height: 1.1em; width: auto; '
                    f'margin: 0 2px;" />'
                )
            else:
                result = (
                    f'<div style="text-align: center; '
                    f'margin: 8px 0;">'
                    f'<img src="data:image/png;base64,{img}" '
                    f'style="max-width: 100%; height: auto; '
                    f'vertical-align: middle;" /></div>'
                )
            utils._latex_cache[cache_key] = result
            return result
        except:
            plt.close(fig)
            return "[Error]"
    #--------------------------------------------------------------

    #--------------------------------------------------------------
    # LaTeX to MathML
    #--------------------------------------------------------------
    @staticmethod
    def latex_to_mathml_inline(latex_str):
        """
        Convert LaTeX to MathML for inline rendering.
        
        Args:
            latex_str (str): LaTeX code
            
        Returns:
            str: MathML HTML or error message
        """
        if not RENDERING_AVAILABLE:
            return "[MathML unavailable]"
            
        try:
            return latex2mathml.converter.convert(latex_str)
        except:
            return "[Error]"
    #--------------------------------------------------------------

    #--------------------------------------------------------------
    # Wrap Code Blocks
    #--------------------------------------------------------------
    @staticmethod
    def wrap_code_with_table(html):
        """
        Wrap code blocks with table styling for Qt rendering.
        
        Args:
            html (str): HTML content with code blocks
            
        Returns:
            str: HTML with styled code blocks
        """
        table_start = (
            '<table width="100%" bgcolor="#f4f6f8" border="0" '
            'cellspacing="0" cellpadding="0" '
            'style="border-radius: 8px; margin: 10px 0; '
            'border: 1px solid #d0d7de; border-collapse: separate;">'
            '<tr><td style="padding: 12px; color: #24292f;">'
        )
        table_end = '</td></tr></table>'
        pattern = r'<div class="codehilite">(.*?)</div>'
        
        return re.sub(
            pattern, 
            lambda m: f"{table_start}{m.group(1)}{table_end}", 
            html, 
            flags=re.DOTALL
        )
    #--------------------------------------------------------------
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
