#-----------------------------------------------------------------------------------------
# Purpouse: This file contains the Operation_Chat_Controller class
#           It is used to control the chat operations between GUI and AI backend
# Programmer: Shanqin Jin
# Email: sjin@mun.ca
# Date: 2025-11-23 
#----------------------------------------------------------------------------------------- 


import json
import re
import io
import base64
import requests
import matplotlib
import matplotlib.pyplot as plt
<<<<<<< HEAD
=======
import latex2mathml.converter
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
import markdown
import mimetypes

from datetime import datetime
from pathlib import Path
from queue import Queue, Empty
from PySide6.QtCore import QTimer, QThread, Signal, Qt
from PySide6.QtGui import QImageReader 

from Operation.Operation_Bubble_Message import BubbleMessage, HTML_WRAPPER
from Utils.Utils import utils

<<<<<<< HEAD
# Import rendering utilities from Utils
latex_to_base64_block = utils.latex_to_base64_block
latex_to_mathml_inline = utils.latex_to_mathml_inline
wrap_code_with_table = utils.wrap_code_with_table
unicode_to_latex = utils.unicode_to_latex

=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
# ============================================================
# Backend rendering configuration and markdown converter setup
# ============================================================
QImageReader.setAllocationLimit(0)
matplotlib.use('Agg')
plt.rcParams['mathtext.fontset'] = 'cm' 
plt.rcParams['font.serif'] = ['DejaVu Serif']

md_converter = markdown.Markdown(extensions=[
    'fenced_code', 'tables', 'nl2br', 'codehilite'
], extension_configs={
    'codehilite': {'css_class': 'codehilite', 'noclasses': False, 'use_pygments': True}
})

<<<<<<< HEAD
# ============================================================================
# Process Mixed Content - LaTeX and Markdown Rendering
# ============================================================================
def process_mixed_content(raw_text):
    # [Added] Remove <think> tags and their content
    text = re.sub(r'<think>.*?</think>\s*', '', raw_text, flags=re.DOTALL)
    
    # [Key Fix] Convert Unicode math symbols to LaTeX first
    text = unicode_to_latex(text)
    
    text = re.sub(r'([^\n])\n\s*-\s+', r'\1\n\n- ', text)
=======
# --- Render helpers for LaTeX and Markdown processing (unchanged core) ---
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
        plt.close(fig); return "[Error]"

def latex_to_mathml_inline(latex_str):
    try: return latex2mathml.converter.convert(latex_str)
    except: return "[Error]"

def wrap_code_with_table(html):
    table_start = (
        '<table width="100%" bgcolor="#f4f6f8" border="0" cellspacing="0" cellpadding="0" '
        'style="border-radius: 8px; margin: 10px 0; border: 1px solid #d0d7de; border-collapse: separate;">'
        '<tr><td style="padding: 12px; color: #24292f;">'
    )
    table_end = '</td></tr></table>'
    pattern = r'<div class="codehilite">(.*?)</div>'
    return re.sub(pattern, lambda m: f"{table_start}{m.group(1)}{table_end}", html, flags=re.DOTALL)

def process_mixed_content(raw_text):
    text = re.sub(r'([^\n])\n\s*-\s+', r'\1\n\n- ', raw_text)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    text = re.sub(r'(?m)^(\s*)(\d+)\.\s+(.*)', r'\1**\2.** \3', text)
    
    ph_map = {}; ctr = 0
    def rep_blk(m):
        nonlocal ctr; k = f"MB{ctr}P"; ctr+=1
<<<<<<< HEAD
        # Support both $$...$$ and \[...\] syntax
=======
        # 兼容 $$...$$ 和 \[...\]
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        latex_code = m.group(1) or m.group(2)
        ph_map[k] = latex_to_base64_block(latex_code.strip(), max_width_px=600)
        return k
        
    def rep_inl(m):
        nonlocal ctr; k = f"MI{ctr}P"; ctr+=1
<<<<<<< HEAD
        # Support both $...$ and \(...\) syntax
        latex_code = m.group(1) or m.group(2)
        latex_stripped = latex_code.strip()
        
        # [Key Fix] Use image rendering for subscript(_) or superscript(^)
        # Because QTextBrowser cannot properly display MathML <msup> and <msub>
        if '_' in latex_stripped or '^' in latex_stripped or '\\begin{matrix}' in latex_stripped or '\\begin{pmatrix}' in latex_stripped:
            # inline=True: Use inline style, aligned with text
            ph_map[k] = latex_to_base64_block(latex_stripped, font_size=11, dpi=120, max_width_px=400, inline=True)
        else:
            ph_map[k] = latex_to_mathml_inline(latex_stripped)
        return k

    # [Key Enhancement] Apply regex patterns for block and inline math 
    text = re.sub(r'(?:\$\$([\s\S]*?)\$\$)|(?:\\\[([\s\S]*?)\\\])', rep_blk, text)
    text = re.sub(r'(?:(?<!\\)\$([^$]+?)(?<!\\)\$)|(?:\\\([\s\S]*?\\\))', rep_inl, text)
