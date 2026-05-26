# PDF Tool

A Python desktop GUI application for common PDF operations, built with CustomTkinter.

## Features

| Button | Description |
|---|---|
| 加入 PDF | Add one or more PDF files to the list |
| 執行合併 | Merge all listed PDFs into one file |
| 交替混合 | Interleave pages from two PDFs alternately |
| 分割頁面 | Split a PDF into individual single-page files |
| 壓縮 PDF | Compress PDF content streams to reduce file size |
| 加密保護 | Password-encrypt a PDF |
| 轉為圖片 | Convert each PDF page to a PNG image |
| 提取文字 | Extract all text from a PDF to a `.txt` file |
| 旋轉頁面 | Rotate all pages by 90°, 180°, or 270° |
| 移除選取 | Remove a selected file from the list |
| 自動排序 | Auto-sort files (numeric first, then alphabetical) |
| 清空列表 | Clear all files from the list |

## Requirements

```
customtkinter
pypdf
pdf2image
Pillow
```

Install with:

```bash
pip install customtkinter pypdf pdf2image Pillow
```

> `pdf2image` also requires [Poppler](https://github.com/oschwartz10612/poppler-windows/releases) to be installed and added to your system PATH.

## Usage

```bash
python PDF_Tool.py
```

1. Click **加入 PDF** to load PDF files.
2. Use the sort/move buttons to arrange the order.
3. Click any operation button to process.
4. Choose an output file or folder when prompted.

## Notes

- Long operations run in a background thread — a progress bar is shown while processing.
- Click a filename in the list to select it before using move/remove buttons.
