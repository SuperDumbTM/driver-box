from abc import abstractmethod, ABC
import time
import config
import os
import subprocess
import install_manager as imgtr

class Driver(ABC):

    conf: config.Conf
    imgt: imgtr.AutoInstallManager
    dri_conf: dict
    
    def __init__(self) -> None:
        self.conf = config.Conf.get_instance()
        self.imgt = imgtr.AutoInstallManager.get_instance()
    
    def get_conf(self) -> dict[str, dict]:
        return self.dri_conf
    
    def find_dri_conf(self, dri_name: str) -> dict[str, str]:
        for key in self.dri_conf.keys():
            if key == dri_name:
                return self.conf[key]
    
    def get_dri_conf(self) -> dict:
        return self.dri_conf

    def manual_install(self, dri_name: str, var):
        """
        directly open the `dri_name`'s installer

        `dri_name`: identifer on drivers configuration file (conf/)
        """
        try:
            path = os.path.join(config.ROOTDIR, self.dri_conf[dri_name]['path'])
            subprocess.Popen([path])
        except Exception as e:
            var.set(str(e))
    
    def auto_install(self, dri_name: str, var):
        """
        add the installation task to queue, execute later

        `dri_name`: identifer on drivers configuration file (conf/)
        """
        path = os.path.join(config.ROOTDIR, self.dri_conf[dri_name]['path'])
        flag = self.dri_conf[dri_name].get('flag',"")
        self.imgt.add_task({'args':[path]+flag.split(","), 'stat_var':var})

    def get_fail_proc(self) -> list:
        return self.imgt.get_fail_proc()

    def reinstall_failed():
        mgt = imgtr.AutoInstallManager.get_instance()
        for task in mgt.get_fail_proc():
            subprocess.Popen(task[0])
    
    @staticmethod
    def start_install():
        mgt = imgtr.AutoInstallManager.get_instance()
        mgt.setDaemon(True)
        mgt.start()
        
    @staticmethod
    def is_finished() -> bool:
        return imgtr.AutoInstallManager.get_instance().is_finished()
    
    @staticmethod
    def has_error() -> bool:
        return imgtr.AutoInstallManager.get_instance().has_error()
    
class DisplayDriver(Driver):
    
    def __init__(self) -> None:
        super().__init__()
        self.dri_conf = self.conf.get_display_conf()

class LanDriver(Driver):
    
    def __init__(self) -> None:
        super().__init__()
        self.dri_conf = self.conf.get_lan_conf()

class OtherDriver(Driver):
    
    def __init__(self) -> None:
        super().__init__()
        self.dri_conf = self.conf.get_other_conf()
        
if __name__ == "__main__":
    c = LanDriver()
    print(c.get_conf())