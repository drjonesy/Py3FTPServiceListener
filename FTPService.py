import os
import shutil
from threading import Thread
from time import sleep
import json
from FTPConnect import FTPConnector

class FTPServiceListener(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        ftpc = FTPConnector()
        ftpc.Settings(filepath="settings/config.json")
        ftpc.Folders(filepath="settings/folders.json")
        Settings = ftpc.Settings()
        Folders = ftpc.Folders()
        ftpc.Connect(ftp_host=Settings['host'], ftp_user=Settings['user'], ftp_password=Settings['pass'])
        while True:
            sleep(Settings['seconds']) # wait then execute
            for key,value in Folders.items():
                if len(ftpc.DirList(value['src'])) > 0:
                    for filepath in ftpc.DirList(value['src']):
                        filename = os.path.basename(filepath)
                        ftpc.UploadFile(_dst=os.path.join(value['dst'], filename), _src=filepath)
                        ftpc.BackupFile(directory=value['src'], _src=filepath)
