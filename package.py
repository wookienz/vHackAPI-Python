import utils
import json
from player import Player
import logging


class Package:

    p = Player()
    ut = utils.Utils()

    def __init__(self):
        pass

    def openallpackages(self):
        """
        Open all packages
         r = int 1 for no packages
         r = '{u'adw': u'0', u'ipsp': u'0', u'scan': u'2', u'netcoins': u'300', u'fw': u'0', u'money': u'5491000',
         u'spam': u'3', u'newcoins': u'19398', u'newmoney': u'17761772', u'pcs': u'0', u'av': u'0',
        u'boost': u'1', u'sdk': u'5'}'
        :return: json object containing winnings or False if no packages openned
        """
        r = self.ut.openallapckages()
        if r == 1 or r == '1':
            return False
        else:
            j = json.loads(r)
            logging.debug("Opened packages and received: {0}".format(j))
            return j

    def buypackages(self, amount):
        """
        Pass in amount of netcoins to use, auto calc how many packages to buy.
        :param amount: 
        :return: 
        """
        pass
