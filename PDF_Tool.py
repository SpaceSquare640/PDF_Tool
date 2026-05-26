import os
import re
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
from pypdf import PdfWriter, PdfReader

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

STRINGS = {
    "en": {
        "title":          "PDF Tool",
        "add_files":      "Add PDF",
        "merge":          "Merge PDF",
        "alt_mix":        "Alternate Mix",
        "split":          "Split Pages",
        "compress":       "Compress PDF",
        "encrypt":        "Encrypt PDF",
        "to_image":       "To Image",
        "to_text":        "Extract Text",
        "rotate":         "Rotate Pages",
        "clear":          "Clear List",
        "move_up":        "Move Up",
        "auto_sort":      "Auto Sort",
        "move_down":      "Move Down",
        "remove":         "Remove",
        "ready":          "Ready",
        "file_count":     "Files: {}",
        "warning":        "Warning",
        "done":           "Done",
        "error":          "Error",
        "warn_min2":      "Please add at least 2 PDF files.",
        "warn_angle":     "Please enter 90, 180, or 270.",
        "merged_ok":      "Merged {} files successfully.",
        "mixed_ok":       "Alternate mix complete.",
        "split_ok":       "Split into {} pages.",
        "compress_ok":    "Compression complete.",
        "encrypt_ok":     "Encryption complete.",
        "image_ok":       "Converted {} pages to PNG.",
        "text_ok":        "Text extracted successfully.",
        "rotate_ok":      "Rotated {}°.",
        "convert_fail":   "Conversion failed: {}",
        "encrypt_title":  "Encrypt",
        "encrypt_prompt": "Enter password:",
        "rotate_title":   "Rotate",
        "rotate_prompt":  "Rotation angle (90 / 180 / 270):",
        "pdf_filter":     "PDF Files",
        "txt_filter":     "Text Files",
    },
    "zh_tw": {
        "title":          "PDF Tool",
        "add_files":      "加入 PDF",
        "merge":          "執行合併",
        "alt_mix":        "交替混合",
        "split":          "分割頁面",
        "compress":       "壓縮 PDF",
        "encrypt":        "加密保護",
        "to_image":       "轉為圖片",
        "to_text":        "提取文字",
        "rotate":         "旋轉頁面",
        "clear":          "清空列表",
        "move_up":        "向上移動",
        "auto_sort":      "自動排序",
        "move_down":      "向下移動",
        "remove":         "移除選取",
        "ready":          "就緒",
        "file_count":     "檔案數量: {}",
        "warning":        "警告",
        "done":           "完成",
        "error":          "錯誤",
        "warn_min2":      "請至少加入 2 個 PDF 檔案。",
        "warn_angle":     "請輸入 90、180 或 270。",
        "merged_ok":      "已合併 {} 個檔案。",
        "mixed_ok":       "交替混合完成。",
        "split_ok":       "已分割為 {} 個頁面。",
        "compress_ok":    "壓縮完成。",
        "encrypt_ok":     "加密完成。",
        "image_ok":       "已轉換 {} 頁為 PNG。",
        "text_ok":        "提取文字成功。",
        "rotate_ok":      "已旋轉 {}°。",
        "convert_fail":   "轉換失敗: {}",
        "encrypt_title":  "加密",
        "encrypt_prompt": "輸入密碼:",
        "rotate_title":   "旋轉",
        "rotate_prompt":  "旋轉角度 (90 / 180 / 270):",
        "pdf_filter":     "PDF 檔案",
        "txt_filter":     "文字檔案",
    },
    "zh_cn": {
        "title":          "PDF Tool",
        "add_files":      "添加 PDF",
        "merge":          "执行合并",
        "alt_mix":        "交替混合",
        "split":          "分割页面",
        "compress":       "压缩 PDF",
        "encrypt":        "加密保护",
        "to_image":       "转为图片",
        "to_text":        "提取文字",
        "rotate":         "旋转页面",
        "clear":          "清空列表",
        "move_up":        "向上移动",
        "auto_sort":      "自动排序",
        "move_down":      "向下移动",
        "remove":         "移除选中",
        "ready":          "就绪",
        "file_count":     "文件数量: {}",
        "warning":        "警告",
        "done":           "完成",
        "error":          "错误",
        "warn_min2":      "请至少添加 2 个 PDF 文件。",
        "warn_angle":     "请输入 90、180 或 270。",
        "merged_ok":      "已合并 {} 个文件。",
        "mixed_ok":       "交替混合完成。",
        "split_ok":       "已分割为 {} 个页面。",
        "compress_ok":    "压缩完成。",
        "encrypt_ok":     "加密完成。",
        "image_ok":       "已转换 {} 页为 PNG。",
        "text_ok":        "提取文字成功。",
        "rotate_ok":      "已旋转 {}°。",
        "convert_fail":   "转换失败: {}",
        "encrypt_title":  "加密",
        "encrypt_prompt": "输入密码:",
        "rotate_title":   "旋转",
        "rotate_prompt":  "旋转角度 (90 / 180 / 270):",
        "pdf_filter":     "PDF 文件",
        "txt_filter":     "文字文件",
    },
}

