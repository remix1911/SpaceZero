import os
import shutil
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from send2trash import send2trash
import lang

class JunkCleanerApp:
    def __init__(self, root):
        self.root = root
        self.lang = lang.get_language()
        self.root.title(self.lang["title"])
        self.root.geometry("900x600")
        self.root.minsize(900, 600)
        
        self.is_scanning = False
        self.found_files = []
        self.total_size = 0
        self.user_agreed = False
        
        self.show_disclaimer()
        if not self.user_agreed:
            self.root.destroy()
            return
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(pady=10)
        ttk.Label(title_frame, text="SpaceZero", font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        ttk.Label(title_frame, text="v1.0.0", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=5)
        ttk.Label(path_frame, text=self.lang["scan_path"]).pack(side=tk.LEFT, padx=5)
        self.path_entry = ttk.Entry(path_frame, width=60)
        self.path_entry.pack(side=tk.LEFT, padx=5)
        self.path_entry.insert(0, os.path.expanduser("~"))
        ttk.Button(path_frame, text=self.lang["browse"], command=self.browse_path).pack(side=tk.LEFT, padx=5)
        
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=5)
        self.temp_var = tk.IntVar(value=1)
        self.log_var = tk.IntVar(value=1)
        self.cache_var = tk.IntVar(value=1)
        ttk.Checkbutton(options_frame, text=self.lang["temp_files"], variable=self.temp_var).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(options_frame, text=self.lang["log_files"], variable=self.log_var).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(options_frame, text=self.lang["cache_files"], variable=self.cache_var).pack(side=tk.LEFT, padx=10)
        
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        self.progress = ttk.Progressbar(progress_frame, length=800, mode='determinate', maximum=100)
        self.progress.pack(pady=5)
        self.status = ttk.Label(progress_frame, text="Ready")
        self.status.pack()
        
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=5)
        self.files_label = ttk.Label(stats_frame, text=f"{self.lang['found_files']} 0")
        self.files_label.pack(side=tk.LEFT, padx=20)
        self.size_label = ttk.Label(stats_frame, text=f"{self.lang['total_size']} 0 KB")
        self.size_label.pack(side=tk.LEFT, padx=20)
        
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.file_list = tk.Listbox(list_frame, width=100, height=15, selectmode=tk.MULTIPLE)
        self.file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(list_frame, command=self.file_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_list.config(yscrollcommand=scrollbar.set)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.scan_btn = ttk.Button(button_frame, text=self.lang["start_scan"], command=self.start_scan)
        self.scan_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = ttk.Button(button_frame, text=self.lang["stop_scan"], command=self.stop_scan, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(button_frame, text=self.lang["select_all"], command=self.select_all).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text=self.lang["deselect_all"], command=self.deselect_all).pack(side=tk.LEFT, padx=10)
        
        self.clean_btn = ttk.Button(button_frame, text=self.lang["clean_selected"], command=self.clean_files, state=tk.DISABLED)
        self.clean_btn.pack(side=tk.RIGHT, padx=10)
        
        ttk.Button(button_frame, text=self.lang["about"], command=self.show_about).pack(side=tk.RIGHT, padx=10)
    
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def show_disclaimer(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.lang["disclaimer_title"])
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        self.center_window(dialog, 500, 400)
        
        text = tk.Text(dialog, wrap=tk.WORD, padx=15, pady=15)
        text.insert(tk.END, self.lang["disclaimer_content"])
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True)
        
        button_frame = ttk.Frame(dialog, padding=10)
        button_frame.pack(fill=tk.X)
        
        def on_disagree():
            dialog.destroy()
        
        def on_agree():
            self.user_agreed = True
            dialog.destroy()
        
        ttk.Button(button_frame, text=self.lang["disagree"], command=on_disagree).pack(side=tk.LEFT, padx=10, expand=True)
        ttk.Button(button_frame, text=self.lang["agree"], command=on_agree).pack(side=tk.RIGHT, padx=10, expand=True)
        
        self.root.wait_window(dialog)
    
    def show_about(self):
        if hasattr(self, 'about_window') and self.about_window.winfo_exists():
            self.about_window.lift()
            return
        
        self.about_window = tk.Toplevel(self.root)
        self.about_window.title(self.lang["about_title"])
        self.about_window.resizable(False, False)
        
        self.center_window(self.about_window, 500, 400)
        
        text = tk.Text(self.about_window, wrap=tk.WORD, padx=15, pady=15)
        text.insert(tk.END, self.lang["about_content"])
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True)
        
        def on_close():
            self.about_window.destroy()
            delattr(self, 'about_window')
        
        ttk.Button(self.about_window, text=self.lang["close"], command=on_close).pack(pady=10)
        self.about_window.protocol("WM_DELETE_WINDOW", on_close)
    
    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
    
    def get_extensions(self):
        exts = []
        if self.temp_var.get():
            exts += ['.tmp', '.temp']
        if self.log_var.get():
            exts += ['.log']
        if self.cache_var.get():
            exts += ['.cache', '.crdownload']
        return exts
    
    def scan_files(self, path):
        exts = self.get_extensions()
        if not exts:
            messagebox.showwarning(self.lang["warning"], self.lang["warning_select"])
            return
        
        skip_dirs = ['$Recycle.Bin', 'System Volume Information', 'Program Files', 
                     'Program Files (x86)', 'Windows', 'ProgramData', '.git', 'node_modules']
        
        total_files = 0
        scanned_files = 0
        
        for root, dirs, files in os.walk(path):
            if not self.is_scanning:
                break
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in exts:
                    total_files += 1
        
        if total_files == 0:
            self.is_scanning = False
            return
        
        for root, dirs, files in os.walk(path):
            if not self.is_scanning:
                break
            
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for file in files:
                if not self.is_scanning:
                    break
                
                ext = os.path.splitext(file)[1].lower()
                if ext in exts:
                    try:
                        fpath = os.path.join(root, file)
                        size = os.path.getsize(fpath)
                        self.found_files.append((fpath, size))
                        self.total_size += size
                        scanned_files += 1
                        progress = int((scanned_files / total_files) * 100)
                        self.progress['value'] = progress
                        self.update_display(fpath)
                    except PermissionError:
                        scanned_files += 1
                        continue
                    except OSError:
                        scanned_files += 1
                        continue
        
        self.is_scanning = False
    
    def update_display(self, fpath):
        self.files_label.config(text=f"{self.lang['found_files']} {len(self.found_files)}")
        if self.total_size >= 1024*1024:
            size_str = f"{self.total_size/(1024*1024):.2f} MB"
        else:
            size_str = f"{self.total_size/1024:.2f} KB"
        self.size_label.config(text=f"{self.lang['total_size']} {size_str}")
        self.file_list.insert(tk.END, fpath)
    
    def start_scan(self):
        self.is_scanning = True
        self.found_files = []
        self.total_size = 0
        self.file_list.delete(0, tk.END)
        
        self.scan_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.clean_btn.config(state=tk.DISABLED)
        self.progress['value'] = 0
        self.status.config(text="Scanning...")
        
        path = self.path_entry.get()
        if not os.path.isdir(path):
            messagebox.showerror("Error", "Invalid path")
            self.reset_scan()
            return
        
        threading.Thread(target=self.scan_files, args=(path,), daemon=True).start()
        self.check_scan()
    
    def check_scan(self):
        if self.is_scanning:
            self.root.after(100, self.check_scan)
        else:
            self.progress['value'] = 100
            self.status.config(text=self.lang["scan_complete"])
            self.scan_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            if self.found_files:
                self.clean_btn.config(state=tk.NORMAL)
    
    def stop_scan(self):
        self.is_scanning = False
    
    def reset_scan(self):
        self.is_scanning = False
        self.progress['value'] = 0
        self.scan_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def select_all(self):
        self.file_list.select_set(0, tk.END)
    
    def deselect_all(self):
        self.file_list.select_clear(0, tk.END)
    
    def clean_files(self):
        selected_files = []
        selected_indices = self.file_list.curselection()
        
        if not selected_indices:
            messagebox.showwarning(self.lang["warning"], self.lang["warning_select"])
            return
        
        for i in selected_indices:
            selected_files.append(self.file_list.get(i))
        
        if not messagebox.askyesno("Confirm", self.lang["confirm_delete"].format(len(selected_files))):
            return
        
        deleted = 0
        failed = 0
        failed_files = []
        
        for idx, fpath in enumerate(selected_files):
            try:
                full_path = os.path.abspath(fpath)
                exists_full = os.path.exists(full_path)
                exists_original = os.path.exists(fpath)
                
                if not exists_full and not exists_original:
                    failed += 1
                    failed_files.append(f"{fpath}\n  → {self.lang['file_not_found']}\n  → Absolute: {full_path}\n  → Index: {idx}")
                    continue
                actual_path = full_path if exists_full else fpath
                
                final_path = actual_path
                if len(final_path) > 200:
                    final_path = f"\\\\?\\{final_path}"
                
                send2trash(final_path)
                deleted += 1
            except PermissionError:
                failed += 1
                failed_files.append(f"{fpath}\n  → {self.lang['permission_denied']}")
            except OSError as e:
                if "being used by another process" in str(e) or "另一个程序正在使用此文件" in str(e):
                    failed += 1
                    failed_files.append(f"{fpath}\n  → {self.lang['file_in_use']}")
                else:
                    failed += 1
                    failed_files.append(f"{fpath}\n  → {self.lang['delete_failed'].format(str(e))}")
            except Exception as e:
                failed += 1
                failed_files.append(f"{fpath}\n  → {self.lang['delete_failed'].format(str(e))}")
        
        self.file_list.delete(0, tk.END)
        for f in self.found_files:
            if f[0] not in selected_files:
                self.file_list.insert(tk.END, f[0])
        
        result_msg = self.lang["success_delete"].format(deleted)
        if failed > 0:
            result_msg += f"\n\n{self.lang['failed_delete'].format(failed)}:\n\n" + "\n".join(failed_files)
        
        messagebox.showinfo(self.lang["clean_complete"], result_msg)
        
        if not self.file_list.size():
            self.clean_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = JunkCleanerApp(root)
    root.mainloop()
