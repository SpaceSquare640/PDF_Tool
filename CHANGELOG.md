# Changelog

**Language / 語言 / 语言:** [English](#english) | [繁體中文](#繁體中文) | [简体中文](#简体中文)

---

## English

### [1.2.0] - 2026-05-27

#### Added
- **Multi-language support** — UI now supports English (default), Traditional Chinese, and Simplified Chinese
- Language selector dropdown in the top-right corner; all buttons, labels, dialogs, and file filters update instantly on switch

### [1.1.0] - 2026-05-27

#### Added
- **Rotate Pages** — rotate all pages by 90°, 180°, or 270°
- **Remove** — remove individual files from the list without clearing all
- **Progress bar** — animated progress bar displayed during any long-running operation

#### Fixed
- `Compress PDF` previously saved output as `.zip` using PdfWriter (incorrect format); now correctly saves as a compressed `.pdf`
- `Move Up / Move Down` relied on fragile cursor-position text parsing; replaced with a tracked `selected_index` variable

#### Improved
- All PDF operations now run on background threads — UI no longer freezes during processing
- Thread-safe UI updates via `self.after(0, ...)` for all messagebox calls from threads
- Input validation added: merge and alt-mix now warn if fewer than 2 files are loaded
- `extract_text()` now handles pages with no extractable text gracefully
- `_run_task()` helper introduced to eliminate duplicated threading logic
- `auto_sort` sort key is now case-insensitive for alphabetical fallback

### [1.0.0] - Initial Release

#### Added
- GUI built with CustomTkinter (dark mode, blue theme)
- Operations: merge, alternate mix, split, compress, encrypt, convert to image, extract text
- Auto-sort (numeric-first) and manual up/down ordering
- Status bar showing file count

---

## 繁體中文

### [1.2.0] - 2026-05-27

#### 新增
- **多語言支援** — 介面支援英文（預設）、繁體中文、簡體中文
- 右上角新增語言選擇下拉選單；切換後所有按鈕、標籤、對話框與檔案篩選器即時更新

### [1.1.0] - 2026-05-27

#### 新增
- **旋轉頁面** — 可將所有頁面旋轉 90°、180° 或 270°
- **移除選取** — 可單獨移除列表中的檔案，無需清空全部
- **進度條** — 執行長時間操作時顯示動態進度條

#### 修正
- 「壓縮 PDF」原本使用 PdfWriter 存為 `.zip`（格式錯誤），現已修正為輸出壓縮後的 `.pdf`
- 「向上/向下移動」原本依賴不穩定的游標位置文字解析，已改為使用可靠的 `selected_index` 索引追蹤

#### 改善
- 所有 PDF 操作現在均於背景執行緒運行，UI 不再因處理而凍結
- 所有來自執行緒的 messagebox 呼叫均使用 `self.after(0, ...)` 確保執行緒安全
- 合併與交替混合操作新增驗證：檔案數量不足時顯示警告
- `extract_text()` 現可優雅處理無法提取文字的頁面
- 新增 `_run_task()` 輔助方法，消除重複的執行緒邏輯
- `auto_sort` 字母排序回退改為不區分大小寫

### [1.0.0] - 初始版本

#### 新增
- 以 CustomTkinter 建立的 GUI（深色模式、藍色主題）
- 功能：合併、交替混合、分割、壓縮、加密、轉圖片、提取文字
- 自動排序（數字優先）與手動上下移動
- 底部狀態列顯示檔案數量

---

## 简体中文

### [1.2.0] - 2026-05-27

#### 新增
- **多语言支持** — 界面支持英文（默认）、繁体中文、简体中文
- 右上角新增语言选择下拉菜单；切换后所有按钮、标签、对话框与文件过滤器即时更新

### [1.1.0] - 2026-05-27

#### 新增
- **旋转页面** — 可将所有页面旋转 90°、180° 或 270°
- **移除选中** — 可单独移除列表中的文件，无需清空全部
- **进度条** — 执行耗时操作时显示动态进度条

#### 修复
- 「压缩 PDF」原本使用 PdfWriter 保存为 `.zip`（格式错误），现已修正为输出压缩后的 `.pdf`
- 「向上/向下移动」原本依赖不稳定的光标位置文字解析，已改为使用可靠的 `selected_index` 索引追踪

#### 改善
- 所有 PDF 操作现在均在后台线程运行，UI 不再因处理而冻结
- 所有来自线程的 messagebox 调用均使用 `self.after(0, ...)` 确保线程安全
- 合并与交替混合操作新增验证：文件数量不足时显示警告
- `extract_text()` 现可优雅处理无法提取文字的页面
- 新增 `_run_task()` 辅助方法，消除重复的线程逻辑
- `auto_sort` 字母排序回退改为不区分大小写

### [1.0.0] - 初始版本

#### 新增
- 以 CustomTkinter 构建的 GUI（深色模式、蓝色主题）
- 功能：合并、交替混合、分割、压缩、加密、转图片、提取文字
- 自动排序（数字优先）与手动上下移动
- 底部状态栏显示文件数量
