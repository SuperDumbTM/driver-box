import os
import sys
import configparser
import json

if getattr(sys, 'frozen', False):
    ROOT = os.path.dirname(sys.executable)
elif __file__:
    ROOT = os.path.dirname(os.path.dirname(__file__))
CONF = os.path.join(ROOT, "conf")

class Config:
    
    # config files path
    display = os.path.join(CONF, "display_driver.conf")
    lan = os.path.join(CONF, "lan_driver.conf")
    other = os.path.join(CONF, "other_driver.conf")
    setting = os.path.join(CONF, "setting.json")
    # type hint
    conf: dict

    
    def __init__(self, path: str) -> None:
        """
        Args:
            path (str): config file path
        """
        self.conf = {}
        self.path = path
        parser = configparser.ConfigParser()
        parser.read_file(open(path, encoding="utf-8"))
        for section in parser.sections():
            self.conf[section] = {}
            for option in parser.options(section):
                self.conf[section][option] = parser[section][option]
    
    def get_conf(self) -> dict:
        return self.conf
    
    def replace_conf(self, new: dict):
        self.conf = new
            
    def update_conf(self, key: str, val: str) -> bool:
        try:
            self.conf[key] = [val]
            return True
        except KeyError as e:
            return False
        
    def write_conf(self):
        parser = configparser.ConfigParser()
        parser.read_dict(self.conf)
        with open(self.path, 'w', encoding="utf-8") as f:
            parser.write(f)
     
     
class Setting(Config):
    
        def __init__(self, path: str) -> None:
            self.path = path
            with open(path, 'r', encoding="utf-8") as f:
                self.conf = json.load(f)
                
        def write_conf(self):
            with open(self.path, 'w', encoding="utf-8") as f:
                json.dump(self.conf, f)
        