![#](PY3FTP_Logo.png)
# PY3 FTP

A simple Python3 FTP Application with log and file backup options. The application is cross-platform but focused on Linux Server development.

Licensed under the **GNU General Public License v3.0**

#### _Basic Overview_
Imports two external JSON formatted files: `/settings/config.json` and `/settings/folders.json` <br>
Using these two files, the application attempts to connect to an FTP Server, copies new files listed in the designated local `src:` directory to the `dst:` directory on the FTP Server.

#### _Setup Options_
You have 2 to 3 options for configuring the application depending upon the Operation System. 

- [Cron Job](#cronjob)
- [Service Edition](#service) _( Infinite Loop )_
- [Manual](#manual)

## Application Structure

> The `/var/www/html/hem/3646/` directory represents an html directory on an Ubunut Linux Server with LAMP installed. 

```bash
| Py3FTPServiceListener
|__ cron
    |__ CronChecker.py
    |__ FTPConnect.py
    |__ run.py
|__ manual
    |__ FTPConnect.py
    |__ RunOnce.py
|__ service
    |__ FTPConnect.py
    |__ FTPService.py
    |__ RunService.py
|__ setting
    |__ config.json
    |__ folders.json
|__ var
    |__www
        |__ html
            |__ hem
                |__ 3646
                    |__ .log
                    |__ .save
                    |__ files
                        |__ sample.txt
|__ .gitignore
|__ LICENSE.md
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


## <u id="cronjob">Cron Job</u> [ crontab -e ]

`Linux Server` focused but you can use the `Windows Task Schedular` as an alternative to the `crontab -e`<br>
Contains three files: `CronChecker.py, FTPConnect.py, run.py`<br>

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

## <u id="service">Service Edition</u> _( Infinite Loop )_
Just like the cronjob version, make sure to test out this system manually before converting it to a Linux Daemon. 

```
python3 /usr/local/bin/Py3FTPServiceListener/service/RunService.py 
```


## <u id="manual">Manual</u>
To execute the application only once without any cronjob checker or inifinite loop use the `RunOnce.py` application located in the `/manual/` directory
```
python3 /usr/local/bin/Py3FTPServiceListener/manual/RunOnce.py 
```
