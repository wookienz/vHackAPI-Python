import logging
import utils

class Missions:

    ut = utils.Utils()

    def __init__(self, obj):
        self.username = obj.username
        self.password = obj.password

    def collectall(self):
        """
        Collect all system prizes from mission tab
        :return: 
        """
        pass