=======
        # 兼容 $...$ 和 \(...\)
        latex_code = m.group(1) or m.group(2)
        ph_map[k] = latex_to_mathml_inline(latex_code.strip())
        return k

    # [关键升级] 
    text = re.sub(r'(?:\$\$([\s\S]*?)\$\$)|(?:\\\[([\s\S]*?)\\\])', rep_blk, text)
    text = re.sub(r'(?:(?<!\\)\$([^\$\n]+?)(?<!\\)\$)|(?:\\\((.*?)\\\))', rep_inl, text)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    
    md_converter.reset()
    html = md_converter.convert(text)
    
    html = wrap_code_with_table(html)
    
    for k, v in ph_map.items(): html = html.replace(k, v)
    return HTML_WRAPPER.format(content=html)


# ============================================================
# TokenManager class (unchanged)
# ============================================================
class TokenManager:
    def __init__(self, filepath= utils.get_usr_dir()/"token_stats.json"):
        self.filepath = filepath
        
<<<<<<< HEAD
        # Default initialization
=======
        # 默认初始化
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.total_tokens = 0
        self.today_tokens = 0
        self.last_date = datetime.now().strftime("%Y-%m-%d")
        
<<<<<<< HEAD
        # Attempt to load data
        self.load_data()

    # ------------------------------------------------------------------------
    # Load Data from File
    # ------------------------------------------------------------------------
    def load_data(self):
        """
        Load data from file.
        Enhanced: Auto-detect old 'currency' data (float), reset to 0 if found.
=======
        # 尝试加载
        self.load_data()

    def load_data(self):
        """
        加载数据。
        增强功能：自动检测旧的'金额'数据(float)，如果发现则重置为0。
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        """
        path = Path(self.filepath)
        
        if not path.exists():
<<<<<<< HEAD
            return  # File doesn't exist, keep default 0
=======
            return # 文件不存在，保持默认的 0
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                raw_total = data.get("total", 0)
                raw_today = data.get("today", 0)
                
<<<<<<< HEAD
                # [Key Logic] Check if float (indicates old currency data)
                # Reset if Total or Today is float
=======
                # [关键逻辑] 检查是否为小数 (说明是旧的金额数据)
                # 只要 Total 或 Today 是浮点数，或者小于 1 但不为 0 (说明是几分钱)，就重置
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                if isinstance(raw_total, float) or isinstance(raw_today, float):
                    print("[INFO] Detected old currency data (floats). Resetting to 0 for Token tracking.")
                    self.reset_to_zero()
                    return

                self.total_tokens = int(raw_total)
                self.today_tokens = int(raw_today)
                self.last_date = data.get("date", self.last_date)
                
<<<<<<< HEAD
                self.check_date_reset()
=======
                self._check_date_reset()
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                
        except Exception as e:
            print(f"[WARN] Data file error: {e}. Resetting to 0.")
            self.reset_to_zero()

<<<<<<< HEAD
    # ------------------------------------------------------------------------
    # Reset to Zero
    # ------------------------------------------------------------------------
    def reset_to_zero(self):
        """Force reset all data to 0 and save"""
=======
    def reset_to_zero(self):
        """强制重置所有数据为 0 并保存"""
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.total_tokens = 0
        self.today_tokens = 0
        self.last_date = datetime.now().strftime("%Y-%m-%d")
        self.save_data()

<<<<<<< HEAD
    # ------------------------------------------------------------------------
    # Check Date Reset
    # ------------------------------------------------------------------------
    def check_date_reset(self):
        """Check date, reset today's count if day changed"""
=======
    def _check_date_reset(self):
        """检查日期，如果跨天则重置今日计数"""
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        current_date = datetime.now().strftime("%Y-%m-%d")
        if current_date != self.last_date:
            self.today_tokens = 0
            self.last_date = current_date
            self.save_data() 

<<<<<<< HEAD
    # ------------------------------------------------------------------------
    # Add Token Usage
    # ------------------------------------------------------------------------
    def add_usage(self, usage_amount):
        self.check_date_reset()
        # Ensure the added amount is an integer
=======
    def add_usage(self, usage_amount):
        self._check_date_reset()
        # 确保加进去的是整数
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        usage_amount = int(usage_amount)
        self.total_tokens += usage_amount
        self.today_tokens += usage_amount
        self.save_data()
        return self.total_tokens, self.today_tokens

<<<<<<< HEAD
    # ------------------------------------------------------------------------
    # Save Data to File
    # ------------------------------------------------------------------------
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    def save_data(self):
        data = {
            "total": self.total_tokens,
            "today": self.today_tokens,
            "date": self.last_date
        }
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[ERR] Failed to save token stats: {e}")


