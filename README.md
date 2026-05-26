# PDF Tool

**Language / 語言 / 语言:** [English](#english) | [繁體中文](#繁體中文) | [简体中文](#简体中文)

---

## English

A Python desktop GUI application for common PDF operations, built with CustomTkinter. Supports English, Traditional Chinese, and Simplified Chinese — default language is English.

### Features

| Button | Description |
|---|---|
| Add PDF | Add one or more PDF files to the list |
| Merge PDF | Merge all listed PDFs into one file |
| Alternate Mix | Interleave pages from two PDFs alternately |
| Split Pages | Split a PDF into individual single-page files |
| Compress PDF | Compress PDF content streams to reduce file size |
| Encrypt PDF | Password-encrypt a PDF |
| To Image | Convert each PDF page to a PNG image |
| Extract Text | Extract all text from a PDF to a `.txt` file |
| Rotate Pages | Rotate all pages by 90°, 180°, or 270° |
| Remove | Remove the selected file from the list |
| Auto Sort | Sort files by number first, then alphabetically |
| Clear List | Clear all files from the list |

### Requirements

```
customtkinter
pypdf
pdf2image
Pillow
```

```bash
pip install customtkinter pypdf pdf2image Pillow
```

> `pdf2image` also requires [Poppler](https://github.com/oschwartz10612/poppler-windows/releases) installed and added to your system PATH.

### Usage

```bash
python PDF_Tool.py
```

1. Click **Add PDF** to load files.
2. Use the sort/move buttons to arrange the order.
3. Click any operation button and choose an output path when prompted.
4. Switch language from the dropdown at the top-right corner.

---

## 繁體中文

以 CustomTkinter 建立的 Python 桌面 GUI 應用程式，提供常見 PDF 操作功能。支援英文、繁體中文與簡體中文，預設語言為英文。

### 功能說明

| 按鈕 | 說明 |
|---|---|
| 加入 PDF | 將一個或多個 PDF 加入列表 |
| 執行合併 | 將列表中所有 PDF 合併為一個檔案 |
| 交替混合 | 將兩個 PDF 的頁面交替合併 |
| 分割頁面 | 將 PDF 拆分為每頁獨立的檔案 |
| 壓縮 PDF | 壓縮 PDF 內容串流以縮小檔案大小 |
| 加密保護 | 為 PDF 設定密碼保護 |
| 轉為圖片 | 將每頁轉換為 PNG 圖片 |
| 提取文字 | 提取 PDF 內所有文字並儲存為 `.txt` |
| 旋轉頁面 | 將所有頁面旋轉 90°、180° 或 270° |
| 移除選取 | 從列表中移除已選取的檔案 |
| 自動排序 | 先按數字排序，再按字母排序 |
| 清空列表 | 清除列表中所有檔案 |

### 安裝需求

```bash
pip install customtkinter pypdf pdf2image Pillow
```

> `pdf2image` 需要另外安裝 [Poppler](https://github.com/oschwartz10612/poppler-windows/releases) 並加入系統 PATH。

### 使用方式

```bash
python PDF_Tool.py
```

1. 點擊「加入 PDF」載入檔案。
2. 使用排序/移動按鈕調整順序。
3. 點擊操作按鈕，並在提示時選擇輸出路徑。
4. 可從右上角下拉選單切換語言。

---

## 简体中文

基于 CustomTkinter 构建的 Python 桌面 GUI 应用，提供常见 PDF 操作功能。支持英文、繁体中文与简体中文，默认语言为英文。

### 功能说明

| 按钮 | 说明 |
|---|---|
| 添加 PDF | 将一个或多个 PDF 添加到列表 |
| 执行合并 | 将列表中所有 PDF 合并为一个文件 |
| 交替混合 | 将两个 PDF 的页面交替合并 |
| 分割页面 | 将 PDF 拆分为每页独立的文件 |
| 压缩 PDF | 压缩 PDF 内容流以减小文件大小 |
| 加密保护 | 为 PDF 设置密码保护 |
| 转为图片 | 将每页转换为 PNG 图片 |
| 提取文字 | 提取 PDF 中所有文字并保存为 `.txt` |
| 旋转页面 | 将所有页面旋转 90°、180° 或 270° |
| 移除选中 | 从列表中移除已选中的文件 |
| 自动排序 | 先按数字排序，再按字母排序 |
| 清空列表 | 清除列表中所有文件 |

### 安装需求

```bash
pip install customtkinter pypdf pdf2image Pillow
```

> `pdf2image` 需要额外安装 [Poppler](https://github.com/oschwartz10612/poppler-windows/releases) 并添加到系统 PATH。

### 使用方法

```bash
python PDF_Tool.py
```

1. 点击「添加 PDF」加载文件。
2. 使用排序/移动按钮调整顺序。
3. 点击操作按钮，并在提示时选择输出路径。
4. 可从右上角下拉菜单切换语言。
