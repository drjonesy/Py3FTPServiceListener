import os
class CronCheck:
    
    @staticmethod    
    def Create(directory="", filename=""):
        """Generates a file in a specified directory with a custom name/cron id"""
        with open( os.path.join(directory, filename), "w" ) as _file:
             _file.close()
    
    @staticmethod
    def Destroy(directory="", filename=""):
        """Deletes/destroys a specified file"""
        os.remove( os.path.join(directory, filename) )

    @staticmethod
    def HasCron(directory="", filename=""):
        """Returns True|False if File Exists"""
        return os.path.isfile( os.path.join(directory, filename) ) 