# ============================================================
# AIChatWorker (unchanged behavior, kept for context)
# ============================================================
class AIChatWorker(QThread):
    """
<<<<<<< HEAD
    Generic AI chat worker thread.
    Supports all OpenAI-compatible APIs: OpenRouter, DeepSeek, OpenAI, Ollama, etc.
    """
    # Signal: Send processed content back to UI
    finished = Signal(dict, object) 
    # Signal: Send token usage statistics
=======
    通用的 AI 聊天工作线程。
    支持 OpenRouter, DeepSeek, OpenAI, Ollama 等所有兼容 OpenAI 格式的 API。
    """
    # 信号：发送处理后的内容回 UI
    finished = Signal(dict, object) 
    # 信号：发送 Token 消耗统计
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    stats_updated = Signal(int)

    def __init__(self, api_key, model, base_url, parent=None):
        super().__init__(parent)
        self.api_key = api_key
        self.model = model
<<<<<<< HEAD
        self.base_url = base_url  # Dynamic API address
        self.queue = Queue()
        self._running = True

    # ------------------------------------------------------------------------
    # Add Task to Queue
    # ------------------------------------------------------------------------
    def add_task(self, msgs, bubble):
        """Add task to queue"""
        self.queue.put((msgs, bubble))

    # ------------------------------------------------------------------------
    # Worker Thread Main Loop
    # ------------------------------------------------------------------------
    def run(self):
        while self._running:
            try:
                # Get task from queue, timeout prevents blocking thread exit
=======
        self.base_url = base_url  # 动态 API 地址
        self.queue = Queue()
        self._running = True

    def add_task(self, msgs, bubble):
        """添加发送任务"""
        self.queue.put((msgs, bubble))

    def run(self):
        while self._running:
            try:
                # 从队列获取任务，超时防止阻塞线程退出
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                task = self.queue.get(timeout=0.5)
            except Empty:
                continue
            
            if task is None:
                break
                
            msgs, bubble = task
            try:
                # print(f"[INFO] Worker sending request to: {self.base_url} | Model: {self.model}")
                
<<<<<<< HEAD
                # Send request (using dynamic Base URL)
=======
                # 发送请求 (使用动态 Base URL)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                resp = requests.post(
                    self.base_url, 
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model, 
                        "messages": msgs, 
                        "temperature": 0.7
                    }, 
                    timeout=60
                )
                resp.raise_for_status()
                
<<<<<<< HEAD
                # Parse response
                response_data = resp.json()
                content = response_data['choices'][0]['message']['content']
                
                # Extract token statistics
=======
                # 解析响应
                response_data = resp.json()
                content = response_data['choices'][0]['message']['content']
                
                # 提取 Token 统计
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                if 'usage' in response_data:
                    total_tokens = response_data['usage']['total_tokens']
                    self.stats_updated.emit(total_tokens)

                if self._running:
<<<<<<< HEAD
                    # Render on main thread via BubbleMessage.set_content / renderLocal.
                    # Do NOT call process_mixed_content here: QThread (LatexFetchThread)
                    # must be started from the GUI thread, and latex_ready must be wired
                    # after the bubble leaves the "Thinking..." state.
                    self.finished.emit(
                        {"raw_text": content, "images": None},
=======
                    # 3. 【关键恢复】在后台线程进行渲染！
                    # ------------------------------------------------------
                    # 这里的 process_mixed_content 包含了 latex 转图片、markdown 转 HTML
                    # 耗时操作都在这里做完，不会卡主界面
                    html_output = process_mixed_content(content)
                    
                    # 4. 发送结果 (包含渲染好的 HTML)
                    # ------------------------------------------------------
                    self.finished.emit(
                        {"html": html_output, "raw_text": content, "images": None}, 
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                        bubble
                    )
                    
            except Exception as e:
                print(f"[Error] AI Worker Failed: {e}")
                if self._running:
                    self.finished.emit(
<<<<<<< HEAD
                        {"raw_text": str(e), "images": None},
=======
                        {"html": f"<p style='color:red'>Error: {e}</p>", "raw_text": str(e), "images": None}, 
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                        bubble
                    )
            finally:
                self.queue.task_done()

<<<<<<< HEAD
    # ------------------------------------------------------------------------
    # Stop Worker Thread
    # ------------------------------------------------------------------------
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    def stop(self):
        self._running = False
        self.queue.put(None)
        self.quit()
        self.wait()

<<<<<<< HEAD
    # ------------------------------------------------------------------------
    # Update Configuration Dynamically
    # ------------------------------------------------------------------------
    def update_config(self, new_api_key, new_base_url, new_model):

        """Dynamically update config without restarting thread"""
=======
    def update_config(self, new_api_key, new_base_url, new_model):

        """动态更新配置，无需重启线程"""
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

        self.api_key = new_api_key
        self.base_url = new_base_url
        self.model = new_model

        print(f"[INFO] Worker config updated: {self.model} @ {self.base_url}")



# ============================================================
# Operation_Chat_Controller
# - adds a robust file resolution helper `resolve_chat_file`
# - uses that helper when opening chat files so UI/disk name mismatch is tolerated
# ============================================================

class Operation_Chat_Controller:

    def __init__(self, main_window, model="openai/gpt-4o"):

        # References to main window components
<<<<<<< HEAD
        self.main_window     = main_window
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.chat_window     = main_window.chat_window
        self.scroll_area     = main_window.chat_window.scroll_area
        self.result_display  = main_window.chat_window.result_layout
        self.side_panel      = main_window.side_panel
        self.setting_window  = main_window.setting_page


        # Get the initial model from the tool bar
        self.model           = main_window.tool_bar.get_current_AI_model()       
        self.model_logo      = main_window.tool_bar.get_current_AI_model_logo()                                              


        # Get the API Key and base URL from settings
        self.api_key  = self.setting_window.get_api_key()
        self.base_url = self.setting_window.get_base_url()  


        self.current_chat_file = None
        self.active_chat_path = None
        self.chat_history = []
        
        # 1. Initialize Token Manager
        self.token_manager = TokenManager() 

        # 2. Initialize Worker
        print(f"[INFO] Initializing AIChatWorker with model: {self.model}, base_url: {self.base_url}")
        print(f"[INFO] Using API Key: {self.api_key}")
        self.worker = AIChatWorker(self.api_key, self.model, self.base_url)

        # 3. Connect Signals
        # worker.finished emits (reply_dict, bubble_widget)
<<<<<<< HEAD
        self.worker.finished.connect(self.on_ai_reply)
=======
        self.worker.finished.connect(self._on_ai_reply)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        
        # [NEW] Connect token stats signal
        self.worker.stats_updated.connect(self.handle_token_update)
        
        self.worker.start()
        
        # Optional: Update UI with loaded stats on startup
        self.handle_token_update(0) 

    # [NEW] Handle Token Updates
<<<<<<< HEAD
    # ========================================================================
    # Handle Token Usage Updates
    # ========================================================================
    def handle_token_update(self, current_usage):
        """
        Handle token usage updates from the worker.
