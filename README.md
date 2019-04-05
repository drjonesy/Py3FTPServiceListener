# Py3FTPServiceListener

A simple Python3 FTP Application broken up into three parts. The main program uses the class `FTPConnector` found in the `FTPConnect.py` file. This program can be run manually by itself. To extend its functionality to act as a constant `System File Watcher` it includes the class `FTPServiceListener` which extends `Thread` found in the `FTPService.py` file. Use the `FTPServiceListener` with the `ftp_listener_service.py` file to run an infite loop with threading. 

## Application Structure
```bash
| Py3FTPServiceListener
|__ cron
    |__ CronChecker.py
    |__ FTPConnect.py
    |__ run.py
|__ service
    |__ FTPConnect.py
    |__ FTPService.py
    |__ RunService.py
|__ setting
    |__ config.json
    |__ folders.json
|__ var
    |__www
        |__ hem
            |__ 3646
                |__ .log
                |__ .save
                |__ files
                    |__ sample.txt
|__ .gitignore
|__ FTPConnect_Template.py
|__ README.md
```

Use the two external `JSON` files located in the `settings` directory to manage the application.

> config.json

Defines the host, username, and password for the designated FTP server. "seconds" = the number of seconds to **_wait_** before running the script again. (Used only with the FTPServiceListener)
```json
{
    "host": "",
    "user": "",
    "pass": "",
    "seconds": 10
}
```

> folders.json

The sample **_src_** directory represents a web directory on a Linux Ubuntu server. The **_dst_** directory is pointing to the designated directory on the connected FTP server.
```json
{
    "3646": {
        "src": "/var/www/hem/3646",
        "dst": "/hemdata/binary/3646"
    }
}
```

## Requirements

The only requirement is that the **src** and **dst** directories exist before running the program in the `settings/folders.json` file.

## Note:

Depending upon the system architecture you may need to provide absolute pathing to both the `config.json` and `folders.json`

## Cron Job [ crontab -e ]

Before setting up and running the cronjob you might need make the script executable.

> chmod u+x /path/to/script.py

```python
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
```

### _Absolute Pathing Required_:
Running this application as a cronjob / contab -e ... requires absolute pathing for the `config.json` and `folders.json`

> If your application is located in: `/usr/local/bin/Py3FTPServiceListener/` 

_Before_

```python
ftpc.Settings(filepath="/settings/config.json")
ftpc.Folders(filepath="/settings/folders.json")
```
_After_

```python
ftpc.Settings(filepath="/usr/local/bin/Py3FTPServiceListener/settings/config.json")
ftpc.Folders(filepath="/usr/local/bin/Py3FTPServiceListener/settings/folders.json")
```

## Setting up the Cron Job
I recommend you use the `nano` editor to configure your environment.

> Type: `crontab -e`

The cronjob should run every minute using the line below.

```bash
# =============================================
# // Python FTP Listener: Run every minute
# =============================================

* * * * * cd /usr/local/bin/Py3FTPServiceListener/cron && python3 run.py
```
If you'd like modify the intervals I recommend using:<br> https://crontab-generator.org/

> **Troubleshooting** <br>
> _If the application isn't running. Try executing the application manually first._
```bash
python3 /usr/local/bin/Py3FTPServiceListener/cron/run.py
```
