import os
import shutil
from threading import Thread
from time import sleep
import json


class Service(Thread):
    def __init__(self, seconds):
        Thread.__init__(self)
        self.__seconds = seconds
        self.daemon = True
        self.start()
    def run(self):
        with open("config.json", "r") as _settings:
            config = json.load(_settings)
        while True:
            sleep(self.__seconds) # 10 seconds
            FileNames = os.listdir(config['src'])
            if len(FileNames) != 0:
                for name in FileNames:
                    shutil.move( os.path.join(config['src'], name), os.path.join(config['dst'], name) )


#Threaded Loop
Listener(seconds=10)
while True:
    pass