LANG_DISPLAY = ["English", "繁體中文", "简体中文"]
LANG_CODE    = {"English": "en", "繁體中文": "zh_tw", "简体中文": "zh_cn"}


class PDFTool(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.lang           = "en"
        self.file_list      = []
        self.selected_index = -1
        self._build_ui()

    # ── i18n ───────────────────────────────────────────────────────────────────

    def t(self, key, *args):
        s = STRINGS[self.lang].get(key, key)
        return s.format(*args) if args else s

    def set_language(self, display_name):
        self.lang = LANG_CODE[display_name]
        self._refresh_texts()

    def _refresh_texts(self):
        self.title(self.t("title"))
        self.title_label.configure(text=self.t("title"))
        for key, btn in self.op_buttons.items():
            btn.configure(text=self.t(key))
        for key, btn in self.sort_buttons.items():
            btn.configure(text=self.t(key))
        count = len(self.file_list)
        self.status_bar.configure(
            text=self.t("file_count", count) if count else self.t("ready")
        )

    # ── UI build ───────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.title(self.t("title"))
        self.geometry("950x860")
        self.configure(fg_color="#000B1E")

        # Title row + language selector
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(15, 5))

        self.title_label = ctk.CTkLabel(
            top_frame, text=self.t("title"),
            font=("微軟正黑體", 28, "bold"), text_color="#58A6FF"
        )
        self.title_label.pack(side="left")

        self.lang_combo = ctk.CTkComboBox(
            top_frame, values=LANG_DISPLAY, width=150,
            command=self.set_language,
            fg_color="#1A3A5A", button_color="#2A5A8A",
            dropdown_fg_color="#011627", text_color="#CCE5FF"
        )
        self.lang_combo.set("English")
        self.lang_combo.pack(side="right", pady=5)

        # File list
        list_outer = ctk.CTkFrame(self, fg_color="#011627", corner_radius=10)
        list_outer.pack(pady=5, padx=30, fill="both", expand=True)

        self.file_display = ctk.CTkTextbox(
            list_outer, fg_color="#000000", text_color="#CCE5FF",
            font=("Consolas", 12), activate_scrollbars=True
        )
        self.file_display.pack(pady=15, padx=15, fill="both", expand=True)
        self.file_display.bind("<Button-1>", self._on_click)

        # Sort / move row
        sort_frame = ctk.CTkFrame(self, fg_color="transparent")
        sort_frame.pack(pady=5)

        move_cfg = dict(width=130, fg_color="#1A3A5A", hover_color="#2A5A8A")
        self.sort_buttons = {
            "move_up":   ctk.CTkButton(sort_frame, text=self.t("move_up"),
                                        command=lambda: self.move_item(-1), **move_cfg),
            "auto_sort": ctk.CTkButton(sort_frame, text=self.t("auto_sort"),
                                        command=self.auto_sort, **move_cfg),
            "move_down": ctk.CTkButton(sort_frame, text=self.t("move_down"),
                                        command=lambda: self.move_item(1), **move_cfg),
            "remove":    ctk.CTkButton(sort_frame, text=self.t("remove"),
                                        command=self.remove_selected,
                                        width=130, fg_color="#5A1A1A", hover_color="#8A2A2A"),
        }
        for col, btn in enumerate(self.sort_buttons.values()):
            btn.grid(row=0, column=col, padx=8)

        # Progress bar
        self.progress = ctk.CTkProgressBar(self, width=600, height=8)
        self.progress.set(0)
        self.progress.pack(pady=(8, 2))

        # Operation buttons grid
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(pady=10, padx=30, fill="x")

        op_pairs = [
            ("add_files", self.add_files),
            ("merge",     self.op_merge),
            ("alt_mix",   self.op_alt_mix),
            ("split",     self.op_split),
            ("compress",  self.op_compress),
            ("encrypt",   self.op_encrypt),
            ("to_image",  self.op_to_image),
            ("to_text",   self.op_to_text),
            ("rotate",    self.op_rotate),
            ("clear",     self.clear_all),
        ]

        self.op_buttons = {}
        for i, (key, cmd) in enumerate(op_pairs):
            btn = ctk.CTkButton(
                grid_frame, text=self.t(key), command=cmd,
                fg_color="#003366", hover_color="#00509E",
                font=("微軟正黑體", 14), height=40
            )
            btn.grid(row=i // 3, column=i % 3, padx=10, pady=8, sticky="ew")
            self.op_buttons[key] = btn

        for col in range(3):
            grid_frame.columnconfigure(col, weight=1)

        self.status_bar = ctk.CTkLabel(
            self, text=self.t("ready"), anchor="w", text_color="#8BADC1"
        )
        self.status_bar.pack(side="bottom", fill="x", padx=25, pady=8)

    # ── Selection ──────────────────────────────────────────────────────────────

    def _on_click(self, _event):
        self.file_display.after(10, self._sync_selection)

    def _sync_selection(self):
        try:
            line_text = self.file_display.get(
                "insert linestart", "insert lineend"
            ).replace("• ", "").strip()
            for i, path in enumerate(self.file_list):
                if os.path.basename(path) == line_text:
                    self.selected_index = i
                    self.update_ui(highlight=i)
                    return
        except Exception:
            pass

    # ── UI helpers ─────────────────────────────────────────────────────────────

    def update_ui(self, highlight: int = -1):
        self.file_display.configure(state="normal")
        self.file_display.delete("1.0", "end")
        for i, f in enumerate(self.file_list):
            self.file_display.insert("end", f"• {os.path.basename(f)}\n")
            if i == highlight:
                self.file_display.tag_add("sel_line", f"{i + 1}.0", f"{i + 1}.end")
                self.file_display.tag_config("sel_line", foreground="#FFD700")
        count = len(self.file_list)
        self.status_bar.configure(
            text=self.t("file_count", count) if count else self.t("ready")
        )

    def _run_task(self, fn):
        self.progress.set(0)
        self.progress.start()

        def _worker():
            try:
                fn()
            finally:
                self.after(0, self.progress.stop)
                self.after(0, lambda: self.progress.set(0))

        threading.Thread(target=_worker, daemon=True).start()

    # ── File management ────────────────────────────────────────────────────────

    def auto_sort(self):
        if not self.file_list:
            return

        def key(p):
            n = os.path.basename(p)
            m = re.match(r"(\d+)", n)
            return (0, int(m.group(1)), n.lower()) if m else (1, n.lower(), n)

        self.file_list.sort(key=key)
        self.selected_index = -1
        self.update_ui()

    def move_item(self, direction: int):
        if self.selected_index == -1 or not self.file_list:
            return
        idx, new_idx = self.selected_index, self.selected_index + direction
        if 0 <= new_idx < len(self.file_list):
            self.file_list[idx], self.file_list[new_idx] = (
                self.file_list[new_idx], self.file_list[idx]
            )
            self.selected_index = new_idx
            self.update_ui(highlight=new_idx)

    def add_files(self):
        files = filedialog.askopenfilenames(
            filetypes=[(self.t("pdf_filter"), "*.pdf")]
        )
        if files:
            self.file_list.extend(files)
            self.auto_sort()

    def remove_selected(self):
        if self.selected_index == -1 or not self.file_list:
            return
        self.file_list.pop(self.selected_index)
        self.selected_index = min(self.selected_index, len(self.file_list) - 1)
        self.update_ui(highlight=self.selected_index if self.file_list else -1)

    def clear_all(self):
        self.file_list.clear()
        self.selected_index = -1
        self.update_ui()

    # ── Operations ─────────────────────────────────────────────────────────────

    def op_merge(self):
        if len(self.file_list) < 2:
            messagebox.showwarning(self.t("warning"), self.t("warn_min2"))
            return
        out = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[(self.t("pdf_filter"), "*.pdf")]
        )
        if not out:
            return

        def task():
            writer = PdfWriter()
            for p in self.file_list:
                writer.append(p)
            with open(out, "wb") as f:
                writer.write(f)
            self.after(0, lambda: messagebox.showinfo(
                self.t("done"), self.t("merged_ok", len(self.file_list))
            ))

        self._run_task(task)

    def op_alt_mix(self):
        if len(self.file_list) < 2:
            messagebox.showwarning(self.t("warning"), self.t("warn_min2"))
            return
        out = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[(self.t("pdf_filter"), "*.pdf")]
        )
        if not out:
            return

        def task():
            r1, r2 = PdfReader(self.file_list[0]), PdfReader(self.file_list[1])
            writer = PdfWriter()
            for i in range(max(len(r1.pages), len(r2.pages))):
                if i < len(r1.pages):
                    writer.add_page(r1.pages[i])
                if i < len(r2.pages):
                    writer.add_page(r2.pages[i])
            with open(out, "wb") as f:
                writer.write(f)
            self.after(0, lambda: messagebox.showinfo(self.t("done"), self.t("mixed_ok")))

        self._run_task(task)

    def op_split(self):
        if not self.file_list:
            return
        out_dir = filedialog.askdirectory()
        if not out_dir:
            return

        def task():
            reader = PdfReader(self.file_list[0])
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                with open(os.path.join(out_dir, f"page_{i + 1}.pdf"), "wb") as f:
                    writer.write(f)
            self.after(0, lambda: messagebox.showinfo(
                self.t("done"), self.t("split_ok", len(reader.pages))
            ))

        self._run_task(task)

    def op_compress(self):
        if not self.file_list:
            return
        out = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[(self.t("pdf_filter"), "*.pdf")]
        )
        if not out:
            return

        def task():
            reader = PdfReader(self.file_list[0])
            writer = PdfWriter()
            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)
            with open(out, "wb") as f:
                writer.write(f)
            self.after(0, lambda: messagebox.showinfo(self.t("done"), self.t("compress_ok")))

        self._run_task(task)

    def op_encrypt(self):
        if not self.file_list:
            return
        pwd = simpledialog.askstring(
            self.t("encrypt_title"), self.t("encrypt_prompt"), show="*"
        )
        if not pwd:
            return
        out = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[(self.t("pdf_filter"), "*.pdf")]
        )
        if not out:
            return

        def task():
            reader, writer = PdfReader(self.file_list[0]), PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(pwd)
            with open(out, "wb") as f:
                writer.write(f)
            self.after(0, lambda: messagebox.showinfo(self.t("done"), self.t("encrypt_ok")))

        self._run_task(task)

    def op_to_image(self):
        if not self.file_list:
            return
        out_dir = filedialog.askdirectory()
        if not out_dir:
            return

        def task():
            try:
                from pdf2image import convert_from_path
                images = convert_from_path(self.file_list[0], dpi=150)
                for i, img in enumerate(images):
                    img.save(os.path.join(out_dir, f"page_{i + 1}.png"), "PNG")
                self.after(0, lambda: messagebox.showinfo(
                    self.t("done"), self.t("image_ok", len(images))
                ))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror(
                    self.t("error"), self.t("convert_fail", e)
                ))

        self._run_task(task)

    def op_to_text(self):
        if not self.file_list:
            return
        out = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[(self.t("txt_filter"), "*.txt")]
        )
        if not out:
            return

        def task():
            reader = PdfReader(self.file_list[0])
            text = "\n".join(p.extract_text() or "" for p in reader.pages)
            with open(out, "w", encoding="utf-8") as f:
                f.write(text)
            self.after(0, lambda: messagebox.showinfo(self.t("done"), self.t("text_ok")))

        self._run_task(task)

    def op_rotate(self):
        if not self.file_list:
            return
        angle = simpledialog.askinteger(
            self.t("rotate_title"), self.t("rotate_prompt"), initialvalue=90
        )
        if angle not in (90, 180, 270):
            messagebox.showwarning(self.t("warning"), self.t("warn_angle"))
            return
        out = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[(self.t("pdf_filter"), "*.pdf")]
        )
        if not out:
            return

        def task():
            reader, writer = PdfReader(self.file_list[0]), PdfWriter()
            for page in reader.pages:
                page.rotate(angle)
                writer.add_page(page)
            with open(out, "wb") as f:
                writer.write(f)
            self.after(0, lambda: messagebox.showinfo(
                self.t("done"), self.t("rotate_ok", angle)
            ))

        self._run_task(task)


if __name__ == "__main__":
    app = PDFTool()
    app.mainloop()
