#!/usr/bin/env python3
import os
from FTPConnect import FTPConnector
from CronChecker import CronCheck

# check if tmp/filename exist.
_dir = "/usr/local/bin/Py3FTPServiceListener/cron/tmp"
_filename = "cron_ftp_active"
if CronCheck.HasCron(directory=_dir, filename=_filename) == True:
    pass # Only run one cron job at a time.
else:
    CronCheck.Create(directory=_dir, filename=_filename)
    # run FTP program
    ftpc = FTPConnector()
    ftpc.Settings(filepath="/usr/local/bin/Py3FTPServiceListener/settings/config.json")
    ftpc.Folders(filepath="/usr/local/bin/Py3FTPServiceListener/settings/folders.json")
    Settings = ftpc.Settings()
    Folders = ftpc.Folders()
    ftpc.Connect(ftp_host=Settings['host'], ftp_user=Settings['user'], ftp_password=Settings['pass'])
    for key,value in Folders.items():
        filesDir = os.path.join(value['src'], "files")
        if len(filesDir) > 0:
            for srcFilepath in ftpc.DirList(filesDir):
                dstFilepath = os.path.join(value['dst'], os.path.basename(srcFilepath))
                ftpc.UploadFile(_dst=dstFilepath, _src=srcFilepath)
                ftpc.SaveCopy(srcDir=value['src'], saveDir=".save", filePath=srcFilepath)
                ftpc.Log(srcDir=value['src'], logDir=".log", filePath=srcFilepath, fileExtension="txt")

CronCheck.Destroy(directory=_dir, filename=_filename)