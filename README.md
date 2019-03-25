# Py3FTPServiceListener

An application that runs a multi-threaded infite loop. The application uses two external JSON files found in the `/settings` directory.
These files define the directory (folders) that will be constantly watched, the FTP info, and second interval which is used to tell the application how often it should execute. 

The application looks at specified directory, generates a list of files found in the directory, uploads each file using FTP if the directory is greater than zero, then moves the file to a backup directory for later use and/or comparison.


### Structure
- FTPConnect.py `class`
- FTPService.py `class`
- ftp_listener_service.py `main`
- settings
    - config.json `config file`
    - folders.json `config file`


