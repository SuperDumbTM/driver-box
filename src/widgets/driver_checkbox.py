from PyQt5 import QtWidgets


class DriverOptionCheckBox(QtWidgets.QCheckBox):

    __dri_id: str = ""

    @property
    def dri_id(self):
        return self.__dri_id

    @dri_id.setter
    def dri_id(self, val: str):
        self.__dri_id = val