=======
    def handle_token_update(self, current_usage):
        """
        Slot to handle token usage updates from the worker.
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        """
        # 1. Update data persistence
        total, today = self.token_manager.add_usage(current_usage)
        
        # 2. Update UI
        # Assuming 'update_tokens' is defined in your SidePanel class
        if hasattr(self.side_panel, 'update_tokens'):
            self.side_panel.update_tokens(current_usage, total, today)
        else:
            print("[WARN] SidePanel does not have 'update_tokens' method.")


    # Update the model for chat controller
<<<<<<< HEAD
    # ========================================================================
    # Update Model Configuration
    # ========================================================================
    def update_model_for_chat_controller(self, new_model, new_model_icon=None):
=======
    def update_model_for_chat_controller(self, new_model, new_model_icon):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

        print("[INFO] Operation_Chat_Controller: model updated to", new_model)

        self.model = new_model
<<<<<<< HEAD
        if new_model_icon is not None:
            self.model_logo = new_model_icon
        elif hasattr(self, "main_window") and hasattr(self.main_window, "tool_bar"):
            self.model_logo = self.main_window.tool_bar.get_current_AI_model_logo()
=======
        self.model_logo = new_model_icon
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

        # Also update worker's model
        # Get the new API Key and base URL from settings
        # If the worker exists, update its config
        new_key = self.setting_window.get_api_key()
        new_url = self.setting_window.get_base_url()

<<<<<<< HEAD
        self.api_key = new_key
        self.base_url = new_url

=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        print(f"[INFO] Updating AIChatWorker with model: {self.model}, new_url: {new_url}")
        print(f"[INFO] Updating API Key: {new_key}")

        if self.worker:
            self.worker.update_config(new_key, new_url, new_model)


    # =========================================================================
    # File helpers: robust chat file resolution
    # - resolve_chat_file will attempt exact and fuzzy matches before giving up.
    # =========================================================================
