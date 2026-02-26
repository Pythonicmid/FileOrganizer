import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
import time
from datetime import datetime


# ─── File Type Categories ────────────────────────────────────────────────────

CATEGORIES = {
    "📸 Photos": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
        ".webp", ".heic", ".heif", ".raw", ".cr2", ".nef", ".svg", ".ico"
    ],
    "🎬 Videos": [
        ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm",
        ".m4v", ".mpeg", ".mpg", ".3gp", ".ts", ".vob"
    ],
    "🎵 Audios": [
        ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a",
        ".opus", ".aiff", ".alac", ".mid", ".midi"
    ],
    "📄 Documents": [
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
        ".txt", ".csv", ".odt", ".ods", ".odp", ".rtf", ".pages",
        ".numbers", ".key", ".epub", ".mobi"
    ],
    "🗜️ Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
        ".iso", ".dmg", ".cab"
    ],
    "💻 Code": [
        ".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp",
        ".cs", ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".sh",
        ".bat", ".ps1", ".sql", ".json", ".xml", ".yaml", ".yml", ".toml"
    ],
    "🖼️ Design": [
        ".psd", ".ai", ".xd", ".fig", ".sketch", ".indd",
        ".afphoto", ".afdesign", ".blend", ".fbx", ".obj"
    ],
    "📦 Executables": [
        ".exe", ".msi", ".apk", ".app", ".deb", ".rpm", ".pkg"
    ],
    "📂 Others": []  # catch-all
}


def get_category(extension: str) -> str:
    ext = extension.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "📂 Others"


# ─── Core Organizer Logic ─────────────────────────────────────────────────────

def get_all_files(folder: str):
    """Recursively get all files from folder and subfolders."""
    all_files = []
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if not file.startswith('.'):
                all_files.append(os.path.join(root, file))
    return all_files


def safe_move(src: str, dest_folder: str, log_callback=None) -> bool:
    """Move a file safely, handling duplicates by renaming."""
    filename = os.path.basename(src)
    dest = os.path.join(dest_folder, filename)

    if os.path.exists(dest):
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}{ext}"
        dest = os.path.join(dest_folder, filename)

    try:
        shutil.move(src, dest)
        if log_callback:
            log_callback(f"✅ Moved: {os.path.basename(src)} → {os.path.basename(dest_folder)}")
        return True
    except Exception as e:
        if log_callback:
            log_callback(f"❌ Error moving {os.path.basename(src)}: {e}")
        return False


def organize_files(source: str, dest: str, log_callback=None, progress_callback=None) -> dict:
    """Main organizer function. Returns stats dict."""
    stats = {"moved": 0, "failed": 0, "skipped": 0, "categories": {}}

    if not os.path.exists(source):
        if log_callback:
            log_callback("❌ Source folder does not exist!")
        return stats

    os.makedirs(dest, exist_ok=True)

    all_files = get_all_files(source)
    total = len(all_files)

    if total == 0:
        if log_callback:
            log_callback("⚠️ No files found in source folder.")
        return stats

    if log_callback:
        log_callback(f"📁 Found {total} file(s) to organize...\n")

    for i, file_path in enumerate(all_files):
        ext = Path(file_path).suffix
        category = get_category(ext)

        category_folder = os.path.join(dest, category)
        os.makedirs(category_folder, exist_ok=True)

        success = safe_move(file_path, category_folder, log_callback)
        if success:
            stats["moved"] += 1
            stats["categories"][category] = stats["categories"].get(category, 0) + 1
        else:
            stats["failed"] += 1

        if progress_callback:
            progress_callback(int((i + 1) / total * 100))

    for root, dirs, files in os.walk(source, topdown=False):
        if root == source:
            continue
        try:
            if not os.listdir(root):
                os.rmdir(root)
        except Exception:
            pass

    return stats


