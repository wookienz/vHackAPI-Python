import utils
import json
from player import Player
import logging


class Package:

    p = Player()
    ut = utils.Utils()

    def __init__(self, obj):
        self.username = obj.username
        self.password = obj.password

    def openallpackages(self):
        """
        Open all packages
        :return: json object containing winnings or False if no packages openned
        """
        userHash = self.ut.gethash()
        r = self.ut.requestString("user::::pass::::uhash", self.username + "::::" + self.password + "::::" + userHash, "vh_openAllBonus.php")
        if r == "1":
            return False
        else:
            j = json.loads(r)
            logging.debug("Openned packages and received: {0}".format(j))
            return j

    def buypackages(self, amount):
        """
        Pass in amount of netcoins to use, auto calc how many packages to buy.
        :param amount: 
        :return: 
        """
        pass
