# 🗂️ File Organizer GUI App

A sleek, dark-themed file organizer built with **Python + Tkinter** (and a sprinkle of drag-and-drop magic 🪄).  
Organize your messy folders by file type with just a few clicks — or just drop a folder in and let it handle the chaos!

## 🌟 Features

- 🎨 Modern **dark mode UI** (thanks to `sv_ttk`)
- 📁 Drag-and-drop folder support
- 🔄 Organizes files by categories:
  - Images (.jpg, .png, .gif...)
  - Videos (.mp4, .avi, .mov...)
  - Documents (.pdf, .docx, .txt...)
  - Music (.mp3, .wav...)
  - Archives (.zip, .rar...)
  - Code files (.py, .js, .cpp...)
  - Others (everything else)
- 📂 Treeview listing with right-click options:
  - Open file
  - Delete file
  - Refresh view
- ⏱️ Progress bar + cancel button for large folders
- 🌗 Theme toggle (Dark ⬌ Light)

## 🛠️ Tech Stack

- Python 3.x
- `tkinter` + `ttk`
- `tkinterdnd2` for drag & drop
- `sv_ttk` for styling
- `shutil`, `os`, `subprocess`

## 🚀 Getting Started

### 1. Clone this repo (or copy your code 😅)
bash
git clone https://github.com/yourusername/file-organizer-gui
cd file-organizer-gui

### 2. Install dependencies

pip install sv-ttk tkinterdnd2

    On Linux/macOS, tkinter might already be installed. If not:

sudo apt install python3-tk

### 3. Run the app

python file_organizer.py

    Make sure you're using Python 3.7+

## 📸 Screenshot

    ![sample](https://github.com/user-attachments/assets/7f671990-62d7-45a2-857b-7264b22fcbf4)


## 💡 To-Do / Upgrades

Add more file categories (e.g., Python packages, executables)

Drag-and-drop files (not just folders)

Export report/log of organized files

Multi-language support 🌍

## 🤖 Author

Built with ❤️ by subhashini
MCA Student | Aspiring Embedded Developer
