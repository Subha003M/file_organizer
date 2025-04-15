import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sv_ttk  # Dark mode theme
import subprocess  # For opening files
from tkinterdnd2 import TkinterDnD, DND_FILES

# File categories
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".py", ".java", ".cpp", ".js", ".html", ".css"],
}

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("900x600")

        # Apply dark mode theme
        sv_ttk.set_theme("dark")

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)
        
        self.folder_path = tk.StringVar()
        self.cancel_flag = False  
        self.files_to_process = []
        self.current_file_index = 0

        self.setup_ui()
    
    def setup_ui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        label = ttk.Label(frame, text="📂 Select Folder to Organize:", font=("Arial", 12, "bold"))
        label.pack(anchor="w", pady=5)
        
        path_frame = ttk.Frame(frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        path_entry = ttk.Entry(path_frame, textvariable=self.folder_path, width=60, font=("Arial", 10))
        path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.browse_button = ttk.Button(path_frame, text="Browse", command=self.browse_folder, style="Accent.TButton")
        self.browse_button.pack(side=tk.LEFT, padx=5)
        
        self.organize_button = ttk.Button(frame, text="🗂 Organize Files", command=self.start_organizing, style="Accent.TButton")
        self.organize_button.pack(pady=10)
        
        self.cancel_button = ttk.Button(frame, text="❌ Cancel", command=self.cancel_organizing, style="Accent.TButton")
        self.cancel_button.pack(pady=10)
        
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        self.progress_label = ttk.Label(self.root, text="", font=("Arial", 10, "bold"), foreground="white")
        self.progress_label.pack(pady=5)

        self.file_tree = ttk.Treeview(self.root, columns=("Name", "Type"), show="headings", height=15)
        self.file_tree.heading("Name", text="📄 File Name")
        self.file_tree.heading("Type", text="📂 Category")
        self.file_tree.pack(pady=10, fill=tk.BOTH, expand=True)

        self.file_tree.bind("<Button-3>", self.show_context_menu)  # Right-click menu
        
        self.theme_button = ttk.Button(self.root, text="🌗 Theme", command=self.toggle_theme, style="Accent.TButton")
        self.theme_button.pack(pady=5)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.display_files()
    
    def on_drop(self, event):
        dropped_folder = event.data.strip().replace('{', '').replace('}', '')
        if os.path.isdir(dropped_folder):
            self.folder_path.set(dropped_folder)
            self.display_files()
    
    def display_files(self):
        self.file_tree.delete(*self.file_tree.get_children())
        folder = self.folder_path.get()
        if os.path.exists(folder):
            for file in os.listdir(folder):
                file_ext = os.path.splitext(file)[1].lower()
                category = next((cat for cat, ext in FILE_CATEGORIES.items() if file_ext in ext), "Others")
                self.file_tree.insert("", tk.END, values=(file, category))
    
    def start_organizing(self):
        folder = self.folder_path.get()
        if not os.path.exists(folder):
            messagebox.showerror("Error", "Folder does not exist.")
            return
        
        self.files_to_process = [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]
        total_files = len(self.files_to_process)
        
        if total_files == 0:
            messagebox.showinfo("Info", "No files found to organize.")
            return
        
        self.progress["value"] = 0
        self.progress["maximum"] = total_files
        
        self.cancel_flag = False  
        self.current_file_index = 0  

        self.process_next_file()

    def process_next_file(self):
        if self.cancel_flag:
            self.progress_label.config(text="❌ Cancelled!", foreground="red")
            return

        if self.current_file_index >= len(self.files_to_process):
            self.display_files()
            messagebox.showinfo("Success", "Files Organized Successfully!")
            self.progress_label.config(text="✅ Done!", foreground="#00FF00")
            return
        
        file = self.files_to_process[self.current_file_index]
        folder = self.folder_path.get()
        file_path = os.path.join(folder, file)
        file_ext = os.path.splitext(file)[1].lower()
        category = next((cat for cat, ext in FILE_CATEGORIES.items() if file_ext in ext), "Others")
        category_path = os.path.join(folder, category)
        os.makedirs(category_path, exist_ok=True)
        shutil.move(file_path, os.path.join(category_path, file))
        
        self.progress["value"] = self.current_file_index + 1
        self.current_file_index += 1

        self.root.after(500, self.process_next_file)  # 0.5 sec delay per file
    
    def cancel_organizing(self):
        self.cancel_flag = True  

    def toggle_theme(self):
        sv_ttk.set_theme("light" if sv_ttk.get_theme() == "dark" else "dark")

    def show_context_menu(self, event):
        item = self.file_tree.identify_row(event.y)
        if not item:
            return
        
        file_name = self.file_tree.item(item, "values")[0]
        folder = self.folder_path.get()
        file_path = os.path.join(folder, file_name)

        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Open", command=lambda: self.open_file(file_path))
        menu.add_command(label="Delete", command=lambda: self.delete_file(file_path, item))
        menu.add_command(label="Refresh", command=self.display_files)
        menu.post(event.x_root, event.y_root)

    def open_file(self, file_path):
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # macOS/Linux
                subprocess.run(["xdg-open", file_path] if "linux" in os.sys.platform else ["open", file_path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

    def delete_file(self, file_path, item):
        if messagebox.askyesno("Confirm Delete", f"Delete {os.path.basename(file_path)}?"):
            try:
                os.remove(file_path)
                self.file_tree.delete(item)
                messagebox.showinfo("Deleted", "File deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete file: {e}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
