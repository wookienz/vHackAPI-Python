import config
from utils import Utils
import json
import logging
import locale

class Player:
    ut = Utils()

    def __init__(self):
        self.username = config.user
        self.password = config.password
        self.money = 0
        self.ip = ''
        self.score = ''
        self.netcoins = ''
        self.boosters = ''
        self.rank = ''
        self.localspyware = ''
        self.remotespyware = ''
        self.email = 0
        self.savedIPs = []
        self.anon_attack = config.anon
        self.installedspyware = []
        self.nclevel = config.nclevel
        # self.init()  # 10 secs
        self.taskpri = config.tasks

    def __repr__(self):
        return "Money: {0}, Score: {1}".format(self.money, self.score)

    def getplayerinfo(self):
        pass

    def setmoney(self, amount):
        """
        Reset money value
        :param amount: int
        :return: None
        """
        self.money = amount
        logging.info("Player money: ${0}".format(locale.format("%d", int(self.money), grouping=True)))

    def getmoney(self):
        return self.money

    def addmoney(self, m):
        self.money += m

    def removespy(self):
        response = self.ut.removespyware()

    def init(self):
        """
        {"id":"924198","money":"14501972","ip":"83.58.131.20",
        "inet":"10","hdd":"10","cpu":"10","ram":"14","fw":"256","av":"410","sdk":"580","ipsp":"50","spam":"71","scan":"436","adw":"76",
        "actadw":"","netcoins":"5550","energy":"212286963","score":"10015",
        "urmail":"1","active":"1","elo":"2880","clusterID":null,"position":null,"syslog":null,
        "lastcmsg":"0","rank":32022,"event":"3","bonus":"0","mystery":"0","vipleft":"OFF",
        "hash":"91ec5ed746dfedc0a750d896a4e615c4",
        "uhash":"9832f717079f8664109ac9854846e753282c72cdf42fe33fb33c734923e1931c","use":"0",
        "tournamentActive":"2","boost":"294","actspyware":"0","tos":"1","unreadmsg":"0"}
        :return:
        """
        data = self.ut.myinfo()
        j = json.loads(data)
        self.setmoney(j['money'])
        self.ip = j['ip']
        self.score = j['score']
        self.netcoins = j['netcoins']
        self.remotespyware = j['actspyware']
        self.rank = j['rank']
        self.boosters = j['boost']
        self.localspyware = j['actadw']
        self.email = int(j['unreadmsg'])
        self.loadIPs()
        if self.localspyware != '':
            logging.info('spyware found, attempting to remove')
            self.removespy()
        self.installedspyware = self.ut.SpywareInfo()  # spyware installed on others


    def attackspyware(self):
        pass

    def refreshinfo(self):
        """
        Refresh player info. Useful after a dev attack to pick up new email etc.
        :return:
        """
        self.init()

    def readmail(self):
        """
        Read any new emails. Print to console.
        :return: None
        """
        if self.email:
            pass

    def loadIPs(self):
        """
        Retrieve notepad ips as a list and place into class variable.
        NOTE: IPs on notepad through game must be clean. '1,2,3,4' only, not words. ie '1.2.3.4 300million'
        :return:
        """
        self.savedIPs = self.ut.getNotepadIPs()

    def saveIP(self, ip, description):
        """
        Givcen an ip string save to notepad
        :param ip:
        :return:
        """
        self.ut.saveNotepadIPs(ip, description)
        self.loadIPs()

    def removeIP(self, ip):
        """
        Remove IP from saved ips notepad
        :param ip:
        :return:
        """
        pass
    # vh_removeNotepadIP.php          "ipid"

