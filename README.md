# 🗂️ File Organizer Pro

> Automatically organize messy folders into clean, categorized structure — with a single click.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=flat-square&logo=windows)

---

## ✨ What It Does

You pick a **Source Folder (A)** full of messy files and a **Destination Folder (B)** — the app scans everything (including subfolders) and moves all files into neatly organized category folders inside B.

**Before:**
```
Folder A/
├── vacation.jpg
├── resume.pdf
├── song.mp3
├── project.zip
└── subfolder/
    ├── video.mp4
    └── notes.txt
```

**After:**
```
Folder B/
├── 📸 Photos/
│   └── vacation.jpg
├── 📄 Documents/
│   ├── resume.pdf
│   └── notes.txt
├── 🎵 Audios/
│   └── song.mp3
├── 🗜️ Archives/
│   └── project.zip
└── 🎬 Videos/
    └── video.mp4
```

---

## 📦 File Categories

| Category | Extensions |
|----------|-----------|
| 📸 Photos | jpg, jpeg, png, gif, webp, heic, raw, svg, bmp... |
| 🎬 Videos | mp4, avi, mkv, mov, wmv, flv, webm... |
| 🎵 Audios | mp3, wav, flac, aac, ogg, m4a, wma... |
| 📄 Documents | pdf, docx, xlsx, pptx, txt, csv, epub... |
| 🗜️ Archives | zip, rar, 7z, tar, gz, iso... |
| 💻 Code | py, js, html, css, java, cpp, json, yaml... |
| 🖼️ Design | psd, ai, fig, sketch, blend, obj... |
| 📦 Executables | exe, msi, apk, deb... |
| 📂 Others | anything not matched above |

---

## 🚀 Download & Use (No Python needed)

1. Go to the [**Releases**](../../releases) page
2. Download `FileOrganizerPro.exe`
3. Double-click and run — that's it!

> ⚠️ Windows may show a "Windows protected your PC" warning. Click **"More info" → "Run anyway"**. This is normal for unsigned apps.

---

## 🐍 Run from Source (Python)

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/FileOrganizerPro.git
cd FileOrganizerPro

# Run directly (no extra installs needed)
python file_organizer.py
```

Requires **Python 3.8+** — no external packages needed.

---

## 🔨 Build the .EXE yourself

```bash
pip install pyinstaller
```

Then either:
- **Double-click `build.bat`** (easiest)
- Or run manually:
  ```bash
  pyinstaller --onefile --windowed --name "FileOrganizerPro" file_organizer.py
  ```

Your `.exe` will appear in the `dist/` folder.

---

## 🖼️ Features

- ✅ Recursive scanning (subfolders included)
- ✅ 8 smart categories, 60+ file extensions
- ✅ Duplicate file protection (auto-renames with timestamp)
- ✅ Cleans up empty folders after organizing
- ✅ Live activity log
- ✅ Progress bar
- ✅ Dark themed UI
- ✅ No internet required
- ✅ Portable — single `.exe`, no installation

---
