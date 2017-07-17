import cStringIO
import json
from base64 import b64decode
import time
import pytesseract
from PIL import Image
import player
from target import targets
from utils import Utils
import logging
import config
import locale
import logging


class Console:
    ut = Utils()
    p = player.Player()
    tgt = targets()

    def __repr__(self):
        pass

    def __init__(self):
        self.winchance = config.winchance
        self.anon_attack = config.anon

    def attack(self, ip=None):
        """
        
        :param ip: 
        :return: 
        """
        logging.info("Attacking....")
        h = self.ut.gethash()
        if h:
            if ip:
                self.attackip(ip)
            else:
                r = self.gettargets(h)
                j = json.loads(r)
                # process list of 6 items. each containing 'hostname' and 'img' keys
                results = self.processtargets(j['data'])
                for i in results:
                    time.sleep(2)
                    self.attackhostname(i['Hostname'])

    def attackhostname(self, hostname):
        """
        Scan, get port, attack
        :param hostname: str - hostname
        :return:
        """
        uhash = self.ut.gethash()
        logging.info('Attacking host {0}'.format(hostname))
        ip = self.hostnameToIP(uhash, hostname)
        # self.tgt.changevalue(hostname, ip=ip)
        self.attackip(ip)

    def attackip(self, ip):
        """
        Result: '{"result":"0","amount":28884687,"elo":4291,"eloch":0,"newmoney":505738794}'
        :param ip: u'36.105.207.122'
        :return: None
        """
        logging.info('Attacking target with ip: {0}'.format(ip))
        uhash = self.ut.gethash()
        time.sleep(1)
        r = self.ut.connectToRemoteHost(ip)
        if r is not False:
            j = json.loads(r)
            if self.attackdecision(j):
                attackport = self.ut.findportnumber(r)
                logging.info('Finding Attack Port {0}'.format(attackport))
                time.sleep(1)
                logging.info('Sending Trojan...')
                result = self.ut.transferTrojan(attackport, ip, uhash)
                if result:
                    j = json.loads(result)
                    print j
                    if j['newmoney'] > 1000000000:
                        pass
                        self.p.saveIP(ip, '')
                    try:
                        logging.info('managed to steal {0}, Rep gained: {1}'.format(locale.currency(j['amount']),
                                                                                    j['eloch']))
                    except Exception as e:
                        pass  # '{"result":"0","amount":4877810,"elo":2955,"eloch":1,"newmoney":5468422}'
                        # self.tgt.removetarget(hostname, ip)
                else:
                    logging.info('IP cant be attacket yet, timer active')


    def attackdecision(self, data):
        if self.anon_attack and data['anonymous'] is "No":
            return False
        if '???' == data['winchance']:
            return False
        elif int(data['winchance']) >= self.winchance:
            return True
        else:
            return False

    def gettargets(self, uhash):
        """
        Return a set of targets as if clicked Console icon for first time.
        :param uhash: game needed value
        :return: string of 6 targets
        """
        response = self.ut.gettargets(uhash)
        return response

    def processtargets(self, l):
        """
        input a list of hostname and img keys containing the computers you can hack.
        :param l: list ['hostname' : '.....','img': 'ojinciosncoisndcviosnvosdnvsnsdnfsnf....']
        :return: list
        """
        targets = []
        for i in l:
            r = self.decodeimages(i)
            # 'Hostname:\nXT73YLBSGG.vHack.cc\nFirewall: 306'
            if "by the FBI" not in r:
                hostname = i['hostname']
                firewall = r.split('\n')[-1].split(':')[1]
                targets.append({r.split('\n')[0].split(':')[0]: hostname, r.split('\n')[-1].split(':')[0]: firewall})
                self.tgt.addtarget(hostname, firewall=firewall)
                # [{'Firewall': ' 241', 'Hostname:': 'XT7H41995C.vHack.cc'}]
        return targets

    def decodeimages(self, i):
        """
        Take base64 code, decode it, file into a buffer insterad of save it, open buffer with PIL. Decode with pytess.
        :param i: item of list, keys: hostname and img
        :return: string 'Hostname:\nXT7H41995C.vHack.cc\nFirewall: 241'
        """
        img = b64decode(i['img'])
        data = cStringIO.StringIO(img)
        decoded_image = Image.open(data)
        final = pytesseract.image_to_string(decoded_image)
        return final

    def hostnameToIP(self, h, hostname):
        """
        Scan each of the 6 targets
        :param h: player hash
        :param hostname: str hostname of target. XT7H41995C.vHack.cc
        :return: str. '{"hostname":"XT-VRAV7Z5.vHack.cc","ipaddress":"76.179.249.20","vuln":"1"}'
        """
        temp = self.ut.scantarget(h, hostname)
        try:
            j = json.loads(temp)
            if j is 1:
                logging.debug(h, hostname, temp)
                return '127.0.0.1'
            else:
                return j['ipaddress']
        except ValueError or TypeError as e:
            print "Error getting value in scantargets function: {0}".format(e)
            return None

    def localhostattack(self):
        self.attack('127.0.0.1')
        self.p.refreshinfo()
        self.p.readmail()

