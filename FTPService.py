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
                filesDir = os.path.join(value['src'], "files")
                if len(filesDir) > 0:
                    for srcFilepath in ftpc.DirList(filesDir):
                        dstFilepath = os.path.join(value['dst'], os.path.basename(srcFilepath))
                        ftpc.UploadFile(_dst=dstFilepath, _src=srcFilepath)
                        ftpc.SaveCopy(srcDir=value['src'], saveDir=".save", filePath=srcFilepath)
                        ftpc.Log(srcDir=value['src'], logDir=".log", filePath=srcFilepath, fileExtension="txt")
