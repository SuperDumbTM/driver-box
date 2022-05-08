import os
import sys
import configparser
import json

if getattr(sys, 'frozen', False):
    ROOTDIR = os.path.dirname(sys.executable)
elif __file__:
    ROOTDIR = os.path.dirname(os.path.dirname(__file__))
SRCDIR = os.path.join(ROOTDIR, "src")
PICDIR = os.path.join(ROOTDIR, "pic")
CONFDIR = os.path.join(ROOTDIR, "conf")


class Conf:
    
    _instance = None
    
    @staticmethod
    def get_instance():
        if Conf._instance is None:
            Conf()
        return Conf._instance
    
    def __init__(self) -> None:
        if Conf._instance is not None:
            raise Exception('Singleton class, use HwInfo.get_instance() instead')
        else:
            self._id = id(self)
            Conf._instance = self
            
            self.dri_conf_dir = CONFDIR
            self.prog_conf_path = os.path.join(ROOTDIR, "config.json")
            self.src_path = os.path.join(ROOTDIR, "src")
    
    def get_app_conf(self) -> dict:
        with open(self.prog_conf_path, "r") as f:
            return json.load(f)

    def get_lan_conf(self) -> dict:
        output = {}
        path = os.path.join(self.dri_conf_dir, "lan_driver.conf")
        parser = configparser.ConfigParser()
        parser.read_file(open(path, encoding="utf-8"))
        
        for sec in parser.sections():
            tmp = dict(parser[sec])
            output[sec] = tmp
        return output

    def get_display_conf(self) -> dict:
        output = {}
        path = os.path.join(self.dri_conf_dir, "display_driver.conf")

        parser = configparser.ConfigParser()
        parser.read_file(open(path, encoding="utf-8"))
        
        for sec in parser.sections():
            tmp = dict(parser[sec])
            output[sec] = tmp
        return output

    def get_other_conf(self) -> dict:
        output = {}
        path = os.path.join(self.dri_conf_dir, "other_driver.conf")
        parser = configparser.ConfigParser()
        parser.read_file(open(path, encoding="utf-8"))
        
        for sec in parser.sections():
            tmp = dict(parser[sec])
            output[sec] = tmp
        return output

if __name__ == "__main__":
    c = Conf.get_instance()