<<<<<<< HEAD
    # ========================================================================
    # Resolve Chat File Path with Fuzzy Matching
    # ========================================================================
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    def resolve_chat_file(self, folder: str, chat_title: str) -> Path:
        """
        Try to find the correct chat JSON file on disk for the requested folder + chat_title.
        Returns a Path if found, else a Path that doesn't exist (so caller can act).
        Resolution strategy:
          1. Exact match: folder/chat_title.json
          2. Sanitized match: folder/sanitize(chat_title).json
          3. Case-insensitive stems: compare sanitized stems
          4. Inspect JSON 'title' field inside files for matches
        This helps when UI title and filesystem filename drift apart (e.g. manual rename or encoding).
        """
        folder_path = Path("ChatHistory") / folder
        if not folder_path.exists() or not folder_path.is_dir():
            return folder_path / f"{chat_title}.json"  # non-existing path

        # helper sanitization
        def _sanitize(s: str):
            if not isinstance(s, str):
                s = str(s)
            s = re.sub(r'[\/\\\:\*\?\"\<\>\|]', '_', s)
            s = re.sub(r'\s+', ' ', s).strip()
            s = s.rstrip(' .')
            return s

        cand_exact = folder_path / f"{chat_title}.json"
        if cand_exact.exists():
            return cand_exact

        cand_sanitized = folder_path / f"{_sanitize(chat_title)}.json"
        if cand_sanitized.exists():
            return cand_sanitized

        # list all jsons and try to match sanitized stems
        all_jsons = list(folder_path.glob("*.json"))
        target_norm = _sanitize(chat_title).lower()
        for p in all_jsons:
            if _sanitize(p.stem).lower() == target_norm:
                return p

        # last resort: inspect 'title' field inside JSON files
        for p in all_jsons:
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and data.get("title", "") == chat_title:
                        return p
            except Exception:
                continue

        # not found
        return folder_path / f"{chat_title}.json"


<<<<<<< HEAD
    # ========================================================================
    # Ensure Chat File Exists
    # ========================================================================
    def ensure_chat_file(self):