# ─── GUI ─────────────────────────────────────────────────────────────────────

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer Pro")
        self.root.geometry("750x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.source_var = tk.StringVar()
        self.dest_var = tk.StringVar()
        self.is_running = False

        self._build_ui()

    def _build_ui(self):
        BG = "#1e1e2e"
        CARD = "#2a2a3e"
        ACCENT = "#7c3aed"
        ACCENT_HOVER = "#6d28d9"
        TEXT = "#e2e8f0"
        SUBTEXT = "#94a3b8"
        ENTRY_BG = "#313147"

        header = tk.Frame(self.root, bg=ACCENT, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="🗂  File Organizer Pro",
                 font=("Segoe UI", 20, "bold"), bg=ACCENT, fg="white").pack(side="left", padx=20, pady=15)
        tk.Label(header, text="Organize files automatically by type",
                 font=("Segoe UI", 10), bg=ACCENT, fg="#c4b5fd").pack(side="right", padx=20)

        content = tk.Frame(self.root, bg=BG, padx=25, pady=20)
        content.pack(fill="both", expand=True)

        def folder_row(parent, label, var, row):
            tk.Label(parent, text=label, font=("Segoe UI", 10, "bold"),
                     bg=BG, fg=SUBTEXT).grid(row=row, column=0, sticky="w", pady=(10, 3), columnspan=2)

            frame = tk.Frame(parent, bg=ENTRY_BG, bd=0, highlightthickness=1,
                             highlightbackground="#404060", highlightcolor=ACCENT)
            frame.grid(row=row+1, column=0, sticky="ew", padx=(0, 8))

            entry = tk.Entry(frame, textvariable=var, font=("Segoe UI", 10),
                             bg=ENTRY_BG, fg=TEXT, bd=0, insertbackground=TEXT, relief="flat")
            entry.pack(fill="x", padx=10, pady=8)

            btn = tk.Button(parent, text="Browse", font=("Segoe UI", 9, "bold"),
                            bg=ACCENT, fg="white", bd=0, relief="flat", cursor="hand2",
                            activebackground=ACCENT_HOVER, activeforeground="white",
                            padx=14, pady=6,
                            command=lambda v=var: self._browse(v))
            btn.grid(row=row+1, column=1, sticky="ew")

        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, minsize=90)

        folder_row(content, "📂  SOURCE FOLDER (Folder A)", self.source_var, 0)
        folder_row(content, "📁  DESTINATION FOLDER (Folder B)", self.dest_var, 2)

        tk.Label(content, text="FILE CATEGORIES", font=("Segoe UI", 10, "bold"),
                 bg=BG, fg=SUBTEXT).grid(row=4, column=0, sticky="w", pady=(20, 8), columnspan=2)

        cat_frame = tk.Frame(content, bg=CARD, bd=0)
        cat_frame.grid(row=5, column=0, columnspan=2, sticky="ew")

        cats = list(CATEGORIES.keys())
        for i, cat in enumerate(cats):
            row_i = i // 4
            col_i = i % 4
            tk.Label(cat_frame, text=cat, font=("Segoe UI", 8),
                     bg=CARD, fg=TEXT, padx=8, pady=5,
                     relief="flat").grid(row=row_i, column=col_i, padx=4, pady=4, sticky="ew")
        for c in range(4):
            cat_frame.columnconfigure(c, weight=1)

        self.org_btn = tk.Button(
            content, text="⚡  ORGANIZE FILES",
            font=("Segoe UI", 12, "bold"), bg=ACCENT, fg="white",
            bd=0, relief="flat", cursor="hand2",
            activebackground=ACCENT_HOVER, activeforeground="white",
            pady=12, command=self._start_organize
        )
        self.org_btn.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(20, 8))

        self.progress = ttk.Progressbar(content, mode="determinate", maximum=100)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TProgressbar", troughcolor=CARD, background=ACCENT, thickness=6)
        self.progress.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        tk.Label(content, text="ACTIVITY LOG", font=("Segoe UI", 9, "bold"),
                 bg=BG, fg=SUBTEXT).grid(row=8, column=0, sticky="w", columnspan=2)

        log_frame = tk.Frame(content, bg=CARD, bd=0, highlightthickness=1, highlightbackground="#404060")
        log_frame.grid(row=9, column=0, columnspan=2, sticky="nsew", pady=(4, 0))
        content.rowconfigure(9, weight=1)

        self.log_box = tk.Text(log_frame, height=8, font=("Consolas", 9),
                               bg=CARD, fg=TEXT, bd=0, relief="flat",
                               insertbackground=TEXT, wrap="word", state="disabled")
        scrollbar = tk.Scrollbar(log_frame, command=self.log_box.yview, bg=CARD)
        self.log_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.log_box.pack(fill="both", expand=True, padx=8, pady=6)

    def _browse(self, var):
        folder = filedialog.askdirectory()
        if folder:
            var.set(folder)

    def _log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _set_progress(self, value):
        self.progress["value"] = value
        self.root.update_idletasks()

    def _start_organize(self):
        if self.is_running:
            return

        source = self.source_var.get().strip()
        dest = self.dest_var.get().strip()

        if not source or not dest:
            messagebox.showwarning("Missing Paths", "Please select both source and destination folders.")
            return

        if source == dest:
            messagebox.showwarning("Same Folder", "Source and destination cannot be the same folder.")
            return

        self.is_running = True
        self.org_btn.configure(text="⏳  Organizing...", state="disabled")
        self.progress["value"] = 0

        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

        thread = threading.Thread(target=self._run_organize, args=(source, dest), daemon=True)
        thread.start()

    def _run_organize(self, source, dest):
        start = time.time()
        self._log(f"🚀 Starting organization...\n📂 Source: {source}\n📁 Dest:   {dest}\n{'─'*50}")

        stats = organize_files(source, dest, self._log, self._set_progress)

        elapsed = round(time.time() - start, 2)
        self._log(f"\n{'─'*50}")
        self._log(f"✅ Done in {elapsed}s  |  Moved: {stats['moved']}  |  Failed: {stats['failed']}")

        if stats["categories"]:
            self._log("\n📊 Summary:")
            for cat, count in sorted(stats["categories"].items(), key=lambda x: -x[1]):
                self._log(f"   {cat}: {count} file(s)")

        self.root.after(0, self._finish_organize)

    def _finish_organize(self):
        self.is_running = False
        self.org_btn.configure(text="⚡  ORGANIZE FILES", state="normal")
        self.progress["value"] = 100
        messagebox.showinfo("Done!", "Files have been organized successfully! 🎉")


def main():
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
