from ftplib import FTP
import shutil
import os
import json
from datetime import datetime, date, time

class FTPConnector:
    def __init__(self, ftp_host="", ftp_user="", ftp_password=""):
        self.__host = ftp_host
        self.__user = ftp_user
        self.__pass = ftp_password
        self.__config = {}
        self.__dirs = {}

    def Connect(self, ftp_host="", ftp_user="", ftp_password=""):
        self.__host = ftp_host
        self.__user = ftp_user
        self.__pass = ftp_password

    def Settings(self, filepath=None):
        if filepath is None:
            return self.__config
        else:
            with open(filepath, "r") as jsonFile:
                self.__config = json.load(jsonFile)
    
    def Folders(self, filepath=None):
        """Uses a json file to return a dictionary that defines the 'src' and 'dst' directories. Can have more than one set."""
        if filepath is None:
            return self.__dirs
        else:
            with open(filepath, "r") as jsonFile:
                self.__dirs = json.load(jsonFile)

    def DirList(self, directory=""):
        """Returns a list of files in the current directory with full paths"""
        return [os.path.join(directory, filename) for filename in os.listdir(directory) if os.path.isfile(os.path.join(directory, filename))]

    def UploadFile(self, _dst="", _src=""):
        with FTP(host=self.__host, user=self.__user, passwd=self.__pass) as ftp:
            ftp.storbinary('STOR {}'.format(_dst), open("{}".format(_src), "rb" ) )
            ftp.close()
    
    def __CreateDir(self, src_dir="", new_dir=""):
        # create directory _backups if not exists
        __dir = os.path.join(src_dir, new_dir) 
        if os.path.isdir(__dir) == False:
            os.mkdir(path=__dir)
    

    def SaveCopy(self, srcDir="", saveDir=".save", filePath=""):
        """Moves file to _backups directory"""
        self.__CreateDir(src_dir=srcDir, new_dir=saveDir)
        filename = os.path.basename(filePath)
        dstFilepath = os.path.join(srcDir, saveDir, filename)
        shutil.move(src=filePath, dst=dstFilepath)

    def Log(self, srcDir="", logDir=".log", filePath="", fileExtension="txt"):
        """Create new hidden log directory if not exists. 
        Create new log file for current date if not exists.
        For each file transferred to FTP and backedup
        append daily log file with: Time | FileName """
        self.__CreateDir(src_dir=srcDir, new_dir=logDir)
        today = datetime.now().date()
        tm = datetime.now().time().replace(microsecond=0)
        logger = os.path.basename(srcDir)
        logFilename = "{}-{}.{}".format(today, logger, fileExtension)
        filename = os.path.basename(filePath)
        _filepath = os.path.join(srcDir, logDir, logFilename)
        with open(_filepath, "a+") as _file:
            _file.write("{} | {}\n".format(tm, filename))
        


# ==== FTPConnector Sample ===

ftpc = FTPConnector()
ftpc.Settings(filepath="settings/config.json")
ftpc.Folders(filepath="settings/folders.json")
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
