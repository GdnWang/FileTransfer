import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from setting import set
import sys


class SettingUI:
    def __init__(self, root, settings_obj):
        self.root = root
        self.settings = settings_obj
        self.root.title("Config")
        icon_path = self.resource_path("FT.ico")
        self.root.iconbitmap(icon_path)
        self.create_widgets()
        self.load_settings()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def create_widgets(self):
        # Upload Server setting
        self.upload_frame = ttk.LabelFrame(self.root, text="Receiving settings")
        self.upload_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # save path
        self.save_path_var = tk.StringVar()
        ttk.Label(self.upload_frame, text="Save to:").grid(row=0, column=0, padx=5, pady=5)

        # select save path
        path_frame = ttk.Frame(self.upload_frame)
        path_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.path_entry = ttk.Entry(path_frame, textvariable=self.save_path_var,
                                    state='readonly', width=35)
        self.path_entry.pack(side=tk.LEFT, padx=(0, 5))

        self.select_btn = ttk.Button(path_frame, text="Select", width=6,
                                     command=self.select_directory)
        self.select_btn.pack(side=tk.LEFT)

        # port
        self.upload_port_var = tk.IntVar()
        ttk.Label(self.upload_frame, text="Port:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Spinbox(self.upload_frame, width=40, from_=1024, to=65535, textvariable=self.upload_port_var).grid(
            row=1, column=1, padx=5, pady=5)

        # Download Server setting
        self.download_frame = ttk.LabelFrame(self.root, text="Sending settings")
        self.download_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # port
        self.download_port_var = tk.IntVar()
        ttk.Label(self.download_frame, text="Port:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Spinbox(self.download_frame, width=40, from_=1024, to=65535, textvariable=self.download_port_var).grid(
            row=0, column=1, padx=5, pady=5)

        # buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.grid(row=2, column=0, pady=10)

        ttk.Button(self.button_frame, text="Save Settings", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Default", command=self.reset_defaults).pack(side=tk.LEFT, padx=5)

    def select_directory(self):
        path = filedialog.askdirectory()
        if path:

            self.save_path_var.set(os.path.normpath(path))

    def load_settings(self): # default settings
        # UploadServer settings
        self.save_path_var.set(self.settings.get("UploadServer.save_path", "./uploads"))
        self.upload_port_var.set(self.settings.get("UploadServer.port"))

        # DownloadServer settings
        self.download_port_var.set(self.settings.get("DownloadServer.port"))

    def save_settings(self):
        try:
            if not 1024 <= self.upload_port_var.get() <= 65535 or not 1024 <= self.download_port_var.get() <= 65535:
                raise Exception("Port should be in range 1024-65535")
            # save receiving settings
            self.settings.set("UploadServer.save_path", self.save_path_var.get())
            self.settings.set("UploadServer.port", self.upload_port_var.get())

            # save sending settings
            self.settings.set("DownloadServer.port", self.download_port_var.get())

            messagebox.showinfo("Success", f"Settings saved to {self.settings.filename}")

            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Fail", f"Failure: {str(e)}")

    def reset_defaults(self):
        if messagebox.askyesno("Confirm", "Reset to default?"):
            self.settings.data = {
                "UploadServer": {
                    "save_path": "",
                    "port": 9091,
                },
                "DownloadServer": {
                    "port": 9092
                }
            }
            self.settings.save()

            # reload interface
            self.load_settings()
            messagebox.showinfo("Success", "Reset to default.")




if __name__ == "__main__":
    config_file = "config.json"
    settings_obj = set(config_file)

    root = tk.Tk()
    app = SettingUI(root, settings_obj)

    root.mainloop()