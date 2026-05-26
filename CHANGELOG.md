# Changelog

## [1.1.0] - 2026-05-27

### Added
- **旋轉頁面 (Rotate Pages)** — rotate all pages by 90°, 180°, or 270°
- **移除選取 (Remove Selected)** — remove individual files from the list without clearing all
- **Progress bar** — animated progress bar displayed during any long-running operation

### Fixed
- `op_compress` previously saved output as `.zip` using PdfWriter (incorrect format); now correctly saves as a compressed `.pdf`
- `move_item` relied on fragile cursor-position text parsing; replaced with a tracked `selected_index` variable for reliable selection

### Improved
- All PDF operations now run on background threads — UI no longer freezes during processing
- Thread-safe UI updates via `self.after(0, ...)` for all messagebox calls from threads
- Input validation added: merge and alt-mix now warn if fewer than 2 files are loaded
- `extract_text()` now handles pages with no extractable text gracefully (returns empty string instead of crashing)
- `_run_task()` helper introduced to eliminate duplicated threading logic across operations
- `auto_sort` sort key is now case-insensitive for alphabetical fallback

## [1.0.0] - Initial Release

### Added
- GUI built with CustomTkinter (dark mode, blue theme)
- Operations: merge, alternate mix, split, compress, encrypt, convert to image, extract text
- Auto-sort (numeric-first) and manual up/down ordering
- Status bar showing file count
