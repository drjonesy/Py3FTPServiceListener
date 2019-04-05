# Py3FTPServiceListener

A simple Python3 FTP Application broken up into three parts. The main program uses the class `FTPConnector` found in the `FTPConnect.py` file. This program can be run manually by itself. To extend its functionality to act as a constant `System File Watcher` it includes the class `FTPServiceListener` which extends `Thread` found in the `FTPService.py` file. Use the `FTPServiceListener` with the `ftp_listener_service.py` file to run an infite loop with threading. 

Use the two external `JSON` files located in the `settings` directory to manage the application.

> config.json

Defines the host, username, and password for the designated FTP server. "seconds" = the number of seconds to **_wait_** before running the script again. (Used only with the FTPServiceListener)

    {
        "host": "",
        "user": "",
        "pass": "",
        "seconds": 10
    }

> folders.json

The sample **_src_** directory represents a web directory on a Linux Ubuntu server. The **_dst_** directory is pointing to the designated directory on the connected FTP server.

    {
        "3646": {
            "src": "/var/www/hem/3646",
            "dst": "/hemdata/binary/3646"
        }
    }


## Structure
- FTPConnect.py `class`
- FTPService.py `class`
- ftp_listener_service.py `main`
- settings\
    - config.json `config file`
    - folders.json `config file`


## Requirements

The only requirement is that the **src** and **dst** directories exist before running the program in the `settings/folders.json` file.

## Note:

Depending upon the system architecture you may need to provide absolute pathing to both the `config.json` and `folders.json`