=======
    def _ensure_chat_file(self):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        """
        Ensures a chat JSON file exists for the current chat window.
        If current_chat_file already exists on disk, keep it.
        Otherwise create a new file under active folder.
        """
        # 1. If file exists, return
        if self.current_chat_file and Path(self.current_chat_file).exists():
            return

        # 2. Create new file logic
        folder = self.side_panel.active_folder or "Default folder"
        base_path = Path("ChatHistory") / folder
        base_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = base_path / f"Chat {timestamp}.json"

        init_data = {
            "title": f"Chat {timestamp}",
            "folder": folder,
            "messages": []
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(init_data, f, ensure_ascii=False, indent=2)

        self.current_chat_file = str(file_path)
        self.side_panel.save_chat_to_folder(folder, title=init_data["title"])


    # ---------------------------------------------------------
    # send_message, _get_image_data_uri, _history_to_messages unchanged
    # (we keep your original behavior; only the file resolution was enhanced)
    # ---------------------------------------------------------
<<<<<<< HEAD
    # ========================================================================
    # Send Message to AI
    # ========================================================================
    def send_message(self, text: str, images: list = None):
        """
        Send message to AI.
        :param text: Text content
        :param images: Image list (Base64 string list or file path list)
        """
        # 1. Modified validation: return only if no text AND no images
        # This allows users to send images without text
        if not text.strip() and not images: 
            return
            
        self.ensure_chat_file()

        w = max(100, self.scroll_area.viewport().width() - 40)
        
        # 2. Modified record saving: pass real images data, not hardcoded None
        self.append_record("user", {"text": text, "images": images})

        # 3. Modified UI creation: pass images to BubbleMessage
        user_bubble = BubbleMessage(
            text=text, 
            images=images,  # <--- Key: Pass images here so UI will display them
=======
    def send_message(self, text: str, images: list = None):

        if not text.strip() and not images: 
            return
            
        self._ensure_chat_file()

        w = max(100, self.scroll_area.viewport().width() - 40)
        
        self._append_record("user", {"text": text, "images": images})

        user_bubble = BubbleMessage(
            text=text, 
            images=images,   
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            is_user=True, 
            parent_width=w
        )
        self.result_display.insertWidget(self.result_display.count()-2, user_bubble)

<<<<<<< HEAD
        # 4. AI bubble stays unchanged
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        ai_bubble = BubbleMessage(
            text="Thinking...", 
            is_user=False, 
            ai_logo=self.model_logo, 
            model_name=self.model, 
            parent_width=w
        )
        self.result_display.insertWidget(self.result_display.count()-2, ai_bubble)

<<<<<<< HEAD
        QTimer.singleShot(0, self.update_all_bubbles_width)
        
        # 5. Send to Worker (Worker reads saved records via history_to_messages)
        # As long as step 2 saved images, history_to_messages will auto-read and send to API
        self.worker.add_task(self.history_to_messages(), ai_bubble)
        
        self.scroll_to_bottom()


    # ========================================================================
    # Scroll Chat View to Bottom
    # ========================================================================
    def scroll_to_bottom(self):
=======
        QTimer.singleShot(0, self._update_all_bubbles_width)

        self.worker.add_task(self._history_to_messages(), ai_bubble)
        
        self._scroll_to_bottom()


    def _scroll_to_bottom(self):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        QTimer.singleShot(0, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))


<<<<<<< HEAD
    # ========================================================================
    # Handle AI Reply
    # ========================================================================
    def on_ai_reply(self, reply: dict, ai_bubble: BubbleMessage):
        """
        Handle AI reply.
        Fixed empty content issue: added raw_text processing logic.
        """
        # 1. Persist and save record
        raw_text = reply.get("raw_text", "")
        
        # [Key Fix] Remove <think> tags before saving to avoid persisting thinking content
        clean_text = re.sub(r'<think>.*?</think>\s*', '', raw_text, flags=re.DOTALL)
        
        self.append_record("assistant", 
                            {"text": clean_text, "images": None}, 
                            model_name=self.model)

        # 2. Defensive programming: create new bubble if missing
=======
    def _on_ai_reply(self, reply: dict, ai_bubble: BubbleMessage):

        raw_text = reply.get("raw_text", "")
        self._append_record("assistant", 
                            {"text": raw_text, "images": None}, 
                            model_name=self.model)

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        if ai_bubble is None:
            w = max(100, self.scroll_area.viewport().width() - 40)
            ai_bubble = BubbleMessage(
                text="Thinking...", is_user=False,
                ai_logo=self.model_logo, 
                model_name=self.model,
                parent_width=w
            )
            self.result_display.insertWidget(self.result_display.count()-2, ai_bubble)

<<<<<<< HEAD
        # 3. Connect scroll signal
        try:
            ai_bubble.content_updated.connect(
                lambda: QTimer.singleShot(0, self.scroll_to_bottom),
=======
        try:
            ai_bubble.content_updated.connect(
                lambda: QTimer.singleShot(0, self._scroll_to_bottom),
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                Qt.SingleShotConnection
            )
        except Exception:
            pass

<<<<<<< HEAD
        # 4. Render on GUI thread (same path as loading history from file)
        ai_bubble.set_content(clean_text)

        # 5. Scroll to bottom
        QTimer.singleShot(0, self.scroll_to_bottom)


    # ========================================================================
    # Append Message Record to Chat History
    # ========================================================================
    def append_record(self, role, content, model_name=None):
        """
        Save message to JSON. Added model_name parameter to record model name.
        """
        if self.current_chat_file: 
            # Build message dictionary
            msg_data = {"role": role, **content}
            
            # If model name provided (usually AI reply), save it
=======
        html_content = reply.get("html")
        
        if html_content:
            ai_bubble.set_pre_rendered_content(html_content)
        else:

            ai_bubble.set_content(raw_text)

        QTimer.singleShot(0, self._scroll_to_bottom)


    def _append_record(self, role, content, model_name=None):

        if self.current_chat_file: 

            msg_data = {"role": role, **content}
            
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            if model_name:
                msg_data["model"] = model_name
                
            self.chat_history.append(msg_data)
            
            try:
                Path(self.current_chat_file).write_text(
                    json.dumps(self.chat_history, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )
            except Exception as e:
                print(f"[ERR] Failed to write chat history: {e}")

    # ... helper for images (unchanged) ...
<<<<<<< HEAD
    # ========================================================================
    # Get Image Data URI
    # ========================================================================
    def get_image_data_uri(self, image_source):
        """
        Helper function: Convert image source (path or Base64) to Data URI format required by API.
        Format example: data:image/png;base64,iVBORw0K...
        """
        # 1. If already Data URI (data:image/...), return directly
        if image_source.startswith("data:"):
            return image_source

        # 2. If local file path, read file and convert
=======
    def _get_image_data_uri(self, image_source):

        if image_source.startswith("data:"):
            return image_source

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        path = Path(image_source)
        if path.is_file():
            try:
                mime_type, _ = mimetypes.guess_type(path)
<<<<<<< HEAD
                if not mime_type: mime_type = "image/png"  # Default fallback
=======
                if not mime_type: mime_type = "image/png" # fallback
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                
                with open(path, "rb") as image_file:
                    base64_encoded = base64.b64encode(image_file.read()).decode('utf-8')
                    return f"data:{mime_type};base64,{base64_encoded}"
            except Exception as e:
                print(f"[ERR] Failed to load image file: {e}")
                return None

<<<<<<< HEAD
        # 3. If pure Base64 string (no prefix), assume PNG and add prefix
        # Simple check: Base64 is usually long and has no path separators
        if len(image_source) > 200 and "/" not in image_source[:50]: 
             return f"data:image/png;base64,{image_source}"

        # 4. Other cases (possibly invalid path), return None
        return None

    # ========================================================================
    # Convert Chat History to API Message Format
    # ========================================================================
    def history_to_messages(self):
        """
        Convert chat history to OpenRouter/OpenAI API standard format.
        Contains robust image processing logic to prevent 400 errors.
        """

        # 1. Get user's System Prompt from settings (persona)
        # Default might be "You are a helpful assistant."
        user_persona = self.setting_window.get_system_prompt()

        # 2. Define [Mandatory format instructions]
        # This tells AI: must use LaTeX, must wrap with $ and $$
=======

        if len(image_source) > 200 and "/" not in image_source[:50]: 
             return f"data:image/png;base64,{image_source}"

        return None

    def _history_to_messages(self):

        user_persona = self.setting_window.get_system_prompt()


>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        latex_instruction = (
            "\n\n[IMPORTANT: LATEX RENDERING RULES]\n"
            "1. All math MUST be valid LaTeX. No Unicode symbols (e.g., use $x^2$ NOT x²).\n"
            "2. Inline math delimiter: single $ only. Forbidden: \\( ... \\).\n"
            "3. Block math delimiter: double $$ only. Forbidden: \\[ ... \\].\n"
            "4. Do NOT wrap equations in markdown code blocks (```).\n"
            "5. Do NOT escape the dollar signs.\n"
<<<<<<< HEAD
            "6. Ensure block math ($$) starts and ends on its own line.\n"
            "7. ALWAYS use block math ($$) for any matrices (e.g., \\begin{pmatrix}, \\begin{matrix}, etc.). Do NOT use inline math ($) for matrices."
        )

        # 3. Concatenate final System Prompt
        final_system_message = user_persona + latex_instruction

        # 4. Build message list
=======
            "6. Ensure block math ($$) starts and ends on its own line."
        )

        final_system_message = user_persona + latex_instruction

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        msgs = [
            {"role": "system", "content": final_system_message}
        ]
        
<<<<<<< HEAD
        # Check if "Send History" checkbox is enabled
        send_history = False
        if hasattr(self.chat_window, 'send_history_cb'):
            send_history = self.chat_window.send_history_cb.isChecked()

        if send_history:
            # Send full conversation history
            for x in self.chat_history:
                role = x["role"]
                text = x.get("text", "")
                images = x.get("images", [])

                if not images:
                    msgs.append({"role": role, "content": text})
                else:
                    content_list = []
                    if text and str(text).strip():
                        content_list.append({"type": "text", "text": str(text)})
                    for img in images:
                        data_uri = self.get_image_data_uri(img)
                        if data_uri:
                            content_list.append({"type": "image_url", "image_url": {"url": data_uri}})
                    if content_list:
                        msgs.append({"role": role, "content": content_list})
        else:
            # Only send the current user message (no history)
            if self.chat_history:
                last = self.chat_history[-1]
                role = last["role"]
                text = last.get("text", "")
                images = last.get("images", [])

                if not images:
                    msgs.append({"role": role, "content": text})
                else:
                    content_list = []
                    if text and str(text).strip():
                        content_list.append({"type": "text", "text": str(text)})
                    for img in images:
                        data_uri = self.get_image_data_uri(img)
                        if data_uri:
                            content_list.append({"type": "image_url", "image_url": {"url": data_uri}})
                    if content_list:
                        msgs.append({"role": role, "content": content_list})
=======
        for x in self.chat_history:
            role = x["role"]
            text = x.get("text", "")
            images = x.get("images", [])

            if not images:
                msgs.append({"role": role, "content": text})
            
            else:
                content_list = []
                
                if text and str(text).strip():
                    content_list.append({"type": "text", "text": str(text)})
                
                for img in images:

                    data_uri = self._get_image_data_uri(img)
                    
                    if data_uri:
                        content_list.append({
                            "type": "image_url",
                            "image_url": {
                                "url": data_uri
                            }
                        })
                    else:
                        print(f"[WARN] Skipping invalid image source in history.")

                if content_list:
                    msgs.append({"role": role, "content": content_list})
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                
        return msgs
    



<<<<<<< HEAD
    # ========================================================================
    # Clear Chat History
    # ========================================================================
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    def clear_history(self):
        if self.active_chat_path: self.active_chat_path.unlink(missing_ok=True)
        self.active_chat_path = None; self.chat_history = []

<<<<<<< HEAD
    # ========================================================================
    # Cleanup Resources
    # ========================================================================
    def cleanup(self): 
        if self.worker: self.worker.stop()

    # ========================================================================
    # Update All Bubble Widths on Window Resize
    # ========================================================================
    def update_all_bubbles_width(self):
=======
    def cleanup(self): 
        if self.worker: self.worker.stop()

    def _update_all_bubbles_width(self):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        try:
            w = max(100, self.scroll_area.viewport().width() - 40)
            for i in range(self.result_display.count()):
                item = self.result_display.itemAt(i)
                if item is None: continue
                wid = item.widget()
                if isinstance(wid, BubbleMessage):
                    wid.update_max_width(w)
<<<<<<< HEAD
            QTimer.singleShot(0, self.scroll_to_bottom)
        except Exception:
            pass

    # ========================================================================
    # Handle New Chat Creation
    # ========================================================================
    def handle_new_chat(self):

        # Fix: use current_chat_file consistently
=======
            QTimer.singleShot(0, self._scroll_to_bottom)
        except Exception:
            pass

    def handle_new_chat(self):
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
        self.chat_window.clear_all_messages()
        self.current_chat_file = None 

        now = datetime.now()
        chat_title = f"Chat {now.strftime('%Y-%m-%d %H-%M-%S')}"
        folder_name = self.side_panel.active_folder or "Default folder"

        folder_path = self.side_panel.storage_root / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)

        chat_file = folder_path / f"{chat_title}.json"
        chat_data = {"title": chat_title, "folder": folder_name, "messages": []}

        try:
            with open(chat_file, "w", encoding="utf-8") as f:
                json.dump(chat_data, f, ensure_ascii=False, indent=2)
<<<<<<< HEAD
            self.current_chat_file = str(chat_file) # Fix: Update the main tracker
=======
            self.current_chat_file = str(chat_file) 
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            print(f"[INFO] New chat file created at: {chat_file}")
        except Exception as e:
            print(f"Failed to create new chat file: {e}")

        self.side_panel.save_chat_to_folder(folder_name, title=chat_title, save_json=False)
        self.side_panel.refresh_chat_list()

<<<<<<< HEAD
        # Adjust the chat input container position
        self.chat_window.messages_count = 0     # Update the message count in chat_window
        self.chat_window.adjust_input_height()
        self.chat_window.update_input_container_position()

    # ========================================================================
    # Handle Opening Existing Chat File
    # ========================================================================
=======
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
    def handle_open_chat_file(self, folder, chat_title):
        """
        Open a chat file and render its messages into the chat window.
        Enhanced: uses resolve_chat_file to handle mismatches between UI title and actual filename.
        """
        # Try to resolve the file robustly
        chat_file = self.resolve_chat_file(folder, chat_title)

        if not chat_file.exists():
            print(f"[WARN] Chat file not found (after fallback search): {chat_file}")
            return

        self.current_chat_file = str(chat_file)
        self.chat_history = [] 
        self.chat_window.clear_all_messages()

        try:
            with open(chat_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return

        if isinstance(data, dict):
            messages = data.get("messages", [])
        elif isinstance(data, list):
            messages = data
        else:
            return

        w = max(100, self.scroll_area.viewport().width() - 40)
        
        for msg in messages:
<<<<<<< HEAD
            # 1. Parse basic fields
=======

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            role = msg.get("role", "user")
            text = msg.get("text", "")
            images = msg.get("images", [])
            
<<<<<<< HEAD
            # [Key Fix] Remove <think> tags when loading history
            if role == "assistant":
                original_text = text
                text = re.sub(r'<think>.*?</think>\s*', '', text, flags=re.DOTALL)
                if '<think>' in original_text:
                    print(f"[DEBUG handle_open_chat_file] Removed <think> tags, original length: {len(original_text)}, cleaned length: {len(text)}")
            
            # 2. [Key Modification] Try to read 'model' field
            # If old history record lacks this field, default to current selected model or "AI"
            saved_model_name = msg.get("model", self.model)

            self.chat_history.append({"role": role, "text": text, "images": images, "model": saved_model_name})

            # 3. Create bubble
=======
            saved_model_name = msg.get("model", self.model) 

            self.chat_history.append({"role": role, "text": text, "images": images, "model": saved_model_name})

>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
            bubble = BubbleMessage(
                text=text,
                images=images,
                is_user=(role=="user"),
                parent_width=w,
<<<<<<< HEAD
                # If assistant, pass the read saved_model_name
                model_name=saved_model_name if role=="assistant" else "User", 
                # Note: ai_logo here might still use the current default logo, or you can dynamically search for the logo based on the name
=======
                model_name=saved_model_name if role=="assistant" else "User", 
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
                ai_logo=self.model_logo if role=="assistant" else None
            )
            self.result_display.insertWidget(self.result_display.count()-2, bubble)

<<<<<<< HEAD

        QTimer.singleShot(0, self.scroll_to_bottom)
=======
        QTimer.singleShot(0, self._scroll_to_bottom)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6

        print(f"[INFO] Loaded chat '{chat_title}' from folder '{folder}'")

        if hasattr(self.chat_window, 'messages_count'):
            self.chat_window.messages_count = len(messages)
        
        if hasattr(self.chat_window, 'chat_line_edit'):
            self.chat_window.chat_line_edit.clear()
            self.chat_window.chat_line_edit.setFocus()
            self.chat_window.pending_images.clear()
            self.chat_window.update_input_container_position()
            
<<<<<<< HEAD
        QTimer.singleShot(20, self.update_all_bubbles_width)
=======
        QTimer.singleShot(20, self._update_all_bubbles_width)
>>>>>>> 7d3060bec8fb91675825225fc2820c0a0193ded6
