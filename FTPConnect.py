from ftplib import FTP
import shutil
import os
import json

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
    
    def __CreateBackupDir(self, _dir=""):
        # create directory _backups if not exists
        __backupsDir = os.path.join(_dir, "_backups") 
        if os.path.isdir(__backupsDir) == False:
            os.mkdir(path=__backupsDir)

    def BackupFile(self, directory="", _src=""):
        """Moves file to _backups directory"""
        self.__CreateBackupDir(_dir = directory)
        filename = os.path.basename(_src)
        shutil.move(src=_src, dst=os.path.join(directory, "_backups", filename))


# ftpc = FTPConnector()
# ftpc.Settings(filepath="settings/config.json")
# ftpc.Folders(filepath="settings/folders.json")
# Settings = ftpc.Settings()
# Folders = ftpc.Folders()
# ftpc.Connect(ftp_host=Settings['host'], ftp_user=Settings['user'], ftp_password=Settings['pass'])
# for key,value in Folders.items():
#     for filepath in ftpc.DirList(value['src']):
#         filename = os.path.basename(filepath)
#         ftpc.UploadFile(dst=os.path.join(value['dst'], filename), src=filepath)