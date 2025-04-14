from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import UploadServer, DownloadServer
from getIp import get_network_info

from threading import Thread

from configWindow import SettingUI
import setting

import os
import sys
import logging

q = ""
upload_server = None
download_server = None


hints = None
uploadStartBtn = None
downloadStartBtn = None



logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s'
)
sys.stdout = open('server.log', 'w')
sys.stderr = open('server.log', 'w')


class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.settings = setting.set("config.json")
        if not self.settings.get("UploadServer.save_path"):
            messagebox.showinfo("Set saving path", 'Set saving path for upload server in "Config"')
        self.net_info = get_network_info()
        self.create()


    def create(self):
        global upload_server
        global downloadStartBtn
        global uploadStartBtn


        self.hints = Text(width=40, height=10)
        self.hints.insert("end", f"Receiving server starts at port {self.settings.get("UploadServer.port")}\n")
        self.hints.insert("end",f"Saving in {self.settings.get("UploadServer.save_path")}\n")
        self.hints.insert("end", f"Sending server starts on port {self.settings.get("DownloadServer.port")}\n")
        self.hints.insert("end", "Network Info:\n\n")
        for iface, info in reversed(self.net_info.items()):
            self.hints.insert("end", iface  + ": ( " + info[1]["address"] + " )\n\n")



        uploadStartBtn = Button(self, text="Receive", command=self.startUpload, fg="black", width=10)
        downloadStartBtn = Button(self, text="Send", command=self.startDownload, fg="black", width=10)
        configBtn = Button(self, text="Config", command=self.openConfigWindow, fg="black", width=10) # not used yet
        self.hints.grid(row=0, column=0, columnspan=3)
        uploadStartBtn.grid(row=1, column=0, sticky=NSEW)
        downloadStartBtn.grid(row=1, column=1, sticky=NSEW)
        configBtn.grid(row=1, column=2, sticky=NSEW)



    def openConfigWindow(self):
        config_window = SettingUI(Toplevel(), self.settings)

    def refreshHint(self):
        self.hints = None
        self.hints = Text(width=40, height=10)
        self.hints.insert("end", f"Receiving server starts at port {self.settings.get("UploadServer.port")}\n")
        self.hints.insert("end", f"Saving in {self.settings.get("UploadServer.save_path")}\n")
        self.hints.insert("end", f"Sending server starts on port {self.settings.get("DownloadServer.port")}\n")
        self.hints.insert("end", "Network Info:\n\n")
        for iface, info in reversed(self.net_info.items()):
            self.hints.insert("end", iface  + ": ( " + info[1]["address"] + " )\n\n")
        self.hints.grid(row=0, column=0, columnspan=3)



    def stopUpload(self):
        global upload_server
        UploadServer.q = True
        upload_server.join()
        upload_server = None
        uploadStartBtn.config(text="Receive", command=self.startUpload, fg="black", bg="white")


    def stopDownload(self):
        global download_server
        DownloadServer.q = True
        download_server.join()
        download_server = None
        downloadStartBtn.config(text="Send", command=self.startDownload, fg="black", bg="white")

    def startUpload(self):
        global uploadStartBtn
        global upload_server
        self.refreshHint()
        if upload_server:
            return
        upload_server = Thread(target=self.startUploadServer)
        upload_server.daemon = True
        upload_server.start()
        while not UploadServer.up:
            pass
        uploadStartBtn.config(text="Stop", command=self.stopUpload, fg="white", bg="red")




    def startDownload(self):
        global download_server
        global downloadStartBtn
        self.refreshHint()
        if download_server:
            return
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        download_server = Thread(target=self.startDownloadServer, args=(file_path,))
        download_server.daemon = True
        download_server.start()
        while not DownloadServer.up:
            pass
        downloadStartBtn.config(text="Stop", command=self.stopDownload, fg="white", bg="red")

    def startUploadServer(self):
        settings = setting.set("config.json")
        port = settings.get("UploadServer.port")
        path = settings.get("UploadServer.save_path")
        UploadServer.run(path, port)

    def startDownloadServer(self, file):
        settings = setting.set("config.json")
        port = settings.get("DownloadServer.port")
        DownloadServer.run(file, port)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    app = GUI()
    app.title("FT")
    icon_path = resource_path("FT.ico")
    app.iconbitmap(icon_path)
    app.mainloop()
