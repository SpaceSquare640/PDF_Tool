import os
import re
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
from pypdf import PdfWriter, PdfReader

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class PDFTool(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PDF Tool")
        self.geometry("950x820")
        self.configure(fg_color="#000B1E")
        self.file_list = []
        self.selected_index = -1
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="PDF Tool", font=("微軟正黑體", 28, "bold"),
                     text_color="#58A6FF").pack(pady=(15, 5))

        list_outer = ctk.CTkFrame(self, fg_color="#011627", corner_radius=10)
        list_outer.pack(pady=5, padx=30, fill="both", expand=True)

        self.file_display = ctk.CTkTextbox(
            list_outer, fg_color="#000000", text_color="#CCE5FF",
            font=("Consolas", 12), activate_scrollbars=True
        )
        self.file_display.pack(pady=15, padx=15, fill="both", expand=True)
        self.file_display.bind("<Button-1>", self._on_click)

        sort_frame = ctk.CTkFrame(self, fg_color="transparent")
        sort_frame.pack(pady=5)

        move_cfg = dict(width=120, fg_color="#1A3A5A", hover_color="#2A5A8A")
        ctk.CTkButton(sort_frame, text="向上移動", command=lambda: self.move_item(-1), **move_cfg).grid(row=0, column=0, padx=8)
        ctk.CTkButton(sort_frame, text="自動排序", command=self.auto_sort, **move_cfg).grid(row=0, column=1, padx=8)
        ctk.CTkButton(sort_frame, text="向下移動", command=lambda: self.move_item(1), **move_cfg).grid(row=0, column=2, padx=8)
        ctk.CTkButton(sort_frame, text="移除選取", command=self.remove_selected,
                      width=120, fg_color="#5A1A1A", hover_color="#8A2A2A").grid(row=0, column=3, padx=8)

        self.progress = ctk.CTkProgressBar(self, width=600, height=8)
        self.progress.set(0)
        self.progress.pack(pady=(8, 2))

        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(pady=10, padx=30, fill="x")

        ops = [
            ("加入 PDF",  self.add_files),
            ("執行合併",  self.op_merge),
            ("交替混合",  self.op_alt_mix),
            ("分割頁面",  self.op_split),
            ("壓縮 PDF",  self.op_compress),
            ("加密保護",  self.op_encrypt),
            ("轉為圖片",  self.op_to_image),
            ("提取文字",  self.op_to_text),
            ("旋轉頁面",  self.op_rotate),
            ("清空列表",  self.clear_all),
        ]

        for i, (text, cmd) in enumerate(ops):
            ctk.CTkButton(
                grid_frame, text=text, command=cmd,
                fg_color="#003366", hover_color="#00509E",
                font=("微軟正黑體", 14), height=40
            ).grid(row=i // 3, column=i % 3, padx=10, pady=8, sticky="ew")

        for col in range(3):
            grid_frame.columnconfigure(col, weight=1)

        self.status_bar = ctk.CTkLabel(self, text="就緒", anchor="w", text_color="#8BADC1")
        self.status_bar.pack(side="bottom", fill="x", padx=25, pady=8)

    # ── Selection ──────────────────────────────────────────────────────────────

    def _on_click(self, _event):
        self.file_display.after(10, self._sync_selection)

    def _sync_selection(self):
        try:
            line_text = self.file_display.get("insert linestart", "insert lineend").replace("• ", "").strip()
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
        self.status_bar.configure(text=f"檔案數量: {len(self.file_list)}" if self.file_list else "就緒")

    def set_status(self, text: str):
        self.status_bar.configure(text=text)
        self.update_idletasks()

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
            self.file_list[idx], self.file_list[new_idx] = self.file_list[new_idx], self.file_list[idx]
            self.selected_index = new_idx
            self.update_ui(highlight=new_idx)

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF 檔案", "*.pdf")])
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
            messagebox.showwarning("警告", "請至少加入 2 個 PDF 檔案")
            return
        out = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF 檔案", "*.pdf")])
        if not out:
            return

        def task():
            writer = PdfWriter()
            for p in self.file_list:
                writer.append(p)
            with open(out, "wb") as f:
                writer.write(f)
            self.after(0, lambda: messagebox.showinfo("完成", f"已合併 {len(self.file_list)} 個檔案"))

        self._run_task(task)

    def op_alt_mix(self):
        if len(self.file_list) < 2:
            messagebox.showwarning("警告", "請至少加入 2 個 PDF 檔案")
            return
        out = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF 檔案", "*.pdf")])
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
            self.after(0, lambda: messagebox.showinfo("完成", "交替混合完成"))

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
            self.after(0, lambda: messagebox.showinfo("完成", f"已分割為 {len(reader.pages)} 個頁面"))

        self._run_task(task)

    def op_compress(self):
        if not self.file_list:
            return
        out = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF 檔案", "*.pdf")])
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
            self.after(0, lambda: messagebox.showinfo("完成", "壓縮完成"))

        self._run_task(task)

    def op_encrypt(self):
        if not self.file_list:
            return
        pwd = simpledialog.askstring("加密", "輸入密碼:", show="*")
        if not pwd:
            return
        out = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF 檔案", "*.pdf")])
        if not out:
            return

        def task():
            reader, writer = PdfReader(self.file_list[0]), PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(pwd)
            with open(out, "wb") as f:
                writer.write(f)
            self.after(0, lambda: messagebox.showinfo("完成", "加密完成"))

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
                self.after(0, lambda: messagebox.showinfo("完成", f"已轉換 {len(images)} 頁為 PNG"))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("錯誤", f"轉換失敗: {e}"))

        self._run_task(task)

    def op_to_text(self):
        if not self.file_list:
            return
        out = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("文字檔案", "*.txt")])
        if not out:
            return

        def task():
            reader = PdfReader(self.file_list[0])
            text = "\n".join(p.extract_text() or "" for p in reader.pages)
            with open(out, "w", encoding="utf-8") as f:
                f.write(text)
            self.after(0, lambda: messagebox.showinfo("完成", "提取文字成功"))

        self._run_task(task)

    def op_rotate(self):
        if not self.file_list:
            return
        angle = simpledialog.askinteger("旋轉", "旋轉角度 (90 / 180 / 270):", initialvalue=90)
        if angle not in (90, 180, 270):
            messagebox.showwarning("警告", "請輸入 90、180 或 270")
            return
        out = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF 檔案", "*.pdf")])
        if not out:
            return

        def task():
            reader, writer = PdfReader(self.file_list[0]), PdfWriter()
            for page in reader.pages:
                page.rotate(angle)
                writer.add_page(page)
            with open(out, "wb") as f:
                writer.write(f)
            self.after(0, lambda: messagebox.showinfo("完成", f"已旋轉 {angle}°"))

        self._run_task(task)


if __name__ == "__main__":
    app = PDFTool()
    app.mainloop()
